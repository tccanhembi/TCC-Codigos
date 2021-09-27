# TCC Anhembi Morumbi - Grupo Engenharia Elétrica Noturno

import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pyodbc
import socket


# Estabelecendo variáveis

temperatura_max = 7.0

temperatura_0 = 0.0
temperatura_1 = 0.0
temperatura_2 = 0.0

Tempo_Porta_0 = 0
Tempo_Porta_1 = 0
Tempo_Porta_2 = 0


Tempo_Temperatura_0 = 0
Tempo_Temperatura_1 = 0
Tempo_Temperatura_2 = 0



dados_coletados = []
dados_separados_error = []
Envios_0 = 0
Envios_1 = 1
Envios_2 = 0

IDs = []
IDs.insert(0, "QMpHfZ")
IDs.insert(1, "0nHwXx")
IDs.insert(2, "Victor")

"""Gerado em : https://www.4devs.com.br/gerador_de_senha"""

ID_Atual = "idatual"
NivelBateriaAtual_0 = "bateriaatual"
NivelBateriaAtual_1 = "bateriaatual"
NivelBateriaAtual_2 = "bateriaatual"


# Define o socket. Onde "0.0.0.0" significa "qualquer IP", na porta "8091".
s = socket.socket()
s.bind(('0.0.0.0', 8091 ))
s.listen(0)


# Definição função email porta aberta, será chamada para enviar um e-mail de alerta de porta aberta
def email_porta_aberta():
        username = "victoranhembirezende@gmail.com"
        password = "uvjqubhxwytbbkkt"
        mail_from = "victoranhembirezende@gmail.com"
        mail_to = "victorfrezende@hotmail.com"
        mail_subject = f'#ID {ID_Atual}Fora de conformidade - Porta Aberta'
        mail_body = "Atenção, a porta do refrigerador está aberta por mais de 1 minuto"
        mimemsg = MIMEMultipart()
        mimemsg['From'] = mail_from
        mimemsg['To'] = mail_to
        mimemsg['Subject'] = mail_subject
        mimemsg.attach(MIMEText(mail_body, 'plain'))
        connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
        connection.starttls()
        connection.login(username, password)
        connection.send_message(mimemsg)
        connection.quit()

# Definição função email temperatura, será chamada para enviar um e-mail de alerta de temperatura
def email_temperatura():
    username = "victoranhembirezende@gmail.com"
    password = "uvjqubhxwytbbkkt"
    mail_from = "victoranhembirezende@gmail.com"
    mail_to = "victorfrezende@hotmail.com"
    mail_subject = f'#ID {ID_Atual}Fora de conformidade - Temperatura'
    mail_body = "Atenção, a Temperatura ultrapassou o limite estabelecido"
    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    mimemsg['Subject'] = mail_subject
    mimemsg.attach(MIMEText(mail_body, 'plain'))
    connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()

# Definição função email bateria, será chamada para enviar um e-mail de alerta de bateria baixa
def email_bateria():
    username = "victoranhembirezende@gmail.com"
    password = "uvjqubhxwytbbkkt"
    mail_from = "victoranhembirezende@gmail.com"
    mail_to = "victorfrezende@hotmail.com"
    mail_subject = f'A Bateria do seu dispoditivo de ID# {ID_Atual} está muito baixa'
    mail_body = "Atenção, a bateria do seu dispositivo está baixa"
    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    mimemsg['Subject'] = mail_subject
    mimemsg.attach(MIMEText(mail_body, 'plain'))
    connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()

# Formula de erro para que o programa não seja encerrado
def error():
    print("Entrando na formula de error()")
    print('')
    print("voltando a coletar os dados")
    coletadados()

# Fórmula principal, onde fica "escutando" e aguardando alguem se comunicar com o computador
def coletadados():
    while 1:
        time.sleep(1)
        client, addr = s.accept()
        while True:
            content = client.recv(2048)

            if len(content) == 0:

                break

