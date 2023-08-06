import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stacking_manual",
    version="0.1.10",
    author="kevin",
    description="manual stacking package for ML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages = setuptools.find_packages(where="src"),
)