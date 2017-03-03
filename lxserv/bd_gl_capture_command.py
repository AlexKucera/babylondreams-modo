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
        """
            TODO:
                * RayGL (Off, Fast, Full)
                * Wireframe
                * Grid
                * Viewport Controls and Info
                * Onion Skinning
                * Silhouette
                * Topology Mode
                * File Path
                * Auto Versioning
                * Replicators (None, All)
                * GL Background (None, Gradient, Environment, Image)
                * GL Reflection (None, Same as BG, Gradient, Environment, Image)
                * Enable Deformers Active
                * Item Visibility
                    * Lights
                    * Cameras
                    * Locators
                    * Texture Locators
                    * Meshes
                    * Instances
                * Workplane
                * Turn off Selections
                * Turn off Normals
                * Fur
                * Displacement
                * Use Shader Tree
                * Advanced
                    * Shadows
                    * Normal Maps
                    * Bump Maps
                    * Lighting (Viewport, Scene, Environment, Scene + Environment)
                    * Background (Viewport, Environment)
                    * Display Override (None, Without Wireframe, Without Wireframe + Widgets)
                    * Visibility (Viewport, Render)
                    * Ambient Occlusion
                    * AA (Off, 2xH, 2xV, 3x, 4x, 6x, 8x, 9x)
                    * Transparency (Off, Fast, Correct)
                    * Screen Space Reflections (Off, Fast, Blurry)
                    * Dither (Off, Ordered)
                * Inactive same as active
                * Disable Bounding Box Display

        :return:
        """
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
        filename = self.commander_arg_value(4)
        filepath = self.commander_arg_value(5)
        first_frame = self.commander_arg_value(6)
        last_frame = self.commander_arg_value(7)

        reload(bd_gl_capture)
        bd_gl_capture.main(gl_recording_size, gl_recording_type, viewport_camera,
                           shading_style, filename, filepath, first_frame, last_frame)


lx.bless(CommandClass, 'bd.gl_capture')
