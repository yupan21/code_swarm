#!/usr/bin/env python

import os
import sys
from bin.merge_logs import merge_log_file


def main(argv):
    cmd = "python E:/codeE/code_swarm/bin/code_swarm"
    merge_path = "E:\codebang\merged"
    root="E:\codebang"
    mergedLog = 'E:\codebang\log.xml'
    for dir in os.listdir(root):
        path = os.path.join(root, dir)
        if os.path.isdir(path):
            print(path)
            os.chdir(path)
            if os.system(cmd) == 0:
                logSrcFile = os.path.join(path, ".code_swarm", "log.xml")
                logFileName = "log_"+dir+".xml"
                logDistFile = os.path.join(merge_path, logFileName)
                if os.path.exists(logSrcFile) and os.path.exists(logDistFile):
                    os.remove(logDistFile)
                os.rename(logSrcFile, logDistFile)
            else:
                print("Error running `%s' in `%s' " % (cmd, os.getcwd()))
    output = open(mergedLog, "w", encoding="utf-8")
    file_list = os.listdir(merge_path)
    file_list = map(lambda file: os.path.join(merge_path, file), file_list)
    file_list = [os.path.join(merge_path, file) for file in file_list]

    merge_log_file(file_list, output)




# Main entry point.
if __name__ == "__main__":
    main(sys.argv)
