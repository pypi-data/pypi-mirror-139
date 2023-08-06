import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='tamarin-iac',  
     version='0.2.0.1',
     author="Alisson Machado",
     author_email="alisson.itops@gmail.com",
     description="Infrastructure as code",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/AlissonMMenezes/Tamarin",
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': ['tamarin=tamarin_iac.tamarin:main'],
    },
    install_requires=[
    "paramiko==2.9.2",
    "PyYAML==6.0",
    "setuptools==60.5.0",
    "terminaltables==3.1.10",
    ]
 )