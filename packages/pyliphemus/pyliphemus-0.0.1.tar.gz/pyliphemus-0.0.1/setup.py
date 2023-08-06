try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pyliphemus',
    version='0.0.1',
    author='baltazarx',
    author_email='qwasar9@protonmail.com',
    url="https://github.com/baltazarx/pyliphemus'",
    description='Simple (at now) BIGSMM api wrapper',
    download_url='https://github.com/baltazarx/pyliphemus',
    license='MIT',

    packages=['pyliphemus'],
    install_requires=['requests', 'loguru'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ]
)
