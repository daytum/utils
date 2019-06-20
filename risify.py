#!/usr/bin/env python

import sys
import os
import json
import subprocess


filename = sys.argv[-1]

basename = os.path.basename(filename).split(".")[0]


with open(sys.argv[-1], "r+") as f:

    data = json.load(f)

    # Add rise metadata if it does not exist

    data["metadata"]["rise"] = {
        "footer": "<img src='https://github.com/daytum/logos/blob/master/daytum_logo_2019.png?raw=true' width='220'>",
        "progress": True,
        "scroll": True,
        "theme": "simple",
        "slideNumber": False,
        "auto_select": None,
        "enable_chalkboard": False,
        "controls": True,
    }

    # Can be changed to True if you wish the slides to autolaunch
    if basename != "index":
        data["metadata"]["rise"]["autolaunch"] = False

    new_cell_list = []
    for cell in data["cells"]:

        # Again, switch to True if you want to hide *all* code cells
        if "code" in cell:
            if "metadata" not in cell:
                cell["metadata"] = {}
                cell["metadata"]["hide_input"] = False

        # If there is a javascript last cell already in the group of cells, exclude
        # it from the new list we are constructing, because we are going to add it to
        # the end next.
        if "javascript_last_cell" not in cell["metadata"]:
            new_cell_list += [cell]

    # Construct our last cell which we will embed javascript into the remove the In/Out tags
    # from the notebook.
    hide_cell = {
        "cell_type": "code",
        "metadata": {
            "hide_input": True,
            "init_cell": True,
            "javascript_last_cell": True,
        },
        "execution_count": 0,
        "outputs": [],
        "source": [
            """%%javascript
function hideElements(elements, start) {
for(var i = 0, length = elements.length; i < length;i++) {
    if(i >= start) {
        elements[i].style.display = \"none\";
    }
}
}
var prompt_elements = document.getElementsByClassName(\"prompt\");
hideElements(prompt_elements, 0)"""
        ],
    }

    # Add the hide_cell code to the end.
    new_cell_list += [hide_cell]

    data["cells"] = new_cell_list

    f.seek(0)
    json.dump(data, f)
    f.truncate()

os.system("jupyter trust " + sys.argv[-1])
