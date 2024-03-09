# Function to perform XOR encryption
def xor_encryption(text, key):
    # Initialize an empty string for encrypted text
    encrypted_text = ""
    
    # Iterate over each character in the text
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    
    # Return the encrypted text
    return encrypted_text

def encryptXOR(var, key):
    return bytes(a ^ b for a, b in zip(var,key))

# The plaintext that we want to encrypt
plain_text = "V3JpdGUtSG9zdCAncHduZWQzMicK"
# The secret key used for encryption
key = "123"
keyRepeat = (len(plain_text) // len(key)+1)*key

# Encrypt the plain_text using the key
encrypted_text = xor_encryption(plain_text, key)
unencrypted_text = xor_encryption(encrypted_text, key)

encrypted_textBytes = encryptXOR(bytes(plain_text, encoding='ASCII'), bytes(keyRepeat, encoding='ASCII'))
decoded_encrypted_textBytes = encrypted_textBytes.decode("ASCII")
decoded_encrypted_textBytes = str(encrypted_textBytes, encoding = "ASCII")
unencrypted_textBytes = encryptXOR(encrypted_textBytes, bytes(keyRepeat, encoding='ASCII'))
# Print the encrypted text
print(f'Encrypted Text: {encrypted_text}')
print(f'UNEncrypted Text: {unencrypted_text}')

print(f'Bytes Encrypted Text: {encrypted_textBytes}')
print(f'Decoded: {decoded_encrypted_textBytes}')
print(f'Bytes UNEncrypted Text: {unencrypted_textBytes}')
