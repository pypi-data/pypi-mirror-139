from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "An AES encryption module."
setup(
    name= "better cryptography",
    author = 'Wyatt Garrioch',
    author_email = "w.garrioch456@gmail.com",
    version = VERSION,
    description = DESCRIPTION,
    long_description = open("/home/eternal_blue/better_cryptography/README.md").read(),
    long_description_content_type="text/markdown",
    packages = find_packages(),
    install_requires = ['pycryptodome', "rsa"],
    keywords=["python", "encryption", "AES", "first package"],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux"
    ]
    
)