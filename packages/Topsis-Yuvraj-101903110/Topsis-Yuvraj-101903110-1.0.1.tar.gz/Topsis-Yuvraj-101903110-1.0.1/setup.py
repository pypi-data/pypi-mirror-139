from setuptools import setup, find_packages

VERSION = '1.0.1'

# Setting up
setup(
    name="Topsis-Yuvraj-101903110",
    version=VERSION,
    author="Yuvraj Sidhu",
    author_email="<yuvrajsidhu10@gmail.com>",
    url = "https://github.com/yuvisidhu19/Topsis-Yuvraj-101903110",
    description="Package to perform TOPSIS",
    packages=find_packages(),
    install_requires=['pandas', 'numpy'],
    keywords=['python', 'topsis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)