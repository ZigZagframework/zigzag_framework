These programs are the input training programs to the deep learning-based vulnerability detector.
The file id2FuncExamples_Training.pkl is the path information of the NonVulnerable samples and Vulnerable samples in the programs.The information is written as a dict with the following form: {int(testcase id):{program filename:{func_name:startline_endline}}}. 
