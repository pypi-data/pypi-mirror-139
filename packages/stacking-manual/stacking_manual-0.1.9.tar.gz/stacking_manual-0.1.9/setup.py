import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stacking_manual",
    version="0.1.9",
    author="kevin",
    description="manual stacking package for ML",
    packages = setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
)