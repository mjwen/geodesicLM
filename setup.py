import os
from setuptools import find_packages
from numpy.distutils.core import setup, Extension


def get_version(fname=os.path.join('geodesicLM', '__init__.py')):
    with open(fname) as fin:
        for line in fin:
            line = line.strip()
            if '__version__' in line:
                v = line.split('=')[1]
                # stripe white space, and ' or " in string
                if "'" in v:
                    version = v.strip("' ")
                elif '"' in v:
                    version = v.strip('" ')
                break
    return version


geolm_f = Extension(
    'geodesicLM._geodesiclm',
    sources=[
        'geodesicLM/geodesiclm.pyf',
        'geodesicLM/accept.f90',
        'geodesicLM/fdavv.f90',
        'geodesicLM/fdjac.f90',
        'geodesicLM/lambda.f90',
        'geodesicLM/geodesiclm.f90',
        'geodesicLM/updatejac.f90',
        'geodesicLM/converge.f90',
        'geodesicLM/dpmpar.f',
        'geodesicLM/dgqt.f',
        'geodesicLM/destsv.f',
    ],
    extra_compile_args=['-O2', '-m64', '-fPIC'],
    libraries=[],
    language='fortran',
)


# this will install geodesiclm.py and _geodesiclm.so in the site-pacakge/geolm directory.
setup(
    name='geodesicLM',
    packages=find_packages(),
    ext_modules=[geolm_f],
    version=get_version(),
    install_requires=['scipy'],
    author='Mingjian Wen',
    author_email='wenxx151@gmail.com',
    url='https://github.com/mjwen/geodesicLM',
    description='Geodesic Levenberg-Marquardt minimization algorithm',
    long_description='Geodesic Levenberg-Marquardt minimization algorithm',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
)
