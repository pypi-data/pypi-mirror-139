import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post141"
version_tuple = (0, 1, 0, 141)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post141")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post15"
data_version_tuple = (0, 1, 0, 15)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post15")
except ImportError:
    pass
data_git_hash = "80ee57d367deb1da4c086a4d97f0e8c40dc2878b"
data_git_describe = "0.1.0-15-g80ee57d"
data_git_msg = """\
commit 80ee57d367deb1da4c086a4d97f0e8c40dc2878b
Merge: fa83afb 760e647
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Mon Feb 21 10:18:13 2022 +0100

    Merge pull request #447 from silabs-oivind/pma_rename_doc
    
    Rename pma_region_t -> pma_cfg_t in documentation

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
