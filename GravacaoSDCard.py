# TCC Anhembi Morumbi - Grupo Engenharia Elétrica Noturno

import socket
import time
import xlsxwriter
import threading
from datetime import datetime
from pytz import timezone

# Estabelecendo variáveis

x = 0

# Define o socket. Onde "0.0.0.0" significa "qualquer IP", na porta "8090".
s = socket.socket()
s.bind(('0.0.0.0', 8090 ))
s.listen(0)

ultimalinha = 1
ultimacoluna = 0


envios_separados = []
dados_separados = []

listacom5 = []

# Função de data e hora para saber quando o arquivo foi criado (hora do computador).

def dataehora():
    data_e_hora_atuais = datetime.now()
    fuso_horario = timezone('America/Sao_Paulo')
    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
    data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime('%d-%m-%Y %H-%M-%S')
    return data_e_hora_sao_paulo_em_texto

# Função que grava os dados no Excel
def gravandodados():
    global dados_separados
    global ultimalinha
    global ultimacoluna
    global dados_separados

    # Cria-se o arquivo em excel com o ID - Hora.xlsx
    outWorkbook = xlsxwriter.Workbook(f'{dados_separados[0]} - {dataehora()}.xlsx')
    # Adiciona uma spreadsheet:
    outSheet = outWorkbook.add_worksheet()

    # Definindo colunas

    """'Escrevendo os títulos'"""
    outSheet.write("A1", "ID")
    outSheet.write("B1", "Ano")
    outSheet.write("C1", "Mês")
    outSheet.write("D1", "Dia")
    outSheet.write("E1", "Hora")
    outSheet.write("F1", "Minuto")
    outSheet.write("G1", "Segundo")
    outSheet.write("H1", "Temperatura")
    outSheet.write("I1", "Status Porta")
    outSheet.write("J1", "Bateria")

    # Pula uma linha após a gravação dos dados
    def atualizalinha():
        global ultimalinha
        ultimalinha = ultimalinha + 1

    # Função Atualizalinha, é chamada toda vez que é gravado um dado na linha 6
    def zeralinha():
        global ultimalinha
        ultimalinha = 1

    # Pula uma coluna após a gravação do dado
    def atualizacoluna():
        global ultimacoluna
        ultimacoluna = ultimacoluna + 1

    # Função zeracoluna é chamada toda vez que é gravado um dado na coluna J
    def zeracoluna():
        global ultimacoluna
        ultimacoluna = 0

    # Função para log.
    def printalinhacoluna():
        global ultimalinha
        global ultimacoluna
        print("")
        print("valor gravado")
        print("")
        print(f'A Posição do arquivo excel está na Linha {ultimalinha} e na Coluna {ultimacoluna}')

    # Função de Erro
    def error():
        print("Erro no recebimento dos dados")

    # Função de gravação para uma linha
    def gravando01():
        global ultimalinha
        global ultimacoluna
        global dados_separados
        printalinhacoluna()
        # Escreve o dado_separado de acordo com a linha e coluna
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[0])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[1])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[2])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[3])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[4])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[5])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[6])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[7])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[8])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[9])
        zeracoluna()
        atualizalinha()
        printalinhacoluna()

    def gravando02():
        global ultimalinha
        global ultimacoluna
        global dados_separados
        gravando01()
        # Gravação da terceira linha, composta pela segunda linha + 1.
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[10])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[11])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[12])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[13])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[14])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[15])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[16])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[17])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[18])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[19])
        zeracoluna()
        atualizalinha()
        printalinhacoluna()

    def gravando03():
        gravando02()
        # Gravação da quarta linha, composta pela terceira linha + 1.
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[20])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[21])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[22])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[23])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[24])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[25])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[26])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[27])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[28])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[29])
        zeracoluna()
        atualizalinha()
        printalinhacoluna()

    def gravando04():
        gravando03()
        # Gravação da quinta linha, composta pela quarta linha + 1.
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[30])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[31])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[32])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[33])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[34])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[35])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[36])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[37])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[38])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[39])
        zeracoluna()
        atualizalinha()
        printalinhacoluna()

    def gravando05():
        gravando04()
        # Gravação da sexta linha, composta pela quinta linha + 1.
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[40])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[41])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[42])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[43])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[44])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[45])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[46])
        atualizacoluna()
        printalinhacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[47])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[48])
        atualizacoluna()
        outSheet.write(ultimalinha, ultimacoluna, dados_separados[49])
        zeracoluna()
        atualizalinha()
        printalinhacoluna()
        zeralinha()
        outWorkbook.close()

    # Double check de para quantidade de Strings dos dados Coletados.

    if len(dados_separados) == 50:
        gravando05()

# Função de error2
def error2():
    print("Foi recebido uma String invalida, ignorando dados...")


# Função principal para coleta e tratamento dos dados recebidos.
def main():
    global envios_separados
    global dados_separados
    global x

    while 1:
        time.sleep(1)

        client, addr = s.accept()

        while True:

            content = client.recv(4096)

            if len(content) == 0:

                break

            else:
                # Caso seja recebido algum conteúdo:
                # Transforma o dado coletado em uma String

                as_string = str(content)
                print(f'O tamanho do conteúdo recebido foi de {len(content)}')
                print(content)
                # O dado correto para ser tratado, deve, necessariamente, conter 377 caracteres
                if len(content) == 377:
                    envios_separados = as_string.split("<")

                    # Aqui separamos a String pelo caracter "<" e adicionamos em uma lista chamada envios_separados
                    # Cada dado é colocado em um elemento, exemplo:
                    # <Victor<Teste, é criado uma lista de 2 elementos, sendo: (Victor, Teste)

                    print(envios_separados)

                    # Neste passo transformamos a lista em String:
                    listabase = str(envios_separados[1])
                    print(envios_separados[1])
                    print(listabase)

                    # Aqui separamos a String pelo caracter "," e adicionamos em uma lista chamada listabase
                    # Cada dado é colocado em um elemento, exemplo:
                    # ",Victor,Teste," é criado uma lista de 3 elementos, sendo: (Victor, Teste, )

                    dados_separados = listabase.split(',')
                    print("Dados Separados já tratados")
                    print(dados_separados)
                    print("")
                    print(f'Tamanho de dados_separados {len(dados_separados)}')
                    # Retira-se o ultimo vazio, que será sempre vazio, como no exemplo anterior
                    dados_separados.pop()
                    print("")
                    print(f'Tamanho de dados separados sem o ultimo elemento: {len(dados_separados)}')
                    print("")
                    print("Dado separado sem o ultimo elemento")
                    print(dados_separados)
                    print(f'Tamanho de dados_separados {len(dados_separados)}')
                    # Após o tratamento dos dados, faz-se a verificação da quantidade de Strings
                    # Dessa forma deixamos o código seguro e enviamos erros
                    if len(dados_separados) > 50 or len(dados_separados) < 50:
                        error2()
                    if len(dados_separados) == 50:
                        # Caso a String seja mesmo de 50 caracteres, fazemos a gravação do dado usando a função:
                        gravandodados()
                else:
                    error2()

                print("O Código foi finalizado")


# Coloca-se em loop a função "main()"
threading.Thread(target=main()).start()
