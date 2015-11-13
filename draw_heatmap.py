import numpy as np
import os
import sys
from PIL import Image

MIN_LON, MIN_LAT = 0, 0
MAX_LAT, MAX_LON = 0, 0

X_SIZE = 100
Y_SIZE = 100

#pixelCoordinate = worldCoordinate * 2^zoomLevel
ZOOM_LEVEL = 1
MULTIPLIER = 1 ** ZOOM_LEVEL

class matrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.original = np.zeros((columns,rows))
        self.matrix = np.zeros((columns,rows))

    def load_data(self, fname):
        global MAX_LAT, MAX_LON, MIN_LAT, MIN_LON

        lat_list = []
        lon_list = []
        data= []
        
        with open(fname, "r") as f:
            for line in f:
                lat, lon, num_cases = line.split()

                lat = float(lat)
                lon = float(lon)

                lat_converted = self.convert_to_mapscale(lat)
                lon_converted = self.convert_to_mapscale(lon)
                
                lat_list.append(lat_converted)
                lon_list.append(lon_converted)
                data.append((lat_converted,lon_converted, num_cases))
        
        MIN_LON = min(lon_list)
        MIN_LAT = min(lat_list)

        print "data", data
        
        print "range lat", np.ptp(lat_list)
        print "range lon", np.ptp(lon_list)
        print "MIN_LAT", MIN_LAT
        print "MIN_LON", MIN_LON
        
        for element in data:
            print "In matrix index lat is", element[0]-MIN_LAT
            print "In matrix index lon is", element[1]-MIN_LON
            print "In matrix case_num is", element[2]
            print " ---- \n"
            
            self.set_matrix(element[0]-MIN_LAT, element[1]-MIN_LON, element[2])
            self.set_original(element[0]-MIN_LAT, element[1]-MIN_LON, element[2])
        


    def convert_to_mapscale(self, value):
        return round(value * MULTIPLIER)
    
    def set_matrix(self, x, y, val):
        self.matrix[x,y] = val

    def set_original(self, x, y, val):
        self.original[x,y] = val

    def set_cell(self, x, y):
        print "CURRENT X", x
        print "CURRENT Y", y
        print "----- \n"
        total = 0
        numUsed = 0
        
        xy_dist = range(-25,25)
        r_dist = 25
        
        for dx in xy_dist:
            for dy in xy_dist:
                if dx == 0 and dy ==0:
                    continue
                
                [u,v] = [x + dx, y + dy]

                if u < 0 or u > self.columns - 1: 
                    continue
                
                if v < 0 or v >self.rows - 1:
                    continue

                if np.sqrt(dx*dx + dy*dy) > r_dist:
                    continue
                
                if self.original[u,v] > 0:
                    total = total + self.original[u,v]
                    numUsed = numUsed + 1

        if numUsed == 0: 
            result = 0
        else:
            result = total/numUsed
        
        self.set_matrix(x,y, result)

def get_color(x, y, val):
    if val == 0:
        return (255,255,255,0)

    val = val.astype(np.int64)
    val = np.round(val, decimals = 0)
    
    colors = [
            (0, 0, 255),
            (0, 86, 255),
            (0, 127, 255),
            (0, 171, 255),
            (0, 213, 255),
            (0, 240, 255),
            (0, 255, 255),
            (0, 255, 0),
            (128, 255, 0),
            (176, 255, 0),
            (218, 255, 0),
            (255, 255, 0),
            (255, 240, 0),
            (255, 208, 0),
            (255, 171, 0),
            (255, 127, 0),
            (255, 91, 0),
            (255, 0, 0),
            ]

    return colors[val]
    

def main():
    if not len(sys.argv) == 2:
        print "Usage", sys.argv[0], "[FNAME]"
        sys.exit(0)

    fname = sys.argv[1]
        
    if not os.path.exists(fname):
        print "Could not find", sys.argv[1]
        sys.exit(0)

    m = matrix(X_SIZE,Y_SIZE)
    m.load_data(fname)
    
    im = Image.new('RGB', (X_SIZE, Y_SIZE))
    IM = im.load()

    for x in range(m.columns):
        for y in range(m.rows):
            if m.original[x,y] > 0:
                continue
            m.set_cell(x, y)
            
            IM[x,y] = get_color(x, y, m.matrix[x,y])

    im.show()
    
if __name__ == "__main__":
    main()
