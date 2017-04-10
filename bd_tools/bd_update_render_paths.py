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
        lx.out(project)

        project_config = bd_globals.projectconfig(scene_path)


        output = '{project_dir}/{img}/{renders}/{shot}/{file}'.format(
            project_dir=project['project_dir'],
            img=project_config['images/parent folder'],
            renders=project_config['images/3d'],
            file=os.path.splitext(file)[0],
            shot=shot['shotname']
        )

        lx.out("The renders will be located at: {}".format(output))

        if not os.path.exists(output):
            os.makedirs(output)

        for item in scene.iterItemsFast('renderOutput'):
            if " " in item.name:
                enabled = item.channel('enable').get()

                if enabled:
                    modo.dialogs.alert('Warning',
                                       "Please use no spaces in renderOutput naming (The offending "
                                       "output is " + item.name + "). It just screws everything up sooner or later.",
                                       dtype='warning')
            else:

                outputtype = item.channel('effect').get()
                filepath = item.channel('filename').get()
                enabled = item.channel('enable').get()

                if filepath is not None and enabled:

                    fileformat = enabled = item.channel('format').get()

                    if fileformat is None or "$FLEX":
                        if outputtype == "shade.normal" or outputtype == "geo.world" or outputtype == "geo.uv" or outputtype == "depth" or outputtype == "motion":
                            fileformat = "openexr_32"
                        else:
                            fileformat = "openexr"

                    if item.name == "rgba":
                        renderpasspath = output
                    else:
                        renderpasspath = "{}_{}/".format(output, item.name)

                    renderoutputpath = renderpasspath + os.path.splitext(file)[0] + "_"
                    lx.out("RenderOutput " + item.name + " will be located at: " +
                           renderpasspath)
                    if not os.path.exists(renderpasspath):
                        os.makedirs(renderpasspath)
                    lx.out("Setting Render Output path to: " + renderoutputpath)
                    item.channel('filename').set(renderoutputpath)
                    lx.out("Setting Render Output format to: " + fileformat)
                    item.channel('format').set(fileformat)

                else:

                    lx.out('Skipping {} as it is either disabled or has no "PATH" filled in'.format(item.name))


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
