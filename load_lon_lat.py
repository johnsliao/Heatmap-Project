# Loads in raw data, writes area codes to txt file

import numpy as np
import sys
import os

def load_long_lat(fname):
    usable_data = []
    num_orders = []
    count = 0
    
    with open(r"C:\temp\num_orders.txt", "r") as f:
        for line in f:
            num_orders.append(line.rstrip())
            
    with open(fname) as f:
        for line in f:            
            lat, lon = line.split(",")
            
            lon = lon.rstrip().strip() # fix formatting

            usable_data.append((lat, lon, num_orders[count]))
            count += 1

    with open(r"C:\temp\formatted_data.txt", "w") as f:
        for element in usable_data:
            f.write(element[0] + " ")
            f.write(element[1]+ " ")
            f.write(element[2] + "\n")

def main():
    if not len(sys.argv) == 2:
        print "Usage", sys.argv[0], "[FNAME]"
        sys.exit(0)

    fname = sys.argv[1]

    if not os.path.exists(fname):
        print "Could not find", fname
        sys.exit(0)
    
    load_long_lat(fname)
    
if __name__ == '__main__':
    main()
