## Instalar & Importar
* import inoryp
* from inoryp import inoryp
* from inoryp import Inoryp

## Importar (inoryp)
* inoryp.inoryp(0) # IP
* inoryp.inoryp(1) # Status
* inoryp.inoryp(2) # Dictionary

## Importar (Inoryp) com Proxies
* inoryp.inoryp(0, "localhost:9150", "socks5") # IP
* inoryp.inoryp(1, "localhost:9150", "socks5") # Status
* inoryp.inoryp(2, "localhost:9150", "socks5") # Dictionary

## Importar Funções:
* inoryp.getIP()     # IP
* inoryp.getCode()   # Status
* inoryp.getJSON()   # Dictionary

## Importar Funções com Proxies
* inoryp.getIP("localhost:9150", "socks5")     # IP
* inoryp.getCode("localhost:9150", "socks5")   # Status
* inoryp.getJSON("localhost:9150", "socks5")   # Dictionary

## Suporte para Proxys
* http & https
* socks5
* socks4

## Exemplo sem proxy
```

import inoryp

informaIP = inoryp.inoryp(0)
print(" Seu IP: " + informaIP)

```
``` Seu IP: 1.1.1.1 ```

## Segundo exemplo, sem proxy:
```

import inoryp

informaIP = inoryp.getIP()
print(" Seu IP: " + informaIP)

```
``` Seu IP: 1.1.1.1 ```

## Exemplo com proxy:
```

import inoryp

informaIP_Proxy = inoryp.inoryp(0, "localhost:9150", "socks5")
print(" Seu IP: " + informaIP_Proxy)

```
``` Seu IP: 45.12.32.1 ```

## Segundo exemplo, com proxy:
```

import inoryp

informaIP_Proxy = inoryp.getIP("localhost:9150", "socks5")
print(" Seu IP: " + informaIP_Proxy)

```
``` Seu IP: 45.12.32.1 ```

# Saiba mais:
* Discord: https://discord.gg/CHsnjZB3Ec