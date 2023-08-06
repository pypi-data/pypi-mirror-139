import setuptools

long_description = "Qt dependency for D-Analyst."

setuptools.setup(
    name = "QPlug",
    version = "1.0.3",
    author = "Agbakosi Adeoluwa(180 Memes), Diachronic Technologies",
    author_email = "adeoluwaagbakosi@gmail.com",
    description = "Qt dependency for D-Analyst ",
    long_description = long_description,
    url = "https://github.com/Diachronic-Technologies/Qtop",
    project_urls = {
        "Bug Tracker":"https://github.com/Diachronic-Technologies/Qtop/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"":"main"},
    packages=setuptools.find_packages(where="main"),
    python_requires=">=3.6",
    install_requires = []
)