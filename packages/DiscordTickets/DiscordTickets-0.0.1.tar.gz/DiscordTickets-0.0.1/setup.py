from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A simple Discord Ticket bot package'
LONG_DESCRIPTION = 'Just a simple Discord Ticket bot package, nothing much!'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="DiscordTickets", 
        version=VERSION,
        author="Ian Cheung",
        author_email="support@ianbrawlstars.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)