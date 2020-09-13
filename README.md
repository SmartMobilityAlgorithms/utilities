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
└─── viz.py ==> We had a problem; ipyleaflet can't run on google colab but it was so good to be ditched for folium
                which is OK and can be run on google colab but we couldn't resist the desire for you to see ipyleaflet in action
                on your local machine.
                
                So, this module knows when you are running local (with if statement) and would use ipyleaflet for visualization
                and if you are running on the cloud it would be using folium, all for the same name of function so you don't
                have to worry about anything - just call the same function and let us worry about all that local/cloud stuff.
```

# Usage

If you are on a local machine you don't have to worry about anything at all, just make sure you installed everything on [Getting Started](https://github.com/SmartMobilityAlgorithms/GettingStarted).

If you are on google colab, just upload the `.zip` file that is present in every repository to the default directory and everything would supposedly be fine.

**If not**, don't hesitate for a second to open an issue here and we would go through the steps with you, you are here to learn search algorithms, not how to use package managers :computer: :computer:.
