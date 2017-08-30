#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Release Notes:

V0.1 Initial Release

"""
import random

import traceback
import math
import lx
import csv
import pyModo

csv_path = "/Users/alex/Downloads/15-06-14/hygdata_v3.csv"
csv_format = ","


cache_m4_path = "/Users/alex/Downloads/15-06-14/hygdata_v3_particles_m4_med.csv"
cache_m6_path = "/Users/alex/Downloads/15-06-14/hygdata_v3_particles_m6_med.csv"
cache_m8_path = "/Users/alex/Downloads/15-06-14/hygdata_v3_particles_m8_med.csv"
cache_m10_path = "/Users/alex/Downloads/15-06-14/hygdata_v3_particles_m10_med.csv"

# FUNCTIONS -----------------------------------------------

def file_len(fname):
    with open(fname) as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i + 1


def colors2float(color):
    color *= 1.0 / 255
    return color


def kelvin2rgb(kelvin):
    kelvin /= 100.0

    if kelvin <= 66:
        red = 1.0
    else:
        red = kelvin - 60
        red = 329.698727446 * (red ** -0.1332047592)
        if red < 0:
            red = 0.0
        elif red > 255:
            red = 1.0
        else:
            red = colors2float(red)

    if kelvin <= 66:
        green = kelvin
        green = 99.4708025861 * math.log(green) - 161.1195681661
        if green < 0:
            green = 0.0
        elif green > 255:
            green = 1.0
        else:
            green = colors2float(green)
    else:
        green = kelvin - 60
        green = 288.1221695283 * (green ** -0.0755148492)
        if green < 0:
            green = 0.0
        elif green > 255:
            green = 1.0
        else:
            green = colors2float(green)

    if kelvin >= 66:
        blue = 1.0
    elif kelvin <= 19:
        blue = 0.0
    else:
        blue = kelvin - 10
        blue = 138.5177312231 * math.log(blue) - 305.0447927307
        if blue < 0:
            blue = 0.0
        elif blue > 255:
            blue = 1.0
        else:
            blue = colors2float(blue)

    return red, green, blue


def spectral2rgb(spectral_type):
    """

    :rtype : float
    """

    spectral = str.lower(spectral_type[0])

    random.seed()
    o_class = random.randrange(30000, 40000, 500)
    b_class = random.randrange(15000, 25000, 500)
    a_class = random.randrange(9000, 14000, 500)
    f_class = random.randrange(6500, 8500, 100)
    g_class = random.randrange(4500, 6000, 100)
    k_class = random.randrange(3800, 4400, 100)
    m_class = random.randrange(3000, 3600, 100)
    random_range = random.randrange(3000, 40000, 1000)

    if spectral == "o":
        red, green, blue = kelvin2rgb(o_class)
    elif spectral == "b":
        red, green, blue = kelvin2rgb(b_class)
    elif spectral == "a":
        red, green, blue = kelvin2rgb(a_class)
    elif spectral == "f":
        red, green, blue = kelvin2rgb(f_class)
    elif spectral == "g":
        red, green, blue = kelvin2rgb(g_class)
    elif spectral == "k":
        red, green, blue = kelvin2rgb(k_class)
    elif spectral == "m":
        red, green, blue = kelvin2rgb(m_class)
    else:
        red, green, blue = kelvin2rgb(random_range)

    return red, green, blue


# noinspection PyArgumentList
def new_gradient(name, shader_type, input_type="particleID"):
    """
    Creates a new Gradient with a preset Input type and Shader Effect.
    :param name: What to call the Gradient after its creation.
    :param input_type: The Input type of the Gradient. Usually incidence or particleID
    :param shader_type: For example lumiAmount or lumiColor
    :return: list
    """
    pyModo.Gradient_Add_New()
    mag_id = pyModo.Gradient_ID_Selected()
    lx.eval("item.name %s gradient" % name)
    lx.eval("texture.setInput %s" % input_type)
    lx.eval("shader.setEffect %s" % shader_type)

    return mag_id[0]


# noinspection PyArgumentList
def magnitude_key(particle_id, magnitude, gradient_id, floor=20.0, ceiling=-20.0):
    """
    Creates the necessary value keys in the specified gradient.
    :param particle_id: The current ID count.
    :param magnitude: The absolute magnitude from the star dataset.
    :param gradient_id: The gradient to add the keys to.
    :return: None
    """
    floor = 1 / pow(2.512, float(floor))
    ceiling = 1 / pow(2.512, float(ceiling))
    brightness = 1 / pow(2.512, float(magnitude))
    brightness = (float(brightness) - floor) / (ceiling - floor) * 40000000000
    lx.eval("channel.key " + str(float(particle_id)) + " " + str(float(brightness))
            + " insert:true channel:{" + gradient_id + ":value}")


# noinspection PyArgumentList
def spectral_key(particle_id, spectral_type, gradient_id):
    """
    Creates the necessary value keys in the specified gradient.
    :param particle_id: The current ID count.
    :param spectral_type: The spectral type from the star dataset.
    :param gradient_id: The gradient to add the keys to.
    :return: None
    """

    if not spectral_type:
        red, green, blue = spectral2rgb("x")
    else:
        red, green, blue = spectral2rgb(spectral_type)

    lx.eval("channel.key " + str(float(particle_id)) + " " + str(red)
            + " insert:true channel:{" + gradient_id + ":color.R}")
    lx.eval("channel.key " + str(float(particle_id)) + " " + str(green)
            + " insert:true channel:{" + gradient_id + ":color.G}")
    lx.eval("channel.key " + str(float(particle_id)) + " " + str(blue)
            + " insert:true channel:{" + gradient_id + ":color.B}")


def star_grads(mag_id, col_id, lower, upper):
    csvreader = csv.reader(open(csv_path, 'rb'))
    count = 0

    for row in csvreader:

        if row[6] == "proper":

            pass

        elif float(upper) > float(row[14]) > float(lower):

            count += 1
            magnitude_key(count, row[14], mag_id)
            spectral_key(count, row[15], col_id)


# noinspection PyArgumentList
def new_blob(name, csv_id, size=0.01, rand_size=0.0001, input_type="particleID"):
    """
    Creates a new Blob with a preset Input type and Shader Effect.
    :param name: What to call the Blob after its creation.
    :param input_type: The Input type of the Gradient. Usually incidence or particleID
    :return: list
    """
    pyModo.Blob_Add_New()
    blob_id = pyModo.Blob_ID_Selected()[0]
    lx.eval("item.name %s blob" % name)
    lx.eval("volume.sizeInput %s" % input_type)
    lx.eval("volume.particle %s" % csv_id)
    lx.eval("item.channel blob$glDisplay false")
    lx.eval("item.channel blob$radius %s" % size)
    lx.eval("item.channel blob$sizeRand %s" % rand_size)

    return blob_id

# noinspection PyArgumentList
def new_csv_cache(name, path, size=1.0):
    """
    Creates a new CSV Cache with a preset Input type and Shader Effect.
    :param name: What to call the Cache after its creation.
    :return: list
    """
    pyModo.CSV_Point_Cache_Add_New()
    csv_id = pyModo.CSV_Point_Cache_ID_Selected()[0]
    lx.eval("item.name %s csvCache" % name)
    lx.eval("item.channel csvCache$seqType still")
    lx.eval("item.channel csvCache$glSize %s" % size)
    lx.eval("item.channel csvCache$filePattern %s" % path)
    return csv_id


def new_group(name, parent, position):
    pyModo.Group_Add_New()
    group_id = pyModo.Group_ID_Selected()[0]
    lx.eval("item.name %s mask" % name)
    lx.eval("texture.parent %s %s" % (parent, position))

    return group_id

def new_blob_group(blob_name):
    lx.eval("select.Item Stars")
    pyModo.Group_Add_New()
    group_id = pyModo.Group_ID_Selected()[0]
    lx.eval("mask.setMesh %s" % blob_name)
    lx.eval("shader.create advancedMaterial")
    lx.eval("item.channel advancedMaterial$diffAmt 0.0")
    lx.eval("item.channel advancedMaterial$specAmt 0.0")

    return group_id

# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
# noinspection PyArgumentList



def main():
    lx.eval("select.drop item")
    meshes = pyModo.Scene_Get_Item_Names_All()

    mag_m4 = False
    mag_m6 = False
    mag_m8 = False
    mag_m10 = False

    col_m4 = False
    col_m6 = False
    col_m8 = False
    col_m10 = False

    blob_m4 = False
    blob_m6 = False
    blob_m8 = False
    blob_m10 = False

    csv_m4 = False
    csv_m6 = False
    csv_m8 = False
    csv_m10 = False

    main_group = False

    csv_m4_id = new_csv_cache("m4_stars_csv_cache", cache_m4_path, 1.0)
    csv_m6_id = new_csv_cache("m6_stars_csv_cache", cache_m6_path, 0.75)
    csv_m8_id = new_csv_cache("m8_stars_csv_cache", cache_m8_path, 0.5)
    csv_m10_id = new_csv_cache("m10_stars_csv_cache", cache_m10_path, 0.25)

    blob_m4_id = new_blob("m4_stars_blobs", csv_m4_id, 20.0, 0.0)
    blob_m6_id = new_blob("m6_stars_blobs", csv_m6_id, 10.0)
    blob_m8_id = new_blob("m8_stars_blobs", csv_m8_id, 6.0)
    blob_m10_id = new_blob("m10_stars_blobs", csv_m10_id, 5.0)

    main_group_id = new_group("Stars", "Render", 2)
    lx.eval("shader.create defaultShader")
    lx.eval("item.channel indType none")
    lx.eval("item.channel shadCast false")
    lx.eval("item.channel shadRecv false")
    lx.eval("item.channel visInd false")
    lx.eval("item.channel visOccl false")

    group_m4_id = new_blob_group("m4_stars_blobs")
    mag_m4_id = new_gradient("Star_Magnitude_M4", "lumiAmount")
    lx.eval("shader.create constant")
    lx.eval("shader.setEffect lumiAmount")
    lx.eval("texture.name M4_Multiplier")
    lx.eval("item.channel textureLayer$blend multiply")
    col_m4_id = new_gradient("Star_Color_M4", "lumiColor")

    group_m6_id = new_blob_group("m6_stars_blobs")
    mag_m6_id = new_gradient("Star_Magnitude_M6", "lumiAmount")
    lx.eval("shader.create constant")
    lx.eval("shader.setEffect lumiAmount")
    lx.eval("texture.name M6_Multiplier")
    lx.eval("item.channel textureLayer$blend multiply")
    lx.eval("item.channel constant$value 0.5")
    col_m6_id = new_gradient("Star_Color_M6", "lumiColor")

    group_m8_id = new_blob_group("m8_stars_blobs")
    mag_m8_id = new_gradient("Star_Magnitude_M8", "lumiAmount")
    lx.eval("shader.create constant")
    lx.eval("shader.setEffect lumiAmount")
    lx.eval("texture.name M8_Multiplier")
    lx.eval("item.channel textureLayer$blend multiply")
    lx.eval("item.channel constant$value 20.0")
    col_m8_id = new_gradient("Star_Color_M8", "lumiColor")

    group_m10_id = new_blob_group("m10_stars_blobs")
    mag_m10_id = new_gradient("Star_Magnitude_M10", "lumiAmount")
    lx.eval("shader.create constant")
    lx.eval("shader.setEffect lumiAmount")
    lx.eval("texture.name M10_Multiplier")
    lx.eval("item.channel textureLayer$blend multiply")
    lx.eval("item.channel constant$value 2000.0")
    col_m10_id = new_gradient("Star_Color_M10", "lumiColor")

    lx.eval("select.Item envMaterial010")
    lx.eval("item.channel envMaterial$type constant")
    lx.eval("item.channel envMaterial$zenColor {0.0 0.0 0.0}")

    lines = file_len(csv_path) - 1
    print(str(lines) + " lines in this file.")

    star_grads(mag_m4_id, col_m4_id, -100.0, 4.009)
    lx.out("Finished M4 class stars")

    star_grads(mag_m6_id, col_m6_id, 4.01, 6.009)
    lx.out("Finished M6 class stars")

    star_grads(mag_m8_id, col_m8_id, 6.01, 8.009)
    lx.out("Finished M8 class stars")

    star_grads(mag_m10_id, col_m10_id, 8.01, 100)
    lx.out("Finished M10 and above class stars")

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
        pass
