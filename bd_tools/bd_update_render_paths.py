#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_update_render_paths.py

Release Notes:

V0.1 Initial Release - 2017-04-10

"""
import imp

import bd_helpers
import modo
import lx
import traceback

from var import *

try:
    imp.find_module('bd_globals')
except ImportError:
    sys.path.append(BD_PIPELINE)
import bd_globals

# FUNCTIONS -----------------------------------------------
# # END FUNCTIONS -----------------------------------------------


# MAIN PROGRAM --------------------------------------------
def main():
    start_timer = bd_helpers.timer()

    scene = modo.Scene()

    scene_path = scene.filename
    if not scene_path:
        modo.dialogs.alert('Warning',
                           'Please save scene first!',
                           dtype='warning')
    else:
        file = os.path.basename(scene_path)
        shot = bd_globals.find_shot_version(scene_path)
        lx.out('File {} is at Version {}.'.format(shot['shotname'], shot['version']))
        project = bd_globals.find_project(scene_path)

        project_config = bd_globals.projectconfig(scene_path)

        output = os.path.join(
            project['project_dir'],
            project_config['images/parent folder'],
            project_config['images/3d'],
            shot['sequence'],
            shot['shotname'],
            os.path.splitext(file)[0]
        )

        lx.out("The renders will be located at: {}".format(output))

        if not os.path.exists(output):
            os.makedirs(output)

        for item in scene.iterItemsFast(lx.symbol.sITYPE_RENDEROUTPUT):

            outputtype = item.channel(lx.symbol.sICHAN_TEXTURELAYER_EFFECT).get()
            filepath = item.channel(lx.symbol.sICHAN_RENDEROUTPUT_FILENAME).get()
            enabled = item.channel(lx.symbol.sICHAN_TEXTURELAYER_ENABLE).get()
            if enabled:
                if filepath:

                    fileformat = enabled = item.channel(lx.symbol.sICHAN_RENDEROUTPUT_FORMAT).get()

                    if fileformat is None or "$FLEX":
                        if outputtype == lx.symbol.s_FX_OUTPUT_SHADING_NORMAL \
                                or outputtype == lx.symbol.s_FX_OUTPUT_WORLD_COORDINATES \
                                or outputtype == lx.symbol.s_FX_OUTPUT_UV_COORDINATES\
                                or outputtype == lx.symbol.s_FX_OUTPUT_DEPTH\
                                or outputtype == lx.symbol.s_FX_OUTPUT_MOTION:

                            fileformat = "openexr_32"

                        else:
                            fileformat = "openexr"

                    if item.name == "rgba":
                        renderpasspath = os.path.join(output, "")
                    else:
                        renderpasspath = os.path.join(output, item.name.replace(" ", "_"), "")

                    renderoutputpath = os.path.join(renderpasspath, os.path.splitext(file)[0] + "_")
                    lx.out("RenderOutput " + item.name + " will be located at: " +
                           renderpasspath)
                    if not os.path.exists(renderpasspath):
                        os.makedirs(renderpasspath)
                    lx.out("Setting Render Output path to: " + renderoutputpath)
                    item.channel(lx.symbol.sICHAN_RENDEROUTPUT_FILENAME).set(renderoutputpath)
                    lx.out("Setting Render Output format to: " + fileformat)
                    item.channel(lx.symbol.sICHAN_RENDEROUTPUT_FORMAT).set(fileformat)

            else:
                pass
                # lx.out('Skipping {} as it is either disabled or has no "PATH" filled in'.format(item.name))

    bd_helpers.timer(start_timer, 'Render Path Update')


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
