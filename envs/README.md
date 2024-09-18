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
2) 


