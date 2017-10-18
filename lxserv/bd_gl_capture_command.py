#!/usr/bin/env python
# encoding: utf-8

"""

A simple example of a blessed MODO command using the commander module.
https://github.com/adamohern/commander for details

Todo:

    * global pipeline config prefs (image paths etc.)

"""
import re

import babylondreams
import lx
import modo
import os

from bd_tools import bd_gl_capture
from bd_tools import bd_helpers
from bd_tools.var import *

__author__ = "Alexander Kucera"
__copyright__ = "Copyright 2017, BabylonDreams - Alexander & Monika Kucera GbR"
__credits__ = ["Alexander Kucera"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Alexander Kucera"
__email__ = "a.kucera@babylondreams.de"
__status__ = "Development"


class CommandClass(babylondreams.CommanderClass):
    _commander_last_used = []

    def commander_arguments(self):
        return [
            {
                'name': 'gl_recording_size',
                'label': "Recording Res (Render res)",
                'datatype': 'string',
                'default': "100%",
                'values_list_type': 'popup',
                'values_list': ['100%', '50%', '25%', '10%']
            },
            {
                'name': 'gl_recording_type',
                'label': "Recording Format",
                'datatype': 'string',
                'default': 'image',
                'values_list_type': 'popup',
                'values_list': [('movie', 'Movie'), ('image', 'Image Sequence')]
            }
            ,
            {
                'name': 'viewport_camera',
                'datatype': 'string',
                'default': 'rendercam',
                'values_list_type': 'popup',
                'values_list': self.get_cameras
            },
            {
                'name': 'shading_style',
                'datatype': 'string',
                'default': 'advgl',
                'values_list_type': 'popup',
                'values_list': [('gnzgl', 'Advanced'), ('advgl', 'Default'), ('texmod', 'Texture Shaded'),
                                ('tex', 'Texture'), ('shade', 'Shaded'), ('vmap', 'Vertex Map'), ('sket', 'Solid'),
                                ('wire', 'Wireframe'), ('shd1', 'Gooch Toon Shading'), ('shd2', 'Cel Shading'),
                                ('shd3', 'Reflection')]
            },
            {
                'name': 'gl_background',
                'label': "GL Background",
                'datatype': 'string',
                'default': 'environment',
                'values_list_type': 'popup',
                'values_list': [('environment', 'Environment'), ('solid', 'None')]
            },
            {
                'name': 'ray_gl',
                'label': "RayGL",
                'datatype': 'string',
                'default': 'off',
                'values_list_type': 'popup',
                'values_list': [('full', ' Full'), ('fast', ' Fast'), ('off', ' Off')]
            },
            {
                'name': 'replicator_visibility',
                'label': "Replicator/Locator Visibility",
                'datatype': 'string',
                'default': 'none',
                'values_list_type': 'popup',
                'values_list': [('always', 'Visible'), ('none', ' Hidden')]
            },
            {
                'name': 'bbox_toggle',
                'label': "Bounding Box Display",
                'datatype': 'string',
                'default': 'full',
                'values_list_type': 'popup',
                'values_list': [('full', 'Geo Visible'), ('bbox', 'BBox On')]
            },
            {
                'name': 'avp_shadows',
                'label': 'Enable AVP Shadows',
                'datatype': 'boolean',
                'default': True
            },
            {
                'name': 'avp_ao',
                'label': 'Enable AVP Ambient Occlusion',
                'datatype': 'boolean',
                'default': True
            },
            {
                'name': 'automatic_naming',
                'label': 'Automatic Name & Path (based on project definition)',
                'datatype': 'boolean',
                'default': True,
            },
            {
                'name': 'file_name',
                'datatype': 'string',
                'default': 'preview',
                'values_list_type': 'sPresetText',
                'values_list': self.capture_file
            },
            {
                'name': 'file_path',
                'datatype': 'string',
                'default': HOME_DIR,
                'values_list_type': 'sPresetText',
                'values_list': self.capture_output
            },
            {
                'name': 'overwrite',
                'label': 'Overwrite? (Versions up if disabled)',
                'datatype': 'boolean',
                'default': True
            },
            {
                'name': 'use_scene_range',
                'datatype': 'boolean',
                'default': True,
            },
            {
                'name': 'first_frame',
                'datatype': 'integer',
                'default': self.get_range()['first'],
            },
            {
                'name': 'last_frame',
                'datatype': 'integer',
                'default': self.get_range()['last'],
            },
        ]

    def get_cameras(self):
        """

        Returns:
            array: Tuple containing the camera.id and the camera.name.
                    For example: [(scene.renderCamera, "Render Camera")]

        """
        scene = modo.Scene()

        all_cameras = [('rendercam', "Render Camera")]

        for camera in scene.iterItemsFast(itype='camera'):
            all_cameras.append((camera.id, camera.name))

        return all_cameras

    def get_range(self):
        scene = modo.Scene()
        frame_range = modo.Scene().currentRange
        frame = {'first': frame_range[0], 'last': frame_range[1]}
        return frame

    def capture_file(self):
        filename = bd_gl_capture.capture_path()
        name = [filename['filename']]
        return name

    def capture_output(self):
        output_path = bd_gl_capture.capture_path()
        output = [output_path['output_path']]
        return output

    def commander_execute(self, msg, flags):
        arguments = self.commander_args()

        reload(bd_gl_capture)
        bd_gl_capture.main(gl_recording_size=arguments['gl_recording_size'],
                           gl_recording_type=arguments['gl_recording_type'],
                           viewport_camera=arguments['viewport_camera'],
                           shading_style=arguments['shading_style'],
                           filename=arguments['file_name'],
                           filepath=arguments['file_path'],
                           first_frame=arguments['first_frame'],
                           last_frame=arguments['last_frame'],
                           raygl=arguments['ray_gl'],
                           replicators=arguments['replicator_visibility'],
                           bg_style=arguments['gl_background'],
                           use_scene_range=arguments['use_scene_range'],
                           automatic_naming=arguments['automatic_naming'],
                           overwrite=arguments['overwrite'],
                           bbox_toggle=arguments['bbox_toggle'],
                           avp_shadows=arguments['avp_shadows'],
                           avp_ao=arguments['avp_ao'],
                           capturefile=self.capture_file()[0],
                           capturepath=self.capture_output()[0])


lx.bless(CommandClass, 'bd.gl_capture')
