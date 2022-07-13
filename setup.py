from setuptools import setup, find_packages
  
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

exec(open("_version.py").read())

install_requires=[
    'pandas',
    'pyntcloud>=0.3.0',
    'pythreejs>=2.3.0',
    ],

setup(
    name="pointcloudprocess", 
    version=__version__,    # version ID
    author="blastxiaol",    
    author_email="blastxiaol@gmail.com",    
    description="A point cloud process package", 
    long_description=long_description,  
    long_description_content_type="text/markdown",
    url="https://github.com/blastxiaol/Pointcloudprocess",   
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
    install_requires=install_requires,
)