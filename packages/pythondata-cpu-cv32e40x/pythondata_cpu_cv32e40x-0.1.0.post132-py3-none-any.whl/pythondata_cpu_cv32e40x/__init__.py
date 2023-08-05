import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post132"
version_tuple = (0, 1, 0, 132)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post132")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post6"
data_version_tuple = (0, 1, 0, 6)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post6")
except ImportError:
    pass
data_git_hash = "f62adb348140ec9f449e9d1ffab216a5b1058e40"
data_git_describe = "0.1.0-6-gf62adb3"
data_git_msg = """\
commit f62adb348140ec9f449e9d1ffab216a5b1058e40
Merge: ae8cce6 e289b7a
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Thu Feb 17 16:02:22 2022 +0100

    Merge pull request #443 from Silabs-ArjanB/ArjanB_clku
    
    Removed unused clock signal

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
