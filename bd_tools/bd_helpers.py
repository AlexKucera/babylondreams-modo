#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_helpers

Release Notes:

    A collection of several often used helper functions.

V0.1 Initial Release - 2017-02-20

"""

import sys
import os
import timeit
import traceback

import lx
import modo

from var import *


def selected(num=1):
    """

    Returns: A list of last N selected items. If the minimum number of selected items is not selected a warning dialog pops up.

    """
    scene = modo.Scene()
    selected = scene.selected

    if len(selected) < num:

        if num == 1:
            filler = "item"
        else:
            filler = "items"

        modo.dialogs.alert("Warning", "Please select at least one {0}.".format(filler), dtype='warning')

    if len(selected) > num:
        selected = selected[-num:]

    return selected


def restoreSelection(listSelections):
    """
    Used together with:

    global save_selection
    save_selection = lx.evalN("query sceneservice selection ? all")

    to save and later restore a selection in modo with

    bd_helpers.restoreSelection(save_selection)

    """

    try:
        # lx.out(listSelections)
        first = True
        for x in listSelections:
            if first:
                lx.eval("select.item {%s} set" % x)
            else:
                lx.eval("select.item {%s} add" % x)
            first = False
        print('Restored selection!')

    except:
        lx.eval('layout.createOrClose EventLog "Event Log_layout" '
                'title:@macros.layouts@EventLog@ width:600 height:600 persistent:true '
                'open:true')
        lx.out("ERROR restoreSelection failed with ", sys.exc_info())
        return None


def timer(elapsed=0.0, name=''):
    """
    Timer function for debugging.

    Example:

        start = bd_helpers.timer()

        bd_helpers.timer(start, "test")

    """
    running_timer = timeit.default_timer()
    if elapsed != 0.0:
        running_time = running_timer - elapsed
        timestring = secondsToHoursMinutesSeconds(running_time)
        if name is not '':
            name += ' '
        print('{0}Running Time: {1}'.format(name, timestring))
    return running_timer


def secondsToHoursMinutesSeconds(seconds):
    """ takes a seconds int or float and returns a string that breaks"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours != 0:
        hours = "{} hours ".format(int(hours))
    else:
        hours = ""
    if minutes != 0:
        minutes = "{} minutes ".format(int(minutes))
    else:
        minutes = ""
    seconds = "{:.2f} seconds".format(seconds)

    secondsToString = '{hours}{minutes}{seconds}'.format(hours=hours, minutes=minutes, seconds=seconds)

    return secondsToString

def walk_up(bottom):

    """
    mimic os.walk, but walk 'up'
    instead of down the directory tree

    os.walk is an awesome generator.
    However, I needed the same functionality, only I wanted to walk 'up' the directory tree.
    This allows searching for files in directories directly above a given directory.

    via: https://gist.github.com/zdavkeos/1098474
    """

    from os import path

    bottom = path.realpath(bottom)

    # get files in current dir
    try:
        names = os.listdir(bottom)
    except Exception as e:
        print(e)
        return

    dirs, nondirs = [], []
    for name in names:
        if path.isdir(path.join(bottom, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    yield bottom, dirs, nondirs

    new_path = path.realpath(path.join(bottom, '..'))

    # see if we are at the top
    if new_path == bottom:
        return

    for x in walk_up(new_path):
        yield x


def debug(string):
    """
    Prints a string to lx.out() if defaults.get('debug') returns True. (See defaults.py)
    Intended for developer debugging only; user messages should use 'status'.
    Inspired by the debug function from Adam O'Hern for Mechanical Color
    """
    if DEBUG:
        t = traceback.extract_stack()[-2]
        print("debug '{filename}' line {line}, {function}\n----------\n{string}".format(filename=os.path.basename(t[0]),
                                                  line=t[1],
                                                  function=t[2],
                                                  string=string))


def status(string):
    """
    Prints a string to lx.out(). Differs from "debug" only in that it's always enabled.
    Useful for user-related messages.
    Inspired by the debug function from Adam O'Hern for Mechanical Color
    """

    print("status:\n----------\n{}".format(string))
