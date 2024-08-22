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
- @article{dauparas2022robust,
  title={Robust deep learning--based protein sequence design using ProteinMPNN},
  author={Dauparas, Justas and Anishchenko, Ivan and Bennett, Nathaniel and Bai, Hua and Ragotte, Robert J and Milles, Lukas F and Wicky, Basile IM and Courbet, Alexis and de Haas, Rob J and Bethel, Neville and others},
  journal={Science},
  volume={378},
  number={6615},  
  pages={49--56},
  year={2022},
  publisher={American Association for the Advancement of Science}
}

TODO:
- Create script that will automate length of binder to generate
- Adapt GeneratingBackbonesandAAseqs.ipynb to a jupyter instance or even just a .py instance
- Adapt DynamicBind/GAABind from jupyter/htc over to colaboratory instances.
