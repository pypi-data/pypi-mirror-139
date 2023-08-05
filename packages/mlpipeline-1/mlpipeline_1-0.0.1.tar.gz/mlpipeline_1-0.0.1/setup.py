from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows'
]

setup(
    name = 'mlpipeline_1',
    version='0.0.1',
    description='An AutoML library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/debjyoti003/ML-Pipeline.git',
    author='Debjyoti Banerjee',
    author_email='debjyoti.banerjee1994@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='AutoML',
    packages=find_packages(),
    install_requires = ['pandas', 'sklearn', 'numpy']
)