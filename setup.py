from setuptools import setup, find_packages

setup(
    name='pandoras_lock',
    version='0.1.0',
    packages=find_packages(),
    # Since you're not using third-party packages, there's no need for install_requires
    # install_requires=[],
    # Including this to avoid any third-party install, makes it clear that it relies on standard library only
    python_requires='>=3.7.2',  # Adjust the version as per your requirements
)
