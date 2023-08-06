from gnupg import GPG
from google.cloud import storage
from googleapiclient.discovery import build
import os


class Client():
    def __init__(self, non_root_user: str) -> None:
        self._non_root_user = non_root_user
        self._gpghome = f"/home/{self._non_root_user}/.gnupg"
        if not os.path.exists(self._gpghome):
            print(f"gpg directory for user {self._non_root_user} does not exist. Creating directory - {self._gpghome}")
            os.mkdir(self._gpghome)
        self._gpg = GPG(gnupghome=self._gpghome)
        self._gpg.encoding='utf-8'
        self._storage_client = storage.Client()
        self._storage_api = build("storage", "v1")
        
    @property
    def non_root_user(self) -> str:
        """Gets the non_root_user attribute"""
        return self._non_root_user
    
    @property
    def gpghome(self) -> str:
        """Gets the gpghome instance attribute"""
        return self._gpghome
    
    @gpghome.setter
    def gpghome(self, value: str) -> None:
        """Sets the gpghome instance attribute to a new value"""
        self._gpghome=value
    
    @non_root_user.setter
    def non_root_user(self, value: str) -> None:
        """Sets the non_root_user instance attribute to a new value"""
        self._non_root_user = value
        
    def generate_keys(self, email: str, passphrase: str, key_length: int=1024):
        """Generate a new public/private key pair for the given email"""
        input_data = self._gpg.gen_key_input(
            name_email=email,
            passphrase=passphrase,
            key_type="RSA",
            key_length= key_length
        )
        return self._gpg.gen_key(input_data)

    def list_keys(self) -> list:
        """List out the known keys to the current instance"""
        return self._gpg.list_keys()

    def export_public_key(self, keyids: str) -> str:
        """Returns a public key as a str"""
        return self._gpg.export_keys(keyids=keyids, secret=False)

    def export_private_key(self, keyids: str, passphrase: str) -> str:
        """Returns a private key as a str"""
        return self._gpg.export_keys(keyids=keyids, secret=True, passphrase=passphrase)

    def export_public_key_to_file(self, keyids: str) -> None:
        """Writes a public key to a file"""
        pub_key = self._gpg.export_keys(keyids=keyids, secret=False)
        with open(f"{self._non_root_user}_pub_key.asc", "w") as keyfile:
            keyfile.write(pub_key)

    def export_private_key_to_file(self, keyids: str, passphrase: str) -> None:
        """Writes a private key to a file"""
        priv_key = self._gpg.export_keys(keyids=keyids, secret=True, passphrase=passphrase)
        with open(f"{self._non_root_user}_priv_key.asc", "w") as keyfile:
            keyfile.write(priv_key)
            
    def import_public_key_from_file(self, keyfile: str) -> None:
        """Import a public key from a file into the current instance"""
        with open(keyfile, "r") as file:
            keydata = file.read()
            import_result = self._gpg.import_keys(key_data=keydata)
            self._gpg.trust_keys(import_result.fingerprints, "TRUST_ULTIMATE")
            
    def import_public_key_from_gcs(self, bucket_name: str, blob_name: str) -> None:
        """Import a public key from gcs into the current instance"""
        bucket = self._storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name).download_as_bytes()
        keydata = blob.decode()
        import_result = self._gpg.import_keys(key_data=keydata)
        self._gpg.trust_keys(import_result.fingerprints, "TRUST_ULTIMATE")
        
    def export_public_key_to_gcs(self, keyids: str, bucket_name: str, blob_name: str) -> None:
        """Write a public key to gcs passing the destination bucket/blob_name"""
        pub_key = self._gpg.export_keys(keyids=keyids, secret=False)
        bucket = self._storage_client.bucket(bucket_name=bucket_name)
        bucket.blob(blob_name=blob_name).upload_from_string(pub_key)
        
    def export_private_key_to_gcs(self, keyids: str, passphrase: str, bucket_name: str, blob_name: str) -> None:
        """Write a private key to gcs passing the destination bucket/blob_name"""
        priv_key = self._gpg.export_keys(keyids=keyids, secret=True, passphrase=passphrase)
        bucket = self._storage_client.bucket(bucket_name=bucket_name)
        bucket.blob(blob_name=blob_name).upload_from_string(priv_key)
        
    def encrypt_file(self, filename: str, recipient: str, output: str) -> None:
        """Encrypts a single file"""
        with open(filename,"r") as f:
            status = self._gpg.encrypt_file(file=f, recipients=[recipient], output=output)
            print(status.ok)
            print(status.status)
            print(status.stderr)
            
    def decrypt_file(self, filename: str, passphrase: str, output: str) -> None:
        """Decrypts a single file"""
        with open(filename, "r") as f:
            status = self._gpg.decrypt_file(file=f, passphrase=passphrase, output=output)
            print(status.ok)
            print(status.status)
            print(status.stderr)
    
    def encrypt_blobs(self, bucket_name: str, blob_prefix: str, email: str, output_folder: str="encrypted") -> None:
        """Encrypts gcs objects meeting the blob_prefix criteria"""
        request = self._storage_api.objects().list(bucket=bucket_name, prefix=blob_prefix)
        response = request.execute()
        bucket = self._storage_client.bucket(bucket_name)
        for obj in response['items']:
            status = self._gpg.encrypt(data=bucket.blob(obj['name']).download_as_bytes().decode(),
                                         recipients=[email],
                                         armor=True)
            print(status.ok)
            print(status.status)
            print(status.stderr)
            bucket.blob(f"{output_folder}/{obj['name'].split('/')[-1]}").upload_from_string(status.data.decode())
            
    def decrypt_blobs(self, bucket_name: str, blob_prefix: str, passphrase: str, output_folder: str="decrypted") -> None:
        """Decrypts gcs objects meeting the blob_prefix criteria"""
        request = self._storage_api.objects().list(bucket=bucket_name, prefix=blob_prefix)
        response = request.execute()
        bucket = self._storage_client.bucket(bucket_name)
        for obj in response['items']:
            status = self._gpg.decrypt(bucket.blob(obj['name']).download_as_bytes().decode(), passphrase=passphrase)
            print(status.ok)
            print(status.status)
            print(status.stderr)
            bucket.blob(f"{output_folder}/{obj['name'].split('/')[-1]}").upload_from_string(status.data.decode())
            
    def remove_public_key(self, fingerprints: str) -> None:
        """Removes the public key from the current GPGClient instance"""
        self._gpg.delete_keys(fingerprints=fingerprints, secret=False)

    def remove_private_key(self, fingerprints: str, passphrase: str) -> None:
        """Removes the private key from the current GPGClient instance"""
        self._gpg.delete_keys(fingerprints=fingerprints, secret=True, passphrase=passphrase)