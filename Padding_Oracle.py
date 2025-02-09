import urllib.request
import urllib.error    
import binascii

TARGET = "http://crypto-class.appspot.com/po?er="
CIPHERTEXT = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"

BLOCK_SIZE = 16

def split_blocks(ciphertext, size):
    return [ciphertext[i:i + size * 2] for i in range(0, len(ciphertext), size * 2)]

class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib.parse.quote(q)
        req = urllib.request.Request(target)
        try:
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return True
            return False
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))
def decrypt_block(po, prev_block, curr_block):
    decrypted_block = [0] * BLOCK_SIZE
    modified_block = list(prev_block)

    for padding_value in range(1, BLOCK_SIZE + 1):
        print(f"正在處理第 {padding_value} 個字節...")
        for guess in range(256):
            modified_block[-padding_value] = guess

            for i in range(1, padding_value):
                modified_block[-i] = decrypted_block[-i] ^ padding_value
            test_cipher = bytes(modified_block) + curr_block
            test_cipher_hex = binascii.hexlify(test_cipher).decode()

            if po.query(test_cipher_hex):
                decrypted_byte = guess ^ padding_value
                decrypted_block[-padding_value] = decrypted_byte
                print(f"找到第 {padding_value} 個字節：{decrypted_byte:02x}")
                break
    return bytes(decrypted_block)

if __name__ == "__main__":
    ciphertext_blocks = split_blocks(CIPHERTEXT, BLOCK_SIZE)
    po = PaddingOracle()

    decrypted_message = b''

    for i in range(1, len(ciphertext_blocks)):
        prev_block = binascii.unhexlify(ciphertext_blocks[i - 1])
        curr_block = binascii.unhexlify(ciphertext_blocks[i])
        decrypted_block = decrypt_block(po, prev_block, curr_block)
        decrypted_message += xor_bytes(decrypted_block, prev_block)
    print(decrypted_message.decode())
