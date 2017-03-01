#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description


"""

Allows adjustments to the center of an object that is the source of a bunch of instances without the instances flying off in all directions.

The basic idea is to save the source world position, then adjust the center, then get the new world position and calculate the offset. Then apply this offset to the transform of all the instances.

Release Notes:

    Seems to work well on fresh CAD imports. Does not seem to work at all on manually created instance hierarchies. Bummer.

V0.1 Initial Release

"""

import traceback
import lx
import modo
import bd_helpers
from var import *

# FUNCTIONS -----------------------------------------------


def getDifference(old, new, adjust, tolerance=0.000001):
    rounded = min(adjust, tolerance)

    adjusted = adjust + (new - old)

    return adjusted


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(center_action):

    start_timer = bd_helpers.timer()

    print '#' * 20
    print 'Adjusting Instance Source Centers'
    print center_action

    scene = modo.Scene()
    save_selection = scene.selected  # Save selection for later

    # Weed out non-sources and find sources for any selected instances.
    sources = []
    already_seen = []
    instances = {}

    for item in save_selection:

        if item.type == "mesh":

            graph = item.itemGraph('meshInst').forward()  # Find any connected instances.

            if len(graph) > 0:
                sources.append(item)
                instances[item] = [graph]

        if item.type == "meshInst":

            if item in already_seen:
                pass
                # print('already got this source')
            else:
                # print('new source')
                graph = item.itemGraph('meshInst').reverse()  # Find the source mesh
                sources.append(graph[0])
                already_seen.extend(graph[0].itemGraph('meshInst').forward())
                instances[graph[0]] = [graph[0].itemGraph('meshInst').forward()]
    sources = list(set(sources))  # Strip all duplicates

    if len(sources) == 0:

        print('No source meshes found. Please select at least one instance or source mesh.')

    else:

        for mesh in sources:

            print("Adjusting mesh {0} of {1}".format(sources.index(mesh), len(sources)))

            # We found instances. Now the fun begins. Grab all the instances and save positions for later

            instance_array = []

            for values in instances[mesh]:
                for value in values:
                    instance_array.append(value)

            instances_dict = {}

            for instance in instance_array:
                instance_pos_x = modo.LocatorSuperType(instance).position.x.get()
                instance_pos_y = modo.LocatorSuperType(instance).position.y.get()
                instance_pos_z = modo.LocatorSuperType(instance).position.z.get()

                instances_dict[instance] = [instance_pos_x, instance_pos_y, instance_pos_z]

            # Grab the source mesh's position, adjust the Center and get the new (offset) position

            original_pos_x = mesh.position.x.get()
            original_pos_y = mesh.position.y.get()
            original_pos_z = mesh.position.z.get()

            mesh.select(replace=True)

            if center_action == 'center.matchWorkplane pos':

                lx.eval('select.convert center')
                lx.eval(center_action)
                lx.eval('select.type item')

            else:

                lx.eval(center_action)

            new_pos_x = mesh.position.x.get()
            new_pos_y = mesh.position.y.get()
            new_pos_z = mesh.position.z.get()

            # Move the item back to the original position. We are using an extra position channel for the offset.
            # This is so Instances don't need to be calculated with hard vector math.

            mesh.position.x.set(original_pos_x)
            mesh.position.y.set(original_pos_y)
            mesh.position.z.set(original_pos_z)

            modo.LocatorSuperType(mesh).transforms.insert(xfrmType='position', placement='append',
                                                          values=(new_pos_x, new_pos_y, new_pos_z),
                                                          name='OffsetCompensate')

            for instance in instance_array:

                modo.LocatorSuperType(instance).transforms.insert(xfrmType='position', placement='append',
                                                                  values=(new_pos_x, new_pos_y, new_pos_z),
                                                                  name='OffsetCompensate')
    scene.select(save_selection)

    bd_helpers.timer(start_timer, 'Overall')

    print('Finished adjusting the instance centers. Adjusted {0} sources.'.format(len(sources)))


# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    try:
        # Argument parsing is available through the
        # lx.arg and lx.args methods. lx.arg returns
        # the raw argument string that was passed into
        # the script. lx.args parses the argument string
        # and returns an array of arguments for easier
        # processing.

        argsAsString = lx.arg()
        argsAsTuple = lx.args()

        main()

    except:
        lx.out(traceback.format_exc())
