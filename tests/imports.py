"""
Registered Target Imports
"""
import sys
import importlib

sys.path.append('/usr/local/bin')

sys.path.append('/home/imgd/.local//bin/')

sys.path.append('/home/imgd/.local/lib/python3.8/site-packages/')


########################################################################################################################
"""
    Target Name:tip_2x
    Author Name:Saurabh
    Organization:TIP
    Register ID:1
    Email:saurabh.goyal@candelatech.com
    description:TIP OpenWIFI 2.X Library
"""

try:
    target = importlib.import_module("tip_2x")
    target = target.tip_2x
except ImportError as e:
    print(e)
    sys.exit("Python Import Error: " + str(e))

########################################################################################################################
########################################################################################################################
"""
    Target Name:lanforge_scripts
    Author Name:Saurabh
    Organization:TIP
    Register ID:2
    Email:saurabh.goyal@candelatech.com
    description:Candela LANforge Based Library
"""

try:
    lanforge_libs = importlib.import_module("lanforge_scripts.lf_libs.lf_libs")
    lf_libs = lanforge_libs.lf_libs
    scp_file = lanforge_libs.SCP_File
    lanforge_tests = importlib.import_module("lanforge_scripts.lf_libs.lf_tests")
    lf_tests = lanforge_tests.lf_tests
except ImportError as e:
    print(e)
    sys.exit("Python Import Error: " + str(e))

########################################################################################################################
########################################################################################################################
"""
    Target Name:perfecto_interop
    Author Name:Saurabh
    Organization:TIP
    Register ID:2
    Email:saurabh.goyal@candelatech.com
    description:Perfecto Based Interop Library
"""

try:
    perfecto_interop = importlib.import_module("perfecto_interop")
    android_tests = perfecto_interop.android_tests
    ios_tests = perfecto_interop.ios_tests
except ImportError as e:
    print(e)
    sys.exit("Python Import Error: " + str(e))

########################################################################################################################
