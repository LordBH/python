import rsa


pubkey, privkey = rsa.newkeys(2048)

message = b'Hello there !'

# encrypt
crypto = rsa.encrypt(message, pubkey)
print(crypto)

# decrypt
message = rsa.decrypt(crypto, privkey)
print(message)
