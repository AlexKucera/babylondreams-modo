#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Allows opening an OpenGL window of defined dimensions for size accurate OpenGL Previews.

Inspired by a function in Adam O'Hern's excellent RenderMonkey 2 kit.
http://www.mechanicalcolor.com/modo-kits/render-monkey

Release Notes:

V0.1 Initial Release - 2016-11-23
v0.2 Trigger GL Recording and close the window after recording has finished - 2016-11-24

"""
import os
import traceback

import lx
import modo


# FUNCTIONS -----------------------------------------------
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------


def main(gl_recording_size=1.0, gl_recording_type='image', viewport_camera='rendercam', shading_style='advgl',
         filename='preview', filepath="", first_frame=1001, last_frame=1250):
    scene = modo.Scene()

    if gl_recording_size == '100%':
        percent = 1.0
    if gl_recording_size == '50%':
        percent = 0.5
    if gl_recording_size == '25%':
        percent = 0.25
    if gl_recording_size == '10%':
        percent = 0.1

    gl_type = gl_recording_type

    if viewport_camera == 'rendercam':
        capture_camera = viewport_camera
        capture_camera_name = scene.renderCamera.name
    else:
        capture_camera = scene.item(viewport_camera)
        capture_camera_name = capture_camera.name

    shading_style = shading_style

    if gl_recording_type == 'movie':
        filepath = '{}{}_{}.mov'.format(filepath, filename, capture_camera_name)
    else:
        filepath = '{0}{1}{3}{1}_{2}.jpg'.format(filepath, filename, capture_camera_name, os.sep)

    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    first_frame = first_frame
    last_frame = last_frame

    selection = scene.selected
    scene.deselect()  # Clears the selection so we don't get any unwanted highlighting in the recording

    # Get Render Resolution
    resX = scene.renderItem.channel('resX').get()
    resY = scene.renderItem.channel('resY').get()

    newResX = int(resX * percent)
    newResY = int(resY * percent)

    lx.eval('layout.create %s width:%s height:%s style:palette' % (capture_camera_name, newResX, newResY))
    lx.eval('viewport.restore base.3DSceneView false 3Dmodel')
    lx.eval('view3d.bgEnvironment background solid')
    lx.eval('view3d.showGrid false')
    lx.eval('view3d.projection cam')
    lx.eval('view3d.controls false')
    lx.eval('view3d.showLights false')
    lx.eval('view3d.showCameras false')
    lx.eval('view3d.showLocators false')
    lx.eval('view3d.showTextureLocators false')
    lx.eval('view3d.showBackdrop false')
    lx.eval('view3d.showSelections false')
    lx.eval('view3d.fillSelected false')
    lx.eval('view3d.outlineSelected false')
    lx.eval('view3d.showSelectionRollover false')
    lx.eval('view3d.shadingStyle ' + shading_style + ' active')
    lx.eval('view3d.wireframeOverlay none active')

    if capture_camera == 'rendercam':
        lx.eval('view3d.renderCamera')
    else:
        lx.eval('view3d.cameraItem ' + capture_camera_name)

    lx.eval('view3d.shadingStyle ' + shading_style)
    lx.eval('view3d.sameAsActive true')

    if shading_style == "gnzgl":
        lx.eval("view3d.showGnzFSAA x9")
        lx.eval("view3d.setGnzTransparency correct")
        lx.eval("view3d.setGnzSSReflections blurry")
        lx.eval("view3d.setGnzDitherMode ordered")
        lx.eval("view3d.showGnzSSAO true")
        lx.eval("view3d.GnzVisOverride all")
        lx.eval("view3d.showGnzShadows true")
        lx.eval("view3d.useGnzNormalMaps true")
        lx.eval("view3d.useGnzBumpMaps true")
        lx.eval("view3d.setGnzVisibility render")
        lx.eval("view3d.setGnzLighting sceneIBLLights")
        lx.eval("view3d.setGnzBackground environment")

    bbox = []
    for item in scene.iterItemsFast(itype='mesh'):
        if item.channel('drawShape').get() == 'custom':
            bbox.append(item)
            item.channel('drawShape').set('default')

    for item in scene.iterItemsFast(itype='meshInst'):
        if item.channel('drawShape').get() == 'custom':
            bbox.append(item)
            item.channel('drawShape').set('default')

    if gl_type == "movie":
        gl_type = ""
    elif gl_type == "image":
        gl_type = 'seq:true'

    lx.eval('gl.capture {0} filename:"{1}" frameS:{2} frameE:{3} autoplay:true'.format(gl_type, filepath,
                                                                                       first_frame, last_frame))

    for item in bbox:
        item.channel('drawShape').set('custom')

    scene.select(selection)

    lx.eval("layout.closeWindow")


# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    try:
        # Argument parsing is available through the 
        # lx.arg and lx.args methods. lx.arg returns 
        # the raw argument string that was passed into 
        # the script. lx.args parses the argument string 
        # and returns an array of arguments for easier 
        # processing.

        argsAsString = lx.arg()
        argsAsTuple = lx.args()

        main()

    except:
        lx.out(traceback.format_exc())
