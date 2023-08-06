import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Boosting_Probit",
    version="0.0.1",
    author="Ou Yang, Qin-Ying",
    author_email="109354014@nccu.edu.tw",
    description="The aim is to address measurement error effects in regression models, and employ boosting procedure to do variable selection and estimation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    
)

