from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='bizchat',
    version='1.0.0',
    description='import this library to use chat from client to server directly',
    long_description=open('README.txt').read() + '\n\n',
    url='',
    author='mayur',
    author_email='mayurdhameliya98@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='server client,chatapp',
    packages=find_packages(),
    install_requires=['']
)
