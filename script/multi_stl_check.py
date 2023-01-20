import os

from script.system_command import runSystemCommand


def checkMultiSTL(soPathDir):
    if os.path.exists(soPathDir):
        libFiles = []
        for filename in os.listdir(soPathDir):
            print(filename)
            if filename.endswith(".so"):
                libFiles.append(filename)
        checkLibsResult = dict()
        for lib in libFiles:
            if checkIsStlLinked(soPathDir + "/" + lib):
                checkLibsResult[lib] = soPathDir + "/" + lib

        if len(checkLibsResult) > 1:
            print("checkMultiSTL True:" + str(checkLibsResult))
            return True
        else:
            print("checkMultiSTL False")
            return False
    else:
        print("checkMultiSTL soPathDir not Found")
        return False


def checkIsStlLinked(soPath):
    size_output: str = runSystemCommand(['nm',
                                         "-D",
                                         "-C",
                                         soPath])
    for line in size_output.split("\n"):
        columns = line.split(" ")
        if len(columns) >= 3 and columns[1] == "T" and columns[2].startswith("std::"):
            print(line)
            print("checkIsStlLinked true")
            return True
    print("checkIsStlLinked false")
    return False
