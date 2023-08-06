from setuptools import setup, find_packages

setup(
    name='spreco',
    version='0.0.1',
    description='Training priors for MRI image reconstruction',
    author="Guanxiong Jason Luo",
    author_email="guanxiong.luo@med.uni-goettingen.de",
    url="https://github.com/mrirecon/spreco",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'tensorflow-gpu',
        'tf-slim==1.1.0',
        'numpy',
        'pillow==8.2.0',
        'matplotlib==3.3.4',
        'scikit-image==0.18.1',
        'pyyaml==5.4.1',
        'tqdm'
    ],
)