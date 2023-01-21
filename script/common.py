# This is a sample Python script.

# 在ndk里面 find ~/Library/Android/sdk/ndk/25.1.8937393 -name [libc++_shared.so crtbegin_dynamic.o   crtend_so.o
# libGLESv3.so         libamidi.so          libc++.so            libicu.so            libmediandk.so
# libstdc++.so crtbegin_so.o        libEGL.so            libOpenMAXAL.so      libandroid.so        libc.so
# libjnigraphics.so    libnativehelper.so   libsync.so crtbegin_static.o    libGLESv1_CM.so      libOpenSLES.so
# libbinder_ndk.so     libcamera2ndk.so     liblog.so            libnativewindow.so   libvulkan.so crtend_android.o
# libGLESv2.so         libaaudio.so         libc++.a             libdl.so             libm.so
# libneuralnetworks.so libz.so
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

from treelib import Tree

exclude_so = []


def getNdkSupportSoOptimize(ndkPath):
    ndk_path_so_list = os.listdir(ndkPath)
    print("ndkPathSoList" + str(ndk_path_so_list))
    for item in ndk_path_so_list:
        if item not in exclude_so and ".so" in item:
            exclude_so.append(item)
    print("exclude_so" + str(len(exclude_so)))
    print("exclude_so" + str(exclude_so))


def parseSoDefinedSymbolOptimize(soPath):
    defined_symbol = []
    # readelf -Ws libcmaketest.so
    command = "readelf -Ws " + soPath + " | awk '$4~/FUNC/ || $4~/OBJECT/ || $4~/WEAK/ && $7!~/UND/ {print $8}'"
    result = os.popen(command)
    result_content = result.read()
    for line in result_content.split("\n"):
        defined_symbol_item = line
        if len(defined_symbol_item) > 0 and defined_symbol_item not in defined_symbol:
            # print(defined_symbol_item_list[1])
            defined_symbol.append(defined_symbol_item)
    return list(set(defined_symbol))


def parseSoUndefinedSymbolOptimize(soPath):
    undefined_symbol = []
    # readelf -Ws libcmaketest.so
    # readelf -Ws /usr/lib/libstdc++.so.6 | grep '^\([[:space:]]\+[^[:space:]]\+\)\{6\}[[:space:]]\+[[:digit:]]\+'
    # readelf -Ws /usr/lib/libstdc++.so.6 | awk '{print $8}'
    # readelf -Ws libc++_shared.so |awk '{print $1,$2,$3,$4,$5,$6,$7,$8 }'
    # https://stackoverflow.com/questions/34732/how-do-i-list-the-symbols-in-a-so-file
    # https://pypi.org/project/elf-diff/
    command = "readelf -Ws " + soPath + " | awk '$7~/UND/ && $8!~/@LIBC/{print $8}'"
    result = os.popen(command)
    result_content = result.read()
    for line in result_content.split("\n"):
        if len(line) > 0 and line not in undefined_symbol:
            undefined_symbol.append(line)
    return undefined_symbol


def parseSoDepsSoLibNameOptimize(soPath):
    deps_libs = []
    # readelf -d libcmaketest.so | grep "NEEDED"
    command = "readelf -d " + soPath + " | grep 'NEEDED' | awk '{print $5}'"
    result = os.popen(command)
    result_content = result.read()
    for line in result_content.split("\n"):
        deps_libs_item = line
        deps_libs_item = deps_libs_item.replace("[", "")
        deps_libs_item = deps_libs_item.replace("]", "")
        if len(deps_libs_item) > 0:  # and deps_libs_item not in exclude_so:
            deps_libs.append(deps_libs_item)
    return deps_libs


def parseNoFoundUndefinedSymbolFunOptimize(check_undefined_symbol):
    if len(check_undefined_symbol) > 0:
        print(check_undefined_symbol)
        z = []
        for diff_symbol_item in check_undefined_symbol:
            if "_Z" in diff_symbol_item:
                command = "c++filt" + " " + diff_symbol_item
                result = os.popen(command)
                result_content = result.read()
                result_content = result_content.replace("\n", "")
                z.append(result_content)
        print(z)
        print("_Z undefined_symbol:" + str(len(z)))


