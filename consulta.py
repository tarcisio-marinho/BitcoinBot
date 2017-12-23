import requests, json, os, datetime, sqlite3, logging


def log(timestamp, mode, message):
    if(not os.path.isdir("config/")):
        os.mkdir("config")

    if(timestamp == None):
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

    else:
        LOG_FORMAT = "%(levelname)s {0} - %(message)s".format(timestamp)
    
    logging.basicConfig(filename = "config/logg.log",
                        level=logging.DEBUG,
                        format=LOG_FORMAT)
    logger = logging.getLogger()
    if(mode == "DEBUG"):
        logger.debug(message)
    
    elif(mode == "INFO"):
        logger.info(message)
    
    elif(mode == "WARNING"):
        logger.warning(message)
    
    elif(mode == "ERROR"):
        logger.error(message)

    elif(mode == "CRITICAL"):
        logger.critical(message)


# fazer no maximo 1 requisição por minuto
def request_API():
    url = "https://api.bitvalor.com/v1/ticker.json"
    try:
        req = requests.get(url)
    except requests.exceptions.ConnectionError:
        log(None, "ERROR", "Sem conexão com a internet.")
    except:
        log(None, "ERROR", "Algum erro desconhecido com a checagem da API ocorreu.")
        return

    if (req.status_code == 200):
        data = json.loads(req.text)
        
        timestamp = data["timestamp"]["exchanges"]["FOX"]
        date = convert_timestamp(timestamp)
        
        print(timestamp, date)
        log(date, "INFO", "checou o preco do bitcoin")
    elif(req.status_code == 304):
        log(None, "WARNING", "Nenhuma alteracao ocorrida desde a última checagem.")
    
    elif(req.status_code == 429):
        log(None, "CRITICAL", "Muitas requisições feitas, se continuar, não poderá fazer mais checagens.")


def file():
    f = open("data.json")
    data = f.read()
    data = json.loads(data)
        
    timestamp = data["timestamp"]["exchanges"]["FOX"]
    date = convert_timestamp(timestamp)

    


def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    request_API()
    #file()
    pass