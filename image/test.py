import os


def checkImageMagick(command):
    result = os.popen(command)
    result_content = result.read()
    for line in result_content.split("\n"):
        print(line)


checkImageMagick("which convert")
checkImageMagick("convert -version")
checkImageMagick("otool -L $(which convert)")
checkImageMagick("which rsvg-convert")

command = "od -bc " + './test.jpg' + " | head -6"
checkImageMagick(command)

command = "convert " + './test.jpg' + " -rotate 45 test_rotate_45.jpg"
checkImageMagick(command)

command = "convert " + './test.jpg' + " -resize 50% test_resize_50.jpg"
checkImageMagick(command)

command = "convert " + './test.jpg' + " -resize 150% test_resize_150.jpg"
checkImageMagick(command)

checkImageMagick("convert " + './test.jpg' + " ./test.png")
