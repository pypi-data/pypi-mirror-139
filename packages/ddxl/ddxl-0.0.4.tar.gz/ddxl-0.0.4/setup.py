from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='ddxl',
      version='0.0.4',
      description='DDXL',
      author='LcsH0s',
      author_email='decastro@et.esiea.fr',
      url='https://github.com/LcsH0s/ddxl',
      long_description=long_description,
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: Unix",
                   "Programming Language :: Python :: 3.9",
                   ],
      packages=find_packages(exclude=["tests.*", "tests"]),
      install_requires=[
          'docker',
      ],
      )
