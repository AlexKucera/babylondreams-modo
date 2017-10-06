#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - modo_render

Release Notes:

V0.1 Initial Release - 2017-09-08

Copyright 2017 - BabylonDreams - Alexander Kucera & Monika Kucera GbR

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


"""

import subprocess
import traceback

import os
import time

import sys

import signal

p = None
modolog_path = ""
modorollinglog_path = ""


# FUNCTIONS -----------------------------------------------
def modo_cmd(string, showlog=False):
    p.stdin.write("{}\n".format(string))
    if showlog:
        modo_show_log()
    else:
        p.stdin.flush()
        print(p.stdout.readline())


def modo_show_log():

    modorollinglog_path = os.path.expanduser("~/modo_rolling.log")
    modorollinglog = open(modorollinglog_path, 'r')
    modorollinglog.seek(0, 2)
    while True:
        line = modorollinglog.readline()
        if not line:
            time.sleep(0.1)
            continue
        print line.strip()


def signal_handler(signal, frame):
    result = raw_input('You pressed Ctrl+C! Are you sure you want to abort the render? (y/n)')
    if result == "y":
        sys.exit(0)
    elif result == "n":
        print("Resuming render.")
        # restore the exit gracefully handler here
        signal.signal(signal.SIGINT, signal_handler)
    else:
        print("Resuming render.")
        # restore the exit gracefully handler here
        signal.signal(signal.SIGINT, signal_handler)

# END FUNCTIONS -----------------------------------------------


# MAIN PROGRAM --------------------------------------------


def main():
    global p
    global modolog_path
    global modorollinglog_path

    modocl = "/Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/modo/beta/11/modo.app/Contents/MacOS/modo_cl"
    modosc = 'scene.open "/Volumes/ProjectsRaid/WorkingProjects/peri/peri-2016_001-ACS/work/modo/05_render/010/010_0010/010_0010_v08_leadingcore.lxo"\n'
    modolog_path = os.path.expanduser("~/modo.log")
    modorollinglog_path = os.path.expanduser("~/modo_rolling.log")

    p = subprocess.Popen(modocl,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         universal_newlines=True,
                         shell=False,
                         bufsize=1)
    print(p.stdout.readline())

    modo_cmd('log.toConsole true')
    modo_cmd('log.toConsoleRolling true')
    modo_cmd('log.subToFile {{}} true "{}"\n'.format(modolog_path))
    modo_cmd('log.subToFileRolling {{}} true "{}"\n'.format(modorollinglog_path))
    modo_cmd('pathalias.create WorkingProjects "/Volumes/ProjectsRaid/WorkingProjects/"')
    modo_cmd(modosc)
    modo_cmd('query sceneservice scene.name ? current')
    modo_cmd('pref.value render.threads auto')
    modo_cmd('select.Item Render')
    modo_cmd('item.channel step 1')
    modo_cmd('item.channel first 1400')
    modo_cmd('item.channel last 1419')
    modo_cmd('item.channel outPat "[<pass>]_[<output>][<LR>].<FFFF>"')
    modo_cmd('render.animation {*} group:passes', showlog=True)
    modo_cmd('scene.close')
    modo_cmd('app.quit')
    print(p.stdout.read())


# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    # Argument parsing is available through the 
    # lx.arg and lx.args methods. lx.arg returns 
    # the raw argument string that was passed into 
    # the script. lx.args parses the argument string 
    # and returns an array of arguments for easier 
    # processing.

    #original_sigint = signal.getsignal(signal.SIGINT)
    #signal.signal(signal.SIGINT, signal_handler)

    try:
        main()
    except:
        print traceback.format_exc()
