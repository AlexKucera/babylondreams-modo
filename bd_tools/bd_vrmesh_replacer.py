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

def convert_proxy(item, proxy, path):
    scene= modo.Scene()
    print("Converting item {} to V-Ray Proxy ({}).".format(item.name, proxy))
    scene.select(item)
    if scene.selected[0].type == lx.symbol.sITYPE_MESH:
        lx.eval("item.setType vray.proxy locator")
        if len(scene.selected) > 1:
            lx.eval("select.itemSourceSelected")
        vrproxy = scene.selected[0]

        # print("Creating V-Ray Proxy and moving it into place.")
        # vrproxy = scene.addItem('vray.proxy', name=proxy)
        # vrproxy = modo.item.LocatorSuperType(item=vrproxy)
        # vrproxy.setParent(i.parent, i.parentIndex)
        # vrproxy.position.set(i.position.get())
        # vrproxy.rotation.set(i.rotation.get())
        # vrproxy.scale.set(i.scale.get())

        print("Setting item {} to vrmesh {}.".format(item.name, proxy))
        vrproxy.channel('vray_file').set(os.path.join(path, proxy + ".vrmesh"))
# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    start_timer = bd_helpers.timer()

    scene = modo.Scene()
    sel = scene.selected

    path = modo.dialogs.dirBrowse(" V-Ray Proxy Path")

    if path:
        proxies = get_proxies(path)

        all_items = []
        meshes = []

        # Get all mesh items in the selected hierarchy
        for i in sel:
            all_items.append(i)
            children = i.children(recursive=True, itemType=lx.symbol.sITYPE_MESH)
            if len(children) > 0:
                all_items += children

        all_items = set(all_items)

        # Filter out any non-meshes
        for i in all_items:
            if i.type == lx.symbol.sITYPE_MESH:
                meshes.append(i)

        meshes = set(meshes)

        if len(meshes) > 0:

            found = False

            m = lx.Monitor(len(proxies))
            m.init(len(proxies) * 2)
            # Go through all proxy files and compare their names to the mesh names
            for proxy in proxies:

                regex = "{}".format(re.escape(proxy))
                m.step(1)

                for i in meshes:
                    match = re.match(regex, i.name)
                    if match:
                        found = True

                        try:
                            convert_proxy(i, proxy, path)

                        except:
                            pass

            # Second round with looser regex to catch any misses
            reduced = []
            for i in meshes:
                if i.type == lx.symbol.sITYPE_MESH:
                    reduced.append(i)

            meshes = set(reduced)

            if len(meshes) > 0:
                for proxy in proxies:

                    regex = "{}[ _\d]*$".format(re.escape(proxy))
                    m.step(1)

                    for i in meshes:

                        match = re.match(regex, i.name)

                        if match:
                            found = True

                            print i
                            print proxy

                            try:
                                convert_proxy(i, proxy, path)

                            except:
                                pass
                else:
                    m.step(len(proxies))

            if not found:
                print("No V-Ray Proxies found for the selected meshes.")

        else:

            print("No meshes to replace. Please select some meshes first.")

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
