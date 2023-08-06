import inspect
import sys, os
from pathlib import Path
from pprint import pprint
from traceback import print_exc

try:
    main_path = Path(inspect.getfile(sys.modules.get("__main__")))
    if os.path.exists(main_path.parent / "maxoptics.conf"):
        __CONFIGPATH__ = main_path.parent / "maxoptics.conf"
    elif os.path.exists(main_path.parent.parent / "maxoptics.conf"):
        __CONFIGPATH__ = main_path.parent.parent / "maxoptics.conf"
    elif os.path.exists(main_path.parent.parent.parent / "maxoptics.conf"):
        __CONFIGPATH__ = main_path.parent.parent.parent / "maxoptics.conf"
    else:
        ind = list(sys.modules.keys()).index("maxoptics")
        secondary_path = Path(inspect.getfile(list(sys.modules.values())[ind - 1]))
        if os.path.exists(secondary_path.parent / "maxoptics.conf"):
            __CONFIGPATH__ = secondary_path.parent / "maxoptics.conf"
        elif os.path.exists(secondary_path.parent.parent / "maxoptics.conf"):
            __CONFIGPATH__ = secondary_path.parent.parent / "maxoptics.conf"
        elif os.path.exists(secondary_path.parent.parent.parent / "maxoptics.conf"):
            __CONFIGPATH__ = secondary_path.parent.parent.parent / "maxoptics.conf"
        else:
            __CONFIGPATH__ = ''

except AttributeError:
    print("Warning: No __main__ modules found, using the default configuration")
    __CONFIGPATH__ = ""

except TypeError:
    print("Warning: No __main__ modules found, using the default configuration")
    __CONFIGPATH__ = ""

# Version Number
__VERSION__ = "0.5.2"


class MosLibrary:
    def __new__(cls, **kws):
        from .sdk import MaxOptics

        cls.mos_instance = MaxOptics(**kws)
        return cls.mos_instance
