from setuptools import setup, find_packages

setup(
    name='traffic-player',  # Required
    version='0.0.1',  # Required
    packages=find_packages(exclude=['frontend']),  # Required
    install_requires=[
        'aiohttp',
        'aiohttp-index',
        'python-socketio',
        'mysql-connector'
    ],
)
