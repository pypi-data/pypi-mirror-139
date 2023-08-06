import setuptools


__version__ = "0.1.1"

with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="deltarescdk",
    version=__version__,

    description="cdk contructs for Deltares Infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Jaap Langemeijer",

    packages=setuptools.find_packages(exclude=("tests",)),

    install_requires=[
        "aws-cdk.core==1.128.0",
        "aws-cdk.aws-s3==1.128.0",
        "aws-cdk.aws-ec2==1.128.0",
        "boto3==1.20.20"
    ],

    python_requires=">=3.6",

    test_require=["pytest"],

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
