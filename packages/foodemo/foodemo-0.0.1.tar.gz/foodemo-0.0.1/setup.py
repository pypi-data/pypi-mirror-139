from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="foodemo",
    version="0.0.1",
    description="Demo project for GitHub Actions",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/RobertoPrevato/FooPythonDemo",
    author="Roberto Prevato",
    author_email="roberto.prevato@gmail.com",
    keywords="foo useless package",
    license="MIT",
    packages=["foo"],
    install_requires=[],
    include_package_data=True,
)
