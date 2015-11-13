# Loads in raw data, writes area codes to txt file

import numpy as np
import sys
import os

def load_CA_zipcodes():
    CA_zipcodes = []
    
    with open(r"C:\temp\ca_zipcodes.txt", "r") as f:
        for line in f:
            CA_zipcodes.append(line.rstrip())
            print line.rstrip()

    return CA_zipcodes

def is_CA_zipcode(input_zip, CA_zipcodes):
    for CA_zipcode in CA_zipcodes:
        if input_zip == CA_zipcode:
            return True
        
    return False    

def load_raw_data(fname):
    raw_data = []
    
    zip_count = 1
    previous_zip_code = 0

    CA_zipcodes = load_CA_zipcodes()

    with open(fname) as f:
        for line in f:  
            item_num, zip_code, tooth = line.split(",")

            item_num = item_num.replace(r'"',"")
            zip_code = zip_code.replace(r'"',"")
            tooth = tooth.replace(r'"',"")
         
            if not item_num.isdigit():
                continue

            if zip_code == "":
                continue

            if not zip_code.isdigit():
                continue
            
            if not is_CA_zipcode(zip_code, CA_zipcodes): # only CA zip codes
                continue

            if not previous_zip_code == zip_code and  not previous_zip_code == 0:
                raw_data.append((previous_zip_code, zip_count))
                zip_count = 1

            if previous_zip_code == zip_code:
                zip_count += 1

            previous_zip_code = zip_code

    with open(r"C:\temp\zipcodes.txt", "w") as f:
        for pair in raw_data:
            f.write(pair[0] + "\n")

    with open(r"C:\temp\num_orders.txt", "w") as f:
        for pair in raw_data:
            f.write(str(pair[1]) + "\n")

def main():
    if not len(sys.argv) == 2:
        print "Usage", sys.argv[0], "[FNAME]"
        sys.exit(0)

    fname = sys.argv[1]

    if not os.path.exists(fname):
        print "Could not find", fname
        sys.exit(0)
    
    load_raw_data(fname)
    
if __name__ == '__main__':
    main()
