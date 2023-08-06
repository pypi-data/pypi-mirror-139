# About
**scriptbox** is a collection of small utilities for everyday tasks.
As development is still in very early stages, **scriptbox** has only one utility
to introduce - **screencapture**, for taking screenshots. More utilities are
coming in the future, however, as I get them done.

# Installation
You should install **scriptbox** by installing it with a specific
python interpreter, like below.

``` bash
python3.10 -m pip install scriptbox
```

# Usage
To use any of the programs, you can simply invoke their name, as described below
in the section `Command`. However, to create a keybinding to invoke any of the
utilities (in i3 config, for example), you need to provide full path to a
utility, as `Default path` describes. Note that the path might vary, depending
where **pip** installs the utilities, so make sure to check it with `which
<utility name>` against any of the utilities, to get the correct path.

| Program       | Command        | Default path               |
| :-----------: | :------------: | :------------------------: |
| screencapture | screencapture  | ~/.local/bin/screencapture |

# Requirements
| Requirement   | Note           | Caveat                  |
| :-----------: | :------------: | :---------------------: |
| Python        | 3.10           |                         |
| OS            | MacOS, Linux   | Not tested on OSX (yet) |
