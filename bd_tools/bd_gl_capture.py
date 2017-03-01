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

import traceback
import sys
import lx
import modo


# FUNCTIONS -----------------------------------------------


def restoreSelection(listSelections):
    """
    Saves a selection for later use.

    Example:

        global save_selection
        save_selection = lx.evalN("query sceneservice selection ? all")

    To restore a selection later:

        bd_utils.restoreSelection(save_selection)



    """

    try:
        # lx.out(listSelections)
        first = True
        for x in listSelections:
            lx.out("Restoring Selection: " + x)
            if first:
                lx.eval("select.item {%s} set" % x)
            else:
                lx.eval("select.item {%s} add" % x)
            first = False

    except:
        lx.eval('layout.createOrClose EventLog "Event Log_layout" '
                'title:@macros.layouts@EventLog@ width:600 height:600 persistent:true '
                'open:true')
        lx.out("ERROR restoreSelection failed with ", sys.exc_info())
        return None


def get_ids(itemtype):
    """
    Get a list of item IDs of type 'type'
    Returns a list of item IDs or None if there are no items of the specified
    type or if there's an error. Error printed is to Event log.
    type - the type of item to be returned (mesh, camera etc)
    """
    try:
        itemlist = []
        numitems = lx.eval('!!query sceneservice ' + itemtype + '.N ?')
        if numitems == 0:
            return None
        else:
            for x in xrange(numitems):
                itemlist.append(
                    lx.eval('query sceneservice ' + itemtype + '.ID ? %s' % x))
            lx.out("Found " + str(numitems) + " " + itemtype + "s: " + ", ".join(
                itemlist))
            return itemlist
    except:
        lx.eval('layout.createOrClose EventLog "Event Log_layout" '
                'title:@macros.layouts@EventLog@ width:600 height:600 persistent:true '
                'open:true')
        lx.out("ERROR get_ids(" + itemtype + ") failed with ", sys.exc_info())
        return None


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------


def main():
    lx.eval("user.defNew gl_viewport_size integer momentary")
    lx.eval('user.def gl_viewport_size username "Open New GL View"')
    lx.eval('user.def gl_viewport_size dialogname "Which resolution do you need to open?"')
    lx.eval("user.def gl_viewport_size list Full;Half;Quarter;Tenth")
    lx.eval('user.def gl_viewport_size listnames "100%;50%;25%;10%"')
    lx.eval("user.value gl_viewport_size")

    mode = lx.eval("user.value gl_viewport_size ?")

    if mode == "Full":
        percent = 1.0
    elif mode == "Half":
        percent = 0.5
    elif mode == "Quarter":
        percent = 0.25
    elif mode == "Tenth":
        percent = 0.1
    else:
        percent = 1

    lx.eval("user.defNew gl_type integer momentary")
    lx.eval('user.def gl_type username "GL Recording Type"')
    lx.eval('user.def gl_type dialogname "Do you want to capture a movie or an image sequence?"')
    lx.eval("user.def gl_type list movie;image")
    lx.eval('user.def gl_type listnames "Movie;Image Sequence"')
    lx.eval("user.value gl_type")

    gl_type = lx.eval("user.value gl_type ?")

    all_cameras = get_ids("camera")
    render_camera = lx.eval("render.camera ?")

    list='rendercam' + ";"
    listnames="Render Camera;"


    for x in all_cameras:

        list += x + ";"
        listnames += lx.eval('query sceneservice item.name ? %s' % x) + ";"

    lx.out(list)
    lx.out(listnames)


    lx.eval("user.defNew viewport_cam integer momentary")
    lx.eval('user.def viewport_cam username "Pick Viewport Camera"')
    lx.eval('user.def viewport_cam dialogname "Which camera do you want to capture?"')
    lx.eval("user.def viewport_cam list " + list)
    lx.eval('user.def viewport_cam listnames "' + listnames + '"')
    lx.eval("user.value viewport_cam")

    capture_camera = lx.eval("user.value viewport_cam ?")
    if capture_camera == 'rendercam':
        capture_camera_name = "RenderCam"
    else:
        capture_camera_name = lx.eval('query sceneservice item.name ? %s' % capture_camera)
    lx.out(capture_camera)
    lx.out(capture_camera_name)

    lx.eval("user.defNew shading_style integer momentary")
    lx.eval('user.def shading_style username "Pick Viewport Shading"')
    lx.eval('user.def shading_style dialogname "Which Shading Style do you want?"')
    lx.eval("user.def shading_style list gnzgl;advgl;texmod;tex;shade;vmap;sket;wire;shd1;shd2;shd3")
    lx.eval('user.def shading_style listnames "Advanced;Default;Texture Shaded;Texture;Shaded;Vertex Map;Solid;Wireframe;Gooch Toon Shading;Cel Shading;Reflection"')
    lx.eval("user.value shading_style")

    shading_style = lx.eval("user.value shading_style ?")

    # Get selection
    save_selection = lx.evalN("query sceneservice selection ? all")

    # Get Render Resolution
    lx.eval("select.item Render")
    resX = float(lx.eval("item.channel resX ?"))
    resY = float(lx.eval("item.channel resY ?"))

    newResX = int(resX * percent)
    newResY = int(resY * percent)

    # Restore selection
    restoreSelection(save_selection)

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
        lx.eval('view3d.cameraItem ' + capture_camera)

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

    if gl_type == "movie":
        lx.eval("gl.capture")
    if gl_type == "image":
        lx.eval("gl.capture seq:true")

    """
    TODO: !gl.capture seq:true filename:/Users/alex/Documents/Untitled.jpg frameS:1001 frameE:1250 autoPlay:false
    """

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
