import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post149"
version_tuple = (0, 1, 0, 149)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post149")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post23"
data_version_tuple = (0, 1, 0, 23)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post23")
except ImportError:
    pass
data_git_hash = "f612df5108bf8dd076a0804cc05ca30b9fb49f1f"
data_git_describe = "0.1.0-23-gf612df5"
data_git_msg = """\
commit f612df5108bf8dd076a0804cc05ca30b9fb49f1f
Merge: e6cce90 7ee7d65
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Wed Feb 23 12:32:36 2022 +0100

    Merge pull request #455 from Silabs-ArjanB/ArjanB_uie
    
    Removed obsolete bitfields

"""

# Tool version info
tool_version_str = "0.0.post126"
tool_version_tuple = (0, 0, 126)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post126")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
