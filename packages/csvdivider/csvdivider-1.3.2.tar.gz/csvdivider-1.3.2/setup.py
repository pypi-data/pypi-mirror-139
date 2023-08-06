import setuptools

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name="csvdivider",
      description="csvdivider",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="MIT",
      version="1.3.2",
      author="Alex Ng",
      author_email="alex_q_wu@qq.com",
      maintainer="Alex Ng",
      maintainer_email="alex_q_wu@qq.com",
      url="https://github.com/AlexNg9527/csvdivider.git",
      packages=setuptools.find_packages(),
      entry_points={
          'console_scripts': ['csvdivide = csvdivider.cli:main']},
      classifiers=[
          'Programming Language :: Python :: 3',
      ])
