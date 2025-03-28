These are the environments associated for both the jupyter notebooks and the batch script runs.



# RFDiffProteinMPNN instructions
1) Create the environment
```
git clone https://github.com/patjiang/openBind.git
cd ./openBind/envs
mamba create -n generate -f RFDiffProteinMPNN.yml
```

2) Activate the environment
```
source activate generate
```

# GAABind instructions
1) This one is very straightforward; you can just do the following:
```
git clone https://github.com/patjiang/openBind.git #this is not required if you are already in the right directory
cd ./openBind/envs
mamba create -n gbind -f gaabind.yml
```

# DynamicBind instructions
1) Start with making the environment for Dynamic bind
```
git clone https://github.com/patjiang/openBind.git #this is not required if you are already in the right directory
cd ./openBind/envs
mamba create -n dynamicbind -f dynamic.yml
```
you can also set up step by step:
```
mamba create -n dynamicbind python=3.10
source activate dynamicbind
mamba install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
mamba install -c conda-forge rdkit
mamba install pyg  pyyaml  biopython -c pyg
mamba install pip
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.0.0+cu117.html
pip install e3nn  fair-esm spyrmsd
```
2) Now make the environment for structural relaxation
```
conda deactivate dynamicbind # you do not necessarily need to do so
mamba create --name relax python=3.8
source activate relax
mamba install -c conda-forge openmm pdbfixer libstdcxx-ng openmmforcefields openff-toolkit ambertools=22 compilers biopython
```



# FAQ - These usually occur with batch scripts:
1) Module not Found?

  a: Make sure when you do python _____scriptname____.py, check to see ```which python``` you are using. Make sure that the environment is both activated, and the python you are using is in the ```.conda/envs/$ENVNAME/bin/python```

2) File not found?

  a: ensure that you change the paths from the template scripts to those that match with your native file system. 



