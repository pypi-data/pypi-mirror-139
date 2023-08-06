import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
      name='comapsmarthome-postgres-client',
     version="0.1.1",
     author="Aurélien Sylvan",
     author_email="aurelien.sylvan@comap.eu",
     description='this library allow to simplify the basic operation in postgres databases like select, insert, update, delete and upsert',
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="",
     package=setuptools.find_packages(
            exclude=["tests"]),
            install_requires=[],
            classifiers=[
                  "Programming Language :: Python :: 3",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
            ]
)