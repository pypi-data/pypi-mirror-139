import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post143"
version_tuple = (0, 1, 0, 143)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post143")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post17"
data_version_tuple = (0, 1, 0, 17)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post17")
except ImportError:
    pass
data_git_hash = "45545c989be4654d1400ebcfead53d57fadbb941"
data_git_describe = "0.1.0-17-g45545c9"
data_git_msg = """\
commit 45545c989be4654d1400ebcfead53d57fadbb941
Merge: 80ee57d db21f94
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Tue Feb 22 08:13:20 2022 +0100

    Merge pull request #449 from Silabs-ArjanB/ArjanB_obiv13
    
    Updated to OBI v1.3

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
