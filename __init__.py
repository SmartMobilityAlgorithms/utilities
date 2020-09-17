import sys

try:
  import google.colab
  sys.path.insert(0, "/content/Utilities")
except:
  pass

from .src import *
