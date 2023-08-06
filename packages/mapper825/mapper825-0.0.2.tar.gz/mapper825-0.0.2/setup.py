from distutils.core import setup
setup(
  name = 'mapper825',         # How you named your package folder (MyLib)
  packages = ['mapper825'],   # Chose the same as "name"
  version = '0.0.2',   # Start with a small number and increase it with every change you make
  install_requires=[
    'numpy',
    'pandas',
    'fiona',
    'shapely',
    'geopandas',
    'plotly',
    'kaleido',
    "setuptools>=42",
    "wheel"
  ]
)