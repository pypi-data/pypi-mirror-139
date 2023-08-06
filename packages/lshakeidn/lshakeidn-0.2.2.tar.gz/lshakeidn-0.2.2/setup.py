import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lshakeidn",
    version="0.2.2",
    author="NaranggiSoko",
    author_email="ranggi_me@yahoo.com",
    description="This package gets the latest earthquake in Indonesia from the official government agency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giesoko/live_indonesia_earthquake",
    project_urls={
        "Website": "https://pramudyasoko.blogspot.com/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
