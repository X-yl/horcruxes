from setuptools import setup


setup(name='horcruxes',
      version='3.1415',
      description='A command line tool to split a file into horcruxes, where the original can be recreated with at least n of the horcruxes',
      author='X-yl',
      license='GNU GPLv3',
      entry_points={
        "console_scripts": [
            "horcruxes = horcruxes.crux:cli",
        ]
    },
      packages=['horcruxes'])

