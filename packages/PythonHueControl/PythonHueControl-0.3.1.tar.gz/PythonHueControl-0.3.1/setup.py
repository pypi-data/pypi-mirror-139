from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='PythonHueControl',
    version='0.3.1',
    packages=['pythonhuecontrol', 'pythonhuecontrol.v1', 'pythonhuecontrol.v1.rule', 'pythonhuecontrol.v1.group',
              'pythonhuecontrol.v1.light', 'pythonhuecontrol.v1.scene', 'pythonhuecontrol.v1.bridge',
              'pythonhuecontrol.v1.sensor', 'pythonhuecontrol.v1.schedule', 'pythonhuecontrol.v2'],
    package_dir={'': '.'},
    url='https://github.com/elnkosc/PythonHueControl',
    license='GPL',
    author='Koen',
    author_email='koen@schilders.org',
    description='Feature Rich Python API for Hue V1 and V2',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
