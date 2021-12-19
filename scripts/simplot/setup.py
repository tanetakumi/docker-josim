from setuptools import setup, find_packages

setup(
    name="simplot", # これがパッケージ名になります～
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
    ],
    entry_points={
        'console_scripts':[
            'simplot = simplot.simplot:main',
        ],
    },
    author="tanetakumi",
    author_email="nutanetakumi@yahoo.co.jp",
    description="simulation and plot from JoSIM result",
    url="https://github.com/tanetakumi/",
    python_requires='>=3.8',
)