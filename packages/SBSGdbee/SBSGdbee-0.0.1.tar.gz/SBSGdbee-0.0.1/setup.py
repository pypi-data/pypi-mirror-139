from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Package for interfacing with the SBSG database'

# Setting up
setup(
    name="SBSGdbee",
    version=VERSION,
    author="Alex Perkins (SBSG UoE)",
    author_email="a.j.p.perkins@sms.ed.ac.uk",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'pandas'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
