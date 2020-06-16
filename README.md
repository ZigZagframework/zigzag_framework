# Robustness of Deep Learning-based Vulnerability Detectors: Attack and Defense #

Automatically detecting software vulnerabilities in source code has attracted much attention. In particular, deep learning-based (DL-based) vulnerability detectors are attractive because they do not require human experts to define features and can achieve low false-positives and low false-negatives. However, their robustness against malicious attacks has not been investigated. 

We initiate the study on the robustness of DL-based vulnerability detectors. We use experiments to demonstrate the feasibility of attacks against them. As a first step towards enhancing their robustness, we propose an innovative ZigZag framework, which can enhance a class of DL-based vulnerability detectors. The key insight underlying the framework is to distinguish feature learning from classifier learning, which allows an innovative ZigZag technique we propose to make the learned features and classifiers “invariant” to attack-caused transformations.

## Dataset ##

Our attack and defense experiments are conducted based on a new dataset, which is derived from the National Vulnerability Database (NVD) and Software Assurance Reference Dataset (SARD). The dataset contains 13,347 programs and their manipulated programs, which lead to 71,252 vulnerable examples and 97,471 non-vulnerable examples at the granularity of function, while noting that a program may contain multiple examples.
