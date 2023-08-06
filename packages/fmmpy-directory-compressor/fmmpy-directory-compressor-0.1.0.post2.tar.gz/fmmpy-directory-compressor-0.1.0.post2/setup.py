import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fmmpy-directory-compressor",
    version="0.1.0.post2",
    author="Wibo Kuipers",
    author_email="w.kuipers@filmage.nl",
    description="Compress a directory into a single .FSA file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/w-kuipers/fmm-directory-compressor",
    project_urls={
        "Bug Tracker": "https://github.com/w-kuipers/fmm-directory-compressor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    include_package_data=True,
)