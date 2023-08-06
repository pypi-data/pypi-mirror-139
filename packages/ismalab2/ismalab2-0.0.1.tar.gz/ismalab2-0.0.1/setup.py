from setuptools import setup

setup(
    name='ismalab2',
    version='0.0.1',    
    description='A example Python package',
    url='https://github.com/isba06',
    author='Ismail Bayramov',
    author_email='example@mail.ru',
    license='BSD 2-clause',
    packages=['ismalab2'],
    install_requires=['scipy',
                      'matplotlib ==2.2',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)