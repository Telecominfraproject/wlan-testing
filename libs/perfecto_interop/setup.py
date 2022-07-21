import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='perfecto_interop',
    version='0.1',
    scripts=['android_lib.py', 'ios_lib.py'],
    author="Shivam Thakur",
    author_email="shivam.thakur@candelatech.com",
    description="TIP OpenWIFI Perfecto Test Automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
