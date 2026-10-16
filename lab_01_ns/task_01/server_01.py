import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9001))

server.listen()
print("Server TCP acceso e in ascolto sulla porta 9001...")

memoria={}

while True:
    print("In attesa...")
    client_socket, client_address = server.accept()
    print("Nuovo client collegato dall'indirizzo: ", client_address)

    #Decoding message
    while True:
        dati_grezzi = client_socket.recv(1024)
        if not dati_grezzi:
            print("Il client ", client_address, " ha chiuso la connessione.")
            break

        messaggio = dati_grezzi.decode('ascii')
        messaggio_pulito = messaggio.strip() #strip rimuove gli \n
        print("Il client ha inviato il comando: ", messaggio_pulito)

        # 1. ECHO function
        if messaggio_pulito.startswith("ECHO "):
            parti = messaggio_pulito.split(" ", 1) #divide al primo spazio
            testo_da_ripetere = parti[1]
            risposta = testo_da_ripetere + "\n"
            client_socket.sendall(risposta.encode('ascii'))

        # 2. PING function
        elif messaggio_pulito == "PING":
            risposta = "PONG\n"
            client_socket.sendall(risposta.encode('ascii'))

        # 3. Memory function (SET)
        elif messaggio_pulito.startswith("SET "):
            parti = messaggio_pulito.split(" ", 2) #divide in 3 parti, ai primi 2 spazi

            if len(parti) == 3:
                chiave = parti[1]
                valore = parti[2]
                memoria[chiave] = valore
                risposta = "OK\n"  # Corretto per il test!
            else:
                risposta = "ERR\n"

            client_socket.sendall(risposta.encode('ascii'))

        # 4. GET function
        elif messaggio_pulito.startswith("GET "):
            parti = messaggio_pulito.split(" ", 1)

            if len(parti) == 2:
                chiave = parti[1]
                if chiave in memoria:
                    risposta = memoria[chiave] + "\n"
                else:
                    risposta = "NOT_FOUND\n"  # Ripristinato NOT_FOUND
            else:
                risposta = "ERR\n"

            client_socket.sendall(risposta.encode('ascii'))

        # 5. ERROR, unknown command
        else:
            risposta = "ERR\n"
            client_socket.sendall(risposta.encode('ascii'))

    client_socket.close()