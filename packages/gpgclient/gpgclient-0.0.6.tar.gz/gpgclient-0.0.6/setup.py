from setuptools import setup, find_packages
setup(name="gpgclient",
        version="0.0.6",
        author="chris pearce",
        author_email="christopher.pearce@bt.com",
        maintainer="cpearce",
        maintainer_email="christopher.pearce@bt.com",
        description="GPG Wrapper Client for leveraging gpg functionality with gcs",
        long_description= open("README.md", "r").read(),
        long_description_content_type='text/markdown',
        packages=['gpg_client'],
        install_requires=["google-cloud-storage>=1.42.3", "python-gnupg>=0.4.8", "google-api-python-client>=2.27.0"],
        include_package_data=True
)