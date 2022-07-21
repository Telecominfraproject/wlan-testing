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
# ######################################################################################################################
# """
#     Target Name:<Vendor-Package-Name>
#     Target Module:<Vendor-Package-Name-0.1>
#     Author Name:<Author Name>
#     Organization:<Vendor Organization Name>
#     Register ID:2
#     Email:shivam.thakur@candelatech.com
#     description:<Description of Library>
# """
# try:
#     target = importlib.import_module("tip_2x")
#     target = target.tip_2x
# except ImportError as e:
#     print(e)
#     sys.exit("Python Import Error: " + str(e))
# ######################################################################################################################
