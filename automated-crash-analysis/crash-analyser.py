import sys


def main():

    if len(sys.argv) < 2:
        print("Usage: python3 crash-analyser.py [FILE]")
        sys.exit()

    logfile = sys.argv[1]
    
    f = open(logfile, "r", encoding="utf8", errors="ignore")
    error_list = getErrors(f)
    
    error_tuples = []
    for error in error_list:
        error_tuples.append(analyseError(error))

    f.close()

    #categorised_list_of_tuples structure: [types_of_errors][error_no](error_no, crash_file_name, diagnosis, unknown_error_statement, error_msg, callstack0, callstack1)
    categorised_list_of_tuples = crashBucketing(error_tuples)

    writeMainReport(categorised_list_of_tuples, len(error_tuples), logfile)
    writeFullAnalysisReport(error_tuples, logfile)

def crashBucketing(error_tuples):

    error_list = []
    for i in error_tuples: 
        if i[2] not in error_list:
            error_list.append(i[2])

    categorised_list_of_tuples = []
    for error in error_list:
        
        new_list = []

        for i in error_tuples:

            if i[2] == error:
                new_list.append(i)

        
        #Perform crash bucketing
        unique = getUniqueCrashes(new_list)
        categorised_list_of_tuples.append(unique)

    #print(categorised_list_of_tuples[0][0][1])
    return categorised_list_of_tuples

def getUniqueCrashes(error_list):

    unique = []
    unqiueSummary = []

    for i in error_list:

        err_msg_lines = i[4].splitlines()
        callstack0 = ""
        callstack1 = ""
        
        for line in err_msg_lines[2:]:
            if "#0" in line:
                #obtain function location 
                temp = line.split(" ", 6)
                callstack0 = temp[6]
            elif "#1" in line:
                #obtain function location 
                temp2 = line.split(" ", 6)
                callstack1 = temp2[6]
            if (callstack0 != "" and callstack1 != "" ):
                break

        callstack = (callstack0, callstack1)
        if callstack not in unqiueSummary:
            unqiueSummary.append(callstack)
            newtuple = i + (callstack)
            unique.append(newtuple)
        
    return unique
    
def writeMainReport(error_list, totalno, logfilename):    

    ignored_errors = ["Unknown Error"]             #add errors to ignore to this list
    interesting_errors_msgs = []
    
    total = 0

    for error_type in error_list:
        total = total + len(error_type)
        if error_type[0][2] not in ignored_errors:
            interesting_errors_msgs = interesting_errors_msgs + error_type




    #Main Report Writing
    newfile = open("main_report.txt", "w", encoding="utf8", errors="ignore")
    newfile.write("Crash Analysis Report for " + logfilename + "\n\n")

    print("============ Overall Crash Analysis Findings ============")
    print("============ Overall Crash Analysis Findings ============", file=newfile)


    print("{:<30} {:>21}".format("Total Number of Crashes:", str(totalno)))
    print("{:<30} {:>21}".format("Total Number of Crashes:", str(totalno)), file=newfile)

    print("{:<30} {:>21}".format("Total Number of Unique Bugs:", str(total)))
    print("{:<30} {:>21}".format("Total Number of Unique Bugs:", str(total)), file=newfile)

    

    for error_type in error_list:    
        print("{:<30} {:>21}".format(str(error_type[0][2]) + ":" ,str(len(error_type))))
        print("{:<30} {:>21}".format(str(error_type[0][2]) + ":" ,str(len(error_type))), file=newfile)
        total = total - len(error_type)

    if total != 0:
        print("ERROR: mismatch in error numbers.")
        print("# of Uncategorised Errors: " + str (uncategorised))
        print("Number of uncategorised errors should always be zero")


    print("\nInteresting Crashes can be found in main_report.txt")
    print("Full analysis of every crash can be found in full_error_analysis.txt\n")


    newfile.write("\n================ Interesting Crashes ================\n\n")

    if (len(interesting_errors_msgs) <= 0):
        newfile.write("None.\n")
        newfile.close()
        return
    else:
        for error in interesting_errors_msgs:
            newfile.write("=============================================================================================================================================\n")
            newfile.write(error[0]+ "\n")
            newfile.write("Crash File Location: " + error[1]+ "\n")
            newfile.write("Diagnosis: " + error[2]+ "\n")
            newfile.write("AddressSanitiser Logs:\n")
            newfile.write(error[4][2:] + "\n")
            newfile.write("=============================================================================================================================================\n\n")

        newfile.close()



    #Unknown Error File Report
    for error_type in error_list:
        if error_type[0][2] == "Unknown Error":
            print("Unknown Errors can be analysed further in unknown_errors.txt\n")
            
            unknown_file = open("unknown_errors.txt", "w", encoding="utf8", errors="ignore")

            unknown_file.write("===================================================================\n")
            unknown_file.write("Unknown Errors Report for " + logfilename + "\n")
            unknown_file.write("===================================================================\n\n")

            for info in error_type:
                unknown_file.write("=============================================================================================================================================\n")            
                unknown_file.write(info[0] + "\n")
                unknown_file.write("Crash File Location: " + info[1]+ "\n")
                unknown_file.write("Diagnosis: " + info[2] + "\n")
                unknown_file.write("AddressSanitiser Logs:\n")
                unknown_file.write(error[4][2:] + "\n")
                unknown_file.write("=============================================================================================================================================\n\n")

            unknown_file.close()
        
