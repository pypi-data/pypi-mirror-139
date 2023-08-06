## rsa_python

This module implements the RSA encryption algorithm. Functions included are `generate_key_pair(bits)` which returns a dictionary containing p, q, phi, public, private, modulus, and the time it took to generate the key pair ("time"). `encrpyt(message, encryption_key, modulus)` to encrypt a message, and `decrypt(cipher, decryption_key, modulus)` to decrypt a cipher. To install the module, run `pip install python_rsa`. Below is an example how to use the module.

```python
from rsa_python import rsa
key_pair = rsa.generate_key_pair(1024)
cipher = rsa.encrypt("Hello World!", key_pair["public"], key_pair["modulus"])
decrypted_message = rsa.decrypt(cipher, key_pair["private"], key_pair["modulus"])
print(decrypted_message)
```