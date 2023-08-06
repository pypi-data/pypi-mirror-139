
import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="Topsis-Manmeet-101903173",
    version="1.0.0",
    author="Manmeet Singh Rekhi",
    author_email="manmeetsingh.rekhi@gmail.com",
    description="Determining Topsis Score and Rank",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/Manmeet476/TOPSIS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["Topsis-Manmeet-101903173"],
    include_package_data=True,
    install_requires='pandas',
    
)