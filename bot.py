from amazon_paapi import AmazonApi
from amazon_paapi import errors
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import emoji
from datetime import datetime, timedelta
import pytz
import random
import os
import sys

#Nome del bot
BOT_NAME = os.environ.get('BOT_NAME')
#Numero di telefono
OWNER_CHAT_ID = int(os.environ.get('OWNER_CHAT_ID'))
# Amazon API credentials
AMAZON_ACCESS_KEY = os.environ.get('AMAZON_ACCESS_KEY')
AMAZON_SECRET_KEY = os.environ.get('AMAZON_SECRET_KEY')
AMAZON_ASSOC_TAG = os.environ.get('AMAZON_ASSOC_TAG')
AMAZON_REGION = os.environ.get('AMAZON_REGION') 

# Telegram API credentials
TELEGRAM_API_TOKEN = os.environ.get('BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.environ.get('CHANNEL_ID')  

#INTERVALLO DI TEMPO FRA UN'OFFERTA E LA SUCCESSIVA (in secondi)
OFFER_DELAY_SECONDS = int(os.environ.get('TIME_INTERVAL'))

#ORARIO INIZIO ATTIVITA' ad es. '09:00:00' NON RIMUOVERE GLI APICI!
START_TIME = os.environ.get('START_TIME') 
#ORARIO FINE ATTIVITA' ad es. '22:00:00' NON RIMUOVERE GLI APICI!
END_TIME = os.environ.get('END_TIME') 
#MESSAGGIO INIZIALE OFFERTA
OFFER_MSG=os.environ.get('OFFER_MSG') 
#MESSAGGIO FINALE OFFERTA
OFFER_MSG_2=os.environ.get('OFFER_MSG_2') 
#PERCENTUALE DELLO SCONTO MINIMO DA TROVARE 
DISC_PERCENT = int(os.environ.get('DISC_PERCENT'))
#THROTTLING RICHIESTE PER API AMAZON
THROTTLING_FACTOR=int(os.environ.get('THROTTLING_FACTOR'))
#NUMERO DI RISULTATI DELLA RICERCA AMAZON (MAX 10)
ITEM_COUNT=int(os.environ.get('ITEM_COUNT'))
#Da 0 a 2 -> Livello dei messaggi di debug da mostrare
VERBOSITY=int(os.environ.get('VERBOSITY'))
#NUMERO DI PAROLE CHIAVI DA SCEGLIERE AD OGNI CICLO DI RICERCA
KEYWORD_COUNT=int(os.environ.get('KEYWORD_COUNT'))
#NUMERO DI POST PRIMA DEGLI AVVISI
WARNING_CNT= int(os.environ.get('WARNING_CNT'))

###########################NON MODIFICARE AL DI SOTTO DI QUESTA RIGA!!!#######################################################


# Initialize Amazon API
amazon = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, AMAZON_REGION, throttling=THROTTLING_FACTOR)

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_API_TOKEN)

def read_lines(file_path):
    with open(file_path, 'r') as file:
        links = file.readlines()
    cleaned_links = [link.strip() for link in links]
    return cleaned_links

# Search for Amazon products
def search_amazon_products(keyword, risparmio_percentuale_minimo):
    try:
        products =  amazon.search_items(keywords=keyword, min_saving_percent=risparmio_percentuale_minimo, item_count=ITEM_COUNT)
    except errors.exceptions.ItemsNotFound:
        sys.stderr.write(f"La ricerca di {keyword} non ha prodotto risultati\n")
        products = None
    except errors.exceptions.TooManyRequests:
        sys.stderr.write(f"Troppe richieste verso API amazon, attendere o incrementare throttling\n")
    except errors.exceptions.MalformedRequest:
        sys.stderr.write(f"Richiesta malformata\n")
        return None
    except errors.exceptions.InvalidArgument:
        sys.stderr.write(f"Argomento non valido\n")
        return None
    except errors.exceptions.RequestError:
        sys.stderr.write(f"Errore nella richiesta\n")
        return None

    return products

def is_amazon_shipped(product):
    for listing in product.offers.listings:
        if listing.delivery_info.is_amazon_fulfilled==True:
            return True
        else:
            return False
        
