from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
install_requires = (here / 'requirements.txt').read_text(encoding='utf-8').splitlines()

setup(
    install_requires=install_requires
)
