lol = "hi"

hello = b"hello" + b"$name$" + b"hdello" + b"$name$" + lol.encode()

print(hello[:hello.rfind(b'$name$')])
print(hello[hello.rfind(b'$name$'):][6:].decode())


from base64 import b64encode
import json
# *binary representation* of the base64 string
oo = b"binary content"

in_file = open("notification.wav", "rb") # opening for [r]eading as [b]inary
data = in_file.read()

jsondata= {
    "omg": oo.decode("utf-8")
}

print(json.dumps(jsondata))