def category_emoji(product):

    if product.item_info is not None and product.item_info.classifications is not None and product.item_info.classifications.product_group is not None and product.item_info.classifications.product_group.display_value is not None:
        categoria=product.item_info.classifications.product_group.display_value
        if categoria=="Giocattolo":
            return ":puzzle_piece:"
        elif categoria=="Prodotti per ufficio":
            return ":briefcase:"
        elif categoria=="Libro":
            return ":open_book:"
        elif categoria=="Prodotti per l'infanzia":
            return ":teddy_bear:"
        elif categoria=="Strumenti per la cura personale":
            return ":soap:"
        elif categoria=="Casa":
            return ":house:"
        elif (categoria=="Salute e bellezza" or categoria=="Bellezza") :
            return ":lipstick:"
        elif categoria=="Sport":
            return ":soccer_ball:"
        elif (categoria=="Drugstore" or categoria=="Drogheria") :
            return ":sponge:"
        elif categoria=="Mobili":
            return ":chair:"
        elif categoria=="Abbigliamento":
            return ":t-shirt:"
        elif categoria=="Videogioco":
            return ":video_game:"
        elif categoria=="Elettronica di consumo":
            return ":pager:"
        elif categoria=="Cucina":
            return ":fork_and_knife:"
        elif categoria=="Scarpe":
            return ":running_shoe:"
        elif categoria=="Prodotti per animali":
            return ":dog_face:"
        elif categoria=="Ricambi e accessori auto":
            return ":automobile:"
        elif categoria=="Wireless":
            return ":satellite:"
        elif categoria=="Bricolage":
            return ":potted_plant:" #🪴
        else:
            return ":exploding_head:"
    else:
        return ":exploding_head:"

