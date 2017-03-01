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
import time

import lx
import modo


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
    running_timer = time.clock()
    if elapsed != 0.0:
        running_time = running_timer - elapsed
        if name is not '':
            name += ' '
        print('{0}Running Time: {1:.2f} seconds'.format(name, running_time))
    return running_timer
