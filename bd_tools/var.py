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
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages/')

current_dir = os.path.dirname(__file__)

# Config
BD_PIPELINE_PATH = os.path.abspath('{path}/{parent}/modules/bd_pipeline'.format(parent=os.pardir, path=current_dir))

if os.path.exists(BD_PIPELINE_PATH):
    BD_PIPELINE = BD_PIPELINE_PATH
else:
    BD_PIPELINE = "/Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/bd_pipeline"

DEBUG = True



# Variables

HOME_DIR = '{}{}'.format(os.path.expanduser('~'), os.sep)
TEMPLATES = os.path.abspath('{path}/{parent}/lxtemplates/'.format(parent=os.pardir, path=current_dir))

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
