from setuptools import setup

from dldseval import __version__

setup(
    name='dlds-eval',
    version=__version__,
    author='Data Spree GmbH',
    author_email='info@data-spree.com',
    url='https://data-spree.com/products/deep-learning-ds',
    license='Apache-2.0',
    description='Evaluation code for Deep Learning DS from Data Spree.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    project_urls={
        # 'Documentation': 'https://docs.data-spree.com/'
    },
    keywords=[
        'dataspree', 'deep learning', 'artificial intelligence'
    ],
    packages=[
        'dldseval'
    ],
    install_requires=[
        'numpy~=1.21',
        'scikit-learn~=1.0'
    ],
    extras_require={
        'build': [
            'pytest',
            'pytest-cov',
            'pytest-sugar'
        ]
    },
    python_requires='>=3.7'
)
