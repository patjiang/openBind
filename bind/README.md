# This Folder is associated with all of the scripts after generation and fileformatting. The assumption is that you have followed the general format that is already set, i.e.:
```
generation_iteration/
├── sys{$DESIGN_NUM}_{$SEQ_NUM} (1)
├    ├── box.csv (1)
├    ├── ligand.mol2 (1)
├    ├── ligand.pdb (1)
├    ├── ligand.sdf (1)
├    ├── ligand.txt (1)
├    ├── pocket.txt (1)
├    └── protein.pdb (1)
├── sys{$DESIGN_NUM}_{$SEQ_NUM} (2)
├    ├── box.csv (2)
├    ├── ligand.mol2 (2)
├    ├── ligand.pdb (2)
├    ├── ligand.sdf (2)
├    ├── ligand.txt (2)
├    ├── pocket.txt (2)
├    └── protein.pdb (2)
├── sys{$DESIGN_NUM}_{$SEQ_NUM} (3)
...
└── sys{$DESIGN_NUM}_{$SEQ_NUM} (n)
     ├── box.csv (n)
     ├── ligand.mol2 (n)
     ├── ligand.pdb (n)
     ├── ligand.sdf (n)
     ├── ligand.txt (n)
     ├── pocket.txt (n)
     └── protein.pdb (n)
```
- So, your associated next step is to use the path to the directory as the inDir in the runbind script, and you can choose any arbitrary string for outDir. We recommend the usage of the same name, because the scripts for results analysis are set up to do so

## For the associated packages and scripts necessary to run the batchscripts/jupynb, make sure to download and unzip the dir from huggingface

### Huggingface link:
Link to download is (here)[https://huggingface.co/datasets/phjiang/openBind_dirs]
