#!/usr/bin/env python

from setuptools import setup, find_packages

from setuptools.command.install import install

class my_install(install):
    def run(self):
        print '=== pre-install ==='
        install.run(self)
        print '=== post-install ==='

'''
In order to use MANIFEST.in to include/exclude files,
we must put the folder of include/exclude files to find_packages(exclude=['somefolder']) list (so these files are considered data files)
any files not in the exclude list are considered source code and cannot be controlled by MANIFEST.in

about find_packages(exclude=['somefolder']):
exclude=['app.web.*'] will remove subfolders in app/web/ but not web/app/*.py
'''
setup(
    name = "mylib", # required
    version = 0.1, # required
    packages = find_packages(exclude=['tests']), # required
    #include_package_data = True, # if wish to manage data files thru MANIFEST.in, set include_package_data = True
    cmdclass={'install': my_install},
)

