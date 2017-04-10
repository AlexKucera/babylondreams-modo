#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_headless_batch_creator

Release Notes:

V0.1 Initial Release - 2017-04-10

"""
import re
import subprocess

import pyperclip

import bd_helpers
import modo
import lx
import traceback

import bd_update_render_paths
from var import *

from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader


# FUNCTIONS -----------------------------------------------
def build_modo_render_command(pathaliases=None, scenes={}):
    searchpath = [TEMPLATES]
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[CoreExtension()]
    )
    template = engine.get_template('modo_render_commands.txt')

    if pathaliases:
        for key in pathaliases:
            '{} "{}"'.format(key, os.path.normpath(pathaliases[key]))

    return template.render({'pathaliases': pathaliases, 'scenes': scenes})


def build_modo_batch(commands=[], headless=""):
    searchpath = [TEMPLATES]
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[CoreExtension()]
    )
    template = engine.get_template('modo_batch.bat')

    return template.render({'modo_cl': headless, 'commands': commands})


def build_modo_bash(commands=[], headless="", render_range={}):
    searchpath = [TEMPLATES]
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[CoreExtension()]
    )
    template = engine.get_template('modo_batch.sh')

    return template.render({'modo_cl': headless, 'commands': commands, 'render_range': render_range})


def renderRegionCheck():
    if modo.Scene().renderItem.channel('region').get():
        result = modo.dialogs.yesNo('Disable Render Region', "Disable Render Region for batch render?")
        if result == "yes":
            lx.out("Proceeding without Render Region.")
            region = "item.channel polyRender$region 0"
        else:
            region = ""
    else:
        lx.out("Proceeding with enabled Render Region.")
        region = ""

    return region

def get_scene_range():
    scene = modo.Scene()

    first_frame = int(scene.renderItem.channel('first').get())
    last_frame = int(scene.renderItem.channel('last').get())
    frame_step = int(scene.renderItem.channel('step').get())

    return "{}-{}x{}".format(first_frame, last_frame, frame_step)


def get_passes():
    scene = modo.Scene()
    passes = scene.renderPassGroups
    render_passes = []
    if len(passes) > 0:
        for pas in passes:
            render_passes.append((pas, pas.name))
    else:
        render_passes.append((None, "No passes in scene"))
    return render_passes

def get_output_pattern():
    scene = modo.Scene()
    if get_passes():
       pattern = "[<pass>]_[<output>][<LR>].<FFFF>"
    else:
       pattern = "[<pass>][<output>][<LR>].<FFFF>"
    return pattern


def get_input_range(frame_range="1001-1250x1"):
    regex = re.compile('(\d+)[-x ]+(\d+)[-x ]+(\d+)')
    match = re.match(regex, frame_range)
    if match:
        return match.group(1), match.group(2), match.group(3)
    else:
        return None


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(use_scene_range=True, frame_range="1001-1250x1", passname="", batchsize=10, pattern=""):
    start_timer = bd_helpers.timer()

    scene = modo.Scene()
    scene_path = scene.filename

    if sys.platform == "darwin":
        headless_path = lx.eval("query platformservice path.path ? exename") + "_cl"
    else:
        headless_path = lx.eval("query platformservice path.path ? exename") + "_cl.exe"

    if not scene_path:
        modo.dialogs.alert('Warning',
                           'Please save scene first!',
                           dtype='warning')
    else:

        # bd_render_paths.main()
        lx.eval('bd.update_render_paths')

        if use_scene_range:
            first_frame, last_frame, frame_step = get_input_range(get_scene_range())
        else:
            first_frame, last_frame, frame_step = get_input_range(frame_range)

        region = renderRegionCheck()

        batch_base_path = "{filepath}/_batch/{filename}".format(filepath=os.path.dirname(scene_path),
                                                                filename=os.path.splitext(os.path.basename(scene_path))[0]
                                                                )
        batch_path = os.path.normpath("{}.bat".format(batch_base_path))
        bash_path = os.path.normpath("{}.sh".format(batch_base_path))

        framelist = range(int(first_frame), int(last_frame) + 1, int(frame_step))
        framelist = chunker(framelist, batchsize)
        all_commands = []

        for framegroup in framelist:
            scene_dict = {}
            first_batch_frame = min(int(minframe) for minframe in framegroup)
            last_batch_frame = max(int(maxframe) for maxframe in framegroup)

            command_path = os.path.normpath("{filepath}/{filename}_batchrender_frames_{first}-{last}.txt".format(
                filepath=batch_base_path,
                filename=os.path.splitext(os.path.basename(scene_path))[0],
                first=first_batch_frame,
                last=last_batch_frame
            ))

            if not os.path.exists(os.path.dirname(command_path)):
                os.makedirs(os.path.dirname(command_path))

            scene_dict[first_batch_frame] = {
                'path': scene_path,
                'first': first_batch_frame,
                'last': last_batch_frame,
                'step': frame_step,
                'pattern': pattern,
                'passes': passname,
                'region': region
            }

            modo_command = build_modo_render_command(scenes=scene_dict,
                                                     pathaliases={
                                                         'WorkingProjects': '/Volumes/ProjectsRaid/WorkingProjects/'
                                                     })

            with open(command_path, mode='w+') as command:
                command.write(modo_command)
                command.close()

            all_commands.append(command_path)

        modo_batch = build_modo_batch(commands=all_commands, headless=headless_path)
        modo_bash = build_modo_bash(commands=all_commands, headless=headless_path, render_range={'first': first_frame, 'last': last_frame})

        with open(batch_path, mode='w+') as batch:
            batch.write(modo_batch)
            batch.close()

        with open(bash_path, mode='w+') as bash:
            bash.write(modo_bash)
            bash.close()
        os.chmod(bash_path, 0755)

        if sys.platform == "darwin":
            pyperclip.copy(bash_path)
            subprocess.Popen(['open', '-a', '/Applications/Utilities/Terminal.app', '-n'])

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
