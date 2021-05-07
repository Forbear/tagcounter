from setuptools import setup

setup(
    name='tagcounter',
    version='0.5.0',
    description='Tagcounter package.',
    url='https://github.com/forbear/tagcounter',
    author='Daniil S',
    author_email='silnydan@gmail.com',
    license='MIT License',
    packages=['tagcounter'],
    install_requires=['kivy>=2.0.0',
                      'beautifulsoup4',
                      'pyyaml'
                      ],
    entry_points={'console_scripts': ['tagcounter = tagcounter']},

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
)
