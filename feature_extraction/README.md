# Feature Extraction

Feature extraction is the process of root cause analysis using the data set generated by data augmentation. The process consists of two steps. First, the analyzer runs the target program with each input in the dataset and records the state of the program. Second, it compares the traces of the crashed and non-crashed inputs and statistically infers the root cause from the difference.

Currently, RCABench supports two types of feature extraction methods as listed in the table below. If you want to add a new method, follow the instructions in ["How to add a new feature extraction method"](#how-to-add-a-new-feature-extraction-method).

| Method | Description |
| ---- | ---- |
| AuroraFE | AuroraFE is a method proposed in [Aurora [USENIX Security'20]](https://www.usenix.org/conference/usenixsecurity20/presentation/blazytko). |
| VulnLocFE | VulnLocFE is a method proposed in [VulnLoc [ASIA CCS'21]](https://dl.acm.org/doi/10.1145/3433210.3437528). |

## How to add a new feature extraction method

To add a new feature extraction method to RCABench, follow the three steps below.