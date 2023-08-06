from setuptools import setup, find_packages

setup(
    name='simpgenalg',
    version='0.1.3',
    description='Genetic Algorithm',
    url='https://github.com/StephenMal/simpgenalg',
    author='Stephen Maldonado',
    author_email='simpgenalg@stephenmal.com',
    packages=find_packages(),
    install_requires=[
        'simptoolbox==0.1.2',\
        'simplogger==0.2.2',\
        'simpcfg==0.1.8'
    ],
    extras_require  ={
        'scipy':['scipy==1.8.0'],
        'viewer':['plotly',\
                  'dash',\
                  'pandas',\
                  'numpy']
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities'
    ]
)
