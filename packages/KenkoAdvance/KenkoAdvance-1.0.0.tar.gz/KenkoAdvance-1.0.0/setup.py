from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='KenkoAdvance',
    version='1.0.0',
    author='AkagiYui',
    author_email='akagiyui@yeah.net',
    description='自用的一些功能',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AkagiYui/KenkoAdvance',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    python_requires=">=3.9",
    license='MIT',
)
