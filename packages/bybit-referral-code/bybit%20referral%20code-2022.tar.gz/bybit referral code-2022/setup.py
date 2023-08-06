import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 bybit referral code
    name="bybit referral code", 
    version="2022",
    author="bybit referral code",
    author_email="bonus2@bybit.com",
    description="bybit referral code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.bybit.com/en-US/invite?ref=XQRLGO",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
