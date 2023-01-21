import os


def diffoscopeCheck(soPathLeft, soPathRight):
    command = "diffoscope " + soPathLeft + " " + soPathRight
    result = os.popen(command)
    result_content = result.read()
    if result_content == '':
        print("diffoscope check is same file")
        return True
    else:
        for line in result_content.split("\n"):
            print(line)
        return False
