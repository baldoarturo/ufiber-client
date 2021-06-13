import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='ufiber-client-3',  
     version='0.1',
     author="Arturo Baldo",
     author_email="baldoarturo@gmail.com",
     description="A Ubiquiti UFiber Client for firmware version 3",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )