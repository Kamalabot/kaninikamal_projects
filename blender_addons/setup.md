Set interpreter in VS Code

Open Command Palette → Python: Select Interpreter.

Choose Blender’s bundled Python.

C:\Program Files\BlenderFoundation\Blender4.5\4.5\python\bin\python.exe

Install BPY Module for 4.5

pip install fake-bpy-module-4.5 (doesn't work)

Adding the below to settings.json

"python.analysis.extraPaths": [
        "C:\\Program Files\\BlenderFoundation\\Blender4.5\\4.5\\python\\bin\\scripts\\modules"
    ],

Accessing settings.json from File -> Preferences -> Settings -> JSON mode (at the top)

Suggested Folder Structure for Blender Projects

blender_addons/
│── hello_blender/                # your addon
│   ├── __init__.py               # entry point
│   ├── operators.py              # custom ops
│   ├── ui.py                     # panels
│   └── utils.py                  # helper functions
│── experiments/                  # one-off scripts
│   ├── spiral.py
│   ├── graph.py
│   └── bouncing_ball.py

Best way to execute the python script in Blender is with Blender Development addon

In Blender:  Edit -> Preferences -> Save & Load -> Allow "Auto Run python scripts"