def writeFullAnalysisReport(error_tuples, logfile):

    newfile = open("full_error_analysis.txt", "w", encoding="utf8", errors="ignore")

    newfile.write("===================================================================\n")
    newfile.write("Full Error Analysis Report for " + logfile + "\n")
    newfile.write("===================================================================\n\n")

    for info in error_tuples:
        newfile.write("=============================================================================================================================================\n")
        newfile.write(info[0] + "\n")
        newfile.write("Crash File Location: " + info[1]+ "\n")
        newfile.write("Diagnosis: " + info[2] + "\n")
        newfile.write("AddressSanitiser Logs:\n")
        if (info[3] != ""):
            newfile.write("Unknown Error Message: " + info[3]+ "\n")
        newfile.write(info[4])
        newfile.write("=============================================================================================================================================\n\n")
    newfile.close()

def analyseError(error):

    strings = error.splitlines()
    error_no = strings[0]
    file_loc = strings[1]
    diagnosis = ""
    unknown_error = ""
    for s in strings:

        if ( "ERROR: AddressSanitizer failed to allocate" in s and "bytes of LargeMmapAllocator (error code: 12)" in s):
            diagnosis = "Out Of Memory"

        elif ("ERROR: AddressSanitizer: heap-use-after-free" in s):
            diagnosis = "Heap Use After Free"

        elif ("ERROR: AddressSanitizer: heap-buffer-overflow on address" in s):
            diagnosis = "Heap Buffer Overflow"
            
        elif ("ERROR: AddressSanitizer: stack-buffer-overflow" in s):
            diagnosis = "Stack Buffer Overflow"
            
        elif ("ERROR: AddressSanitizer: global-buffer-overflow" in s):
            diagnosis = "Global Buffer Overflow"

        elif ("ERROR: AddressSanitizer: stack-use-after-return" in s):
            diagnosis = "Stack Use After Return"

        elif ("ERROR: AddressSanitizer: stack-use-after-scope" in s):
            diagnosis = "Stack Use After Scope"
            
        elif ("ERROR: AddressSanitizer: initialization-order-fiasco" in s):
            diagnosis = "Initialization Order Fiasco"

        elif ("ERROR: LeakSanitizer: detected memory leaks" in s):
            diagnosis = "Memory Leaks"

        elif ("ERROR: AddressSanitizer: SEGV on unknown address" in s):
            diagnosis = "NULL pointer Dereference"
            
        elif ("ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed" in s):
            diagnosis = "Invalid Free"

        #Add more error categories if necessary.


    #Crash is categorised as Unknown if no matching pattern is found.
    if (diagnosis == ""):
        for s in strings:
            if("ERROR: AddressSanitizer" in s):
                diagnosis = "Unknown Error"
                unknown_error = s

    #This occurs when there is no errors found.
    if (diagnosis == ""):
            diagnosis = "Unknown Error"


    error_msg = error.split("\n")
    error_msg = error_msg[2:]
    error_msg = '\n'.join(error_msg)
    
    return error_no, file_loc, diagnosis, unknown_error, error_msg;

def getErrors(logfile):

    error_no = 0;
    keyword_search_pattern = "Error No. #"

    line_list = logfile.readlines()
    error_msg = ""
    error_list = []
    
    for line in line_list:

        #if its a new error msg, add the existing msg to list
        if (line == (keyword_search_pattern + str(error_no+1)+"\n")):
            error_list.append(error_msg)
            error_msg = ""
            error_no = error_no + 1

        error_msg = error_msg + line

    #for the last error msg
    error_list.append(error_msg)

    return error_list;

if __name__ == "__main__":
    main()
