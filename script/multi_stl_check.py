import os

from script.system_command import runSystemCommand


def checkMultiSTL(soPathDir):
    if os.path.exists(soPathDir):
        lib_files = []
        for filename in os.listdir(soPathDir):
            print(filename)
            if filename.endswith(".so"):
                lib_files.append(filename)
        check_libs_result = dict()
        for lib in lib_files:
            if checkIsStlLinked(soPathDir + "/" + lib):
                check_libs_result[lib] = soPathDir + "/" + lib

        if len(check_libs_result) > 1:
            print("checkMultiSTL True:" + str(check_libs_result))
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
