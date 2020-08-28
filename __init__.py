import sys, os
sys.path.append(os.path.abspath(".."))

try:
  import google.colab
  sys.path.insert(0, "/content/Utilities")
except:
  pass

import utils