from setuptools import setup, find_packages

exec(open("conset.py", encoding="utf-8").read())

LONG_DESC = open("README.rst", encoding="utf-8").read()

setup(
    name="conset",
    version=__version__,
    description="Efficient storage for sets of mostly-consecutive integers",
    url="https://github.com/smurfix/conset",
    long_description=LONG_DESC,
    author="Matthias Urlichs",
    author_email="matthias@urlichs.de",
    license="MIT -or- Apache License 2.0",
    py_modules=["conset"],
    keywords=[
        "set", "coalesce", "compact", "consecutive",
    ],
    python_requires=">=3.4",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
)
