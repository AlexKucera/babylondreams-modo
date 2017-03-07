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
import re
import traceback

import lx
import modo

from bd_tools import bd_helpers

# FUNCTIONS -----------------------------------------------


def capture_path():
    scene = modo.Scene()
    scene_path = scene.filename
    output = os.path.expanduser('~')
    file = 'preview'
    if scene_path is not None:
        file = os.path.splitext(os.path.basename(scene_path))[0]
        dir = os.path.dirname(scene_path)

        for path, directory, files in bd_helpers.walk_up(dir):

            if 'img' in directory:

                output_path = '{0}{1}img{1}cg{1}previews{1}'.format(path, os.sep)

                if not os.path.exists(output_path):
                    os.makedirs(output_path)

                output = output_path  # '{0}{1}_preview.jpg'.format(output_path, file)

    return {'output_path': output, 'filename': file}
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------


def main(gl_recording_size=1.0, gl_recording_type='image', viewport_camera='rendercam', shading_style='advgl',
         filename='preview', filepath="", first_frame=1001, last_frame=1250, raygl='off', replicators=False,
         bg_style='environment', use_scene_range=True, automatic_naming=True, overwrite=True):
    scene = modo.Scene()

    # Initialize main variables

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

    if automatic_naming:
        filename = capture_path()['filename']
        filepath = capture_path()['output_path']

    if gl_recording_type == 'movie':
        filepath = '{}{}_{}.mov'.format(filepath, filename, capture_camera_name)
    else:
        filepath = '{0}{1}{3}{1}_{2}.jpg'.format(filepath, filename, capture_camera_name, os.sep)

    print(filepath)
    if not overwrite:
        exists = True
        version = 1
        while exists:

            if os.path.exists(filepath):
                path = os.path.split(filepath)
                name = os.path.splitext(path[1])

                regex = re.compile('(.*)(_v)([0-9]{2,}$)')
                match = re.match(regex, name[0])

                if match is None:
                    version = '01'
                    new_name = name[0]
                else:
                    new_name = match.group(1)
                    version = str(int(version) + 1).zfill(2)

                if gl_recording_type == 'image':
                    new_path = "{0}_v{1}".format(path[0], version)
                else:
                    new_path = path[0]

                filepath = "{0}{1}{2}_v{3}{4}".format(new_path, os.sep, new_name, version, name[1])
            else:
                exists = False

    print(filepath)

    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    if use_scene_range:
        first_frame = scene.renderItem.channel('first').get()
        last_frame = scene.renderItem.channel('last').get()
    else:
        first_frame = first_frame
        last_frame = last_frame

    if replicators:
        replicator_visibility = 'always'
    else:
        replicator_visibility = 'none'

    selection = scene.selected
    scene.deselect()  # Clears the selection so we don't get any unwanted highlighting in the recording

    # Get Render Resolution
    resX = scene.renderItem.channel('resX').get()
    resY = scene.renderItem.channel('resY').get()

    newResX = int(resX * percent)
    newResY = int(resY * percent)

    lx.eval('layout.create %s width:%s height:%s style:palette' % (capture_camera_name, newResX, newResY))
    lx.eval('viewport.restore base.3DSceneView false 3Dmodel')
    lx.eval('view3d.bgEnvironment background {0}'.format(bg_style))
    lx.eval('view3d.bgEnvironment reflection linked')
    lx.eval('view3d.showGrid false')
    lx.eval('view3d.projection cam')
    lx.eval('view3d.controls false')
    lx.eval('view3d.showLights true')
    lx.eval('view3d.showCameras false')
    lx.eval('view3d.showMeshes true')
    lx.eval('view3d.showInstances true')

    if replicators:
        lx.eval('view3d.showLocators True')
    else:
        lx.eval('view3d.showLocators false')

    lx.eval('view3d.showTextureLocators false')
    lx.eval('view3d.showPivots none')
    lx.eval('view3d.showCenters none')
    lx.eval('view3d.showBackdrop false')
    lx.eval('view3d.showSelections false')
    lx.eval('view3d.fillSelected false')
    lx.eval('view3d.outlineSelected false')
    lx.eval('view3d.silhouette false')
    lx.eval('view3d.onionSkin false')
    lx.eval('view3d.enableDeformers true')
    lx.eval('view3d.useShaderTree true')
    lx.eval('view3d.meshSmoothing true')
    lx.eval('view3d.drawDisp true')
    lx.eval('view3d.drawFur true')
    lx.eval('view3d.showSelectionRollover false')
    lx.eval('view3d.shadingStyle ' + shading_style + ' active')
    lx.eval('view3d.wireframeOverlay none active')
    lx.eval('view3d.showWireframeItemMode false')
    lx.eval('view3d.showWorkPlane no')
    lx.eval('view3d.rayGL {0}'.format(raygl))
    lx.eval('pref.value preview.rglQuality draft')
    lx.eval('view3d.replicators {0}'.format(replicator_visibility))

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

    print('gl.capture {0} filename:"{1}" frameS:{2} frameE:{3} autoplay:true'.format(gl_type, filepath,
                                                                                     first_frame, last_frame))
    lx.eval('gl.capture {0} filename:"{1}" frameS:{2} frameE:{3} autoplay:true'.format(gl_type, filepath,
                                                                                       first_frame, last_frame))
    #lx.eval('gl.capture {0} filename:"{1}" frameS:{2} frameE:{3} autoplay:true'.format(gl_type, filepath,
    #                                                                                   first_frame, last_frame))

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
