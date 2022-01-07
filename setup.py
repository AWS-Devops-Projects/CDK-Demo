import setuptools

CDK_VERSION="1.51.0"

with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cdk_image_analyzer",
    version="0.0.1",

    description="A CDK demo app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Maurice Borgmeier",

    package_dir={"": "infrastructure"},
    packages=setuptools.find_packages(where="cdk_image_analyzer"),

    install_requires=[
        f"aws-cdk.aws-dynamodb=={CDK_VERSION}",
        f"aws-cdk.aws-lambda=={CDK_VERSION}",
        f"aws-cdk.aws-lambda-event-sources=={CDK_VERSION}",
        f"aws-cdk.aws-s3=={CDK_VERSION}",
        f"aws-cdk.core=={CDK_VERSION}",
        "lambda-bundler==0.1.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

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
