import random

pas = ""
for y in range(18):
    pas += random.choice("abcdef0123456789")
print(f"0000000000000000000000000000000000000000000000{pas}")
