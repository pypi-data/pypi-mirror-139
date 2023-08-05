import setuptools

setuptools.setup(
    name="pyscreamor",
    version="0.0.2",
    author="Devecor",
    author_email="devecor@163.com",
    description="A small example package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://devecor.cn",
    project_urls={
        "Bug Tracker": "https://devecor.cn",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
