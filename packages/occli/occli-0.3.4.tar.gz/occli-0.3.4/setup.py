import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="occli",
    version="0.3.4",
    author="Richard Mwewa",
    author_email="richardmwewa@duck.com",
    packages=["occli"],
    description="Unofficial Command Line Interface for OpenCorporates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rly0nheart/occli",
    license="GNU General Public License v3 (GPLv3)",
    install_requires=["requests"],
    classifiers=[
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        "console_scripts": [
            "occli=occli.main:occli",
            ]
    }
)
