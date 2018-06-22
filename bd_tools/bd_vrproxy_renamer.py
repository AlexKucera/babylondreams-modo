#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - vray_proxy_renamer
Release Notes:
V0.1 Initial Release - 2018-06-13
"""
import subprocess

import modo
import lx
import traceback
import os


def main():
    scene = modo.Scene()

    # loop through v-ray proxies and rename based on its file name
    for item in scene.iterItems('vray.proxy'):
        filename = "_".join(os.path.splitext(os.path.basename(item.channel('vray_file').get()))[0].lower().split())
        item.name = filename


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
