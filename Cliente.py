'''
Created on 3 de ago de 2018

@author: alline
'''

import SimplesTFTP

nome_arquivo = SimplesTFTP.nomeArquivo() # passa nome do arquivo
HOST = SimplesTFTP.Ip() #informa o IP do servidor
PORT = int(SimplesTFTP.Porta()) #informa o porta 
SimplesTFTP.iniciaCliente(nome_arquivo,HOST,PORT) # inicia o cliente
