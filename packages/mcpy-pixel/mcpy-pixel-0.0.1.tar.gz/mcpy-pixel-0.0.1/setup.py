from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
setup(
    name='mcpy-pixel',
    version='0.0.1',
    description='A Simple Python Wrapper for the Minecraft Hypixel API!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/savagedevelops/pypixelapi',  
    project_urls={
        "Savage Development": "https://www.savagedevelopment.tk",
        "Bug Tracker" : "https://github.com/savagedevelops/pypixelapi/issues"
    },
    author='Savage Development',
    author_email='support@savagedevelopment.tk',
    license='MIT',
    classifiers=classifiers,
    keywords='hypixel',
    install_requires=['requests'],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)