async def send_to_telegram_channel(max_discount_product):
    
    orig_display_value = ""
    max_percentage_discount = 0
    new_price=""
    chosen_msg = ""
    #Itera nei listing del prodotto con lo sconto maggiore
    if max_discount_product.offers.listings and max_discount_product.offers.listings is not None:
        for listing in max_discount_product.offers.listings:
            if listing.price.savings is not None:
                if listing.price.savings.percentage > max_percentage_discount:
                    max_percentage_discount=listing.price.savings.percentage
                    orig_display_value=listing.price.display_amount
                    if listing.saving_basis is not None and listing.saving_basis.price_type=='WAS_PRICE':
                        orig_display_value=listing.saving_basis.display_amount
                        new_price=listing.price.display_amount
                        chosen_msg = f"{str(category_emoji(max_discount_product))} PASSA DA {orig_display_value} A {new_price} {str(category_emoji(max_discount_product))}"
                    elif listing.saving_basis is not None and  listing.saving_basis.price_type=='LIST_PRICE':
                        chosen_msg = f"{str(category_emoji(max_discount_product))} {listing.price.savings.percentage}% DI SCONTO {str(category_emoji(max_discount_product))}"
                    elif listing.saving_basis is not None and listing.saving_basis.price_type=='LOWEST_PRICE_STRIKETHROUGH':
                        orig_display_value=listing.saving_basis.display_amount
                        new_price=listing.price.display_amount
                        chosen_msg = f"{str(category_emoji(max_discount_product))} " + "\u0336".join(f"{orig_display_value}")+ f" :left_arrow_curving_right: " + f"{new_price} " + f"{str(category_emoji(max_discount_product))}"
                    elif listing.price.savings.display_amount is not None and listing.price.savings.display_amount!="":
                        chosen_msg = f"{str(category_emoji(max_discount_product))} {listing.price.savings.percentage}% DI SCONTO {str(category_emoji(max_discount_product))}"
                    else:
                        chosen_msg = f"{str(category_emoji(max_discount_product))} GRANDE SCONTO {str(category_emoji(max_discount_product))}"

    keyboard = [[InlineKeyboardButton("Apri nell'app", url=max_discount_product.detail_page_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    final_message = emoji.emojize(f"{OFFER_MSG}\n\n" + f"{chosen_msg} \n\n" + f"{OFFER_MSG_2}\n\n" + f"LINK: {max_discount_product.detail_page_url}")
    #await bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=max_discount_product.images.primary.large.url, caption=final_message, reply_markup=reply_markup )
    await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=final_message, reply_markup=reply_markup)  
    VERBOSITY>=1 and sys.stdout.write(f"Pubblicato prodotto: {max_discount_product.detail_page_url} \n")

def has_minimum_discount(product):

    for listing in product.offers.listings:
        if listing.price and listing.price.savings is not None:
            if listing.price.savings.percentage >= DISC_PERCENT:
                return True
            else:
                return False
async def main():
    

    italy_timezone = pytz.timezone('Europe/Rome')
    lista_esclusi = read_lines("esclusi.txt")
    start_time_obj = datetime.strptime(START_TIME, '%H:%M:%S').time()
    end_time_obj = datetime.strptime(END_TIME, '%H:%M:%S').time()
    warning_noprods_cnt = 0
    warning_fewprods_cnt = 0
    VERBOSITY>=1 and sys.stdout.write(f"{BOT_NAME} AVVIATO\n")

    while True:
        current_time = datetime.now(italy_timezone).time()
        
        if start_time_obj <= current_time <= end_time_obj:
            
            try:  
                #Per ogni parola chiave nella lista effettua la ricerca e aggiungi articoli alla lista
                keywords = read_lines("lista.txt")
                selected_keywords = random.sample(keywords, KEYWORD_COUNT)
                promo_products_list = []
                VERBOSITY>=1 and sys.stdout.write("Ricerca articoli in corso...\n")
                for keyword in selected_keywords:
                    products= search_amazon_products(keyword, DISC_PERCENT)
                    if products is not None:
                        promo_products_list.extend(products.items)
                        VERBOSITY==2 and sys.stdout.write(f"{len(products.items)} risultati per {keyword}\n")
                        
                #Filtra gli articoli nella lista: prende soltanto quelli con sconto attivo e spediti da Amazon
                prod_list_final = [product for product in promo_products_list if
                   product.offers and product.offers.listings and is_amazon_shipped(product) and has_minimum_discount(product) and
                   any(listing.saving_basis is not None for listing in product.offers.listings)]

                #Escludi gli articoli il cui ASIN è nella lista esclusi
                filtered_list = [product for product in prod_list_final if product.asin not in lista_esclusi]
                
                VERBOSITY>=1 and sys.stdout.write(f"{len(filtered_list)} prodotti idonei trovati\n")
                #Se la lista ottenuta dai filtraggi ha almeno un articolo
                if len(filtered_list)>0:
                    if len(filtered_list)<10 and warning_fewprods_cnt%WARNING_CNT==0:
                        await bot.send_message(text=f"Il tuo bot {BOT_NAME} sta esaurendo i prodotti idonei, per favore aggiorna la lista o libera la lista esclusi.", chat_id=OWNER_CHAT_ID)
                    chosen_product = random.choice(filtered_list)
                else:
                    chosen_product = random.choice(prod_list_final)
                    VERBOSITY>=1 and sys.stdout.write("I PRODOTTI NUOVI DA POSTARE SONO ESAURITI, STO RIPOSTANDO PRODOTTI POTENZIALMENTE GIA' POSTATI\n")
                    VERBOSITY>=1 and sys.stdout.write("AGGIORNARE LA LISTA PER TROVARE PRODOTTI NUOVI\n")
                    if warning_noprods_cnt%WARNING_CNT==0:
                        await bot.send_message(text=f"Attenzione, il tuo bot {BOT_NAME} ha esaurito tutti gli articoli idonei e sta postando offerte vecchie.", chat_id=OWNER_CHAT_ID)
                #Aggiungi l'articolo selezionato alla lista esclusi    
                with open ("esclusi.txt", "a") as file:
                    file.write(chosen_product.asin + "\n")
                lista_esclusi.append(chosen_product.asin)
                
                await send_to_telegram_channel(chosen_product)
                
            except TypeError as e:
                sys.stderr.write(f"Error: {e}")
                continue
            await asyncio.sleep(OFFER_DELAY_SECONDS) #Aspetta l'intervallo di tempo indicato
        else:
            VERBOSITY>=1 and sys.stdout.write("Orario di attività terminato\n")
            await asyncio.sleep(60)  # Controlla l'orario ogni minuto
        
   

if __name__ == "__main__":

    asyncio.run(main())
