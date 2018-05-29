#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_select_by_size

Release Notes:

V0.1 Initial Release - 2018-05-29

Copyright 2018 - BabylonDreams - Alexander Kucera & Monika Kucera GbR

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

import bd_helpers
from var import *
from pprint import pprint


# FUNCTIONS -----------------------------------------------


def get_bbox_info(mesh):
    scene = modo.Scene()
    item = dict()

    x1 = mesh.geometry.boundingBox[0][0]
    y1 = mesh.geometry.boundingBox[0][1]
    z1 = mesh.geometry.boundingBox[0][2]

    x2 = mesh.geometry.boundingBox[1][0]
    y2 = mesh.geometry.boundingBox[1][1]
    z2 = mesh.geometry.boundingBox[1][2]

    x_length = abs(x1 - x2)
    y_length = abs(y1 - y2)
    z_length = abs(z1 - z2)

    item['longest'] = max(x_length, y_length, z_length)
    item['shortest'] = min(x_length, y_length, z_length)
    item['area'] = x_length * z_length
    item['volume'] = x_length * z_length * y_length

    return item


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------


def main(mode='volume', size='0.02', invert=False):
    start_timer = bd_helpers.timer()

    scene = modo.Scene()

    print(mode)
    print(size)
    print(invert)
    filtered_meshes = []

    for mesh in scene.meshes:
        if invert:
            if get_bbox_info(mesh)[mode] > size:
                filtered_meshes.append(mesh)
        else:
            if get_bbox_info(mesh)[mode] < size:
                filtered_meshes.append(mesh)

    scene.select(filtered_meshes)

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
        print(traceback.format_exc())
