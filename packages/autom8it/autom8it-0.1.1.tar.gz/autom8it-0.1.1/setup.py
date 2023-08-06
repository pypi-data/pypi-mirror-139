import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="autom8it",
    version="0.1.1",
    author="Eldad Bishari",
    author_email="eldad@1221tlv.org",
    description="Automate IT operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eldad1221/autom8it",
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML==6.0',
        'cerberus==1.3.4',
        'quickbe==0.1.2',
        'boto3==1.20.41',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
