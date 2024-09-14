Hello! This is the filepath made to be used with HTC (High-Throughput Computing). Attached will be .py scripts I have created as well as possible system requirements. I will not include slurm commands and my batch scripts, however, as those likely differ from institution to institution
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 555.58.02              Driver Version: 555.58.02      CUDA Version: 12.5     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA A100-SXM4-80GB          On  |   00000000:01:00.0 Off |                    0 |
| N/A   53C    P0            205W /  500W |    2129MiB /  81920MiB |     73%      Default |
|                                         |                        |             Disabled |
+-----------------------------------------+------------------------+----------------------+
```

System requirements (With the environment.yml as given): CUDA12+, python 3.10 
