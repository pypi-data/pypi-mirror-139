import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xrayconfigurator",  # Replace with your own username
    version="0.0.32",
    author="Ondrej Jurcak",
    author_email="ondrej@surglogs.com",
    description="Configuration helper for xray",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["aws-xray-sdk>=2.9.0", "sentry-sdk[flask]>=1.5.5"],
    setup_requires=["wheel"],
    test_suite="nose.collector",
    tests_require=["nose", "wheel", "flask-sqlalchemy>=2.4.4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
