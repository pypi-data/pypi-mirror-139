from setuptools import setup, find_packages
from pathlib import Path

# this_directory = Path(__file__).parent
# with open("README.md", "rb") as f:
#     long_description = f.read()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='stacking_manual',
    version='0.1.4',
#     license='MIT',
#     author="Giorgos Myrianthous",
#     author_email='email@example.com',
#     packages=find_packages('src'),
#     package_dir={'': 'src'},
#     url='https://github.com/gmyrianthous/example-publish-pypi',
#     keywords='example project',
    install_requires=[
        'scikit-learn',
        'pandas'
      ],
    long_description = long_description

)