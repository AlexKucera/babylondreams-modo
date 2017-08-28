#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_bake_camera

Release Notes:

V0.1 Initial Release - 2017-08-28

"""
import subprocess

import bd_helpers
import modo
import lx
import traceback

from var import *


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    start_timer = bd_helpers.timer()

    scene = modo.Scene()

    item = scene.selected

    if len(item) > 1:
        message = "Please select only one item."
        modo.dialogs.alert(message, message, dtype='error')

    elif len(item) == 0:

        message = "Please select at least one camera."
        modo.dialogs.alert(message, message, dtype='error')

    elif item[0].type != "camera":

        message = "Please select a camera."
        modo.dialogs.alert(message, message, dtype='error')

    else:

        cam = item[0]
        bake_cam_name = os.path.splitext(scene.name)[0] + "_bakeCam"
        bake_cam = scene.addCamera(name=bake_cam_name)

        # Parent to animated camera
        scene.select(bake_cam)
        scene.select(cam, add=True)
        lx.eval("constraintTransform type:pos")

        scene.select(bake_cam)
        scene.select(cam, add=True)
        lx.eval("constraintTransform type:rot")

        # Link relevant channels
        cam.channel("focalLen") >> bake_cam.channel("focalLen")
        cam.channel("apertureX") >> bake_cam.channel("apertureX")
        cam.channel("apertureY") >> bake_cam.channel("apertureY")
        cam.channel("offsetX") >> bake_cam.channel("offsetX")
        cam.channel("offsetY") >> bake_cam.channel("offsetY")
        cam.channel("focusDist") >> bake_cam.channel("focusDist")
        cam.channel("fStop") >> bake_cam.channel("fStop")

        # Bake Animation
        scene.select(bake_cam)
        lx.eval("?item.bake 0")

        # Bake non-transform channels
        lx.eval("select.drop channel")
        lx.eval("select.channel {{{0}:focalLen}} add".format(bake_cam.id))
        lx.eval("select.channel {{{0}:apertureX}} add".format(bake_cam.id))
        lx.eval("select.channel {{{0}:apertureY}} add".format(bake_cam.id))
        lx.eval("select.channel {{{0}:offsetX}} add".format(bake_cam.id))
        lx.eval("select.channel {{{0}:offsetY}} add".format(bake_cam.id))
        lx.eval("select.channel {{{0}:focusDist}} add".format(bake_cam.id))
        lx.eval("select.channel {{{0}:fStop}} add".format(bake_cam.id))
        lx.eval("?channel.bake 0")

        scene.select(bake_cam)
        lx.eval("item.selectChannels anim")

        # FBX Export
        export_value = lx.eval("user.value sceneio.fbx.save.exportType ?")
        lx.eval("user.value sceneio.fbx.save.exportType FBXExportSelection")

        if scene.filename:
            filename = scene.filename
        else:
            filename = os.path.join(os.path.expanduser('~'), "untitled.lxo")
        newpath = os.path.splitext(filename)[0] + "_camera_bake.fbx"
        print "Exporting to {0}".format(newpath)
        lx.eval("scene.saveAs {0} fbx true".format(newpath))

        # Cleanup
        scene.removeItems(bake_cam)
        lx.eval("user.value sceneio.fbx.save.exportType {0}".format(export_value))
        modo.dialogs.alert(title="Export Finished", message="The camera has been exported to {0}".format(newpath))
        subprocess.Popen(['open', os.path.dirname(newpath)])

    bd_helpers.timer(start_timer, ' Overall')


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
