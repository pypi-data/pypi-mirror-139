from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Topsis-Sarthak-401903029",
    version="1.0.1",
    description="A Python package for Multiple Criteria Decision Making (MCDM) using TOPSIS made by Sarthak Vohra, a student of Thapar Institute of Engineering and Technology, Patiala.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Sarthak Vohra",
    author_email="svohra_bemba19@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["topsis_Sarthak_401903029"],
    include_package_data=True,
    install_requires=["pandas"],
    entry_points={
        "console_scripts": [
            "Topsis-Sarthak-401903029=topsis_Sarthak_401903029.__init__:main",
        ]
    },
)
