import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pfsc-lang",
    version="0.0.1",
    license="MPL-2.0",
    author="Steve Kieffer",
    author_email="sk@skieffer.info",
    description="Proofscape Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)

