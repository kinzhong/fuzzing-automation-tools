# Intro
This tool automates crash triaging for fuzzing.

Firstly, run-crashes.sh will find and execute all obtained crash files from fuzzing and compiling them into a large crash file. run-crashes.sh currently uses AFL's crash id naming system to identify crashes. This can be modified easily by changing the header variable located at the top of the script.

Next, the crash analyser will analyse the crash files, interpret the ASan error messages and perform crash bucketing to provide a report on the findings. It will also identify vulnerabilities such as buffer overflows and null pointer dereference. The analyser generates two reports. Main_report.txt contains all key findings while full_error_analysis contains the analysis of every crash provided. 

# Requirements
The crash analyser requires the program to be compiled with ASan enabled.

# Usage
Runs all obtained crash files and pipe output to crashes.log.
```
./run-crashes.sh $INPUT_DIR $ASAN-INSTRUMENTED-PROGRAM "OTHER COMMANDLINE OPTIONS" > crashes.log 2>&1
```

Runs crash analysis on all crash logs and generate reports.
```
python3 crash-analyser.py $CRASH-LOG
```

