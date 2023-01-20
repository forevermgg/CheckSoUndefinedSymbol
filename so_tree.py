# coding=utf-8
import optparse
import os

parser = optparse.OptionParser()
parser.add_option('-n', '--ndk', dest='ndk', help='NDK ROOT path to your NDK installation')
parser.add_option('-c', '--checkSoName', dest='checkSoName', help='object file name (e.g. .so containing '
                                                                  'debug symbols)')
parser.add_option('-p', '--checkSoPath', dest='checkSoPath', help='object file path (e.g. .so containing '
                                                                  'debug symbols)')
# parse
(options, args) = parser.parse_args()

if __name__ == '__main__':
    # exit on missing options
    if not (options.ndk and options.checkSoName and options.checkSoPath):
        parser.print_help()
    else:
        if not os.path.exists(options.ndk):
            raise RuntimeError(options.ndk + " not found")
        else:
            print("ndk：" + options.ndk)
        if not os.path.exists(options.checkSoPath):
            raise RuntimeError(options.checkSoPath + " not found")
        else:
            print("checkSoPath：" + options.checkSoPath)
        if not os.path.exists(options.checkSoPath + "/" + options.checkSoName):
            raise RuntimeError(options.checkSoPath + " not found")
        else:
            print("checkSoName：" + options.checkSoName)
