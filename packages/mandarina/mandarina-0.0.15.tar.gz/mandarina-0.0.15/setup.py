import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mandarina",
    version="0.0.15",
    author="Alen Frey",
    author_email="mailtoalenf@gmail.com",
    description="Friendly data science library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sunpip/mandarina",
    packages=setuptools.find_packages(exclude="test"),
    install_requires=[
        'psutil',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
