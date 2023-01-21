import os

from script.system_command import runSystemCommand


def isSoStripped(soFilePath):
    if isSoStrippedByReadElf(soFilePath) and isSoStrippedByFile(soFilePath):
        print("isSoStripped False")
        return False
    else:
        print("isSoStripped True")
        return True


def isSoStrippedByFile(soFilePath):
    # readelf -S libskia.so | grep debug | awk '{print $2}'
    size_output: str = runSystemCommand(['file',
                                         soFilePath])
    if "debug_info" in size_output and "not stripped" in size_output:
        print("isSoStrippedByFile False")
        return False
    else:
        print("isSoStrippedByFile True")
        return True


def isSoStrippedByReadElf(soFilePath):
    # readelf -S libskia.so | grep debug | awk '{print $2}'
    command = "readelf -S " + soFilePath + " | grep debug | awk '{print $2}'"
    result = os.popen(command)
    result_content = result.read()
    for line in result_content.split("\n"):
        print(line)
        if "debug_info" in line:
            print(line)
            print("isSoStrippedByReadElf False")
            return False
    print("isSoStrippedByReadElf True")
    return True
