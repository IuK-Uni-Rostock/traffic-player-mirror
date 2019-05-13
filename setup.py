from setuptools import setup, find_packages

setup(
    name='traffic-player',  # Required
    version='0.0.1',  # Required
    packages=find_packages(exclude=['frontend']),  # Required
    install_requires=[
        'aiohttp>=3.0,<4',
        'aiohttp-index>=0.1',
        'python-socketio>=4.0,<5',
        'mysql-connector>=2.0,<3',
        'pika>=1.0,<2',
        'networkx>=2.0,<3',
        'knxmap @ git+https://github.com/takeshixx/knxmap.git'
    ],
)
