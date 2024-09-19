from Bio.PDB import PDBParser
from Bio.PDB.PDBIO import PDBIO
import json
import numpy as np
import matplotlib.pyplot as plt
from python_pdb.parsers import parse_pdb_to_pandas
from openbabel import openbabel
import csv
import os

from argparse import ArgumentParser, Namespace, FileType
#-----------------------------------------------
#Import Args
parser = ArgumentParser()

parser.add_argument('--dir', type=str, default='', help='name of dir that was called in generation step')
parser.add_argument('--parts', type=bool, default=False, help='whether the directories are in parts')
parser.add_argument('--mins', type = bool, default = True, help = 'Whether or not to minimize the number of computed structures')

args = parser.parse_args()


from Bio.PDB import PDBParser
from Bio.PDB.PDBIO import PDBIO
import json
import numpy as np
import matplotlib.pyplot as plt
from python_pdb.parsers import parse_pdb_to_pandas
from openbabel import openbabel
import csv
import pandas as pd
import os


def nearest_residues(pdbDF, box, num):
  reslist = []
  add_thresh = 0
  df1 = pdbDF.sort_values('pos_x')
  xthresh = add_thresh + box[3]
  df2 = df1.loc[(df1['pos_x'] > (box[0] - xthresh)) & (df1['pos_x'] < (box[0] + xthresh))]
  #print(df2.size)

  df3 = df2.sort_values('pos_y')
  ythresh = add_thresh + box[4]
  df4 = df3.loc[(df3['pos_y'] > (box[1] - ythresh)) & (df3['pos_y'] < (box[1] + ythresh))]
  #print(df4.size)

  df5 = df4.sort_values('pos_z')
  zthresh = add_thresh + box[5]
  df6 = df5.loc[(df5['pos_z'] > (box[2] - zthresh)) & (df5['pos_z'] < (box[2] + zthresh))]
  #print(df6.size)


  unique_residues = set(df6['residue_seq_id'])
  for i in unique_residues:
    toadd = f"{list(df6.loc[df6['residue_seq_id'] == i]['chain_id'])[0]}_{i}_{list(df6.loc[df6['residue_seq_id'] == i]['residue_name'])[0]}"
    reslist.append(toadd)

  return reslist

def get_box(lf, pf, resnum = 10):
  with open(lf, 'r') as f:
    ldf = parse_pdb_to_pandas(f.read())

  minX = min(ldf["pos_x"])
  minY = min(ldf["pos_y"])
  minZ = min(ldf["pos_z"])

  maxX = max(ldf["pos_x"])
  maxY = max(ldf["pos_y"])
  maxZ = max(ldf["pos_z"])
  box = [((maxX + minX)/2), ((maxY + minY)/2), ((maxZ + minZ)/2), maxX-minX, maxY-minY, maxZ-minZ]

  with open(pf, 'r') as f:
    pdf = parse_pdb_to_pandas(f.read())

  residues  = nearest_residues(pdf, box, resnum)

  return box, residues

def file_Traversal(inDir):
    if("outputs" in os.listdir()):
        a = os.listdir("outputs")
        if(inDir in a):
            b = os.listdir(f"outputs/{inDir}")
            if("all_pdb" in b):
                out = [f"{x}" for x in os.listdir(f"outputs/{inDir}/all_pdb")]
            else:
                out = None
        else:
            out = None
                
    else:
        out = None
    return out

def min_set(inDir):
    print(f"./outputs/{inDir}/mpnn_results.csv")
    try:
        a = pd.read_csv(f"./outputs/{inDir}/mpnn_results.csv")
        
    except:
        print("file does not exist, please check your pathing")
        return None
    else:
        b = a[a["rmsd"] < 15].sort_values(by='Unnamed: 0')
        out = []
        for i in b.index:
            d = b.loc[i]["design"]
            num = b.loc[i]["n"]
            pth = (f"design{d}_n{num}.pdb")
            out.append(pth)
        return out

