# Utilities

This is behind the scenes for all the repositories and code in the book.

---

Here is the general structure and where to look at if you want to see what is happening

```
utils
│       
└─── common.py ==> This module is here for providing a nice interface to unnecessary complexity,
|                  like handling graphs produced from osmnx and other utilities associated with
│                  graphs.
│ 
│
└─── problem.py ==> This module is for problem-specific utilities like the heuristic functions 
│                   or data structures used in algorithms
│ 
│
│
└─── jupyter.py ==> This module is for handling the quirks of jupyter notebook without 
│                   polluting the notebook with distracting commands and functions
│ 
│ 
│ 
│  
└─── viz.py ==> Wrapper around `folium` and `ipyleaflet` to ease visualization and choose the appropriate 
                library for visulaization based on the size of the graph and the environment the notebook
                running at.
```

# Usage

If you are on a local machine you don't have to worry about anything at all, just make sure you installed everything on [Getting Started](https://github.com/SmartMobilityAlgorithms/GettingStarted).

If you are on google colab, just upload the `.zip` file that is present in every repository to the default directory and everything would supposedly be fine.

**If not**, don't hesitate for a second to open an issue here and we would go through the steps with you, you are here to learn search algorithms, not how to use package managers :computer: :computer:.
