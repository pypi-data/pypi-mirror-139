import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post128"
version_tuple = (0, 1, 0, 128)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post128")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post2"
data_version_tuple = (0, 1, 0, 2)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post2")
except ImportError:
    pass
data_git_hash = "35944de48a0fe8de162bdccac707389aca955aaa"
data_git_describe = "0.1.0-2-g35944de"
data_git_msg = """\
commit 35944de48a0fe8de162bdccac707389aca955aaa
Merge: 380b9fd 223b014
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Thu Feb 17 09:00:53 2022 +0100

    Merge pull request #441 from silabs-halfdan/parameterized_clic_id
    
    Parameterized width of CLIC clic_irq_id_i, clic_irq_id_o signals.

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
