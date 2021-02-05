# Robustness of Deep Learning-based Vulnerability Detectors: Attack and Defense #

Automatically detecting software vulnerabilities in source code has attracted much attention. In particular, deep learning-based (DL-based) vulnerability detectors are attractive because they do not require human experts to define features and can achieve low false-positives and low false-negatives. However, their robustness against malicious attacks has not been investigated. 

We initiate the study on the robustness of DL-based vulnerability detectors. We use experiments to demonstrate the feasibility of attacks against them. As a first step towards enhancing their robustness, we propose an innovative ZigZag framework, which can enhance a class of DL-based vulnerability detectors. The key insight underlying the framework is to distinguish feature learning from classifier learning, which allows an innovative ZigZag technique we propose to make the learned features and classifiers “invariant” to attack-caused transformations.

## Dataset ##

Our attack and defense experiments are conducted based on a new dataset, which is derived from the National Vulnerability Database (NVD) and Software Assurance Reference Dataset (SARD). The dataset contains 6,803 programs and their manipulated programs, which lead to 50,562 vulnerable examples and 80,043 non-vulnerable examples at the granularity of function, while noting that a program may contain multiple examples. 

In order to compare the effectiveness of vulnerability detectors operating at different granularities (i.e., function vs. program slice), we take vulnerable (i.e., positive) examples and non-vulnerable (i.e., negative) examples at the granularity of function as the ground truth, because each vulnerability can map to a function and each function has at most one vulnerability in our dataset.

The manipulated programs are obtained by applying 8 composite code transformations, which are selected from what are offered by the source-to-source tool known as [Tigress](https://tigress.wtf/). These 8 code transformations, are shown in the following table. 


|No.|Name|Description|
|:-|:-|:-|
|CT-1|EncodeStrings|Replace literal strings with calls to a function that generates them|
|CT-2|RndArgs|Reorder function arguments and/or add bogus arguments|
|CT-3|Flatten|Remove control flow from a function|
|CT-4|MergeSimple|Merge multiple functions into one without control-flow flattening|
|CT-5|MergeFlatten|Merge multiple functions into one with control-flow flattening|
|CT-6|SplitTop|Split top-level statements into multiple functions|
|CT-7|SplitBlock|Split a basic block into multiple functions|
|CT-8|SplitRecursive| Split a basic block into multiple functions, and split the calls to split functions|
