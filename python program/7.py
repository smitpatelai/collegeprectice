#open

file1 = open("AHMADBAD.txt","r").read()
print(file1)

# write
file2 = open("AHMADBAD.txt","w")
data=file2.write("Surat")

#read

file3 = open("AHMADBAD.txt","r").read()
print(file3)

file4 = open("AHMADBAD.txt","a")
file4.write(" Mumbai")

file5 = open("AHMADBAD.txt","r").read()
print(file5)


# file right to /n
#DELHI ---> STARTING