import setuptools

with open("../readme.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="a7dtester",
    version="0.0.4",
    author="Uladzislau Khamkou",
    description="simple test runner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    py_modules=["a7dtester"],
    entry_points = {'console_scripts': ['test_with_a7dtester=a7dtester:main']},
    package_dir={"": "."},
    install_requires=['a7d>=0.0.5'],
)
