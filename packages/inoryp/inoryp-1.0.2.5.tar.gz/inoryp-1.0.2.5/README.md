## Instalar & Importar
* import inoryp
* from inoryp import inoryp
* from inoryp import Inoryp

## Importar (inoryp)
* inoryp.inoryp(0) # IP
* inoryp.inoryp(1) # Status
* inoryp.inoryp(2) # Dictionary

## Importar (Inoryp)
* inoryp.Inoryp().myIP    # IP
* inoryp.Inoryp().myCode  # Status
* inoryp.Inoryp().myDic   # Dictionary

## Como usar, exemplo:
```
import inoryp

informaIP = inoryp.inoryp(0)
print(" Seu IP: " + informaIP)
```
``` Seu IP: 1.1.1.1 ```

## Segundo exemplo:
```
import inoryp

informaIP = inoryp.Inoryp().myIP
print(informaIP)
```
``` Seu IP: 1.1.1.1 ```

# Saiba mais:
* Discord: https://discord.gg/CHsnjZB3Ec