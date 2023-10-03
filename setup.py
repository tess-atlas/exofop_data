from setuptools import setup, find_packages





setup(
    name='exofop_data',
    version='0.1',
    description='A TESS-Atlas utility for querying ExoFOP data and checking which targets have 2-minute cadence data available.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['tess-atlas'],
)
