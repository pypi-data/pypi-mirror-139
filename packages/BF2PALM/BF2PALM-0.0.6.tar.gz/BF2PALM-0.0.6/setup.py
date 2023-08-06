from setuptools import setup,find_packages
setup(name='BF2PALM',
      version='0.0.6',
      description='Transfer building footprint to 2D DEM for LES simulation',
      author='Jiachen Lu',
      author_email='jiachensc@gmail.com',
      requires= ['numpy','matplotlib','shapely','math','pandas','scipy','osmnx'], 
      packages=find_packages(),
      license="MIT",
      python_requires=">=3.6",
      )
