import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cabpacob_ast_drawer",
    version="0.0.228",
    author="Cabpacob",
    author_email="Cabpacob@github.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cabpacob/advanced_python",
    project_urls={
        "Bug Tracker": "https://github.com/Cabpacob/advanced_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "hw_1"},
    packages=setuptools.find_packages(where="hw_1"),
    python_requires=">=3.6",
)
