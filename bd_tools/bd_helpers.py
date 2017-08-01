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
import json
import sys
import os
import timeit
import traceback

import lx
import modo


class QueryDict(dict):
    """
    Creates a Dictionary that is browseable by path.

    Example:

        query_dict = {'key': {'subkey': 'value'}}

        print query_dict['key/subkey']

    """

    def __getitem__(self, key_string):
        current = self
        try:
            for key in key_string.split('/'):
                current = dict.__getitem__(current, key)
            return current
        except (TypeError, KeyError):

            return None


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

        modo.dialogs.alert("Warning", "Please select at least {1} {0}.".format(filler, num), dtype='warning')

        return None

    if len(selected) > num:
        selected = selected[-num:]

        return selected

    if len(selected) == num:

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


def load_json():
    """
    Returns a queryable dictionary from a JSON file.

    :return: vars (QueryDict)

    """

    jsonpath = modo.dialogs.customFile('fileOpen', 'Open File', ('json',), ('JSON File',), ('*.json',))

    if jsonpath is not None:
        config_path = os.path.normpath(jsonpath)
        with open(config_path) as json_data:
            try:
                vars = QueryDict(json.load(json_data))
                return vars
            except:
                modo.dialogs.alert("Loading JSON failed",
                                   "The provided file does not appear to be valid JSON.\n{}".format(
                                       traceback.format_exc().splitlines()[-1]),
                                   dtype='error')

    else:

        return None


def save_json(dictdata="", prefix=""):
    """
    Saves a dictionary to a JSON file.

    """

    jsonpath = modo.dialogs.customFile('fileSave', 'Save File', ('json',), ('JSON File',), ext=('json',),
                                       path=default_json_path(prefix))

    if jsonpath is not None:
        config_path = os.path.normpath(jsonpath)

        if not os.path.exists(os.path.dirname(config_path)):
            try:
                os.makedirs(os.path.dirname(config_path))
            except:
                print(traceback.format_exc())

        with open(config_path, 'w+') as outfile:
            json.dump(dictdata, outfile, sort_keys=True, indent=4)

            outfile.close()
            print("{} written to {}".format(os.path.basename(config_path), os.path.dirname(config_path)))


def default_json_path(prefix=""):
    scene = modo.Scene()

    filename = scene.filename
    if not filename:
        filedir = lx.eval("query platformservice path.path ? temp")
        filename = "untitled"

    else:
        filedir = os.path.dirname(filename)
        filename = os.path.splitext(filename)[0]

    jsonpath = os.path.normpath(
        os.path.join(
            filedir,
            "{}{}".format(prefix, filename)
        )
    )

    return jsonpath


def get_channels(item, type=None, forbidden_channels=[], isAnimated=False):
    item_channels = []
    for channel in item.channels():
        if channel.name not in forbidden_channels:
            if type is "name":
                item_channels.append(channel.name)
            if type is "index":
                item_channels.append(channel.index)
            if type is None:
                pass
    if type is None:
        item_channels = item.channels()
    return item_channels


def channel_copy_paste(item_id, channel_name, cmd="copy"):
    lx.eval("select.channel {{{0}:{1}}} set".format(item_id, channel_name))
    if cmd is "paste":
        lx.eval("channel.paste")
    elif cmd is "copy":
        print("Copying {}".format(channel_name))
        lx.eval("channel.copy")


def get_tags(item):
    if item.hasTag("anim"):
        if item.readTag("anim"):
            tag = item.readTag("anim")
            return tag
    return None
