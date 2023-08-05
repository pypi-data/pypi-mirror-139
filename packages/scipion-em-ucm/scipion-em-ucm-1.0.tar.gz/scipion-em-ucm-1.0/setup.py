from setuptools import setup, find_packages

setup(
    # The first three are required for uploading to PyPI.
    name='scipion-em-ucm',
    version='1.0',
    description='Scipion plugin with map validations',

    license='GPL-3',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jordi Burguet-Castell, Javier Vargas',
    author_email='jburguet@ucm.es, jvargas@fis.ucm.es',
    url='https://gitlab.com/jordibc/scipion-em-ucm',
    keywords='scipion cryoem imageprocessing validation',
    packages=find_packages(),
    install_requires=[open('requirements.txt').read().splitlines()],
    entry_points={'pyworkflow.plugin': 'ucm = ucm'},
    package_data={
       'ucm': ['icon.png', 'protocols.conf'],
    }
)
