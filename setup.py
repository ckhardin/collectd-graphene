from setuptools import find_packages, setup
from setuptools.command.build_py import build_py

class npmbuild_py(build_py):

    def run(self):
        import os
        import shutil
        import subprocess
        workdir = os.path.join(os.getcwd(), "frontend")
        if not self.dry_run:
            subprocess.check_call(['npm', 'install'], cwd=workdir)
            subprocess.check_call(['npm', 'run', 'relay'], cwd=workdir)
            subprocess.check_call(['npm', 'run', 'build'], cwd=workdir)
            flask_frontend = os.path.join(self.build_lib,
                                          "collectd_graphene", "frontend")
            if os.path.exists(flask_frontend):
                shutil.rmtree(flask_frontend)
            shutil.copytree(os.path.join(workdir, "build"),
                            flask_frontend, symlinks=True)
        build_py.run(self)


# keep in sync with requirements.txt
requirements=[
    'Flask==1.0.2',
    'Flask-GraphQL==2.0.0',
    'Flask-Webpack==0.1.0',
    'graphene>=2.1.3',
    'rrdtool>=0.1.10'
]

setup(
    name='collectd-graphene',
    version='0.3.0',
    author='Charles Hardin',
    author_email='ckhardin@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    cmdclass={'build_py': npmbuild_py },
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
