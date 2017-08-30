#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""
babylondreams - bd_create_material_outputs

Release Notes:

V0.1 Initial Release - 2017-08-28

"""

import bd_helpers
import modo
import lx
import traceback


# FUNCTIONS -----------------------------------------------
def addmask(mask, mask_type):
    scene = modo.Scene()

    # Grab Material Group Name, remove any "(Material)" suffix and spaces
    mask_name = "_".join(mask.name.replace("(Material)", "").split())
    mask_type_name = mask_type.split(".")[1]  # Get only the effect name, e.g: shade.alpha → alpha

    # Create renderoutput
    output = scene.addItem(lx.symbol.sITYPE_RENDEROUTPUT, name="{}_{}".format(mask_name, mask_type_name))

    # Set up renderoutput
    output.channel(lx.symbol.sICHAN_TEXTURELAYER_EFFECT).set(mask_type)
    output.channel(lx.symbol.sICHAN_RENDEROUTPUT_COLORSPACE).set("nuke-default:linear")
    output.channel(lx.symbol.sICHAN_RENDEROUTPUT_CLAMP).set(False)
    output.channel(lx.symbol.sICHAN_RENDEROUTPUT_FILENAME).set("path")
    output.channel(lx.symbol.sICHAN_RENDEROUTPUT_FORMAT).set("openexr")

    # Parent the output to its material mask
    output.setParent(mask, index=len(mask.children()) + 1)

    return output


# END FUNCTIONS -----------------------------------------------


# MAIN PROGRAM --------------------------------------------
def main():
    start_timer = bd_helpers.timer()

    scene = modo.Scene()
    sel = scene.selectedByType(lx.symbol.sITYPE_MASK)

    if len(sel) == 0:
        lx.out('No Material Groups selected!')
    else:
        outputs = []
        for mask in sel:
            color = False
            alpha = False
            for child in mask.children():
                if child.type == lx.symbol.sITYPE_RENDEROUTPUT:
                    effect = child.channel(lx.symbol.sICHAN_TEXTURELAYER_EFFECT).get()

                    if effect == lx.symbol.s_FX_OUTPUT_ALPHA:
                        print("{} has already an Alpha output.".format(mask.name))
                        alpha = True

                    if effect == lx.symbol.s_FX_OUTPUT_FINAL_COLOR:
                        print("{} has already a RGB output.".format(mask.name))
                        color = True

            if not color:
                print('Adding RGB output to {}'.format(mask.name))
                outputs.append(addmask(mask, lx.symbol.s_FX_OUTPUT_FINAL_COLOR))
            if not alpha:
                outputs.append(addmask(mask, lx.symbol.s_FX_OUTPUT_ALPHA))
                print('Adding Alpha output to {}'.format(mask.name))

        scene.select(outputs, add=False)

    bd_helpers.timer(start_timer, ' Overall')


# END MAIN PROGRAM -----------------------------------------------

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
