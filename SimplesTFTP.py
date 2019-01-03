
'''
Created on 31 de Julho de 2018

@author: alline
'''
import socket 
import pickle
import os
#import sys


C_TAM_PACT = 200
S_TAM_PACT = 1024
TAM_ARQ = None
NUM_PCT = None
SOCK_TIMEOUT = 5

        
## Cliente ##
   
sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def iniciaCliente(nome,HOST,PORT):
    x = 0
    TAM_ARQ = os.path.getsize('/home/alline/Documents/'+ nome) #verifica tamanho do pacote a ser enviado
    NUM_PCT = TAM_ARQ/C_TAM_PACT
    print NUM_PCT
    while x <= 4: # tenta enviar 4 vezes 
            msg_inicio = pacoteInicio(nome, NUM_PCT)
            sock_udp.sendto(msg_inicio, (HOST, PORT))
            x+=1
            sock_udp.settimeout(SOCK_TIMEOUT)
            try:
                Ack_inicio = sock_udp.recvfrom(C_TAM_PACT)
                Ack_in = Ack_inicio[0]
                TrataResposta(Ack_in,nome,NUM_PCT,HOST,PORT)  
                #sock_udp.close()
            except sock_udp.settimeout:
                print ('Erro: Tempo de espera esgotado')  
              


def nomeArquivo():
    print ('Escreva o nome do arquivo.\n (Ex.:texto.txt)')
    nome_arq = raw_input()
    return nome_arq

def Ip():
    print ('Informa o IP do servidor que deseja se conectar.\n (Ex.: 191.36.15.69)')
    ip = raw_input()
    return ip

def Porta():
    print ('Informa a porta.\n (Ex.: 2090)')
    porta = raw_input()
    return porta

def pacoteInicio(nome, num_pct):
    b = (nome,num_pct)
    b_bytes = pickle.dumps(b) #serializa para enviar 
    return b_bytes   

def finaliza(ACK,num_pct):
    if(ACK == num_pct):  #finaliza transmissao e informa que arquivo foi enviado para cliente
        return

def pacoteConcatena(dado, num, flag):
    a = (num,dado,flag)
    a_bytes = pickle.dumps(a) #serializa para enviar 
    return a_bytes 
  
def verificaAck(num_seq,ACK):
    if(num_seq is not ACK):  #verifica se ack recebido do cliente e ultimo pacote enviado
        return 

def TrataResposta(Ack_resp,nome,NUM_PCT,HOST, PORT):        
    if(Ack_resp == 'OK'):
            print('Iniciando envio do arquivo...'), Ack_resp
            seq = 0
            try:
                arq = open('/home/alline/Documents/'+ nome ,'rb')  
            except:
                print ('Erro: Ao abrir arquivo')
            
            while NUM_PCT >= 0:
                    y = 0
                    dado = arq.read(C_TAM_PACT)
                    if (NUM_PCT > 0):
                        flag = 0
                        dado_bytes = pacoteConcatena(dado, seq, flag) 
                        dado = pickle.loads(dado_bytes) 
                        print dado
                        sock_udp.sendto(dado_bytes, (HOST, PORT))
                    else:
                        flag = 1
                        dado_bytes = pacoteConcatena(dado, seq, flag)
                        dado = pickle.loads(dado_bytes)
                        sock_udp.sendto(dado_bytes, (HOST, PORT))
                        print ('Ultimo pacote enviado com sucesso!')
                        print dado
                        print ('Programa finalizado')
                        break
                        arq.close()
                        sock_udp.close()
                        exit()
                        #sock_udp.close()
                    sock_udp.settimeout(SOCK_TIMEOUT)
                    try:
                        ACK = sock_udp.recvfrom(C_TAM_PACT)
                        ACK_SEQ = ACK[0]
                        verifica = verificaAck(seq, ACK_SEQ)
                        if(verifica == True): #verifica se numero de sequecia e igual ao Ack de sequencia recebido
                            y = 0
                            while y <= 4: # Se for diferente, tenta enviar o mesmo pacote 4 vezes
                                    dado_bytes = pacoteConcatena(dado, seq, flag)
                                    sock_udp.sendto(dado_bytes, (HOST, PORT))
                                    y+=1
                                    if(y == 4):
                                        print ('Erro: Perda de conexao, tente mais tarde')      
                    except sock_udp.settimeout:
                        print ('Erro: Tempo de espera esgotado')
                    #print NUM_PCT 
                    NUM_PCT-=1
                    seq+=1
    elif(Ack_resp == 'ERRO1'):
        print ('Erro 1: Arquivo ja existente')  
    elif(Ack_resp == 'ERRO2'):
        print ('Erro 2: Sem espaco em memoria para armazenar ')  
    else:
        print ('Erro 3: Tente mais tarde. Perda de conexao') 
         
    exit()
  
## Servidor ##

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
HOST = ''

def iniciaServidor(PORT):
    orig = (HOST, PORT)
    udp.bind(orig)
    msg, cliente = udp.recvfrom(S_TAM_PACT)
    
    msg_s = pickle.loads(msg)
    num_pacotes = msg_s[1]
    nome = msg_s[0]
    print nome
    print num_pacotes
     
    ACK = verificaNome(nome)
    print ACK
    udp.sendto(ACK,cliente) 
    # ack_bytes = pickle.dumps(ACK)   
    try: 
        arq = open('/home/alline/Documents/'+ nome, 'wb')
    except:
        print ('Erro: Ao abrir o Arquivo') 
    
    i=0
    while i<=num_pacotes: #num_pacotes>=0:   
        dado,cliente = udp.recvfrom(S_TAM_PACT)
        convert = pickle.loads(dado)
        ACK_nseq = convert[0]
        conteudo = convert[1]
        flag_s = convert[2]
        print ('Flag: ') , flag_s
        print ('Sequencia Recebida: ') , ACK_nseq
        
        if(flag_s == 0):
            arq.write(conteudo)
            seq = str(ACK_nseq)
            print ('Sequencia enviada: '), seq     
            udp.sendto(seq,cliente)
            i+=1       
        else:
            arq.write(conteudo)
            print ('Ultimo pacote enviado: ') , ACK_nseq
            arq.close()
            udp.close()
            exit()   
        
    
def verificaNome(nome):
    #fileName = Path(nome) 
    if os.path.isfile('/home/alline/Documents/'+ nome):
        print ("File exist")
        return 'ERRO1'
    else:
        return 'OK'  
  

