#Set Current Directory
from argparse import ArgumentParser, Namespace, FileType
import os
os.chdir("/scratch/phjiang/gbind/") #pathto directory
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
import pickle
import argparse
from glob import glob
from multiprocessing import Pool
import GAABind
from GAABind.data.feature_utils import get_ligand_info, get_protein_info, get_chem_feats, read_mol, get_coords

import warnings
warnings.filterwarnings('ignore')

import torch
import pandas as pd
from GAABind.utils import set_global_seed
from GAABind.data.graph_dataset import DockingTestDataset
from GAABind.data.collator import collator_test_3d
from GAABind.option import set_args
from GAABind.models.DockingPoseModel import DockingPoseModel
from GAABind.docking.docking_utils import (
    docking_data_pre,
    ensemble_iterations,
)
from torch.utils.data import DataLoader

import time

def load_model():
    # load model
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    parser = set_args()
    args = parser.parse_args(args=[])
    set_global_seed(args.seed)
    ckpt_path = './GAABind/saved_model/best_epoch.pt'
    state_dict = torch.load(ckpt_path, map_location='cpu')
    new_state_dict = dict()
    for key in state_dict.keys():
        layer_name = key[7:]
        new_state_dict[layer_name] = state_dict[key]
    
    model = DockingPoseModel(args).to(device)
    model.load_state_dict(new_state_dict)
    return model, args, device


def most_recent(directory):
    a = os.listdir(directory)
    b = [f"{directory}/{x}" for x in a if "." not in x]
    latest = max(b, key=os.path.getmtime)
    return latest

def checkprevProg(inDir, outDir):
    path = ""
    output = []
    
    if("part" in inDir):
        path = inDir.split("part")[0]
    else:
        path = inDir
    try:
        evaluated = os.listdir(f"./outputs/{outDir}")
    except:
        print("no previous progress")
        os.mkdir(f"./outputs/{outDir}")
        return [x for x in os.listdir(inDir) if "." not in x]
    else:
        paths = [x for x in os.listdir(inDir) if "." not in x]
        if(len(evaluated) != 0):
            if(os.path.isdir(path)):
                output = [y for y in paths if y not in evaluated]
                output.append(most_recent(inDir))
                #print(paths, np.sort(np.array(evaluated)))
            else:
                output = paths
        else:
            output = paths
            
        return output
    

