from setuptools import setup, find_namespace_packages


setup(
    name='clean_folder',
    version='0.0.3',
    packages=['clean_folder'],
    author='ShaTa',
    description='Clean folder from',
    entry_points={
        'console_scripts':['clean-folder = clean_folder.clean:main']
    }
)