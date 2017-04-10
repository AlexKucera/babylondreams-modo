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

def contractor(range):
    """
    Yields the current SequentialRange contents as a list of tuples.
    Each tuple represents (first, last, increment) of a continuous frame
    range.  The purpose of contractor is to provide a quick means of
    seeing all the continuous and discontinuous ranges in the
    SequentialRange object via a Generator object.

    :yields: each (first, last, incr) tuple.
    :ytype: tuple
    """
    frames = sorted(list(range))
    total = len(frames)
    curr_idx = 0
    while curr_idx < total:
        first, last, incr = frames[curr_idx], frames[curr_idx], 1
        if curr_idx + 2 < total:
            last_idx = curr_idx + 2
            curr_incr = frames[curr_idx + 1] - frames[curr_idx]
            while last_idx < total:
                if curr_incr == frames[last_idx] - frames[last_idx - 1]:
                    last = frames[last_idx]
                    incr = curr_incr
                    curr_idx = last_idx
                else:
                    break
                last_idx += 1
        yield (first, last)
        curr_idx += 1


def write_result(line, mode='a+'):
    scene = modo.Scene()
    path = os.path.splitext(scene.filename)[0] + "_split_passes.txt"
    with open(path, mode=mode) as output:
        output.write(line)
        output.close()


def log(line, mode='a+'):

    print(line)
    write_result(line + "\n", mode)


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------


def main():

    # Initial Setup
    scene = modo.Scene()

    start = bd_helpers.timer()

    func_name = BLEND_COMMAND

    frame_range = modo.Scene().currentRange

    fps = modo.Scene().fps

    regex = re.compile('({0}_)(.*)(_cnstnt)'.format(func_name))
    regex_mask = re.compile('({0}_)(.*)(_msk)'.format(func_name))

    # Find all Group Masks in the scene and turn them off
    for item in scene.iterItemsFast(itype='mask'):
        match = regex_mask.match(item.name)
        if match:
            item.channel('enable').set(0)

    try:
        fade_passes = modo.item.RenderPassGroup('fade_passes')
    except:
        fade_passes = scene.addRenderPassGroup('fade_passes')

    log("#"*10, mode='w')

    # Find all Constant texture layers in the scene
    for item in scene.iterItemsFast(itype='constant'):
        match = regex.match(item.name)
        if match:  # .group(2) == "Teapot":
            layer = "{0}{1}".format(match.group(1), match.group(2))
            log(layer)

            # Get all keyframes and their values for this item
            keyframes = item.channel('value').envelope.keyframes
            keyframe = []
            for key in range(0, keyframes.numKeys):
                keyframes.setIndex(key)
                keyframe.append({'frame': int(round(keyframes.time*fps)), 'value': keyframes.value})

            blending = []
            visible = []
            invisible = []

            i = 0
            for key in keyframe:

                # If we are not on the first keyframe get the keyframe before it to compare it to
                # otherwise just use the first keyframe
                if i == 0:
                    previous_value = keyframe[0]['value']
                else:
                    previous_value = keyframe[i - 1]['value']

                if i == 0:
                    if key['value'] == 1.0:
                        invisible.append((frame_range[0], key['frame']))
                    else:
                        visible.append((frame_range[0], key['frame']))
                if i == len(keyframes)-1:
                    if key['value'] == 1.0:
                        invisible.append((key['frame'], frame_range[1]))
                    else:
                        visible.append((key['frame'], frame_range[1]))


                # If the keyframe and the previous keyframe differ we have a blend.
                # Now we need to figure out if we are blending in or out
                if previous_value != key['value']:

                    blending.append((keyframe[i - 1]['frame'], key['frame']))

                    # # If the keyframe is 0 we end a blend range
                    # if key['value'] == 0.0:
                    #     print ("Blending In During {}".format(blending[-1:]))
                    #     visible_range.append(keyframe[i - 1]['frame'])
                    #
                    # # A value of 1 means we are starting a blend range
                    # elif key['value'] == 1.0:
                    #     print ("Blending Out During {}".format(blending[-1:]))
                    #     visible_range.append(key['frame'])
                    #
                    # # Anything else and this function does not work. We need keys to be either 0 or 1.
                    # # Kick the animator if he did anything else!
                    # else:
                    #     print "Not a valid key."

                elif previous_value == key['value'] and key['value'] == 0.0:

                    visible.append((keyframe[i - 1]['frame'], key['frame']))

                elif previous_value == key['value'] and key['value'] == 1.0:

                    if i == 0:
                        invisible.append((keyframe[0]['frame'], key['frame']))
                    else:
                        invisible.append((keyframe[i - 1]['frame'], key['frame']))

                i += 1

            visible_range = []
            condensed_visible_range =  []
            for blend in blending:
                visible_range += (range(blend[0], blend[1]+1, 1))
            for vis in visible:
                visible_range += (range(vis[0], vis[1]+1, 1))
            for x in contractor(sorted(set(visible_range))):
                condensed_visible_range.append(x)

            invisible_range = []
            condensed_invisible_range = []
            for blend in blending:
                invisible_range += (range(blend[0], blend[1] + 1, 1))
            for invis in invisible:
                invisible_range += (range(invis[0], invis[1]+1, 1))
            for x in contractor(sorted(set(invisible_range))):
                condensed_invisible_range.append(x)

            # condensed_visible_range = []
            # shot_range = range(frame_range[0], frame_range[1] + 1)
            # visible_range = sorted(set(shot_range) - set(invisible_range))
            # for x in contractor(sorted(visible_range)):
            #     condensed_visible_range.append(x)

            log("Blending Ranges: {}".format(blending))
            log("Invisible Range {}".format(condensed_invisible_range))
            log("Complete Visible Range: {}".format(condensed_visible_range))

            blend_grp = item.parent.itemGraph('shadeLoc').forward()[0]

            try:
                on_pass = scene.item('{}_on'.format(blend_grp.name))
            except:
                on_pass = fade_passes.addPass('{}_on'.format(blend_grp.name))
            on_pass.active = True

            fade_passes.addChannel(blend_grp.channel('render'))
            blend_grp.channel('render').set('on')
            lx.eval('edit.apply')

            try:
                off_pass = scene.item('{}_off'.format(blend_grp.name))
            except:
                off_pass = fade_passes.addPass('{}_off'.format(blend_grp.name))
            off_pass.active = True

            fade_passes.addChannel(blend_grp.channel('render'))
            blend_grp.channel('render').set('off')
            lx.eval('edit.apply')

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
