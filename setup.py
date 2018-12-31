from setuptools import find_packages, setup

# keep in sync with requirements.txt
requirements=[
    'Flask==1.0.2',
    'Flask-GraphQL==2.0.0',
    'Flask-Webpack==0.1.0',
    'graphene>=2.1.3',
    'rrdtool'
]

setup(
    name='collectd-graphene',
    version='0.1.0',
    author='Charles Hardin',
    author_email='ckhardin@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: User Interfaces',
        'Framework :: Flask',
        'Operating System :: POSIX',
    ]
)
