from setuptools import setup, find_packages
import codecs
import sys
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Python toolset for creating GUI-like experience interfaces in console environment.'
long_description: str = None

def test_filecontent(file_name):
    try:
        print(f'Reading {file_name}')
        with codecs.open(os.path.join(here, file_name), encoding='utf-8') as fh:
            long_description = '\n' + fh.read()
    except:
        print(f'Could not open {file_name}... Terminating process to avoid unexpected behavior.')
        sys.exit()
        
    if long_description.strip() not in (None, ''):
        print(f'{file_name} contains data. Read scuccessfull.')
    else: 
        print(f'Loaded empty {file_name}... Terminating process to avoid unexpected behavior.')
        sys.exit()
        
file_check_list = [
                   'README.md',
                   'LICENSE',
                   'pyproject.toml',
                  ]
for file in file_check_list:
    test_filecontent(file)

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
      
setup(
    name="pycon-gui",
    version=VERSION,
    author="nativeme (Lukasz Kaniak)",
    author_email="<lukaszkaniak@gamil.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/nativeme/pycon-arrow-menu",
    project_urls={
        "Bug Tracker": "https://github.com/nativeme/pycon-arrow-menu/issues",
    },
    long_description=long_description,
    install_requires=[
                      'colorama',
                      'commonmark',
                      'Pygments',
                      'rich',
                      'getch==1.0; platform_system == "Linux"'
                     ],
    keywords=[
              'menu',
              'arrow',
              'navigatable',
              'color',
              'recursive',
              'align',
              'marker'
             ],
    classifiers=[
                 "Development Status :: 4 - Beta",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License",
                 "Operating System :: Unix",
                 "Operating System :: Microsoft :: Windows",
                ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6"
)