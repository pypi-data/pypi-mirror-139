import setuptools

with open("README.md", "r", encoding="utf-8") as readme:
    README = readme.read()

setuptools.setup(
    name='PyTimbre',
    version='0.4.1',
    description='Python conversion of Timbre Toolbox',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=setuptools.find_packages(),
    author='Frank Mobley',
    author_email='mobssoft@gmail.com',
    keywords=['machine learning', 'feature extraction', 'MATLAB', 'audio'],
    url='https://gitlab.com/python-audio-feature-extraction/pytimbre',
    download_url='',
    install_requires=['numpy', 'scipy', 'statsmodels', 'nptdms'],
    python_requires=">=3.6"
)
