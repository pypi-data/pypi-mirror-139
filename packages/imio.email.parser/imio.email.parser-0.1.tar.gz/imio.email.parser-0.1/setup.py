# -*- coding: utf-8 -*-

from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name="imio.email.parser",
    version="0.1",
    packages=["imio", "imio.email", "imio.email.parser"],
    package_dir={"": "src"},
    url="https://pypi.org/project/imio.email.parser",
    license="GPL",
    author="Nicolas Demonté",
    author_email="support@imio.be",
    description="",
    long_description=long_description,
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    install_requires=[
        "mail-parser",
        "beautifulsoup4>=4.6.3",
        "email2pdf",
        "html5lib",
        "lxml",
#        "pdfminer3k",  not sure it's needed. Or try pdfminer.six for python2
        "pypdf2",
        "python-magic",
        "reportlab",
        "requests",
        "six",
    ],
    entry_points="""
    [console_scripts]
    emailtopdf = imio.email.parser.main:emailtopdf
    """,
)
