#!/usr/bin/env python
# encoding: utf-8
# Alexander Kucera
# babylondreams.de

# Description
"""

Release Notes:

V0.1 Initial Release

"""

import csv
import traceback

csv_path = "/Users/alex/Downloads/15-06-14/hygdata_v3.csv"
csv_format = ","
distance_type = "_med"

# Different particle sets based on absolute magnitude
csv_particles_m4 = "/Users/alex/Downloads/15-06-14/hygdata_v3_particles_m4" + \
                   distance_type + ".csv"
csv_particles_m6 = "/Users/alex/Downloads/15-06-14/hygdata_v3_particles_m6" + \
                   distance_type + ".csv"
csv_particles_m8 = "/Users/alex/Downloads/15-06-14/hygdata_v3_particles_m8" + \
                   distance_type + ".csv"
csv_particles_m10 = "/Users/alex/Downloads/15-06-14/hygdata_v3_particles_m10" + \
                   distance_type + ".csv"

# Maximum distance possible in modo normalized to the largest distance in the star catalogue
if distance_type == "_med":
    precision_limit = 100000 * 1000  # 1999999999000000
else:
    precision_limit = 100000  # 1999999999000000

largest_distance = 99996.065513
max_number = 1 / largest_distance * precision_limit

# FUNCTIONS -----------------------------------------------

def file_len(fname):
    with open(fname) as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i + 1


# END FUNCTIONS -----------------------------------------------

# MAIN PROGRAM --------------------------------------------
def main():
    lines = file_len(csv_path) - 1
    print(str(lines) + " lines in this file.")

    csvreader = csv.reader(open(csv_path, 'rb'))

    with open(csv_particles_m4, 'w') as csvwriter:
        csvwriter.write("ptcl.id, ptcl.pos.X, ptcl.pos.Y, ptcl.pos.Z, ptcl.vel.X, "
                        "ptcl.vel.Y, ptcl.vel.Z, ptcl.age\n")
        count = 0
        for row in csvreader:

            if row[6] == "proper" or row[6] == "Sol":
                pass
            elif float(row[14]) < 4.01:
                count += 1
                x = str(float(row[17]) * max_number)
                y = str(float(row[18]) * max_number)
                z = str(float(row[19]) * max_number)
                csvwriter.write(str(count) + ", " + x + ", " + y + ", " + z +
                                ", 0.0, 0.0, 0.0, 1.0\n")
            else:
                pass

    csvreader = csv.reader(open(csv_path, 'rb'))

    with open(csv_particles_m6, 'w') as csvwriter:
        csvwriter.write("ptcl.id, ptcl.pos.X, ptcl.pos.Y, ptcl.pos.Z, ptcl.vel.X, "
                        "ptcl.vel.Y, ptcl.vel.Z, ptcl.age\n")
        count = 0
        for row in csvreader:

            if row[6] == "proper" or row[6] == "Sol":
                pass
            elif 6.01 > float(row[14]) > 4.01:
                count += 1
                x = str(float(row[17]) * max_number)
                y = str(float(row[18]) * max_number)
                z = str(float(row[19]) * max_number)
                csvwriter.write(str(count) + ", " + x + ", " + y + ", " + z +
                                ", 0.0, 0.0, 0.0, 1.0\n")
            else:
                pass

    csvreader = csv.reader(open(csv_path, 'rb'))

    with open(csv_particles_m8, 'w') as csvwriter:
        csvwriter.write("ptcl.id, ptcl.pos.X, ptcl.pos.Y, ptcl.pos.Z, ptcl.vel.X, "
                        "ptcl.vel.Y, ptcl.vel.Z, ptcl.age\n")
        count = 0
        for row in csvreader:

            if row[6] == "proper" or row[6] == "Sol":
                pass
            elif 8.01 > float(row[14]) > 6.01:
                count += 1
                x = str(float(row[17]) * max_number)
                y = str(float(row[18]) * max_number)
                z = str(float(row[19]) * max_number)
                csvwriter.write(str(count) + ", " + x + ", " + y + ", " + z +
                                ", 0.0, 0.0, 0.0, 1.0\n")
            else:
                pass

    csvreader = csv.reader(open(csv_path, 'rb'))

    with open(csv_particles_m10, 'w') as csvwriter:
        csvwriter.write("ptcl.id, ptcl.pos.X, ptcl.pos.Y, ptcl.pos.Z, ptcl.vel.X, "
                        "ptcl.vel.Y, ptcl.vel.Z, ptcl.age\n")
        count = 0
        for row in csvreader:

            if row[6] == "proper" or row[6] == "Sol":
                pass
            elif float(row[14]) > 8.01:
                count += 1
                x = str(float(row[17]) * max_number)
                y = str(float(row[18]) * max_number)
                z = str(float(row[19]) * max_number)
                csvwriter.write(str(count) + ", " + x + ", " + y + ", " + z +
                                ", 0.0, 0.0, 0.0, 1.0\n")
            else:
                pass

# END MAIN PROGRAM -----------------------------------------------

if __name__ == '__main__':
    try:

        main()

    except Exception, e:
        traceback.print_exc()
