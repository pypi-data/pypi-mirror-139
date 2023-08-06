from setuptools import setup

def readme():
    with open('pythonhuecontrol/readme.md') as f:
        return f.read()

setup(
    name='PythonHueControl',
    version='0.3.3',
    packages=['pythonhuecontrol', 'pythonhuecontrol.v1', 'pythonhuecontrol.v1.rule', 'pythonhuecontrol.v1.group',
              'pythonhuecontrol.v1.light', 'pythonhuecontrol.v1.scene', 'pythonhuecontrol.v1.bridge',
              'pythonhuecontrol.v1.sensor', 'pythonhuecontrol.v1.schedule', 'pythonhuecontrol.v2'],
    package_dir={'': '.'},
    url='https://github.com/elnkosc/PythonHueControl',
    license='GPL',
    author='Koen',
    author_email='koen@schilders.org',
    description='Feature Rich Python API for Hue V1 and V2',
    long_description=readme(),
    long_description_content_type='text/markdown'
)
