#!/usr/bin/env python

from setuptools import setup, find_packages

from setuptools.command.install import install

class my_install(install):
    def run(self):
        print '=== pre-install ==='
        install.run(self)
        print '=== post-install ==='

setup(
    name = "mylib", # required
    version = 0.1, # required
    packages = find_packages(), # required
    #include_package_data = True, # if use MANIFEST.in
    cmdclass={'install': my_install},
)

