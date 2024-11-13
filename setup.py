from setuptools import setup, find_packages

setup(
    name="directory_cleanup",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-dotenv',
        'colorama',
        'pytest',
        'pytest-asyncio',
        'pytest-cov'
    ],
) 