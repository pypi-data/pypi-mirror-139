from setuptools import setup

__project__ = 'window_maker'
__version__ = '0.0.1'
__description__ = 'a python module which you can easy make windows'
__packages__ = ['window']
__requires__ = ['tkinter']

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    requires = __requires__
)
