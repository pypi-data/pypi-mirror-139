import setuptools

packages = \
['piercrop']

package_data = \
{'': ['*']}

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="piercrop", # Replace with your own username
    version="0.1.0.0.0",
    author="Surasak Choedpasuporn",
    author_email="surasak.cho@gmail.com",
    description="A PIER's crop insurance project package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/surasakcho/piercrop",
    packages=packages,
    package_data=package_data,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

