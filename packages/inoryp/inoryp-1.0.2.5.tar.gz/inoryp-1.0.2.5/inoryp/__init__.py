import Raney
import requests

cbanco = {"API_01": "https://sinkable-coils.000webhostapp.com/py.php"}

def getIP(proxy="0", metodo="0"):
    if proxy != "0":
        if(metodo == "http"):
            try:
                proxy_http = {
                    "http": "http://" + str(proxy),
                    "https": "https://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_http).text
            
            except:
                buscarPor = "0.0.0.0" 
            
            return buscarPor

        elif(metodo == "socks5"):
            try:
                proxy_socks5 = {
                    "http": "socks5://" + str(proxy),
                    "https": "socks5://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks5).text

            except:
                buscarPor = "0.0.0.0"
                
            return buscarPor

        elif(metodo == "socks4"):
            try:
                proxy_socks4 = {
                    "http": "socks4://" + str(proxy),
                    "https": "socks4://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks4).text

            except:
                buscarPor = "0.0.0.0"
            
            return buscarPor

        else:
            return "Você precisa informar qual método deseja utilizar: http ou socks5"

    else:
        buscarPor = requests.get(cbanco["API_01"]).text
        return buscarPor

def getCode(proxy="0", metodo="0"):
    if proxy != "0":
        if(metodo == "http"):
            try:
                proxy_http = {
                    "http": "http://" + str(proxy),
                    "https": "https://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_http).status_code
            
            except:
                buscarPor = "0.0.0.0" 
            
            return buscarPor

        elif(metodo == "socks5"):
            try:
                proxy_socks5 = {
                    "http": "socks5://" + str(proxy),
                    "https": "socks5://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks5).status_code
    
            except:
                buscarPor = "0.0.0.0"
                
            return buscarPor

        elif(metodo == "socks4"):
            try:
                proxy_socks4 = {
                    "http": "socks4://" + str(proxy),
                    "https": "socks4://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks4).status_code
                
            except:
                buscarPor = "0.0.0.0"
                
            return buscarPor


        else:
            return "Você precisa informar qual método deseja utilizar: http ou socks5"

    else:
        buscarPor = requests.get(cbanco["API_01"]).status_code
        return buscarPor

def getJSON(proxy="0", metodo="0"):
    if proxy != "0":
        if(metodo == "http"):
            try:
                proxy_http = {
                    "http": "http://" + str(proxy),
                    "https": "https://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_http)
                buscarDicionary = {
                    "IP": buscarPor.text,
                    "Codigo": buscarPor.status_code,
                    "Sessao": Raney.criar(0, "C", 20)
                }
                
            except:
                buscarDicionary = {
                    "IP": "0.0.0.0",
                    "Codigo": "-1",
                    "Sessao": Raney.criar(0, "C", 20)
                }

            return buscarDicionary

        elif(metodo == "socks5"):
            try:
                proxy_socks5 = {
                    "http": "socks5://" + str(proxy),
                    "https": "socks5://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks5)
                buscarDicionary = {
                    "IP": buscarPor.text,
                    "Codigo": buscarPor.status_code,
                    "Sessao": Raney.criar(0, "C", 20)
                }

            except:
                buscarDicionary = {
                    "IP": "0.0.0.0",
                    "Codigo": "-1",
                    "Sessao": Raney.criar(0, "C", 20)
                }
                
            return buscarDicionary

        elif(metodo == "socks4"):
            try:
                proxy_socks4 = {
                    "http": "socks4://" + str(proxy),
                    "https": "socks4://" + str(proxy)
                }
                buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks4)
                buscarDicionary = {
                    "IP": buscarPor.text,
                    "Codigo": buscarPor.status_code,
                    "Sessao": Raney.criar(0, "C", 20)
                }

            except:
                buscarDicionary = {
                    "IP": "0.0.0.0",
                    "Codigo": "-1",
                    "Sessao": Raney.criar(0, "C", 20)
                }
                
            return buscarDicionary

        else:
            return "Você precisa informar qual método deseja utilizar: http ou socks5"

    else:
        buscarPor = requests.get(cbanco["API_01"])
        buscarDicionary = {
            "IP": buscarPor.text,
            "Codigo": buscarPor.status_code,
            "Sessao": Raney.criar(0, "C", 20)
        }
        return buscarDicionary


def inoryp(conteudo=-1, proxy="0", metodo="0"):
    if conteudo == 0:
        if proxy != "0":
            if metodo == "http":
                try:
                    proxy_http = {"http": "http://" + str(proxy),"https": "https://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_http).text
                    return buscarPor

                except:
                    buscarPor = "0.0.0.0"
                    return buscarPor

            elif metodo == "socks5":
                try:
                    proxy_socks5 = {"http": "socks5://" + str(proxy),"https": "socks5://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks5).text
                    return buscarPor
                
                except:
                    buscarPor = "0.0.0.0"
                    return buscarPor
            
            elif metodo == "socks4":
                try:
                    proxy_socks4 = {"http": "socks4://" + str(proxy),"https": "socks4://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks4).text
                    return buscarPor

                except:
                    buscarPor = "0.0.0.0"
                    return buscarPor

            else:
                return " [" + str(metodo) + "] Esse método não é compatível com a livrária."

        else:
            try:
                buscarPor = requests.get(cbanco["API_01"]).text
                return buscarPor

            except:
                buscarPor = "0.0.0.0"
                return buscarPor

    elif conteudo == 1:
        if proxy != "0":
            if metodo == "http":
                try:
                    proxy_http = {"http": "http://" + str(proxy),"https": "https://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_http).status_code
                    return buscarPor

                except:
                    buscarPor = "0.0.0.0"
                    return buscarPor

            elif metodo == "socks5":
                try:
                    proxy_socks5 = {"http": "socks5://" + str(proxy),"https": "socks5://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks5).status_code
                    return buscarPor

                except:
                    buscarPor = "0.0.0.0"
                    return buscarPor
            
            elif metodo == "socks4":
                try:
                    proxy_socks4 = {"http": "socks4://" + str(proxy),"https": "socks4://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks4).status_code
                    return buscarPor

                except:
                    buscarPor = "0.0.0.0"
                    return buscarPor

            else:
                return " [" + str(metodo) + "] Esse método não é compatível com a livrária."

        else:
            buscarPor = requests.get(cbanco["API_01"]).status_code
            return buscarPor

    elif conteudo == 2:
        if proxy != "0":
            if metodo == "http":
                try:
                    proxy_http = {"http": "http://" + str(proxy),"https": "https://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_http)
                    buscarDicionary = {
                        "IP": buscarPor.text,
                        "Codigo": buscarPor.status_code,
                        "Sessao": Raney.criar(0, "C", 20)
                    }
                    return buscarDicionary

                except:
                    buscarDicionary = {
                        "IP": "0.0.0.0",
                        "Codigo": "-1",
                        "Sessao": Raney.criar(0, "C", 20)
                    }
                    return buscarDicionary

            elif metodo == "socks5":
                try:
                    proxy_socks5 = {"http": "socks5://" + str(proxy),"https": "socks5://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks5)
                    buscarDicionary = {
                        "IP": buscarPor.text,
                        "Codigo": buscarPor.status_code,
                        "Sessao": Raney.criar(0, "C", 20)
                    }
                    return buscarDicionary

                except:
                    buscarDicionary = {
                        "IP": "0.0.0.0",
                        "Codigo": "-1",
                        "Sessao": Raney.criar(0, "C", 20)
                    }
                    return buscarDicionary
            
            elif metodo == "socks4":
                try:
                    proxy_socks4 = {"http": "socks4://" + str(proxy),"https": "socks4://" + str(proxy)}
                    buscarPor = requests.get(cbanco["API_01"], proxies=proxy_socks4)
                    buscarDicionary = {
                        "IP": buscarPor.text,
                        "Codigo": buscarPor.status_code,
                        "Sessao": Raney.criar(0, "C", 20)
                    }
                    return buscarDicionary
                
                except:
                    buscarDicionary = {
                        "IP": "0.0.0.0",
                        "Codigo": "-1",
                        "Sessao": Raney.criar(0, "C", 20)
                    }
                    return buscarDicionary

            else:
                return " [" + str(metodo) + "] Esse método não é compatível com a livrária."

        else:
            try:
                buscarPor = requests.get(cbanco["API_01"])
                buscarDicionary = {
                    "IP": buscarPor.text,
                    "Codigo": buscarPor.status_code,
                    "Sessao": Raney.criar(0, "C", 20)
                }
                return buscarDicionary

            except:
                buscarDicionary = {
                    "IP": "0.0.0.0",
                    "Codigo": "-1",
                    "Sessao": Raney.criar(0, "C", 20)
                }
                return buscarDicionary

    else:
        try:
            buscarPor = requests.get(cbanco["API_01"]).text
            return buscarPor

        except:
            buscarPor = "0.0.0.0"
            return buscarPor