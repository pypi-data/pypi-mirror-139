from setuptools import setup, find_packages


requirements = [
    'requests',
    'pywal',
    'downloader-cli',
    'beautifulsoup4',
    'dbus-python',
    'simber'
]

setup(
    name='QuickWall',
    packages=find_packages(),
    author='Deepjyoti Barman',
    author_email='deep.barman30@gmail.com',
    description='Set any wallpaper from commandline',
    long_description='Set any wallpaper from Unsplash from the commandline',
    url='http://github.com/deepjyoti30/QuickWall',
    entry_points={
        'console_scripts': [
            'quickwall = QuickWall.__main__:main_handler',
            'QuickWall = QuickWall.__main__:main_handler'
        ]
    },
    version='0.0.5',
    license='MIT',
    install_requires=requirements,
)