# Caso seja recebido algum conteúdo:

            else:

                print(content)
                # Transforma o dado coletado em uma String
                as_string = str(content)
                # Verifica-se o tamanho da String
                print(f'O Tamanho da String Recebida foi de : {len(content)}')
                # O dado correto para ser tratado, deve, necessariamente, conter 259 caracteres
                if len(content) == 259:
                    # Aqui separamos a String pelo caracter "<" e adicionamos em uma lista chamada dados_separados
                    # Cada dado é colocado em um elemento, exemplo:
                    # <Victor<Teste, é criado uma lista de 2 elementos, sendo: (Victor, Teste)
                    dados_separados = as_string.split("<")
                    print(len(dados_separados))

                    # Faz-se um double check, porque a lista deve ter necessariamente 7 elementos.
                    # Caso ela tenha uma quantidade de elementos diferentes de 7, entrará na função error().
                    if len(dados_separados) != 7:
                        print("Comando Post fora de conformidade")
                        client.close()
                        error()

                    # Caso os dados estejam corretos,atribuimos o valor da lista de dados_separados para dados_coletados

                    global dados_coletados
                    dados_coletados = dados_separados
                    global ID_Atual
                    ID_Atual = dados_separados[3]

                    # Por motivos de segurança,o código irá verificar se o ID enviado via comando Post é um ID permitido

                    # Caso o ID fornecido esteja na lista permitida, seguiremos com o código

                    if ID_Atual in IDs:
                        print(f'ID Atual: {ID_Atual}')
                        # Atualiza dados é a função que coletará e tratará o dado fornecido pela ESP32.
                        atualiza_dados()

                    else:
                        print(f'ID: {dados_coletados[3]} Não Reconhecido')
                # Caso a quantidade de caracteres seja diferente de 259, entraremos na fórmula de error().
                else:
                    error()

        client.close()
        print("Operação finalizada.")


# Função de tratamento de dados, responsável por organizar os dados em suas variáveis corretas.

