import sys, os
sys.path.append("../utils")

try:
  import google.colab
  sys.path.insert(0, "/content/Utilities")
except:
  pass

from .utils import *
