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

    # We add two keys to initialize the envelope in case it does not exist. This will add new keys to potentially
    # already existing keys creating a broken animation
    key = min(keys["keys"])
    print key
    channel.set(keys["keys"][key]["value"], keys["keys"][key]["time"], key=True)
    key = iter(keys["keys"]).next()
    print key
    channel.set(keys["keys"][key]["value"], keys["keys"][key]["time"], key=True)

    # Here we delete all keys from the channel to ensure we start from a clean slate.
    channel.envelope.clear()

    # Now we create the actual keys for the whole frame range
    for key in keys["keys"]:
        channel.set(keys["keys"][key]["value"], keys["keys"][key]["time"], key=True)

    keyframes = channel.envelope.keyframes

    # Here we set each keys slope and type
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
        anim_data = bd_helpers.load_json()

        if anim_data is None:

            modo.dialogs.alert("No Tags!",
                               "The provided file contains no useable information",
                               dtype='info')

        else:

            targetGroup = selected[0]

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
                    target = tagsTarget[tag]
                    # First we paste the item's channels
                    if "channels" in anim_data["items"][tag]:
                        for channel in target.channels():
                            if channel.name in anim_data["items"][tag]["channels"]:
                                set_keys(channel, anim_data["items"][tag]["channels"][channel.name],
                                         anim_data["items"][tag]["channels"][channel.name]["type"])

                    # Now we find any Transform items associated with the source item and copy those
                    if "transforms" in anim_data["items"][tag]:
                        for transform in anim_data["items"][tag]["transforms"]:
                            source_transform_type = anim_data["items"][tag]["transforms"][transform]["type"]
                            exists = False
                            # check if the transform type already exists
                            for target_transform in modo.item.LocatorSuperType(item=target).transforms:
                                if target_transform.type == source_transform_type or target_transform.type == "translation" and source_transform_type == "position":
                                    exists = True
                                    target_transform_id = target_transform

                            # if it does not create it
                            if not exists:
                                target_transform_id = target.transforms.insert(source_transform_type)

                            for channel in target_transform_id.channels():
                                if channel.name in anim_data["items"][tag]["transforms"][transform]:
                                    if channel.name == "type" or channel.name == "name":
                                        pass
                                    else:
                                        set_keys(channel,
                                                 anim_data["items"][tag]["transforms"][transform][channel.name],
                                                 anim_data["items"][tag]["transforms"][transform][channel.name]["type"])

                else:
                    missingTags.append("{} ({})".format(tag, anim_data["items"][tag]["name"]))
                    print("{} has not corresponding tag in the target.".format(anim_data["items"][tag]["name"]))

            bd_helpers.timer(start, "Finished Animation Transfer")

            if missingTags:
                message = ""
                for missing in missingTags:
                    message = "{}\n{}".format(message, missing)
                message = "The provided file contains tags that are missing in the target hierarchy.\n" \
                          "The following tags cannot be found:\n{}".format(message)
                modo.dialogs.alert("Missing Tags!",
                                   message,
                                   dtype='info')
                print(message)


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