def runbind(inDir, outDir):
    start_time = time.time()
    #input_paths = ['sys31']  #(Example)
    ptemp = os.listdir(inDir)
    input_paths = checkprevProg(inDir, outDir)
    #print(input_paths)
    for i,x in enumerate(tqdm(input_paths)):
        #print(f"\n\tBegan evaluation of ligand: {input_paths[i]}\n")
        passed = True
        input_path = f"./{inDir}/{input_paths[i]}"
        name = os.path.basename(input_path)
        mol_file = glob(f'{input_path}/ligand.txt')[0]
        pocket_file = glob(f'{input_path}/pocket.txt')[0]
        
        pro_file = glob(f'{input_path}/protein.pdb')[0]
        #pocket_file = f'./templates/pocket2.txt'
        #Hard code file location -- decreases unnecessary file read times (?)
        
        poc_res = open(pocket_file).read().splitlines()
        #print('using dataset path: ', mol_file, pro_file, pocket_file)
        #print('using the following reisudes as target pocket: ', ','.join(poc_res))
        
        if not os.path.exists(f'./outputs/{outDir}'):
            os.makedirs(f"./outputs/{outDir}")
        
        output_dir = f'./outputs/{outDir}/{input_paths[i]}' #replace the save path by your own
    
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, f'{name}.pkl')
        new_data = {}
        try:
            input_mol = read_mol(mol_file)
        except:
            print("\tfailed to read ligand from file -- RDKit Error")
            passed = False
        else:
            try:
                mol, smiles, coordinate_list = get_coords(input_mol)
            except:
                print(f'\tgenerate input ligand coords failed for {name}')
                passed = False
            
        if passed:
            lig_atoms, lig_atom_feats, lig_edges, lig_bonds = get_ligand_info(mol)
            poc_pos, poc_atoms, poc_atom_feats, poc_edges, poc_bonds = get_protein_info(pro_file, poc_res)
            
            new_data.update({'atoms': lig_atoms, 'coordinates': coordinate_list, 'pocket_atoms': poc_atoms,
                            'pocket_coordinates': poc_pos, 'smi': smiles, 'pocket': name,'lig_feats': lig_atom_feats,
                            'lig_bonds': lig_edges, 'lig_bonds_feats': lig_bonds, 'poc_feats': poc_atom_feats, 
                            'poc_bonds': poc_edges, 'poc_bonds_feats': poc_bonds, 'mol': mol})

            
            pass2 = True
            try:
                new_data = get_chem_feats(new_data)
            except:
                print(f"\t failed to generate chemical features for {name}")
                pass2 = False
            else:
                f_out = open(output_path, 'wb')
                pickle.dump(new_data, f_out)
                f_out.close()
        
                # load model
                model, args, device = load_model()
        
                inference_save_path = os.path.join(output_dir, f'{name}.pkl')   #define the save path of inference
                test_dataset = DockingTestDataset(output_dir, args.conf_size)
                test_dataloader = DataLoader(test_dataset, batch_size=args.batch_size, num_workers=args.num_workers, shuffle=False, collate_fn=collator_test_3d)
                
                outputs = []
                with torch.no_grad():
                    model.eval()
                    for batch in test_dataloader:
                        for dicts in batch[:2]:
                            for key in dicts.keys():
                                dicts[key] = dicts[key].to(device)
                
                        with torch.cuda.amp.autocast():
                            pred = model(batch)
                
                        mol_token_atoms = batch[0]['x'][:,:,0]
                        poc_token_atoms = batch[1]['x'][:,:,0]
                        poc_coords = batch[1]['pos']
                
                        logging_output = {}
                
                        logging_output["smi_name"] = batch[2]['smi_list']
                        logging_output["pocket_name"] = batch[2]['pocket_list']
                        logging_output['mol'] = batch[2]['mol']
                        logging_output["cross_distance_predict"] = pred[0].data.detach().cpu().permute(0, 2, 1)
                        logging_output["holo_distance_predict"] = pred[1].data.detach().cpu()
                        logging_output["atoms"] = mol_token_atoms.data.detach().cpu()
                        logging_output["pocket_atoms"] = poc_token_atoms.data.detach().cpu()
                        logging_output["holo_center_coordinates"] = batch[2]['holo_center_list']
                        logging_output["pocket_coordinates"] = poc_coords.data.detach().cpu()
                        logging_output['pred_affinity'] = pred[-1].data.detach().cpu()
                        outputs.append(logging_output)
                        #print(logging_output['pred_affinity'])
                
                    pickle.dump(outputs, open(inference_save_path, "wb"))
        
                mol_list, smi_list, pocket_list, pocket_coords_list, distance_predict_list, holo_distance_predict_list,\
                        holo_center_coords_list, pred_affi_list = docking_data_pre(inference_save_path)
                iterations = ensemble_iterations(mol_list, smi_list, pocket_list, pocket_coords_list, distance_predict_list,\
                                                     holo_distance_predict_list, holo_center_coords_list, pred_affi_list)
        
                cache_dir = os.path.join(output_dir, "cache")
                os.makedirs(cache_dir, exist_ok=True)
                cache_file = os.path.join(cache_dir, f'{name}.pkl')
                
                pd.to_pickle(next(iterations), cache_file)
                
                output_ligand_path = os.path.join(output_dir, name)
                cmd = "python ./GAABind/docking/coordinate_model.py --input {}  --output-path {}".format(cache_file, output_ligand_path)
                os.system(cmd)
                print(f'Prediction fininshed for {input_paths[i]}.\n')
    print("--- Batch complete. Time Elapsed: %5.5fs---" % (time.time() - start_time))

parser = ArgumentParser()

parser.add_argument('--inpath', type=str, default='', help='input path')
parser.add_argument('--outpath', type=str, default='', help='output path')

args = parser.parse_args()



runbind(f"{args.inpath}", f"{args.outpath}")
