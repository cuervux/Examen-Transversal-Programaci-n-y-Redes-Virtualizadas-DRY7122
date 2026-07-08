vlan = int(input("Ingrese la VLAN: "))

if 1 <= vlan <= 1005:
    print("Rango normal")
elif 1006 <= vlan <= 4094:
    print("Rango extendido")
else:
    print("VLAN inválida")