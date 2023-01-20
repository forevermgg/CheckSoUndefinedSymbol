import os


def diffoscopeCheck(soPathLeft, soPathRight):
    command = "diffoscope " + soPathLeft + " " + soPathRight
    result = os.popen(command)
    resultContent = result.read()
    if resultContent == '':
        print("diffoscope check is same file")
        return True
    else:
        for line in resultContent.split("\n"):
            print(line)
        return False
