from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="topsis_Kushagra_101917112",
    version="0.1",
    description="A Python package implementing TOPSIS technique.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Kushagra Rastogi",
    author_email="kushagrarastogi2014@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["topsis_Kushagra_101917112"],
    include_package_data=True,
    install_requires=['numpy',
                      'pandas',
                      'sys',
                      'math'
     ],
     entry_points={
        "console_scripts": [
            "topsis=topsis_python.topsis:main",
        ]
     },
)
