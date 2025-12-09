import base64

# Paste your Base64 string here
b64_string = "base64_string"

# If the string contains a prefix like: data:image/png;base64,XXXXX
if "," in b64_string:
    b64_string = b64_string.split(",")[1]

# Decode the Base64 string
image_bytes = base64.b64decode(b64_string)

# Save image
output_file = "output.docx"   # change to .jpg if needed

with open(output_file, "wb") as f:
    f.write(image_bytes)

print(f"Image saved as {output_file}")
