#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - texture_effect_chooser
Release Notes:
V0.1 Initial Release - 2018-06-13
"""
import subprocess

import modo
import lx
import traceback
import os
import json
import sys
from pprint import pprint


def lxprint(msg):
    lx.out(msg)
    # print(msg)


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


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def load_json():
    """
    Returns a queryable dictionary from a JSON file.
    :return: vars (QueryDict)
    """
    configs = lx.eval('query platformservice path.path ? configs')
    config_file = "texture_effect_chooser_config.json"
    jsonpath = os.path.join(configs, config_file)
    if not os.path.exists(jsonpath):
        jsonpath = os.path.join(os.path.dirname(__file__), os.pardir, "setup", config_file)
        if not os.path.exists(jsonpath):
            jsonpath = os.path.join(os.path.dirname(__file__), config_file)
            if not os.path.exists(jsonpath):
                jsonpath = os.path.join(os.path.dirname(sys.argv[0]), config_file)

    if jsonpath is not None:
        config_path = os.path.normpath(jsonpath)
        with open(config_path) as json_data:
            try:
                vars = QueryDict(byteify(json.load(json_data)))
                return vars
            except:
                modo.dialogs.alert(
                    "Loading JSON failed",
                    "The provided file does not appear to be valid JSON.\n{}".format(
                        traceback.format_exc().splitlines()[-1]),
                    dtype='error'
                )

    else:

        return None


def ListTextureEffects(category=lx.symbol.sSHADE_SURFACE):
    # Texture Effects
    # internalName, userName = ListTextureEffects()

    # Render Outputs
    # internalName, userName = ListTextureEffects(lx.symbol.sSHADE_OUTPUT)

    # Light Effects
    # internalName, userName = ListTextureEffects(lx.symbol.sSHADE_LIGHT)

    # Environment Effects
    # internalName, userName = ListTextureEffects(lx.symbol.sSHADE_ENVIRONMENT)

    internal = []
    user = []

    host_svc = lx.service.Host()
    msg_svc = lx.service.Message()
    msg = lx.object.Message(msg_svc.Allocate())

    for i in xrange(host_svc.NumServers(lx.symbol.a_TEXTUREEFFECT)):
        srv = host_svc.ServerByIndex(lx.symbol.a_TEXTUREEFFECT, i)

        tag = srv.InfoTag(lx.symbol.sTFX_CATEGORY)

        if tag == category:
            internalName = srv.UserName()

            try:
                msg.SetMessage('frame.material', internalName, 0)
            except:
                pass
            else:
                userName = msg_svc.MessageText(msg)
                internal.append(internalName)
                user.append(userName)

    return internal, user


def generate_effects_list():
    # Reads out the config and combines it with a dynamically generated list of modo channel effects for the modo dialog.
    vars = load_json()
    textureEffects = []
    for key in sorted(vars['channels']):
        textureEffects.append(('base_{}'.format("_".join(key.lower().split(" "))), " ".join(key.split("_")).title()))

    textureEffects.append(('internal_command', 'Use modo Command Dialog'))
    internalName, userName = ListTextureEffects()
    for ni, nu in zip(internalName, userName):
        textureEffects.append((ni, nu))

    return textureEffects


def generate_effects_type():
    # Pops up the modo channel effects dialog and then queries the selected effect.
    scene = modo.Scene()
    previousSelection = scene.selected
    dummy = scene.addItem(lx.symbol.sITYPE_IMAGEMAP)
    scene.select(dummy)
    lx.eval('shader.setEffect')
    effectType = dummy.channel(lx.symbol.sICHAN_TEXTURELAYER_EFFECT).get()
    lx.eval('texture.delete')
    scene.select(previousSelection)
    return effectType


def generate_id_list():
    # Reads out the config and builds a list of predefined filter words for the modo dialog.
    vars = load_json()
    ids = [('base_all', 'All Default Filters')]
    for key in sorted(vars['filter']):
        ids.append(('base_{}'.format("_".join(key.lower().split(" "))), " ".join(key.split("_")).title()))

    return ids


def apply_channel_fx_to_scene(texture_id, effectType):
    # loop through textures and apply channel effect if associated texture has texture id in its file name
    scene = modo.Scene()
    applied = False
    for item in scene.iterItems(lx.symbol.sITYPE_IMAGEMAP):
        for i in item.itemGraph('shadeLoc').forward():
            if i.type == lx.symbol.sITYPE_VIDEOCLIP or i.type == lx.symbol.sITYPE_VIDEOSEQUENCE or i.type == lx.symbol.sITYPE_VIDEOSTILL:
                filename = os.path.splitext(os.path.basename(i.channel('filename').get()))[0].lower()
                for id in texture_id:
                    if id in filename:
                        item.channel(lx.symbol.sICHAN_TEXTURELAYER_EFFECT).set(effectType)
                        applied = True
    if not applied:
        print("No textures of type {} in this scene. Nothing was changed.".format(effectType))
    else:
        print("All textures of type {} adjusted.".format(effectType))


def get_effectType(channel_fx, base_filter, base_all, config, texture_id):
    # figure out which channel effects we are using. either the supplied list, the modo internal command or the base types from the config file
    effectType = None

    if channel_fx == 'internal_command':
        effectType = generate_effects_type()
    elif channel_fx.startswith("base_"):
        channel_fx = " ".join(channel_fx[5:].split("_"))
        if base_filter or base_all:
            if channel_fx in config['channels'].keys():
                effectType = eval(config['channels'][channel_fx][texture_id])
        else:
            if base_all:
                texture_id = 'diffuse'
            effectType = eval(config['channels']['modo'][texture_id])
    else:
        effectType = channel_fx

    return effectType


def main(texture_id, channel_fx):
    scene = modo.Scene()

    config = load_json()
    base_filter = False
    base_all = False

    # prep the word filter
    if texture_id == 'base_all':
        base_all = True
    elif texture_id.startswith("base_"):
        texture_id = texture_id[5:]
        for key in config['filter']:
            if texture_id in config['filter'][key]:
                texture_filter = config['filter'][key]
                base_filter = True
    else:
        # none of the predefined filters are used. grab the text input and turn it into a list
        texture_filter = "".join(texture_id.lower().split()).split(',')
    if not base_all:
        effectType = get_effectType(channel_fx, base_filter, base_all, config, texture_id)
        apply_channel_fx_to_scene(texture_filter, effectType)
    else:

        for filter in config['filter']:
            effectType = get_effectType(channel_fx, base_filter, base_all, config, filter)

            apply_channel_fx_to_scene(config['filter'][filter], effectType)


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
