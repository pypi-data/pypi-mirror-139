import setuptools

setuptools.setup(
    name="htlib",
    version="0.14",
    author="Harol Alvarado, Hedrich Apaza",
    author_email="harolav3@gmail.com, Vlandemir2411@hotmail.com",
    description="htlib package",
    url="https://github.com/harol1997/htlib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "pyserial==3.5",
        "requests==2.26.0"
    ],
    long_description="documentation >> https://htlib.readthedocs.io/en/latest/\ngithub >> https://github.com/harol1997/htlib"
)
