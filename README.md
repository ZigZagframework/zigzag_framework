# Robustness of Deep Learning-based Vulnerability Detectors: Attack and Defense #

Automatically detecting software vulnerabilities in source code has attracted much attention. In particular, deep learning-based (DL-based) vulnerability detectors are attractive because they do not require human experts to define features and can achieve low false-positives and low false-negatives. However, their robustness against malicious attacks has not been investigated. 

We initiate the study on the robustness of DL-based vulnerability detectors. We use experiments to demonstrate the feasibility of attacks against them. As a first step towards enhancing their robustness, we propose an innovative ZigZag framework, which can enhance a class of DL-based vulnerability detectors. The key insight underlying the framework is to distinguish feature learning from classifier learning, which allows an innovative ZigZag technique we propose to make the learned features and classifiers “invariant” to attack-caused transformations.

## Dataset ##

Our attack and defense experiments are conducted based on a new dataset, which is derived from the National Vulnerability Database (NVD) and Software Assurance Reference Dataset (SARD). The dataset contains 13,347 programs and their manipulated programs, which lead to 71,252 vulnerable examples and 97,471 non-vulnerable examples at the granularity of function, while noting that a program may contain multiple examples. 

In order to compare the effectiveness of vulnerability detectors operating at different granularities (i.e., function vs. program slice), we take vulnerable (i.e., positive) examples and non-vulnerable (i.e., negative) examples at the granularity of function as the ground truth, because each vulnerability can map to a function and each function has at most one vulnerability in our dataset.

The manipulated programs are obtained by applying 8 code transformations, which are selected from what are offered by the source-to-source tool known as [Tigress](http://tigress.cs.arizona.edu/index.html). These 8 transformations are shown in the following table. 

|Type|Description|
|:-|:-|
|1|Data transformations|
|1-1|Replace literal strings with calls to a function that generates them|
|1-2|Reorder function arguments and/or add bogus arguments|
|2|Control transformations|
|2-1|Remove control flow from a function (i.e., control-flow flattening)|
|2-2|Merge multiple functions into one without control-flow flattening|
|2-3|Merge multiple functions into one with control-flow flattening|
|2-4|Split the top-level list of statements into multiple functions|
|2-5|Split a basic block into multiple functions|
|2-6| Split a basic block into multiple functions, and calls to split functions are also allowed to be split out|
