import setuptools

DESCRIPTION = 'Creates a static .html file with charts using Google Charts API'

setuptools.setup(
    name="plot2html",
    version="0.0.3",
    author="Rafael Rodrigues Troiani",
    author_email="rafael.r.troiani@gmail.com",
    description=DESCRIPTION,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[],
    keywords=['python', 'Google Charts', 'html'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)