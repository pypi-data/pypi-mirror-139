import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fridrich",
    version="1.0.2",
    author="Nilusink",
    author_email="nilusink@protonmail.com",
    description="packs all fridrich functions in one package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nilusink/Fridrich",
    project_urls={
        "Official Website": "http://info.fridrich.xyz",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)
