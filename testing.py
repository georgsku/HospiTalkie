filename= "./Messages/Ola-1242.wav"

file = filename[filename.rfind("/"):][1:].split("-")[0]
res = file

name = res[0]
print(name)