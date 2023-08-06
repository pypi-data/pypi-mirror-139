from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='Topsis-Dhairya-101916016',
    version='1.5.0',
    packages=['Topsis-Dhairya-101916016'],
    url='',
    license='MIT',
    author='Dhairya Aggarwal',
    author_email='daggarwal_be19@thapar.edu',
    include_package_data=True,
    install_requires=[],
    description='TOPSIS Score calculation for MDM',
    long_description=README,
    long_description_content_type="text/markdown",
)
