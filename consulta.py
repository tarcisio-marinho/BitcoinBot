import requests, json, os, datetime, sqlite3, logging, time

""" INFO
last: preço em Reais baseado no último trade de cada exchange e ponderado pelo volume do período
high: maior valor em Reais de uma operação no período
low: menor valor em Reais de uma operação no período
vol: volume em BTC de operações no período
vwap: preço médio em Reais no período (volume weighted average price)
money: volume em Reais de operações no período
trades: número de operações no período

"""

def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


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
        return

    except:
        log(None, "ERROR", "Algum erro desconhecido com a checagem da API ocorreu.")
        return

    if (req.status_code == 200):
        data = json.loads(req.text)
         
        request_date = convert_timestamp(data["timestamp"]["exchanges"]["FOX"])

        foxbit_exchanges_1h = data["ticker_1h"]["exchanges"]["FOX"]

        foxbit_open = data["ticker_1h"]["exchanges"]["FOX"]["open"]
        foxbit_last = data["ticker_1h"]["exchanges"]["FOX"]["last"]
        foxbit_vwap = data["ticker_1h"]["exchanges"]["FOX"]["vwap"]
        foxbit_money = data["ticker_1h"]["exchanges"]["FOX"]["money"]
        foxbit_high = data["ticker_1h"]["exchanges"]["FOX"]["high"]
        foxbit_low = data["ticker_1h"]["exchanges"]["FOX"]["low"]
        foxbit_trades = data["ticker_1h"]["exchanges"]["FOX"]["trades"]
        foxbit_vol = data["ticker_1h"]["exchanges"]["FOX"]["vol"]

        print(foxbit_high, foxbit_last, foxbit_low, foxbit_money, 
              foxbit_open, foxbit_open, foxbit_trades, foxbit_vol, foxbit_vwap)

        log(request_date, "INFO", "checou o preco do bitcoin")
        
    elif(req.status_code == 304):
        log(None, "WARNING", "Nenhuma alteracao ocorrida desde a última checagem.")
    
    elif(req.status_code == 429):
        log(None, "CRITICAL", "Muitas requisições feitas, se continuar, não poderá fazer mais checagens.")


    
if __name__ == "__main__":

    while(1):
        request_API()
        time.sleep(60) # new requisition every 1 minute
    
    pass