"""
    Registered Target Imports

"""
import sys
import importlib

sys.path.append('/usr/local/bin')
########################################################################################################################
"""
    Target Name:tip_2x
    Target Module:tip-2x-0.1
    Author Name:Shivam Thakur
    Organization:Telecom Infra Project
    Register ID:1
    Email:shivam.thakur@candelatech.com
    description:TIP OpenWIFI 2.X Library
"""
try:
    target = importlib.import_module("tip_2x")
    target = target.tip_2x
except ImportError as e:
    print(e)
    sys.exit("Python Import Error: " + str(e))
########################################################################################################################
# ########################################################################################################################
# """
#     Target Name:LANforge Traffic Generator Library
#     Target Module:lanforge-scripts-0.0.1
#     Author Name:Shivam Thakur
#     Organization:Candela Technologies
#     Register ID:2
#     Email:support@candelatech.com
#     description:Libraries specific to Candela Wifi Test Automation
# """
# try:
#     lanforge_scripts = importlib.import_module("lanforge_scripts")
#     lf_libs = lanforge_scripts.lf_libs
# except ImportError as e:
#     print(e)
#     sys.exit("Python Import Error: " + str(e))
# ########################################################################################################################
########################################################################################################################
"""
    Target Name:Perforce Interop Library
    Target Module:perfecto-interop-0.0.1
    Author Name:Sushant Bawiskar
    Organization:Perforce
    Register ID:3
    Email:support@candelatech.com
    description:Libraries specific to Interop Wifi Test Automation with Perfecto
"""
try:
    perfecto_interop = importlib.import_module("perfecto_interop")
    perfecto_libs = perfecto_interop.perfecto_libs
except ImportError as e:
    print(e)
    sys.exit("Python Import Error: " + str(e))
########################################################################################################################
