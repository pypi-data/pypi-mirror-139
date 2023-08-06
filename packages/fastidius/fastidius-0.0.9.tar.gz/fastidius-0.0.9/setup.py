from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='fastidius',
    version='0.0.9',
    author='John Kealy',
    author_email='johnckealy.dev@gmail.com',
    license='MIT',
    description='A full stack web app creator with FastAPI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/johnckealy/fastidius',
    py_modules=['cli', 'src'],
    packages=find_packages(),
    package_data={
        '': ['src/docker-compose.yml'],
        '': ['src/README.md'],
    },
    include_package_data=True,
    install_requires=[requirements],
    python_requires='>=3.9',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        fastidius=cli:app
    '''
)
