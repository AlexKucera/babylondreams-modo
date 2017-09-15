#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_vrmesh_replacer

Release Notes:

V0.1 Initial Release - 2017-09-15

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

import os
import traceback

import lx
import modo
import re

import time

import bd_helpers
from var import *


# FUNCTIONS -----------------------------------------------

def get_proxies(path=None):
    proxies = []

    # make sure we have a directory path
    if not os.path.isdir(path):
        path = os.path.split(path)[0]

    # get all vrmesh files
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            if os.path.splitext(f)[1] == ".vrmesh":
                proxies.append(os.path.splitext(f)[0])

    return set(proxies)


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    start_timer = bd_helpers.timer()

    scene = modo.Scene()
    sel = scene.selected

    path = modo.dialogs.dirBrowse(" V-Ray Proxy Path")
    proxies = get_proxies(path)

    all_items = []
    meshes = []
    for i in sel:
        all_items.append(i)
        children = i.children(recursive=True, itemType=lx.symbol.sITYPE_MESH)
        if len(children) > 0:
            all_items.append(children)

    for i in all_items:
        if i.type == lx.symbol.sITYPE_MESH:
            meshes.append(i)

    for proxy in proxies:
        regex = ".*{}.*".format(re.escape(proxy))

        for i in meshes:
            match = re.match(regex, i.name)
            if match:
                print("Converting item {} to V-Ray Proxy.".format(i.name))
                vrproxy = scene.addItem('vray.proxy', name=proxy)
                vrproxy.setParent(i.parent, i.parentIndex)
                vrproxy.position.set(i.position.get())
                vrproxy.rotation.set(i.rotation.get())
                vrproxy.scale.set(i.scale.get())
                print("Setting item {} to vrmesh {}.".format(i.name, proxy))
                vrproxy.channel('vray_file').set(os.path.join(path, proxy + ".vrmesh"))

    bd_helpers.timer(start_timer, os.path.splitext(os.path.basename(__file__))[0])


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
