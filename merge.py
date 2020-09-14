from collections import namedtuple
import os
from os import path
import re
import sys
import shutil

from lxml import etree

# ((?P<series>[^_0-9-]*)\[(?P<series_index>[0-9]*)\])?\s*(?P<title>[^_].+)-\s*(?P<author>[^_-]+)?

BASE_SERIES_PATH = os.path.join('output', 'series')
BASE_NON_SERIES_PATH = os.path.join('output', 'non_series')
RE_SERIES = re.compile(r'([^_0-9-]+) \[(\d+)\] ([^_0-9-]+)')
Metadata = namedtuple('Metadata', ['author', 'title', 'series', 'series_index'])

def process_opf(filename):
  with open(filename) as f: 
    root = etree.parse(f).getroot()

  metadata = root.find('.//{http://www.idpf.org/2007/opf}metadata')
  title = metadata.find('{http://purl.org/dc/elements/1.1/}title').text
  author = metadata.find('{http://purl.org/dc/elements/1.1/}creator').text
  series = None
  index = None

  md = RE_SERIES.match(title)
  if md:
    series = md.group(1)
    index = md.group(2)
    title = md.group(3)

  return Metadata(author, title, series, index)


if len(sys.argv) < 2 or not path.isdir(sys.argv[1]):
  print('usage: merge.py <top directory> -run')
  sys.exit(1)

topdir = sys.argv[1]

for root, dirs, files in os.walk(topdir, topdown=False):
  metadata = None
  for name in files:
    if name.endswith('.opf'):
      metadata = process_opf(os.path.join(root, name))
  if metadata:
    frag = os.path.join(os.path.basename(os.path.normpath(os.path.join(root, '../..'))),
                        os.path.basename(os.path.normpath(os.path.join(root, '..'))),
                        os.path.basename(root))
    if metadata.series:
      out = os.path.join(BASE_SERIES_PATH, frag)
    else:
      out = os.path.join(BASE_NON_SERIES_PATH, frag)
    shutil.copytree(root, out)