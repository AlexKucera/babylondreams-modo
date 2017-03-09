#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_blend_hierarchy_split_passes

Release Notes:

    TODO:
    * https://docs.python.org/2/library/xml.etree.elementtree.html
    * https://developer.apple.com/library/content/documentation/AppleApplications/Reference/FinalCutPro_XML/Topics/Topics.html#//apple_ref/doc/uid/TP30001149-CH294-SW19

V0.1 Initial Release - 2017-02-22

"""

import re
import modo
import lx
import traceback
from pprint import pprint

from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------


def main():
    scene = modo.Scene()

    func_name = BLEND_COMMAND

    frame_range = modo.Scene().currentRange
    frame_range = range(frame_range[0], frame_range[1]+1)

    fps = modo.Scene().fps
    regex = re.compile('({0}_)(.*)(_cnstnt)'.format(func_name))

    print("#"*10)

    for item in scene.items(itype='constant', superType=True):
        match = regex.match(item.name)
        if match:
            if match.group(2) == "Teapot":
                layer = "{0}{1}".format(match.group(1), match.group(2))
                print layer

                # for frame in frame_range:
                #     print(item.channel('value').get(frame / fps))
                print item.channel('value').isAnimated
                print item.channel('value').envelope.keyframes.numKeys
                for key in range(0, item.channel('value').envelope.keyframes.numKeys):
                    print key
                    keyframe = item.channel('value').envelope.keyframes.first()
                    print keyframe
                    print item.channel('value').envelope.keyframes.time
                    # print item.channel('value').envelope.keyframes.value

                blend_grp = item.parent.itemGraph('shadeLoc').forward()[0]
                # pprint(blend_grp.channels())



# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    # Argument parsing is available through the 
    # lx.arg and lx.args methods. lx.arg returns 
    # the raw argument string that was passed into 
    # the script. lx.args parses the argument string 
    # and returns an array of arguments for easier 
    # processing.

    argsAsString = lx.arg()
    argsAsTuple = lx.args()

    try:
        main()
    except:
        print(traceback.format_exc())
