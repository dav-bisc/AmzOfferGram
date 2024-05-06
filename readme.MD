# DarrionGram

Questo software genera post con link di affiliazione Amazon su un canale telegram a propria scelta.


## Tabella dei contenuti

- [Caratteristiche](#caratteristiche)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Contributi](#contributi)
- [Licenza](#licenza)

## Caratteristiche

- Messaggi personalizzabili.
- Orari di attività.
- Frequenza dei post personalizzabile.
- Parole chiave per la ricerca facilmente modificabili tramite file di testo.
- Possibilità di escludere articoli mediante codice ASIN in un file di testo.
- Leggero e portabile grazie a tecnologia di containerazzazione Docker.
- Robusto rispetto ai fallimenti: il container si riavvia autonomamente in caso di arresto inatteso.

## Requisiti
1. Creare un bot con BotFather e ottenere il token.
2. Possedere un account affiliato ad amazon con chiave di accesso e segreta per la PA API.
3. Impostare il bot come amministratore del canale Telegram dove si desidera pubblicizzare i prodotti.

## Installazione

1. È necessario installare [Docker Desktop](https://www.docker.com/products/docker-desktop/) per utilizzare il software.
2. Compilare la sezione apposita nel file **dockerfile**, fornendo le informazioni richieste.
3. Avviare **Docker Desktop**.
4. Avviare lo script **costruisci_bot.bat** e fornire il nome che si desidera assegnare al bot.
In alternativa, si può avviare lo script da terminale:

```bash
.\costruisci_bot.bat
```
## Utilizzo

- È sufficiente avviare o mettere in pausa il container Docker per l'esecuzione del software. 
- Se si desidera modificare la lista delle parole chiave o degli elementi esclusi, bisogna utilizzare lo script **costruisci_bot.bat** per rendere le modifiche effettive.
- Se si desidera modificare delle impostazioni nel **dockerfile**, bisogna utilizzare lo script **costruisci_bot.bat** per renderle effettive.

## Contributi

Davide Biscardi
davide.biscardi@proton.me

## Licenza

Darriongram © 2023 by Davide Biscardi is licensed under CC BY 4.0 


