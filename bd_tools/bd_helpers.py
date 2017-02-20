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

import modo
import lx
import traceback


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
