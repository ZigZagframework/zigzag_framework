# Towards Making Deep Learning-based Vulnerability Detectors Robust

We focus on deep learning-based vulnerability detection in source code. 
We propose the ZigZag framework to improve the robustness of existing deep learning-based detectors. The key idea is to seperate feature learning from classifier learning, which makes the learned features and classifiers “constant” to code transformations.

Our dataset is derived from the [NVD](https://nvd.nist.gov/) and the [SARD](https://samate.nist.gov/SRD/index.php). The dataset contains 6,803 programs and their manipulated programs, corresponding to 50,562 vulnerable examples and 80,043 non-vulnerable examples at the granularity of function. 

To compare the effectiveness of deep learning-based detectors at different granularities, we use vulnerable examples and non-vulnerable examples at the granularity of function as the ground truth. We apply 8 composite code transformations to generate manipulated programs, which are selected from the source-to-source tool [Tigress](https://tigress.wtf/). 
