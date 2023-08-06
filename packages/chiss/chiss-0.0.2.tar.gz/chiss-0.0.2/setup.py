from setuptools import setup, find_packages

VERSION = '0.0.02'
DESCRIPTION = "Le module chiss feat crevard"
LONG_DESCRIPTION = "Le module chiss e*a été créer avec amour pour détécter les plus gros rat de france"

setup(
    name='chiss',
    version=VERSION,
    author="jachou",
    author_email="tuascruquejallaismettremonemail@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyscroll'],
    keywords=['python','rat','crevard','ratus','fr','pince'],
    classifiers=[
    ]
)

