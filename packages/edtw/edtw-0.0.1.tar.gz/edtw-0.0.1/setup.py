
from setuptools import setup, find_packages


setup(
    name='edtw',
    version='0.0.1',
    license='MIT',
    author="Evgenii Kudriavtsev",
    author_email='qkudev@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/qkudev/edtw',
    keywords='python, dwt, entropy, mutual information',
    install_requires=[
        'scikit-learn',
        'numpy'
    ],

)
