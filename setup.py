from setuptools import setup, find_packages

exec(open("conset/_version.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="conset",
    version=__version__,
    description="Efficient storagge for sets of mostly-consecutive integers",
    url="https://github.com/smurfix/conset",
    long_description=LONG_DESC,
    author="Matthias Urlichs",
    author_email="matthias@urlichs.de",
    license="MIT -or- Apache License 2.0",
    packages=find_packages(),
    install_requires=[
        "trio",
    ],
    keywords=[
        # COOKIECUTTER-TRIO-TODO: add some keywords
        # "async", "io", "networking", ...
    ],
    python_requires=">=3.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: Trio",
        # COOKIECUTTER-TRIO-TODO: Remove any of these classifiers that don't
        # apply:
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # COOKIECUTTER-TRIO-TODO: Consider adding trove classifiers for:
        #
        # - Development Status
        # - Intended Audience
        # - Topic
        #
        # For the full list of options, see:
        #   https://pypi.org/classifiers/
    ],
)
