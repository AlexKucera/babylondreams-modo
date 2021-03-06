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
import traceback

import lx
import modo
import pyperclip
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

import bd_globals
import bd_helpers
from var import *


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


def build_modo_preview_render_command(pathaliases=None, scenes={}):
    searchpath = [TEMPLATES]
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[CoreExtension()]
    )
    template = engine.get_template('modo_preview_render_commands.txt')

    if pathaliases:
        for key in pathaliases:
            '{} "{}"'.format(key, os.path.normpath(pathaliases[key]))

    return template.render({'pathaliases': pathaliases, 'scenes': scenes})

def build_modo_render_command_win(pathaliases=None, scenes={}):
    searchpath = [TEMPLATES]
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[CoreExtension()]
    )
    template = engine.get_template('modo_render_commands_win.txt')

    if pathaliases:
        for key in pathaliases:
            '{} "{}"'.format(key, os.path.normpath(pathaliases[key]))

    for scene in scenes:
        scenes[scene]['path'] = format_filename(scenes[scene]['path'], 'win32')

    return template.render({'pathaliases': pathaliases, 'scenes': scenes})


def build_modo_preview_render_command_win(pathaliases=None, scenes={}):
    searchpath = [TEMPLATES]
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[CoreExtension()]
    )
    template = engine.get_template('modo_preview_render_commands_win.txt')

    if pathaliases:
        for key in pathaliases:
            '{} "{}"'.format(key, os.path.normpath(pathaliases[key]))

    for scene in scenes:
        scenes[scene]['path'] = format_filename(scenes[scene]['path'], 'win32')

    return template.render({'pathaliases': pathaliases, 'scenes': scenes})


def build_modo_batch(commands=[], headless=""):
    import ntpath
    searchpath = [TEMPLATES]
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[CoreExtension()]
    )
    template = engine.get_template('modo_batch.bat')
    win_commands = []
    for command in commands:
        win_commands.append(ntpath.normpath(format_filename(command, 'win32')))

    headless = ntpath.normpath(r"C:\Program Files\Luxology\modo\11.0v1\modo_cl.exe")

    return template.render({'modo_cl': ntpath.normpath(headless), 'commands': win_commands})


def build_modo_bash(commands=[], headless="", render_range={}):
    searchpath = [TEMPLATES]
    engine = Engine(
        loader=FileLoader(searchpath),
        extensions=[CoreExtension()]
    )
    template = engine.get_template('modo_batch.sh')

    return template.render({'modo_cl': headless, 'commands': commands, 'render_range': render_range})


def renderRegionCheck():
    if modo.Scene().renderItem.channel(lx.symbol.sICHAN_POLYRENDER_REGION).get():
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
    frame_range = modo.Scene().currentRange
    first_frame = frame_range[0]
    last_frame = frame_range[1]
    frame_step = int(modo.Scene().renderItem.channel(lx.symbol.sICHAN_POLYRENDER_STEP).get())

    return "{}-{}x{}".format(first_frame, last_frame, frame_step)


def get_passes():
    passes = modo.Scene().renderPassGroups
    render_passes = []
    if len(passes) > 0:
        for pas in passes:
            render_passes.append((pas.id, pas.name))
        render_passes.append((None, "No passes"))
    else:
        render_passes.append((None, "No passes in scene"))
    return render_passes


def get_output_pattern():
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


