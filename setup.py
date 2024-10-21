from setuptools import setup, find_packages

setup(
    name='yaml_diff',  
    version='0.3', 
    description='A tool to compare YAML configuration files', 
    author='Rasul Karimov',
    author_email='rasul.karimov@gmail.com',
    packages=find_packages(), 
    install_requires=[
        'pyyaml',
    ],
    python_requires='>=3.6', 
)