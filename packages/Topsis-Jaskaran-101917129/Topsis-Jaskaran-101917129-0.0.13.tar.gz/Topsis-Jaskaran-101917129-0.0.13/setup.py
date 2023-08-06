from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = 'TOPSIS:Topsis(Technique for Order Preference by Similarity to Ideal Solution): Of the numerous criteria decision-making (MCDM) methods, TOPSIS is a practical and useful technique for ranking and selecting a number of possible alternatives by measuring Euclidean distances. TOPSIS, is a simple ranking method in conception and application.USED: import topsislib as tb    df=tb.topsis(dff,weights,impacts).'

# Setting up
setup(
    name="Topsis-Jaskaran-101917129",
    version=VERSION,
    author="Jaskaran Singh Purewal",
    author_email="jaskaransinghpurewal7@gmail.com",
    description=DESCRIPTION,
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