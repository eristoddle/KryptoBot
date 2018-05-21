import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kryptobot",
    packages=['kryptobot'],
    version="0.0.1",
    author="Stephan Miller",
    author_email="stephanmil@gmail.com",
    description="Cryptocurrency trading bot framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eristoddle/KryptoBot",
    zip_safe=False,
    install_requires=[
          'markdown',
          'pypubsub',
          'requests',
          'SQLAlchemy',
          'psycopg2',
          'pyti',
          'ccxt',
          'pandas',
          'enigma-catalyst',
          'matplotlib'
      ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
