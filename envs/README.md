These are the environments associated for both the jupyter notebooks and the batch script runs.



# RFDiffProteinMPNN instructions
1) To start with, make sure that you download the weights for alphafold, as well as the learning rate schedules for RFDiffusion
```
apt-get install aria2
aria2c -q -x 16 https://files.ipd.uw.edu/krypton/schedules.zip
aria2c -q -x 16 http://files.ipd.uw.edu/pub/RFdiffusion/6f5902ac237024bdd0c176cb93063dc4/Base_ckpt.pt
aria2c -q -x 16 http://files.ipd.uw.edu/pub/RFdiffusion/e29311f6f1bf1af907f9ef9f44b8328b/Complex_base_ckpt.pt
aria2c -q -x 16 https://storage.googleapis.com/alphafold/alphafold_params_2022-12-06.tar
tar -xf alphafold_params_2022-12-06.tar -C params
touch params/done.txt
git clone https://github.com/sokrypton/RFdiffusion.git
```
If you do not have sudo perms (i.e. running on htc), you can download the above separately (locally) and upload them to the online environment. It will take much much longer, but it shouldn't break anything.

2)  Now, you can start downloading the environment
```
git clone https://github.com/patjiang/openBind.git
cd ./openBind/envs
mamba create -n generate -f RFDiffProteinMPNN.yml
```

3) Activate the environment
```
source activate generate
```

4) If you are planning to run using jupyter, make sure to do:
```
mkjupy generate
```

5) At this point, it should all be done!


# GAABind instructions
1) This one is very straightforward; you can just do the following:
```
git clone https://github.com/patjiang/openBind.git #this is not required if you are already in the right directory
cd ./openBind/envs
mamba create -n gbind -f gaabind.yml
```

#FAQ - These usually occur with batch scripts:
1) Module not Found?
a: Make sure when you do python _____scriptname____.py, check to see ```which python``` you are using. Make sure that the environment is both activated, and the python you are using is in the ```.conda/envs/$ENVNAME/bin/python```

2) File not found?
a: ensure that you change the paths from the template scripts to those that match with your native file system. 



