# openBind
Open Source Code for ASU iGEM 2024 De Novo Design Project


This Repository serves as a series of Colaboratory Notebooks and other implementations; feel free to tinker the code depending on the amount of compute resources you have available.

## IMPORTANT NOTE
To use any of the batchscripts/jupyter notebook codes, please follow the following steps listed below:

#TODO - Conda Env installation, Hardware Requirements

#TODO - Conda Package Management

#TODO - Comparison of runtimes for generating 64 binders

For the sake of this comparison, we will do a minimally sufficient task. We will first generate 8 unique structures, and 8 possible sequences from each structure. Then, the formatting and evaulation using GAABind and DynamicBind will be the same format. In each step, we will record the relative CHE and cost of running the code, as well as the time that each step took. If one of the steps takes an arbitrarily long amount of time to compute, we will denote it with a DNC (Did not compute).

  - Define out for each approach - Minimal Computation colaboratory, Maximal Computation colaboratory, batchscripts, Jupyter Notebook
  - For Minimal Computation, use T4 gpu only, in Maximal Computation, batchscripts, Jupyter Notebook, use A100_80 GPU's

#TODO - Comparison of CHE (Core-Hour Equivalents) as well as market price computation costs


References/Attributions:
- https://github.com/sokrypton/ColabDesign
- https://github.com/RosettaCommons/RFdiffusion
  - Watson, J.L., Juergens, D., Bennett, N.R. et al. De novo design of protein structure and function with RFdiffusion. Nature 620, 1089–1100 (2023). https://doi-org.ezproxy1.lib.asu.edu/10.1038/s41586-023-06415-8
- https://github.com/dauparas/ProteinMPNN
  - J. Dauparas et al. ,Robust deep learning–based protein sequence design using ProteinMPNN.Science378,49-56(2022).DOI:10.1126/science.add2187
- https://github.com/Mercuryhs/GAABind
  - Huishuang Tan, Zhixin Wang, Guang Hu, GAABind: a geometry-aware attention-based network for accurate protein–ligand binding pose and binding affinity prediction, Briefings in Bioinformatics, Volume 25, Issue 1, January 2024, bbad462, https://doi-org.ezproxy1.lib.asu.edu/10.1093/bib/bbad462

TODO:
- Create script that will automate length of binder to generate
- Adapt GeneratingBackbonesandAAseqs.ipynb to a jupyter instance or even just a .py instance
- Adapt DynamicBind/GAABind from jupyter/htc over to colaboratory instances.
