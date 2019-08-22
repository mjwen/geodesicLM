from distutils.core import setup

# this will install geodesiclm.py and _geodesiclm.so in the site-pacakge/geolm directory.
setup(
    name='geolm',
    packages=['geolm'],
    package_dir={'geolm': 'pythonInterface'},
    package_data={'geolm': ['_geodesiclm.so']},
)
