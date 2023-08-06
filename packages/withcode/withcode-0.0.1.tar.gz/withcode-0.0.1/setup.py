from setuptools import setup
import withcode
setup(
    name='withcode',
    version=withcode.__version__,    
    description='Offline python module to match visualisation and sound features of create.withcode.uk',
    url='https://github.com/pddring/withcode',
    author='Pete Dring',
    author_email='pddring@gmail.com',
    license='MIT',
    packages=['withcode'],
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
)