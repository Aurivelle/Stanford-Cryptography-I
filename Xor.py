def xor_strings(plaintext, ciphertext_hex):
    try:

        plaintext_bytes = plaintext.encode("ascii")
    except UnicodeEncodeError:
        print(
            "Including non-ASCII characters in the plaintext is not supported. Please re-enter."
        )
        return None

    try:

        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    except ValueError:
        print("Ciphertext is not a valid hexadecimal string. Please re-enter.")
        return None

    min_len = min(len(plaintext_bytes), len(ciphertext_bytes))

    if min_len == 0:
        print("Both plaintext and ciphertext must be non-empty. Please re-enter.")
        return None

    xored_bytes = bytes(
        [plaintext_bytes[i] ^ ciphertext_bytes[i] for i in range(min_len)]
    )

    return xored_bytes.hex()


def main():
    print("=== Tool for Xor the Message and the Ciphertext ===")
    plaintext = input("Please enter the plaintext: ")
    ciphertext_hex = input("Please enter the ciphertext (in hexadecimal): ")

    result = xor_strings(plaintext, ciphertext_hex)
    if result is not None:
        print(f"Result : {result}")


if __name__ == "__main__":
    main()
