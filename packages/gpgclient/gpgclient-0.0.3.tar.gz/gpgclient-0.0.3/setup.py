from setuptools import setup, find_packages
setup(name="gpgclient",
        version="0.0.3",
        author="cpearce",
        author_email="christopherpearce10@gmail.com",
        packages=find_packages(where=".", include="*"),
        install_requires=["google-cloud-storage>=1.42.3", "python-gnupg>=0.4.8", "google-api-python-client>=2.27.0"]
)