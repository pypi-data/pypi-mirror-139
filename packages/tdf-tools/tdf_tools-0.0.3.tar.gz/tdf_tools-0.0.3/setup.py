import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tdf_tools",
    version="0.0.3",
    author="xujian",
    author_email="17826875951@163.com",
    description="flutter开发流程工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.2dfire.net/app/flutter/tools/package_tools",
    # packages=setuptools.find_packages(),
    packages=['tdf_tools'],
    install_requires=[
        'ruamel.yaml',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'tdf_init=tdf_tools:create',
            'tdf_tools=tdf_tools:process'
        ]
    }
)
