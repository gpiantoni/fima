from setuptools import setup, find_packages

setup(
    name='fima',
    version='0.2',
    description='finger mapping analysis',
    url='https://github.com/gpiantoni/fima',
    author="Gio Piantoni",
    author_email='fima@gpiantoni.com',
    license='GPLv3',
    classifiers=[
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fima=fima.bin.command:main',
        ],
    },
)
