import hashlib

def compute_file_hash(file_path):
    BLOCK_SIZE = 1024
    with open(file_path, 'rb') as f:
        blocks = []
        while True:
            block = f.read(BLOCK_SIZE)
            if not block :
                break
            blocks.append(block)
    h=b''
    for block in reversed(blocks):
        hasher = hashlib.sha256()
        hasher.update(block + h)
        h = hasher.digest()
    return h.hex()
file_path = "C:\\Users\\USER\\Downloads\\6.1.intro.mp4_download"
h0_hash = compute_file_hash(file_path)
print(h0_hash)
