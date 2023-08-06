from distutils.core import setup, Extension

setup(
    name = 'pyobjinfo',
    version = '1.0',
    description="Provides stats info about PyObject",
    author="Vladas Tamošaitis",
    author_email="amd.vladas@gmail.com",
    license="MIT",
    ext_modules = [
        Extension('pyobjinfo', ['obj_info.c'])
    ]
)
