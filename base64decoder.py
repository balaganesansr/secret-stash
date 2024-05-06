import base64
x = input("Enter the hash value : ").encode()
decoded = base64.b64decode(x).decode()
print(decoded)
