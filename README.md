# openBind
Open Source Code for ASU iGEM 2024 De Novo Design Project


This Repository serves as a series of Colaboratory Notebooks and other implementations; feel free to tinker the code depending on the amount of compute resources you have available.

## IMPORTANT NOTE
To use any of the batchscripts/jupyter notebook codes, please follow the instructions inside the envs folder



## Comparison of runtimes for generating 64 binders

For the sake of this comparison, we will do a minimally sufficient task. We will first generate 8 unique structures, and 8 possible sequences from each structure. Then, the formatting and evaulation using GAABind and DynamicBind will be the same format. In each step, we will record the CHE of running the code, as well as the time that each step took. If one of the steps takes an arbitrarily long amount of time to compute, we will denote it with a DNC (Did not compute).

  - Define out for each approach - Minimal Computation colaboratory, Maximal Computation colaboratory, batchscripts, Jupyter Notebook
  - For Minimal Computation, use T4 gpu only, in Maximal Computation, batchscripts, Jupyter Notebook, use A100_80 GPU's

#TODO - Comparison of CHE (Core-Hour Equivalents) as well as market price computation costs


References/Attributions:


[ColabDesign](https://github.com/sokrypton/ColabDesign)

[RFdiffusion](https://github.com/RosettaCommons/RFdiffusion)
```bibtex
    {
        RFdiffusion,
        title={{De novo design of protein structure and function with RFdiffusion.}}, 
        author={Watson, J.L., Juergens, D., Bennett, N.R. et al.},
        booktitle={Nature},
        year={2023},
        url={https://doi-org.ezproxy1.lib.asu.edu/10.1038/s41586-023-06415-8}
    }
```
[ProteinMPNN](https://github.com/dauparas/ProteinMPNN)
```bibtex
  {
      ProteinMPNN,
      title={{Robust deep learning–based protein sequence design using ProteinMPNN}}
      author = {J. Daupras et al.}
      booktitle={Science}
      year={2022}
      url={https://www.science.org/doi/10.1126/science.add2187}
  }
```
[GAABind](https://github.com/Mercuryhs/GAABind)
```bibtex
    GAABind,
    title = {{GAABind: a geometry-aware attention-based network for accurate protein–ligand binding pose and binding affinity prediction}}
    author = {H. Tan, Z. Wang, G. Hu, et al.}
    booktitle={Briefings in Bioinformatics, Volume 25, Issue 1}
    year={2024}
    url={https://doi-org.ezproxy1.lib.asu.edu/10.1093/bib/bbad462}
```

