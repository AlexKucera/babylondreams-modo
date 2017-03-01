#!/usr/bin/env python
# encoding: utf-8

"""

A simple example of a blessed MODO command using the commander module.
https://github.com/adamohern/commander for details

"""

import babylondreams
import lx
import modo

from bd_tools import bd_gl_capture

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
                'datatype': 'percent',
                'default': 1.0,
                'values_list_type': 'popup',
                'values_list': [1.0, .5, .25, .1]
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
                'default': self.renderCam(),
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
                'name': 'light_visibility',
                'datatype': 'boolean',
                'default': True
            },
        ]

    def renderCam(self):
        """

        Returns:
            string: Returns the render camera's ID.

        """
        scene = modo.Scene()
        return scene.renderCamera.id

    def get_cameras(self):
        """

        Returns:
            array: Tuple containing the camera.id and the camera.name.
                    For example: [(scene.renderCamera, "Render Camera")]

        """
        scene = modo.Scene()
        cameras = scene.items(itype='camera', superType=True)

        all_cameras = [(scene.renderCamera, "Render Camera")]

        for camera in cameras:
            all_cameras.append((camera.id, camera.name))

        return all_cameras

    def commander_execute(self, msg, flags):
        """

        Args:
            msg:
            flags:
        """
        gl_recording_size = self.commander_arg_value(0)
        gl_recording_type = self.commander_arg_value(1)

        reload(bd_gl_capture)
        bd_gl_capture.main()


lx.bless(CommandClass, 'bd.gl_capture')
