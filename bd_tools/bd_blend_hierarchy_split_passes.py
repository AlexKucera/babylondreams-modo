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

import bd_helpers
from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------


def main():
    scene = modo.Scene()

    start = bd_helpers.timer()

    func_name = BLEND_COMMAND

    frame_range = modo.Scene().currentRange
    frame_range = range(frame_range[0], frame_range[1]+1)

    fps = modo.Scene().fps
    regex = re.compile('({0}_)(.*)(_cnstnt)'.format(func_name))

    print("#"*10)

    for item in scene.items(itype='constant', superType=True):
        match = regex.match(item.name)
        if match:
            layer = "{0}{1}".format(match.group(1), match.group(2))
            print layer

            keyframes = item.channel('value').envelope.keyframes
            keyframe = []
            for key in range(0, keyframes.numKeys):
                keyframes.setIndex(key)
                keyframe.append({'frame': int(round(keyframes.time*fps)), 'value': keyframes.value})

            blend_range = "{}-".format(keyframe[0]['frame'])
            i = 0
            for key in keyframe:

                if not i == 0:
                    previous_value = keyframe[i - 1]['value']
                else:
                    previous_value = keyframe[0]['value']

                # if i + 1 < len(keyframe):
                #     next_value = keyframe[i + 1]['value']
                # else:
                #     next_value = keyframe[-1]['value']

                if previous_value != key['value']:

                    if key['value'] == 0:
                        blend_range = ("{}{}, ".format(blend_range, key['frame']))
                    elif key['value'] == 1:
                        blend_range = ("{}{}-".format(blend_range, keyframe[i - 1]['frame']))
                    else:
                        print "Not a valid key."

                i += 1

            print blend_range

            blend_grp = item.parent.itemGraph('shadeLoc').forward()[0]
            # print blend_grp.name
            # pprint(blend_grp.channels())
    bd_helpers.timer(start, 'Splitting {} Hierarchy'.format(str.capitalize(func_name)))

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