def format_filename(s, format):
    """
    Takes a UNIX path and turns it into a Windows path.
    
    """

    if sys.platform == "darwin":

        unix_path = bd_globals.bdconfig()['projects dir']
        win_path = os.path.normpath(
            os.path.join(
                bd_globals.bdconfig()['alt drive'],
                bd_globals.bdconfig()['projects location']
            )
        )

    elif sys.platform == "win32":

        win_path = bd_globals.bdconfig()['projects dir']
        unix_path = os.path.normpath(
            os.path.join(
                bd_globals.bdconfig()['alt drive'],
                bd_globals.bdconfig()['projects location']
            )
        )

    if format == "win32":
        filename = s.replace(unix_path, win_path)
        filename = filename.replace('/', '\\')
        return filename
    elif format == "darwin":
        filename = s.replace(win_path, unix_path)
        filename = filename.replace('\\', '/')
        return filename
    else:
        print ("ERROR no valid OS given for path transform")
        return None


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(proc='manual', use_scene_range=True, frame_range="1001-1250x1", passname="", batchsize=10, pattern="",
         preview=False, time=5.0, perFrame='frame', conv=0.975, geoUpdate=False):

    start_timer = bd_helpers.timer()

    scene = modo.Scene()
    scene_path = scene.filename

    if passname != "None":
        passname = "group:{}".format(scene.item(passname).name)
    else:
        passname = ""

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

        batch_base_path = os.path.join(
            os.path.dirname(scene_path),
            "_batch",
            os.path.splitext(os.path.basename(scene_path))[0]
        )
        frames = "_Frames{}-{}".format(first_frame, last_frame)
        batch_path = os.path.normpath("{}{}.bat".format(batch_base_path, frames))
        bash_path = os.path.normpath("{}{}.sh".format(batch_base_path, frames))

        framelist = range(int(first_frame), int(last_frame) + 1, int(frame_step))
        framelist = chunker(framelist, batchsize)
        all_commands = []
        all_commands_win = []

        for framegroup in framelist:
            scene_dict = {}
            first_batch_frame = min(int(minframe) for minframe in framegroup)
            last_batch_frame = max(int(maxframe) for maxframe in framegroup)

            command_path = os.path.normpath(
                os.path.join(
                    batch_base_path,
                    "{filename}_batchrender_frames_{first}-{last}.txt".format(
                        filename=os.path.splitext(os.path.basename(scene_path))[0],
                        first=first_batch_frame,
                        last=last_batch_frame
                    )
                )
            )

            if not os.path.exists(os.path.dirname(command_path)):
                os.makedirs(os.path.dirname(command_path))

            command_path_win = os.path.normpath(
                os.path.join(
                    "{}_win".format(batch_base_path),
                    "{filename}_batchrender_frames_{first}-{last}.txt".format(
                        filename=os.path.splitext(os.path.basename(scene_path))[0],
                        first=first_batch_frame,
                        last=last_batch_frame
                    )
                )
            )

            if not os.path.exists(os.path.dirname(command_path_win)):
                os.makedirs(os.path.dirname(command_path_win))

            scene_dict[first_batch_frame] = {
                'path': scene_path,
                'first': first_batch_frame,
                'last': last_batch_frame,
                'step': frame_step,
                'pattern': pattern,
                'passes': passname,
                'region': region,
                'time': time,
                'perFrame': perFrame,
                'conv': conv,
                'geoUpdate': geoUpdate
            }

            if preview:
                modo_command = build_modo_preview_render_command(scenes=scene_dict,
                                                                 pathaliases={
                                                                     'WorkingProjects': bd_globals.bdconfig()['projects dir']
                                                                 })
            else:
                modo_command = build_modo_render_command(scenes=scene_dict,
                                                         pathaliases={
                                                             'WorkingProjects': bd_globals.bdconfig()['projects dir']
                                                         })

            with open(command_path, mode='w+') as command:
                command.write(modo_command)
                command.close()

            all_commands.append(command_path)

            if preview:
                modo_command_win = build_modo_render_command_win(scenes=scene_dict,
                                                                 pathaliases={
                                                                     'WorkingProjects': os.path.normpath(
                                                                         os.path.join(
                                                                             bd_globals.bdconfig()['alt drive'],
                                                                             bd_globals.bdconfig()['projects location']
                                                                         )
                                                                     )
                                                                 })
            else:
                modo_command_win = build_modo_render_command_win(scenes=scene_dict,
                                                                 pathaliases={
                                                                     'WorkingProjects': os.path.normpath(
                                                                         os.path.join(
                                                                             bd_globals.bdconfig()['alt drive'],
                                                                             bd_globals.bdconfig()['projects location']
                                                                         )
                                                                     )
                                                                 })

            with open(command_path_win, mode='w+') as command:
                command.write(modo_command_win)
                command.close()

            all_commands_win.append(command_path_win)

        modo_batch = build_modo_batch(commands=all_commands_win)
        modo_bash = build_modo_bash(commands=all_commands, headless=headless_path,
                                    render_range={'first': first_frame, 'last': last_frame})

        with open(batch_path, mode='w+') as batch:
            batch.write(modo_batch)
            batch.close()

        with open(bash_path, mode='w+') as bash:
            bash.write(modo_bash)
            bash.close()
        os.chmod(bash_path, 0755)

        lx.eval('scene.save')

        if proc == 'manual':

            if sys.platform == "darwin":
                pyperclip.copy(bash_path)
                subprocess.Popen(['open', '-a', '/Applications/Utilities/Terminal.app', '-n'])
            else:
                pyperclip.copy(batch_path)
                os.system("start /B start cmd.exe")

        else:
            if sys.platform == "darwin":
                proc = subprocess.Popen([bash_path])
                print proc.pid
            else:
                proc = subprocess.Popen([batch_path])
                print proc.pid

    bd_helpers.timer(start_timer, 'Headless Batch Creator')


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
