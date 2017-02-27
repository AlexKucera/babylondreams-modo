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

# FUNCTIONS -----------------------------------------------


def getDifference(old, new, adjust, tolerance=0.000001):
    rounded = min(adjust, tolerance)

    adjusted = adjust + (new - old)

    return adjusted


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main(center_action):
    scene = modo.Scene()
    save_selection = lx.evalN("query sceneservice selection ? all")  # Save selection for later
    counter = False

    for item in save_selection:

        source = False
        mesh = scene.item(item)

        if mesh.type != "mesh":
            # If the selected item is not a mesh break the loop as we only want to adjust the centers of mesh items.
            print("Not a mesh: {0}".format(item))

        else:

            graph = mesh.itemGraph('meshInst')

            # Check if a mesh has any instances connected to it

            if graph.forward():
                source = True

            if source:

                counter = True

                # We found instances. Now the fun begins. Grab all the instances and save positions for later

                mesh.select(replace=True)
                lx.eval("select.itemInstances")
                instances = lx.evalN("query sceneservice selection ? all")

                instances_dict = {}

                for instance in instances:
                    instance_pos_x = modo.LocatorSuperType(instance).position.x.get()
                    instance_pos_y = modo.LocatorSuperType(instance).position.y.get()
                    instance_pos_z = modo.LocatorSuperType(instance).position.z.get()

                    instances_dict[instance] = [instance_pos_x, instance_pos_y, instance_pos_z]

                # Grab the source mesh's position, adjust the Center and get the new (offset) position

                original_pos_x = mesh.position.x.get()
                original_pos_y = mesh.position.y.get()
                original_pos_z = mesh.position.z.get()

                mesh.select(replace=True)

                lx.eval(center_action)

                new_pos_x = mesh.position.x.get()
                new_pos_y = mesh.position.y.get()
                new_pos_z = mesh.position.z.get()

                mesh.position.x.set(original_pos_x)
                mesh.position.y.set(original_pos_y)
                mesh.position.z.set(original_pos_z)

                offset_pos_x = getDifference(original_pos_x, new_pos_x, original_pos_x)
                offset_pos_y = getDifference(original_pos_y, new_pos_y, original_pos_y)
                offset_pos_z = getDifference(original_pos_z, new_pos_z, original_pos_z)

                # modo.LocatorSuperType(mesh).transforms.insert(xfrmType='position', placement='append',
                #                                              values=(offset_pos_x, offset_pos_y, offset_pos_z),
                #                                              name='OffsetCompensate')

                modo.LocatorSuperType(mesh).transforms.insert(xfrmType='position', placement='append',
                                                              values=(new_pos_x, new_pos_y, new_pos_z),
                                                              name='OffsetCompensate')

                for instance in instances:
                    instance_pos_x = instances_dict[instance][0]
                    instance_pos_y = instances_dict[instance][1]
                    instance_pos_z = instances_dict[instance][2]

                    new_instance_pos_x = getDifference(original_pos_x, new_pos_x, instance_pos_x)
                    print("X\n\norig: {0}\nnew: {1}\ninst: {2}\ninst_new:{3}".format(
                        original_pos_x, new_pos_x, instance_pos_x, new_instance_pos_x))
                    new_instance_pos_y = getDifference(original_pos_y, new_pos_y, instance_pos_y)
                    print("Y\n\norig: {0}\nnew: {1}\ninst: {2}\ninst_new:{3}".format(
                        original_pos_y, new_pos_y, instance_pos_y, new_instance_pos_y))
                    new_instance_pos_z = getDifference(original_pos_z, new_pos_z, instance_pos_z)
                    print("Z\n\norig: {0}\nnew: {1}\ninst: {2}\ninst_new:{3}".format(
                        original_pos_z, new_pos_z, instance_pos_z, new_instance_pos_z))

                    # modo.LocatorSuperType(instance).position.x.set(new_instance_pos_x)
                    # modo.LocatorSuperType(instance).position.y.set(new_instance_pos_y)
                    # modo.LocatorSuperType(instance).position.z.set(new_instance_pos_z)

                    modo.LocatorSuperType(instance).transforms.insert(xfrmType='position', placement='append',
                                                                      values=(new_pos_x, new_pos_y,
                                                                              new_pos_z),
                                                                      name='OffsetCompensate')

    bd_helpers.restoreSelection(save_selection)

    if not counter:
        print("No Meshes were selected.")


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
