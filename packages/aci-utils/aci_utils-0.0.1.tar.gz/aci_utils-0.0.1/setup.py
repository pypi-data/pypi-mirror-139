import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aci_utils',
    version='0.0.1',
    license='MIT',
    author="Endika Zuazo",
    author_email='endikazuazo@gmail.com',
    description="Define una clase para interactuar con la API de Cisco ACI",
    packages=setuptools.find_packages(),
    keywords='example project',
)