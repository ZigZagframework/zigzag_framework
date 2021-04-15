# Robustness of Deep Learning-based Vulnerability Detectors: Attack and Defense #

We propose the ZigZag framework to improve existing DL-based vulnerability detectors. The key idea is to distinguish feature learning from classifier learning, which allows ZigZag  to make the learned features and classifiers “constant” to code transformations.

Our dataset is derived from the [NVD](https://nvd.nist.gov/) and the [SARD](https://samate.nist.gov/SRD/index.php). The dataset contains 6,803 programs and their manipulated programs, corresponding to 50,562 vulnerable examples and 80,043 non-vulnerable examples at the granularity of function. 

To compare the effectiveness of deep learning-based detectors at different granularities, we take vulnerable examples and non-vulnerable examples at the granularity of function as the ground truth. We apply 8 composite code transformations to generate manipulated programs, which are selected from the source-to-source tool [Tigress](https://tigress.wtf/). 