def atualiza_dados():

    """ID # 0"""
    # Temos na lista "dados_coletados" a seguinte organização e indexação: (Veja que o tamanho da lista é = 7)
    # Lista: (dados do cabeçalho http,Status porta, Temperatura, ID, Tensão, Data e Hora, restante dos dados)
    # Index: (_________0____________,_______1_____,_____2______,_3_,__4___,______5______,________6__________)

    # Função "if" para validar se o ID coletado foi o 0 (neste caso o ID 0 é : QMpHfZ)

    if dados_coletados[3] == IDs[0]:

        temperatura_0 = float(dados_coletados[2])
        global NivelBateriaAtual_0
        NivelBateriaAtual_0 = dados_coletados[4]
        NivelBateriaAtual_0 = float(dados_coletados[4])

        # Estabelece os parâmetros de bateria Alta, Média e Baixa

        if NivelBateriaAtual_0 >= 4.00:
            bateria = str("Alta")
        if 3.8 < NivelBateriaAtual_0 < 4.0:
            bateria = str("Média")
        if NivelBateriaAtual_0 <= 3.8:
            bateria = str("Baixa")

        if (dados_coletados[1]) == "aberta":
            porta = "Aberta"
            global Tempo_Porta_0
            # Faz o incremento na variável "Tempo_Porta" a cada vez que recebe a informação de porta aberta.
            Tempo_Porta_0 = Tempo_Porta_0 + 1

        else:
            # Zera o valor de "Tempo_Porta" caso a porta tenha sido fechada.

            porta = "Fechada"
            Tempo_Porta_0 = 0

        if Tempo_Porta_0 >= 10:
            # Caso seja recebido o valor de Porta Aberta durante 10 verificações,envia-se um e-mail ao responsável

            email_porta_aberta()
            print(f'Atingimos o tempo máximo de Porta Aberta: {Tempo_Porta_0}s .')
            print('Um e-mail de alerta de Porta Aberta foi enviado.')
            # Após o envio de e-mail, é zerado o valor de Tempo Porta para que a contagem recomece.

            Tempo_Porta_0 = 0

        if temperatura_0 >= temperatura_max:
            global Tempo_Temperatura_0
            # Faz o incremento na variável "Tempo_Temperatura" cada vez que recebe a informação de Temperatura excedida
            Tempo_Temperatura_0 = Tempo_Temperatura_0 + 1

        else:
            Tempo_Temperatura_0 = 0

        if Tempo_Temperatura_0 >= 10:
            # Caso seja recebido o valor de Temp excedida durante 10 verificações,envia-se um e-mail ao responsável
            email_temperatura()
            print(f'Atingimos o tempo máximo de Temperatura excedida: {Tempo_Temperatura_0}s .')
            print('Um e-mail de alerta de Temperatura foi enviado.')
            Tempo_Temperatura_0 = 0

        # Uma vez que for identificada a bateria Baixa, envia-se um e-mail ao responsável
        if bateria == "Baixa":
            email_bateria()
            print("Como a bateria está baixa, enviamos um e-mail para o responsável")


            """ SQL SERVER """

        #Linhas para verificação do código via Monitor

        print(f'Temperatura Atual: {dados_coletados[2]}ºC')
        print(f'A porta está: {porta}')
        print(f'Tempo Temperatura : {Tempo_Temperatura_0}')
        print(f'Tempo Porta: {Tempo_Porta_0}')
        global Envios_0
        Envios_0 = Envios_0 + 1
        print(f'Foram enviados pelo ID# 0 um total de : {Envios_0} vezes')

        # Busca a tabela no SQL Server
        def read(conn):
            cursor = conn.cursor()
            cursor.execute("select * from dbo.TCC_Pratica")

        conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=LAPTOP-4SEELUEC\SQLEXPRESS;"
            "Database=TCC;"
            "Trusted_Connection=yes;"
            "UID=sa;"
            "PWD=tccsa2021;"
        )

        # Cria-se uma nova linha na tabela do SQL de acordo com os dados coletados
        def create(conn):

            dataehoraarduino = dados_coletados[5]
            print(f'Dados enviados de dataehora: {dados_coletados[5]}')

            cursor = conn.cursor()
            cursor.execute(
                'insert into dbo.TCC_Pratica(Time_Stamp,Status_Porta,Sensor_Temp,Id_Sensor,Battery_level,Alarme) values(?,?,?,?,?,?);',
                (dataehoraarduino, porta, dados_coletados[2], ID_Atual, bateria, "TesteAlarme")
            )
            print("Dados Exportados para o SQL com Sucesso")
            print('')
            print('')
            print(dataehoraarduino)
            print(f'Nível da Bateria = {bateria}')
            print('')
            conn.commit()
            read(conn)

        read(conn)
        create(conn)
        conn.close()
        print("FOI UTILIZADO O ID #0")

    # A mesma parte do código se repetirá para os IDs 1 e 2.
    """ID #1"""

    if dados_coletados[3] == IDs[1]:

        temperatura_1 = float(dados_coletados[2])
        global NivelBateriaAtual_1
        NivelBateriaAtual_1 = dados_coletados[4]
        NivelBateriaAtual_1 = float(dados_coletados[4])
        if NivelBateriaAtual_1 >= 4.00:
            bateria = str("Alta")
        if 3.8 < NivelBateriaAtual_1 < 4.0:
            bateria = str("Média")
        if NivelBateriaAtual_1 <= 3.8:
            bateria = str("Baixa")

        if (dados_coletados[1]) == "aberta":
            porta = "Aberta"
            global Tempo_Porta_1
            Tempo_Porta_1 = Tempo_Porta_1 + 1

        else:
            porta = "Fechada"
            Tempo_Porta_1 = 0

        if Tempo_Porta_1 >= 10:
            email_porta_aberta()
            print(f'Atingimos o tempo máximo de Porta Aberta: {Tempo_Porta_1}s .')
            print('Um e-mail de alerta de Porta Aberta foi enviado.')
            Tempo_Porta_1 = 0

        if temperatura_1 >= temperatura_max:
            global Tempo_Temperatura_1
            Tempo_Temperatura_1 = Tempo_Temperatura_1 + 1

        else:
            Tempo_Temperatura_1 = 0

        if Tempo_Temperatura_1 >= 10:
            email_temperatura()
            print(f'Atingimos o tempo máximo de Temperatura excedida: {Tempo_Temperatura_1}s .')
            print('Um e-mail de alerta de Temperatura foi enviado.')
            Tempo_Temperatura_1 = 0

        if bateria == "Baixa":
            email_bateria()
            print("Como a bateria está baixa, enviamos um e-mail para o responsável")

            """ SQL SERVER """
        print(f'Temperatura Atual: {dados_coletados[2]}ºC')
        print(f'A porta está: {porta}')
        print(f'Tempo Temperatura : {Tempo_Temperatura_1}')
        print(f'Tempo Porta: {Tempo_Porta_1}')
        global Envios_1
        Envios_1 = Envios_1 + 1
        print(f'Foram enviados pelo ID# 1 um total de : {Envios_1} vezes')

        def read(conn):
            cursor = conn.cursor()
            cursor.execute("select * from dbo.TCC_Pratica")

        conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=LAPTOP-4SEELUEC\SQLEXPRESS;"
            "Database=TCC;"
            "Trusted_Connection=yes;"
            "UID=sa;"
            "PWD=tccsa2021;"
        )

        def create(conn):

            dataehoraarduino = dados_coletados[5]
            print(f'Dados enviados de dataehora: {dados_coletados[5]}')

            cursor = conn.cursor()
            cursor.execute(
                'insert into dbo.TCC_Pratica(Time_Stamp,Status_Porta,Sensor_Temp,Id_Sensor,Battery_level,Alarme) values(?,?,?,?,?,?);',
                (dataehoraarduino, porta, dados_coletados[2], ID_Atual, bateria, "TesteAlarme")
            )
            print("Dados Exportados para o SQL com Sucesso")
            print('')
            print('')
            print(dataehoraarduino)
            print(f'Nível da Bateria = {bateria}')
            print('')
            conn.commit()
            read(conn)

        read(conn)
        create(conn)
        conn.close()
        print("FOI UTILIZADO O ID #1")

    """ID #2"""
    if dados_coletados[3] == IDs[2]:

        temperatura_2 = float(dados_coletados[2])
        global NivelBateriaAtual_2
        NivelBateriaAtual_2 = float(dados_coletados[4])
        if NivelBateriaAtual_2 >= 4.00:
            bateria = str("Alta")
        if 3.8 < NivelBateriaAtual_2 < 4.0:
            bateria = str("Média")
        if NivelBateriaAtual_2 <= 3.8:
            bateria = str("Baixa")

        if (dados_coletados[1]) == "aberta":
            porta = "Aberta"
            global Tempo_Porta_2
            Tempo_Porta_2 = Tempo_Porta_2 + 1

        else:
            porta = "Fechada"
            Tempo_Porta_2 = 0

        if Tempo_Porta_2 >= 10:
            email_porta_aberta()
            print(f'Atingimos o tempo máximo de Porta Aberta: {Tempo_Porta_2}s .')
            print('Um e-mail de alerta de Porta Aberta foi enviado.')
            Tempo_Porta_2 = 0

        if temperatura_2 >= temperatura_max:
            global Tempo_Temperatura_2
            Tempo_Temperatura_2 = Tempo_Temperatura_2 + 1

        else:
            Tempo_Temperatura_2 = 0

        if Tempo_Temperatura_2 >= 10:
            email_temperatura()
            print(f'Atingimos o tempo máximo de Temperatura excedida: {Tempo_Temperatura_2}s .')
            print('Um e-mail de alerta de Temperatura foi enviado.')
            Tempo_Temperatura_2 = 0

        if bateria == "Baixa":
            email_bateria()
            print("Como a bateria está baixa, enviamos um e-mail para o responsável")

            """ SQL SERVER """
        print(f'Temperatura Atual: {dados_coletados[2]}ºC')
        print(f'A porta está: {porta}')
        print(f'Tempo Temperatura : {Tempo_Temperatura_2}')
        print(f'Tempo Porta: {Tempo_Porta_2}')
        global Envios_2
        Envios_2 = Envios_2 + 1
        print(f'Foram enviados pelo ID# 2 um total de : {Envios_2} vezes')

        def read(conn):
            cursor = conn.cursor()
            cursor.execute("select * from dbo.TCC_Pratica")
        conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=LAPTOP-4SEELUEC\SQLEXPRESS;"
            "Database=TCC;"
            "Trusted_Connection=yes;"
            "UID=sa;"
            "PWD=tccsa2021;"
        )

        def create(conn):

            dataehoraarduino = dados_coletados[5]
            print(f'Dados enviados de dataehora: {dados_coletados[5]}')

            cursor = conn.cursor()
            cursor.execute(
                'insert into dbo.TCC_Pratica(Time_Stamp,Status_Porta,Sensor_Temp,Id_Sensor,Battery_level,Alarme) values(?,?,?,?,?,?);',
                (dataehoraarduino, porta, dados_coletados[2], ID_Atual, bateria, "TesteAlarme")
            )
            print("Dados Exportados para o SQL com Sucesso")
            print('')
            print('')
            print(dataehoraarduino)
            print(f'Nível da Bateria = {bateria}')
            print('')
            conn.commit()
            read(conn)
        read(conn)
        create(conn)
        conn.close()
        print("FOI UTILIZADO O ID #2")

# Loop da função "coletadados()"


threading.Thread(target=coletadados()).start()
