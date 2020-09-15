from setuptools import setup

setup(name='horcruxes',
      version='2.7.post2',
      url='https://github.com/X-yl/horcruxes',
      description='A command line tool to split a file into horcruxes, so that the original can be recreated with at least k horcruxes',
      author='X-yl',
      long_description= open('README.md').read().replace('—', '-'),
      license='GNU GPLv3',
      long_description_content_type='text/markdown',
      entry_points={
        "console_scripts": [
            "horcruxes = horcruxes.crux:cli",
        ]
      },
      install_requires=[
            "click>=7.1.2",
            "mmh3>=2.5.1",
            "pycryptodome>=3.9.8",
            "tqdm>=4.48.2",
      ],
      python_requires=">=3.8",
      packages=['horcruxes'])
