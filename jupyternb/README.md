Hello! This is the path for primarily interactive jupyter instances.

For further clarification, the environment was built and ran with these specs:


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

A100_80 is not required, unless a larger batch of sequences are being generated.
