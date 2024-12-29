from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text()

setup_args = dict(
    name='pscachier',
    version='0.1.1',
    description='pscachier',
    long_description_content_type="text/markdown",
    long_description=README,
    url='https://github.com/psadmin-io/pscachier',
    author='psadmin.io',
    author_email='info@psadmin.io',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(),
    keywords=['PeopleSoft', 'PeopleTools','Tuxedo'],    
    include_package_data=True,
    install_requires=["Click"],
    entry_points={
        "console_scripts": [
            "pscachier=pscachier.pscachier:cli",
        ]
    },
)

if __name__ == '__main__':
    setup(**setup_args) 
