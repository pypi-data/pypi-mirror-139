__author__ = "Vanessa Sochat, Alec Scott"
__copyright__ = "Copyright 2021-2022, Vanessa Sochat and Alec Scott"
__license__ = "Apache-2.0"

import importlib
import pkgutil

# A paks plugin (a pakage) can be discovered via install OR used on demand
# given that the user has dependencies needed installed.

installed_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg in pkgutil.iter_modules()
    if name.startswith("pakage_")
}
