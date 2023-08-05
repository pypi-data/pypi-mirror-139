from setuptools import setup, find_packages
from os.path import abspath, dirname, join

# Fetches the content from README.md
# This will be used for the "long_description" field.
README_MD  =  open(join(dirname(abspath(__file__)), "README.md")).read()

setup(
    name = "FireCaptcha",
    version = "0.0.2",
    packages = ['FireCaptcha'],
    description = "Highly customizable captcha generator",
    long_description = README_MD,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Memetelve/FireCaptcha",
    author_name = "Memetelve",
    author_email = "maciek@marszalkowski.pl",

    include_package_data=True,

    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only"
    ],
    keywords = "captcha, security",

    install_requires = [
        'Pillow',
    ]
)