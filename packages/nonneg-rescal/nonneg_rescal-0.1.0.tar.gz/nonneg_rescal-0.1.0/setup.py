from setuptools import setup, find_packages

setup(
    name='nonneg_rescal',
    author='Denis Krompass',
    author_email='dekromp@gmail.com',
    classifiers=[],
    description='non-negative RESCAL Tensor-Factorization',
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
    ],
    long_description=open('README.txt').read(),
    long_description_content_type='text/plain',
    url='https://github.com/bkj/nonneg_rescal',
    keywords=['non-negative', 'tensor', 'factorization', 'rescal'],
    license='BSD3',
    packages=find_packages(),
    version="0.1.0",
)
