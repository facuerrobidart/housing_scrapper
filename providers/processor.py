import logging
from providers.zonaprop import Zonaprop
from providers.argenprop import Argenprop
from providers.mercadolibre import Mercadolibre
from providers.properati import Properati
from providers.inmobusqueda import Inmobusqueda
from persistence.mongo import Mongo

mongoClient = Mongo()

def register_property(conn, prop):
    stmt = 'INSERT INTO properties (internal_id, provider, url) VALUES (:internal_id, :provider, :url)'
    try:
        conn.execute(stmt, prop)
    except Exception as e:
        print(e)

def process_properties(provider_name, provider_data):
    provider = get_instance(provider_name, provider_data)

    new_properties = []

    for prop in provider.next_prop():
        logging.info(f"Processing property {prop['internal_id']}")
        # check if property is already in the database
        db_prop = mongoClient.find_one({'internal_id': prop['internal_id'], 'provider': prop['provider']})

        if not db_prop:
            logging.info(f"Property {prop['internal_id']} not in the database, notifying.")
            new_properties.append(prop)
            mongoClient.insert(prop)
        else:
            logging.info(f"Property {prop['internal_id']} already in the database, not notifying.")

    return new_properties

def get_instance(provider_name, provider_data):
    if provider_name == 'zonaprop':
        return Zonaprop(provider_name, provider_data)
    elif provider_name == 'argenprop':
        return Argenprop(provider_name, provider_data)
    elif provider_name == 'mercadolibre':
        return Mercadolibre(provider_name, provider_data)
    elif provider_name == 'properati':
        return Properati(provider_name, provider_data)
    elif provider_name == 'inmobusqueda':
        return Inmobusqueda(provider_name, provider_data)
    else:
        raise Exception('Unrecognized provider')
