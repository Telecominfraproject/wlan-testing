import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='dut_lib_template',
    version='0.1',
    scripts=['tip_2x.py', 'controller.py', 'ap_lib.py', 'SetupLibrary.py', 'openwrt_ctl.py'],
    author="Shivam Thakur",
    author_email="shivam.thakur@candelatech.com",
    description="TIP OpenWIFI 2.X Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
