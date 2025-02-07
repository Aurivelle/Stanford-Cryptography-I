from Crypto.Cipher import AES
import binascii


def aes_ctr_encrypt(plaintext, key):
    iv = b"\x00" * 16
    nonce = iv
    counter = 0

    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b""

    for i in range(0, len(plaintext), 16):
        block = plaintext[i : i + 16]
        counter_block = nonce + counter.to_bytes(16, byteorder="big")
        keystream = cipher.encrypt(counter_block)
        encrypted_block = bytes(a ^ b for a, b in zip(block, keystream))
        ciphertext += encrypted_block
        counter += 1
    return nonce + ciphertext


def aes_ctr_decrypt(ciphertext, key):
    iv = ciphertext[:16]
    cipher_blocks = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = b""
    counter = int.from_bytes(iv, byteorder="big")

    for i in range(0, len(cipher_blocks), 16):
        block = cipher_blocks[i : i + 16]
        counter_block = counter.to_bytes(16, byteorder="big")
        keystream = cipher.encrypt(counter_block)
        decrypted_block = bytes(a ^ b for a, b in zip(block, keystream))
        plaintext += decrypted_block
        counter += 1
    return plaintext


key = binascii.unhexlify("36f18357be4dbd77f050515c73fcf9f2")
ciphertext = binascii.unhexlify(
    "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"
)
decrypted_plaintext = aes_ctr_decrypt(ciphertext, key)
print(decrypted_plaintext.decode("latin-1"))
