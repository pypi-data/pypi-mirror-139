from setuptools import setup

with open('README.md') as file:
    README = file.read()

setup(
    name='flightclient',
    version='0.6',
    description='Aircraft Tracking Library (unofficial Flightradar24 client)',
    long_description_content_type='text/markdown',
    long_description=README,
    author='Danila Lugovoy',
    author_email='zhestkiyflex@gmail.com',
    license = "MIT",
    url='https://github.com/danilalugovoy/flightclient',
    install_requires=["requests"],
    zip_safe=False,
    packages=['flightclient']
)