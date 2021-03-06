import requests, json, os, datetime, sqlite3, logging, time
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from sys import argv
from statistics import mean

""" INFO
last: preço em Reais baseado no último trade de cada exchange e ponderado pelo volume do período
high: maior valor em Reais de uma operação no período
low: menor valor em Reais de uma operação no período
vol: volume em BTC de operações no período
"""

def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


def log(timestamp, mode, message):
    if(not os.path.isdir("data/")):
        os.mkdir("config")

    if(timestamp == None):
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

    else:
        LOG_FORMAT = "%(levelname)s {0} - %(message)s".format(timestamp)
    
    logging.basicConfig(filename = "data/logg.log",
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

def save_last(last):
    if(not os.path.isdir("data/")):
        os.mkdir("config")
    
    with open("data/lasts.txt", "a+") as f:
        f.write(last + "\n")


def request_API():

    url = "https://api.blinktrade.com/api/v1/BRL/ticker"
    try:
        timestamp = time.time()
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
        request_date = convert_timestamp(timestamp)

        foxbit_vol = data["vol"]
        foxbit_high = data["high"]
        foxbit_sell = data["sell"]
        foxbit_low = data["low"]
        foxbit_buy = data["buy"]
        foxbit_last = data["last"] 

        print(request_date ,"->", "HIGH:", foxbit_high, "- LOW:", foxbit_low, "- LAST: ", foxbit_last)


        log(request_date, "INFO", str(data))
        save_last(str(foxbit_last))

        return foxbit_last


def send_mail(send_from, send_to, subject, text):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    with open("data/logg.log", "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename("data/logg.log")
        )
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="data/logg.log"'
    msg.attach(part)


    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()

    # Email e senha da Eliza, por favor não utilizar #
    smtp.login('elizabot123@gmail.com','boteliza123')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


def media(n, offset=None):
    with open("data/lasts.txt") as f:
        avg_line_length = 74
        to_read = n + (offset or 0)

        while 1:
            try:
                f.seek(-(avg_line_length * to_read), 2)
            except IOError:
                # woops.  apparently file is smaller than what we want
                # to step back, go to the beginning instead
                f.seek(0)
            pos = f.tell()
            lines = f.read().splitlines()
            if len(lines) >= to_read or pos == 0:
                lista = lines[-to_read:offset and -offset or None]
                break
            avg_line_length *= 1.3

        new = []
        for i in lista:
            new.append(float(i))
        return(mean(new))

def calcula_percentage(novo, antigo):
    x = (novo*100)/antigo
    if(novo > antigo):
        x = x-100
    else:
        x = 100 - x
    return X

if __name__ == "__main__":

    while(1):
        preco_bitcoin = request_API()
        time.sleep(60) # new requisition every 1 minute

        num_lines = sum(1 for line in open('data/lasts.txt'))
        numero_de_minutos = 15

        if(num_lines % numero_de_minutos == 0):
            hora = convert_timestamp(time.time())
            media_preco_bitcoin = media(numero_de_minutos)
            if(len(argv) > 2):
                try:
                    send_mail("elizabot123@gmail.com", argv[1], "Média dos bitcoins"
                            , "eae men kkk, A média do bitcoin nos últimos "+ str(numero_de_minutos) + ' minutos, foi: R$' +
                             str(media_preco_bitcoin) + "\nDATA DA CHECAGEM:" + str(hora))
                except:
                    log(hora, "ERROR", "Erro ao enviar email para: " + argv[1])

            else:
                try:
                    send_mail("elizabot123@gmail.com", "tarcisio_marinho09@hotmail.com", "Média dos bitcoins"
                            , "eae men kkk, A média do bitcoin nos últimos "+ str(numero_de_minutos) + ' minutos, foi: R$' + 
                            str(media_preco_bitcoin) + "\nDATA DA CHECAGEM:" + str(hora))
                except:
                    log(hora, "ERROR", "Erro ao enviar email para: tarcisio_marinho09@hotmail.com")

                try:
                    send_mail("elizabot123@gmail.com", "felix_ruan09@hotmail.com", "Média dos bitcoins"
                            , "eae men kkk, A média do bitcoin nos últimos "+ str(numero_de_minutos) + ' minutos, foi: R$' + 
                            str(media_preco_bitcoin) + "\nDATA DA CHECAGEM:" + str(hora))
                except:
                    log(hora, "ERROR", "Erro ao enviar email para: felix_ruan09@hotmail.com")
