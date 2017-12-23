import requests, json, os, datetime, sqlite3, logging, time
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from sys import argv

""" INFO
last: preço em Reais baseado no último trade de cada exchange e ponderado pelo volume do período
high: maior valor em Reais de uma operação no período
low: menor valor em Reais de uma operação no período
vol: volume em BTC de operações no período
vwap: preço médio em Reais no período (volume weighted average price)
money: volume em Reais de operações no período
trades: número de operações no período
open: preço da primeira operação naquela exchange no período
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

def save_open(last):
    if(not os.path.isdir("config/")):
        os.mkdir("config")
    
    with open("config/opens.txt", "a+") as f:
        f.write(last + "\n")

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

        # datetime
        request_date = convert_timestamp(data["timestamp"]["exchanges"]["FOX"])

        #dict
        foxbit_exchanges_1h = data["ticker_1h"]["exchanges"]["FOX"]

        # all features
        foxbit_last = foxbit_exchanges_1h["last"]
        foxbit_high = foxbit_exchanges_1h["high"]
        foxbit_low = foxbit_exchanges_1h["low"]
        foxbit_vol = foxbit_exchanges_1h["vol"]
        foxbit_vwap = foxbit_exchanges_1h["vwap"]
        foxbit_money = foxbit_exchanges_1h["money"]
        foxbit_trades = foxbit_exchanges_1h["trades"]
        foxbit_open = foxbit_exchanges_1h["open"]


        log(request_date, "INFO", str(foxbit_exchanges_1h))
        save_open(str(foxbit_open))
        
    elif(req.status_code == 304):
        log(None, "WARNING", "Nenhuma alteracao ocorrida desde a última checagem.")
    
    elif(req.status_code == 429):
        log(None, "CRITICAL", "Muitas requisições feitas, se continuar, não poderá fazer mais checagens.")


def send_mail(send_from, send_to, subject, text):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    with open("config/logg.log", "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename("config/logg.log")
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="config/logg.log"'
    msg.attach(part)


    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()

    # Email e senha da Eliza, por favor não utilizar #
    smtp.login('elizabot123@gmail.com','boteliza123')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == "__main__":

    while(1):
        request_API()
        time.sleep(60) # new requisition every 1 minute

        num_lines = sum(1 for line in open('config/opens.txt'))

        if(num_lines % 60 == 0):
            hora = convert_timestamp(time.time())
            if(len(argv) > 2):
                try:
                    send_mail("elizabot123@gmail.com", argv[1], "oi, eu tenho atualizacoes"
                            , "eae men kkk, cheque as atualizacoes de como estao os bitcoins kkk - " + str(hora))
                except:
                    log(hora, "ERROR", "Erro ao enviar email para: " + argv[1])

            else:
                try:
                    send_mail("elizabot123@gmail.com", "tarcisio_marinho09@hotmail.com", "oi, eu tenho atualizacoes"
                            , "eae men kkk, cheque as atualizacoes de como estao os bitcoins kkk - " + str(hora))
                except:
                    log(hora, "ERROR", "Erro ao enviar email para: tarcisio_marinho09@hotmail.com")

                try:
                    send_mail("elizabot123@gmail.com", "felix_ruan09@hotmail.com", "oi, eu tenho atualizacoes"
                            , "eae men kkk, cheque as atualizacoes de como estao os bitcoins kkk - " + str(hora))
                except:
                    log(hora, "ERROR", "Erro ao enviar email para: felix_ruan09@hotmail.com")