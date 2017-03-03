#!/usr/bin/env python
# encoding: utf-8

"""

A simple example of a blessed MODO command using the commander module.
https://github.com/adamohern/commander for details

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
__version__ = "1.0.0"
__maintainer__ = "Alexander Kucera"
__email__ = "a.kucera@babylondreams.de"
__status__ = "Development"


class CommandClass(babylondreams.CommanderClass):
    _commander_last_used = []

    def commander_arguments(self):
        return [
            {
                'name': 'gl_recording_size',
                'label': "Recording Size (based on render size)",
                'datatype': 'string',
                'default': "100%",
                'values_list_type': 'popup',
                'values_list': ['100%', '50%', '25%', '10%']
            },
            {
                'name': 'gl_recording_type',
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
                'name': 'replicators',
                'datatype': 'boolean',
                'default': True
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
                'name': 'first_frame',
                'datatype': 'integer',
                'default': self.get_range('first'),
            },
            {
                'name': 'last_frame',
                'datatype': 'integer',
                'default': self.get_range('last'),
            },
        ]

    def get_cameras(self):
        """

        Returns:
            array: Tuple containing the camera.id and the camera.name.
                    For example: [(scene.renderCamera, "Render Camera")]

        """
        scene = modo.Scene()
        cameras = scene.items(itype='camera', superType=True)

        all_cameras = [('rendercam', "Render Camera")]

        for camera in cameras:
            all_cameras.append((camera.id, camera.name))

        return all_cameras

    def get_range(self, switch='first'):
        scene = modo.Scene()
        frame = scene.renderItem.channel(switch).get()
        return frame

    def capture_path(self):
        scene = modo.Scene()
        scene_path = scene.filename
        output = os.path.expanduser('~')
        file = 'preview'
        if scene_path is not None:
            file = os.path.splitext(os.path.basename(scene_path))[0]
            dir = os.path.dirname(scene_path)

            for path, directory, files in bd_helpers.walk_up(dir):

                if 'img' in directory:

                    output_path = '{0}{1}img{1}cg{1}previews{1}'.format(path, os.sep)

                    if not os.path.exists(output_path):
                        os.makedirs(output_path)

                    output = output_path  # '{0}{1}_preview.jpg'.format(output_path, file)

        return {'output_path': output, 'filename': file}

    def capture_file(self):
        filename = self.capture_path()
        name = [filename['filename']]
        return name

    def capture_output(self):
        output_path = self.capture_path()
        output = [output_path['output_path']]
        return output

    def commander_execute(self, msg, flags):

        gl_recording_size = self.commander_arg_value(0)
        gl_recording_type = self.commander_arg_value(1)
        viewport_camera = self.commander_arg_value(2)
        shading_style = self.commander_arg_value(3)
        bg_stlye = self.commander_arg_value(4)
        raygl = self.commander_arg_value(5)
        replicators = self.commander_arg_value(6)
        filename = self.commander_arg_value(7)
        filepath = self.commander_arg_value(8)
        first_frame = self.commander_arg_value(9)
        last_frame = self.commander_arg_value(10)

        reload(bd_gl_capture)
        bd_gl_capture.main(gl_recording_size, gl_recording_type, viewport_camera, shading_style, filename, filepath,
                           first_frame, last_frame, raygl, replicators, bg_stlye)


lx.bless(CommandClass, 'bd.gl_capture')
