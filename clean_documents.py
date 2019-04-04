import os
import sys
import re

if len(sys.argv)<3:
    print("Script to remove all non alphanumeric characters")
    print("invalid arguments:")
    print("python %s input_directory output_directory"%(sys.argv[0]))
input_dir = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.exists(output_dir):
    os.path.makedirs(output_dir)

for f in os.listdir(input_dir):
    if not f.endswith("txt"):
        continue
    fw = open(os.path.join(output_dir,f),"w")
    for l in open(os.path.join(input_dir,f)):
        fw.write(re.sub(r'[^a-zA-Z0-9_ ]+', '', l))
    fw.close()

