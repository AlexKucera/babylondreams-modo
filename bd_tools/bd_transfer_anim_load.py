#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
BabylonDreams-modo-Kit - bd_transfer_anim

Release Notes:
    Copy the animation from one selected item to another. It will copy all animated channels from the
    first object to the second object. Any channels that are missing on the second object will be listed
    at the end for manual fixing. Please make sure you have Warning dialogs enabled in modo, otherwise the user
    won't get a popup dialog.

V0.1 Initial Release - 2017-02-13

"""

import modo
import lx
import traceback
from pprint import pprint

from bd_tools import bd_helpers

# These channels show up as animated even if there are no keys on them. Not a reliable source to determin animation.
forbidden_channels = ["localMatrix", "wposMatrix", "wrotMatrix", "wsclMatrix", "wpivPosMatrix", "wpivRotMatrix",
                      "worldMatrix", "glstate", "crvGroup", "matrix", "wParentMatrix", "glsurf", "mesh"]

scene = None
fps = None


# FUNCTIONS -----------------------------------------------


def set_keys(channel=None, keys=None, type=None):
    for key in keys["keys"]:
        channel.set(keys["keys"][key]["value"], keys["keys"][key]["time"], key=True)

    keyframes = channel.envelope.keyframes

    if type == "boolean" or type == "integer":
        pass
    else:
        for key in keys["keys"]:
            keyframes.setIndex(int(key))

            # Set in
            keyframes.SetSlopeType(keys["keys"][key]["in"]["slope_type"][0], 1)
            keyframes.SetSlope(keys["keys"][key]["in"]["slope"], 1)
            keyframes.SetWeight(keys["keys"][key]["in"]["slope_weight"], 0, 1)

            # Set out
            keyframes.SetSlopeType(keys["keys"][key]["out"]["slope_type"][0], 2)
            keyframes.SetSlope(keys["keys"][key]["out"]["slope"], 2)
            keyframes.SetWeight(keys["keys"][key]["out"]["slope_weight"], 0, 2)


# END FUNCTIONS -----------------------------------------------


# MAIN PROGRAM --------------------------------------------
def main():
    global scene
    global fps

    scene = modo.Scene()
    fps = scene.fps

    selected = bd_helpers.selected(1)

    if selected is not None:

        start = bd_helpers.timer()

        print("\n\nStarting Animation transfer…")

        reload(bd_helpers)
        anim_data = bd_helpers.load_json("anim_export_cache/anim_export_")

        if anim_data is None:

            modo.dialogs.alert("No Tags!",
                               "The provided file contains no useable information",
                               dtype='info')

        else:

            targetGroup = selected[0]

            # get all target tags
            # loop through the JSON data by tag
                # select targets by tag
                    # loop through JSON channels
                        # apply animation to target channels
                    # loop through JSON transforms
                        # apply/create animation on target transforms

            tagsTarget = dict()

            tag = bd_helpers.get_tags(targetGroup)

            if tag is not None:
                tagsTarget[tag] = targetGroup

            for child in targetGroup.children(recursive=True):
                tag = bd_helpers.get_tags(child)

                if tag is not None:
                    tagsTarget[tag] = child

            missingTags = []
            for tag in anim_data["items"]:

                if tag in tagsTarget:
                    print("Transferring animation from {} to {}".format(anim_data["items"][tag]["name"],
                                                                        tagsTarget[tag].name))
                else:
                    missingTags.append("{} ({})".format(tag, anim_data["items"][tag]["name"]))
                    print("{} has not corresponding tag in the target.".format(anim_data["items"][tag]["name"]))

            #     items_anim = dict()
            #     items_anim = {
            #         "01 __description__": "This is an automated export of an animated hierarchy or rig.",
            #         "02 __URL__": "https://github.com/AlexKucera/babylondreams-modo"
            #     }
            #
            #     for tag in tagsTarget:
            #
            #         items_anim[tag] = {"name": tagsTarget[tag].name}
            #
            #         animated_channels, item_channels = get_channels(source=tagsTarget[tag])
            #         print animated_channels
            #         if animated_channels:
            #             items_anim[tag]["channels"] = item_channels
            #
            #         animated_transforms, item_transforms = get_transforms(source=tagsTarget[tag])
            #         print animated_transforms
            #         if animated_transforms:
            #             items_anim[tag]["transforms"] = item_transforms
            #
            #         if animated_channels or animated_transforms:
            #             print("Getting animation from {0} ({1})".format(tagsTarget[tag].name, tagsTarget[tag].id))
            #
            #     if len(items_anim) > 0:
            #         reload(bd_helpers)
            #         bd_helpers.save_json(items_anim, "anim_export_cache/anim_export_")

            if missingTags:
                message = ""
                for missing in missingTags:
                    message = "{}\n{}".format(message, missing)
                modo.dialogs.alert("Missing Tags!",
                                   "The provided file contains tags that are missing in the target hierarchy.\n"
                                   "The following tags cannot be found:\n{}".format(message),
                                   dtype='info')


        bd_helpers.timer(start, "Finished Animation Transfer")


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
        print traceback.format_exc()
