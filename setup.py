from setuptools import setup, Extension

sfc_module = Extension('TestDLL', sources = ['module.cpp'])

setup(
    name='TestDLL',
    version='1.1',
    description='C++ extension',
    ext_modules=[sfc_module]
)