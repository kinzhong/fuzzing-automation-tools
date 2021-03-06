# Intro
This tool automates crash triaging for fuzzing using.

Firstly, run-crashes.sh will find and execute all obtained crash files from fuzzing and compiling them into a large logfile. 

Next, the crash analyser will analyse the logs, interpret the AddressSanitizer error messages and perform crash bucketing to provide a report on the findings. It will also identify vulnerabilities such as buffer overflows and null pointer dereference. The analyser generates two reports. main_report.txt contains all key findings while full_error_analysis.txt contains the crash analysis for every crash file. 

Samples reports can be found [here](https://github.com/kinzhong/fuzzing-automation-tools/tree/main/automated-crash-analysis/sample_reports).

# Requirements
The crash analyser requires the program to be compiled with AddressSanitizer enabled.

# Usage
Runs all obtained crash files and pipe output to crashes.log.
```
./run-crashes.sh $INPUT_DIR $ASAN-INSTRUMENTED-PROGRAM "OTHER COMMANDLINE OPTIONS" > crashes.log 2>&1
```

Runs crash analysis on all crash logs and generate reports.
```
python3 crash-analyser.py $CRASH-LOG
```

# Cross Compatibility with Other Fuzzers
As the analyser purely uses AddressSanitizer for its analysis, other fuzzers are also compatible. 

Currently, run-crashes.sh uses AFL's crash id naming system to identify crashes. Thus, modify the header variable located at the top of [run-crashes.sh](https://github.com/kinzhong/fuzzing-automation-tools/blob/main/automated-crash-analysis/run-crashes.sh) to something that can correctly match the crash file names. 
