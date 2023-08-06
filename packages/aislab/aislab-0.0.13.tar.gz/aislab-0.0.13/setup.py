import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="aislab",
    version="0.0.13",
    author="Alexander Efremov",
    author_email="",
    description="AISLAB - AI System Laboratory - module for development of AI systems.",
#    long_description=long_description,
    long_description_content_type="text/markdown",
    
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[],
    python_requires='>=3.6',
)
