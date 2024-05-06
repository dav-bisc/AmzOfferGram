
FROM python:3.9-slim


WORKDIR /app

COPY . /app 

RUN pip install -r requirements.txt
# ########################## COMPILARE I CAMPI SOTTOSTANTI ###############################
#NOME DEL BOT
ENV BOT_NAME="BabyBot"
# NUMERO DI TELEFONO PER GLI AVVISI
ENV OWNER_CHAT_ID=${OWNER_CHAT_ID}
#TOKEN DEL BOT OTTENUTO DA BOT FATHER
ENV BOT_TOKEN=${BOT_TOKEN}
#ID DEL CANALE O DEL GRUPPO (visibile in telegram web)
ENV CHANNEL_ID=${CHANNEL_ID}
#INTERVALLO DI TEMPO TRA UN CICLO DI RICERCA E UN ALTRO
ENV TIME_INTERVAL=270
#CHIAVE DI ACCESSO PA API DI AMAZON (visibile nel pannello strumenti del portale affiliati)
ENV AMAZON_ACCESS_KEY=${AMAZON_ACCESS_KEY}
#CHIAVE SEGRETA PA API DI AMAZON (visibile nel pannello strumenti del portale affiliati, SOLO ALLA CREAZIONE)
ENV AMAZON_SECRET_KEY=${AMAZON_SECRET_KEY}
#Partner tag (visibile nel portale affiliati)
ENV AMAZON_ASSOC_TAG=${AMAZON_ASSOC_TAG}
#Regione amazon (usare codici internazionali)
ENV AMAZON_REGION='IT'
#ORARI DI INIZIO E FINE ATTIVITA' - NOTA BENE: il bot funziona se l'orario attuale è compreso fra START_TIME ed END_TIME: START_TIME<=orario attuale<=END_TIME
# NON USARE 00:00:00 COME END_TIME O LA CONDIZIONE NON RISULTERA' SODDISFATTA E IL BOT NON FUNZIONERA'!
ENV START_TIME='00:01:00'
ENV END_TIME='23:59:00'
#MESSAGGIO AL DI SOPRA DEL LINK
ENV OFFER_MSG=":fire: IN PROMOZIONE  :fire:"
#MESSAGGIO AL DI SOTTO DEL LINK
ENV OFFER_MSG_2=":check_mark_button: SPEDITO DA AMAZON :check_mark_button:"
#PERCENTUALE MINIMA DI SCONTO DA CERCARE
ENV DISC_PERCENT=10
#THROTTLING FACTOR: intervallo di tempo tra una singola richiesta ad amazon API e la seguente. Con valori minori rende più veloce la ricerca ma rischia di bloccare il bot
#Valore consigliato: 2, valore massimo: 4
ENV THROTTLING_FACTOR=2
#Numero di prodotti restituiti dalla singola ricerca. NOTA BENE: IL VALORE MASSIMO E' 10
#Valori minori renderanno più veloce il funzionamento ma i prodotti trovati verranno esauriti più in fretta
ENV ITEM_COUNT=10
#Specifica il livello dei messaggi dei debug da mostrare (da 0 a 2)
ENV VERBOSITY=2
#Numero di parole chiave da selezionare per ricerca
ENV KEYWORD_COUNT=20
#Numero di post da aspettare prima di inviare avvisi
ENV WARNING_CNT=8
########################### FINE CAMPI DA COMPILARE ################################

CMD ["python","-u", "bot.py"]
