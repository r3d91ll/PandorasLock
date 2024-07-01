from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='PandorasLock',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A module for securing sensitive information in text data, inspired by Pandora\'s Box',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/PandorasLock",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.7.2',
    install_requires=[
        'requests>=2.25.1',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'pytest-cov>=2.12.1',
        ],
    },
    include_package_data=True,
    package_data={
        'pandoras_key': ['config/*.json'],
    },
)