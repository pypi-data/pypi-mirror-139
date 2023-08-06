# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zodipy', 'zodipy.data']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0',
 'astropy>=5.0.1',
 'astroquery>=0.4.3,<0.5.0',
 'healpy>=1.15.0,<2.0.0',
 'numpy>=1.21',
 'scipy>=1.7.1,<2.0.0',
 'typing_extensions>=3.10.0.1']

setup_kwargs = {
    'name': 'zodipy',
    'version': '0.4.0',
    'description': 'Zodipy is a python tool that simulates the Zodiacal emission.',
    'long_description': '\n<img src="imgs/zodipy_logo-nobg.png" width="350">\n\n[![PyPI version](https://badge.fury.io/py/zodipy.svg)](https://badge.fury.io/py/zodipy)\n![Tests](https://github.com/MetinSa/zodipy/actions/workflows/tests.yml/badge.svg)\n[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)\n\n\n---\n\n\n*Zodipy* is a Python simulation tool for Zodiacal Emission (Interplanetary Dust Emission). It allows you to compute the \nsimulated interplanetary dust emission for a timestream of pixels, or at an instant in time.\n\n![plot](imgs/zodi_default.png)\n\n## Installing\nZodipy is available at PyPI and can be installed with ``pip install zodipy``.\n\n## Features\nThe full set of features and use-cases will be documentated in the nearby future.\n\n**Initializing an Interplantery Dust Model:** *Zodipy* implements the [Kelsall et al. (1998)](https://ui.adsabs.harvard.edu/abs/1998ApJ...508...44K/abstract) Interplanetary Dust Model. Additionally, it is possible to include the various emissivity fits from the Planck collaboration.\n```python\nfrom zodipy import Zodipy\n\nmodel = Zodipy(model="DIRBE")\n```\n\n**Instantaneous emission:** We can make a map of the simulated instantaneous emission seen by an observer using the `get_instantaneous_emission` function, which queries the observer position given an epoch through the JPL Horizons API:\n```python\nimport healpy as hp\nimport astropy.units as u\n\nemission = model.get_instantaneous_emission(\n    800*u.GHz, \n    nside=256, \n    observer="Planck", \n    epochs=59215,  # 2010-01-01 (iso) in MJD\n    coord_out="G"\n)\n\nhp.mollview(emission, norm="hist")\n```\n![plot](imgs/zodi_planck.png)\n\nThe `epochs` input must follow the convention used in [astroquery](https://astroquery.readthedocs.io/en/latest/jplhorizons/jplhorizons.html). If multiple dates are passed to the function, the returned emission becomes the average over all instantaneous maps.\n\nThe individual components can be retrieved by setting the keyword `return_comps=True`. Following is an example of the simulated *instantaneous emission* with Zodipy seen from L2 for each component at October 6th 2021.\n\n![plot](imgs/comps.png)\n\n\n**Time-ordered emission:** We can make a time-stream of simulated emission for a sequence of time-ordered pixels using the `get_time_ordered_emission` function. This requires specifying the heliocentric ecliptic cartesian position of the observer (and optionally the Earth) associated with each chunk of pixels. In the following we use the first day of time-ordered pixels from the DIRBE instrument of the COBE satellite (Photometric Band 6, Detector A, first day of observations) to make a simulated time-stream:\n```python\nimport astropy.units as u\nimport matplotlib.pyplot as plt\nfrom zodipy import Zodipy\n\nmodel = Zodipy()\n\n# Read in DIRBE tod information\ndirbe_tods = ...\ndirbe_pixels = ...\ndirbe_position = ...  \n\ntimestream = model.get_time_ordered_emission(\n    25*u.micron\n    nside=128,\n    pixels=dirbe_pixels,\n    observer_pos=dirbe_position,\n    color_corr=True, # Include the DIRBE color correction factor\n)\n\nplt.plot(dirbe_tods, label="DIRBE TODS")\nplt.plot(timestream, label="Zodipy simulation")\nplt.legend()\nplt.show()\n```\n![plot](imgs/timestream.png)\n\n\n**Binned time-ordered emission:** By setting `bin=True` in the function call, the simulated emission is binned into a HEALPIX map. In the following, we compare *Zodipy* simulated maps with the observed binned time-ordered data by DIRBE in week maps.\n\n```python\nimport astropy.units as u\nimport matplotlib.pyplot as plt\nfrom zodipy import Zodipy\n\nmodel = Zodipy()\n\nnside = 128\nwavelen = 25*u.micron\n\ndirbe_tod_chunks = [...]\ndirbe_pixel_chunks = [...]\ndirbe_positions = [...]\n\nemission = np.zeros(hp.nside2npix(nside))\nhits_map = np.zeros(hp.nside2npix(nside))   \n    \nfor day, (pixels, dirbe_pos) in enumerate(\n    zip(dirbe_pixel_chunks, dirbe_positions),\n    start=1\n):\n    \n    # Get unique pixel hit and numbers to build hits_map\n    unique_pixels, counts = np.unique(pixels, return_counts=True)\n    hits_map[unique_pixels] += counts\n\n    emission += model.get_time_ordered_emission(\n        wavelen,\n        nside=nside,\n        pixels=pixels,\n        observer_pos=dirbe_position,\n        bin=True,\n        color_corr=True\n    )\n\n    if day % 7 == 0:\n        zodi_emission /= hits_map\n        hp.mollview(zodi_emission)\n\n        # Reset emission and hits map for next week\n        emission = np.zeros(hp.nside2npix(nside)) \n        hits_map = np.zeros(hp.nside2npix(nside)) \n```\n\n![plot](imgs/tods.gif) \n![plot](imgs/zodipy.gif)\n',
    'author': 'Metin San',
    'author_email': 'metinisan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MetinSa/zodipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.10',
}


setup(**setup_kwargs)