def checkSoOptimize(soPath, soName, ndkSoPath):
    print(soPath + "/" + soName)
    deps_libs = generateSoTreeOptimize(soPath, soName, ndkSoPath)
    print(deps_libs)
    check_undefined_symbol = parseSoUndefinedSymbolOptimize(soPath + "/" + soName)

    check_undefined_symbol = list(set(check_undefined_symbol))
    print(len(check_undefined_symbol))
    check_defined_symbol = []
    for lib in deps_libs:
        if lib == soName:
            print(lib + " no need exec ")
        else:
            if lib not in exclude_so:
                lib_defined_symbol = parseSoDefinedSymbolOptimize(soPath + "/" + lib)
            else:
                lib_defined_symbol = parseSoDefinedSymbolOptimize(ndkSoPath + "/" + lib)
            print(lib + " defined_symbol:" + str(len(lib_defined_symbol)))
            for symbol in lib_defined_symbol:
                if symbol not in check_defined_symbol:
                    check_defined_symbol.append(symbol)
    for need_symbol in check_defined_symbol:
        if need_symbol in check_undefined_symbol:
            check_undefined_symbol.remove(need_symbol)
    print(len(check_undefined_symbol))
    parseNoFoundUndefinedSymbolFunOptimize(check_undefined_symbol)


def checkSoTreeOptimize(soPath, identifier_name, soName, ndkSoPath, tree, merge_so_libs):
    deps_libs = parseSoDepsSoLibNameOptimize(soPath + "/" + soName)
    so_data = dict()
    so_data["soName"] = soName
    so_data["soPath"] = soPath
    merge_so_libs[soName] = soPath
    if identifier_name == "Root":
        identifier_name = identifier_name + "@" + soName
        tree.create_node(tag=soName, identifier=identifier_name, data=so_data)
    else:
        tree.create_node(tag=soName, identifier=identifier_name + "@" + soName, parent=identifier_name,
                         data=so_data)
        identifier_name = identifier_name + "@" + soName
    for lib in deps_libs:
        if lib not in exclude_so:
            checkSoTreeOptimize(soPath, identifier_name, lib, ndkSoPath, tree, merge_so_libs)
        else:
            checkSoTreeOptimize(ndkSoPath, identifier_name, lib, ndkSoPath, tree, merge_so_libs)


def generateSoTreeOptimize(soPath, soName, ndkSoPath):
    tree = Tree()
    merge_so_libs = dict()
    getNdkSupportSoOptimize(ndkSoPath)
    checkSoTreeOptimize(soPath,
                        "Root",
                        soName,
                        ndkSoPath,
                        tree,
                        merge_so_libs)
    tree.show()
    tree.to_graphviz()
    libs = []
    for keySoName, valueSoPath in merge_so_libs.items():
        print('{key}:{value}'.format(key=keySoName, value=valueSoPath))
        if keySoName != soName:
            libs.append(keySoName)
    print(str(libs) + " " + soName)
    return libs


def generateSoTree(soPath, soName, ndkSoPath):
    tree = Tree()
    merge_so_libs = dict()
    getNdkSupportSoOptimize(ndkSoPath)
    checkSoTreeOptimize(soPath,
                        "Root",
                        soName,
                        ndkSoPath,
                        tree,
                        merge_so_libs)
    tree.show()
    tree.to_graphviz()

    for keySoName, valueSoPath in merge_so_libs.items():
        print('{key}:{value}'.format(key=keySoName, value=valueSoPath))


def checkSoMd5(soPath):
    command = "md5 " + soPath + " | awk '{print $4}'"
    result = os.popen(command)
    result_content = result.read()
    for line in result_content.split("\n"):
        print(line)


def checkSoBuildId(soPath):
    command = "readelf -n " + soPath
    result = os.popen(command)
    result_content = result.read()
    for line in result_content.split("\n"):
        print(line)
