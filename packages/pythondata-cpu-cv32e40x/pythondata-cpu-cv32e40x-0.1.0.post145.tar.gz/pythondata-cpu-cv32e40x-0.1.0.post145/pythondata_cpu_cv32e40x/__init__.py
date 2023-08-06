import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post145"
version_tuple = (0, 1, 0, 145)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post145")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post19"
data_version_tuple = (0, 1, 0, 19)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post19")
except ImportError:
    pass
data_git_hash = "337529c353ad74cda2690263252bcdbcf95c79c8"
data_git_describe = "0.1.0-19-g337529c"
data_git_msg = """\
commit 337529c353ad74cda2690263252bcdbcf95c79c8
Merge: 45545c9 978641b
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Tue Feb 22 10:16:21 2022 +0100

    Merge pull request #450 from silabs-oivind/align_mpu_e40s_e40x
    
    Update MPU to support data access in instruction side. In preparation…

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
