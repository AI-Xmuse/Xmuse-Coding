from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="eeg-analyze",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个用于脑电信号(EEG)分析的Python工具包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/eeg-analyze",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/eeg-analyze/issues",
        "Documentation": "https://github.com/your-username/eeg-analyze/tree/main/docs",
    },
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "mne>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    keywords="eeg, brain, signal processing, neuroscience",
) 