import os
from os import path
import sys
import shutil

if len(sys.argv) < 2 or not path.isdir(sys.argv[1]):
  print('usage: main.py <top directory> -run')
  sys.exit(1)

topdir = sys.argv[1]
run = len(sys.argv) > 2 and sys.argv[2] == '-run'

if run:
  print('Warning: actually deleting directories')
else:
  print('Dry run: printing directories that would be deleted')

for root, dirs, files in os.walk(topdir, topdown=False):
  found_opf = False
  found_other = False
  for name in files:
    if name.endswith('.opf'):
      found_opf = True
    else:
      found_other = True
  if found_opf and not found_other:
    if run:
      shutil.rmtree(root)
    else:
      print(root)
