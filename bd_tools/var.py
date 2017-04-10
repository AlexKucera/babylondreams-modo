#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - var.py

Release Notes:

V0.1 Initial Release - 2017-02-24

"""

# Commands
import os

# Config
BD_PIPELINE = "/Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/bd_pipeline"
DEBUG = True



# Variables

HOME_DIR = '{}{}'.format(os.path.expanduser('~'), os.sep)

BLEND_COMMAND = 'fade'

CENTER_BBOX = 'Center to BBox'
CENTER_WPLANE = 'Center to Workplane'
CENTER_TOP = 'Center to BBox Top'
CENTER_BOTTOM = 'Center to BBox Bottom'
CENTER_LEFT = 'Center to BBox Left'
CENTER_RIGHT = 'Center to BBox Right'
CENTER_FRONT = 'Center to BBox Front'
CENTER_BACK = 'Center to BBox Back'

# Commands

INSTANCE_REROUTE = 'bd.instance_reroute'
