from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['workshop'],
    scripts=['scripts/sub_node.py', 'scripts/camera_stream.py'],
    package_dir={'': 'src'}
)

setup(**d)
