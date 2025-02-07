from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii


def pkcs5_pad(data):
    pad_len = 16 - (len(data) % 16)
    padding = bytes([pad_len] * pad_len)
    return data + padding


def pkcs5_unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]


def aes_cbc_encrypt(plaintext, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pkcs5_pad(plaintext)

    ciphertext = b""
    previous_block = iv

    for i in range(0, len(padded_plaintext), 16):
        block = padded_plaintext[i : i + 16]
        xor_block = bytes(a ^ b for a, b in zip(block, previous_block))
        encrypted_block = cipher.encrypt(xor_block)
        ciphertext += encrypted_block
        previous_block = encrypted_block
    return iv + ciphertext


def aes_cbc_decrypt(ciphertext, key):
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext_blocks = ciphertext[16:]
    plaintext = b""
    previous_block = iv
    for i in range(0, len(ciphertext_blocks), 16):
        block = ciphertext_blocks[i : i + 16]
        decrypted_block = cipher.decrypt(block)
        plaintext_block = bytes(a ^ b for a, b in zip(decrypted_block, previous_block))
        plaintext += plaintext_block
        previous_block = block
    return pkcs5_unpad(plaintext)


key = binascii.unhexlify("140b41b22a29beb4061bda66b6747e14")
print(key, len(key))
ciphertext_hex = "5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253"
ciphertext = binascii.unhexlify(ciphertext_hex)

plaintext = aes_cbc_decrypt(ciphertext, key)
print(plaintext.decode())