def convResults(dir, path, parts, inDir, mins = True):
  parser = PDBParser()
  io = PDBIO()
  if(mins):
      plist = min_set(inDir)
      if(plist != None):
          print("Successfully Read Files from Dir")
      else:
          print("Failed")
          return None
  else:
      plist = file_Traversal(inDir)
      if(plist != None):
          print("Successfully Read Files from Dir")
      else:
          print("Failed")
          return None
  i = 0
  pnum = 1
  for j in plist: #Depreciated, do not use
    k = f"./outputs/{inDir}/all_pdb/{j}"
    if(mins):
        dnum = j.split("_")[0].split("design")[1]
        nnum = j.split("_")[1].split("n")[1].split(".")[0]
    if parts:
      structure = parser.get_structure(path,k)
      pdb_chains = structure.get_chains()
      index = i
      if(int(index) == 0):
        pnum = 1
        os.system(f"mkdir {dir}/part{pnum}")
      elif((int(index))%64 == 0):
        pnum += 1
        os.system(f"mkdir {dir}/part{pnum}")
      os.system(f"mkdir {dir}/part{pnum}/{path}{index}")

      for chain in pdb_chains:
          io.set_structure(chain)
          fil = str(structure.get_id()) + "_" + str(chain.get_id()) + ".pdb"
          io.save(f"{dir}/part{pnum}/{path}{index}/{fil}")

      box, residues = get_box(f"{dir}/part{pnum}/{path}{index}/{path}_B.pdb", f"{dir}/part{pnum}/{path}{index}/{path}_A.pdb")

      with open(f'{dir}/part{pnum}/{path}{index}/box.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(box)
        file.close()

      with open(f'{dir}/part{pnum}/{path}{index}/pocket.txt', 'w', newline='') as file:
        for aa in residues:
          file.write(f"{aa}\n")
        file.close()

      os.system(f"/home/phjiang/.conda/envs/formatter/bin/obabel ./{dir}/part{pnum}/{path}{index}/{path}_B.pdb -O ./{dir}/part{pnum}/{path}{index}/ligand.sdf")
      os.system(f"/home/phjiang/.conda/envs/formatter/bin/obabel /content/{dir}/part{pnum}/{path}{index}/{path}_B.pdb -O ./{dir}/part{pnum}/{path}{index}/ligand.mol2")
      os.system(f"/home/phjiang/.conda/envs/formatter/bin/obabel /content/{dir}/part{pnum}/{path}{index}/{path}_B.pdb -O temp.smi")
      smiles = open(f"temp.smi").read().split("	")[0]
      #print(smiles)
      open(f"./{dir}/part{pnum}/{path}{index}/ligand.txt", "w").write(smiles)
      #os.system(f"rm out/{path}/{path}_B.pdb")
      os.rename(f"./{dir}/part{pnum}/{path}{index}/{path}_A.pdb", f"./{dir}/part{pnum}/{path}{index}/protein.pdb")
      os.rename(f"./{dir}/part{pnum}/{path}{index}/{path}_B.pdb", f"./{dir}/part{pnum}/{path}{index}/ligand.pdb")
      #os.system(f"rm tmp{index}.pdb")
      i += 1
    else:
      structure = parser.get_structure(path,k)
      pdb_chains = structure.get_chains()
      if(mins):
        index = dnum+"_"+nnum
      else:
        index = i
      os.system(f"mkdir {dir}/{path}{index}")
      for chain in pdb_chains:
          io.set_structure(chain)
          fil = str(structure.get_id()) + "_" + str(chain.get_id()) + ".pdb"
          io.save(f"{dir}/{path}{index}/{fil}")

      box, residues = get_box(f"{dir}/{path}{index}/{path}_B.pdb", f"{dir}/{path}{index}/{path}_A.pdb")

      with open(f'{dir}/{path}{index}/box.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(box)
        file.close()

      with open(f'{dir}/{path}{index}/pocket.txt', 'w', newline='') as file:
        for aa in residues:
          file.write(f"{aa}\n")
        file.close()

      os.system(f"/home/phjiang/.conda/envs/formatter/bin/obabel ./{dir}/{path}{index}/{path}_B.pdb -O ./{dir}/{path}{index}/ligand.sdf")
      os.system(f"/home/phjiang/.conda/envs/formatter/bin/obabel ./{dir}/{path}{index}/{path}_B.pdb -O ./{dir}/{path}{index}/ligand.mol2")
      os.system(f"/home/phjiang/.conda/envs/formatter/bin/obabel ./{dir}/{path}{index}/{path}_B.pdb -O temp.smi")
      smiles = open(f"temp.smi").read().split("	")[0]
      #print(smiles)
      open(f"./{dir}/{path}{index}/ligand.txt", "w").write(smiles)
      #os.system(f"rm out/{path}/{path}_B.pdb")
      os.rename(f"./{dir}/{path}{index}/{path}_A.pdb", f"./{dir}/{path}{index}/protein.pdb")
      os.rename(f"./{dir}/{path}{index}/{path}_B.pdb", f"./{dir}/{path}{index}/ligand.pdb")
      #os.system(f"rm tmp{index}.pdb")
      i += 1

import warnings
warnings.filterwarnings('ignore')
dir = "final1"
path = "sys"
parts = False


os.system(f"mkdir ./{dir}")



import warnings
warnings.filterwarnings('ignore')
dir = args.dir
path = "sys"
parts = args.parts
mins = args.mins

os.system(f"mkdir ./{dir}")

convResults(dir, path, parts, dir, mins)