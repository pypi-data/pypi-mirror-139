import setuptools


packages = \
['pierpy']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy'],

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='pierpy',  
    version='0.3.0.7',
    author="Surasak Choedpasuporn",
    author_email="surasakc@bot.or.th",
    description="A python package for internally use in PIER",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/surasakcho/pierpy",
    packages=packages,
    package_data=package_data,
    install_requires=install_requires,
    python_requires='>=3.6.1,<4.0.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
     ],    
 )