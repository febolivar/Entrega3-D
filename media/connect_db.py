""" Batch database connection module """

# Database

import psycopg2
from datetime import datetime

# Connect parameters variables

DATA_CONNECTION = {
#    'user': 'proyecto1usr',
    'user': 'postgres',
    'password': 'Dsa123',
    'host': '127.0.0.1', 
    'port': '5432',
#    'database': 'proyecto1',
    'database': 'Proyecto1',
}

IN_PROCESS_DESIGNS_QUERY = (
    "SELECT u.first_name, u.email, d.design_create_date, i.image_original, i.id , i.image_design_id "
    "FROM designs_design AS d "
    "INNER JOIN designs_image AS i "
	"ON d.id = i.image_design_id "
    "INNER JOIN auth_user AS u "
	"ON d.design_creator_id = u.id "
    "WHERE design_state_id = 1 "
)

UPDATE_IMAGE = (
    "UPDATE public.designs_image "
	"SET image_processed='%s' "
    "WHERE id= %s;"
)

UPDATE_DESIGN_STATUS = (
    "UPDATE public.designs_design "
    "SET design_state_id = 2 "
    "WHERE id= %s;"
)


# Methods

def connect_to_data_base():
    """ Method to connect to database """
    try:
        connection = psycopg2.connect(**DATA_CONNECTION)

        cursor = connection.cursor()

        cursor.execute("SELECT version();")
        #record = cursor.fetchone()
        
        print("{} \t Conexión Base de datos realizada con éxito".format(datetime.now()))
    
        return connection, cursor

    except (Exception, psycopg2.Error) as error:
        print("{} \t Error en el método connect_to_data_base".format(datetime.now()))
        print("Error en la conexión a la base de datos", error)
    
    return None


def close_connection(connection):
    """ Method to close a database connection """
    try:
        if(connection):

            connection.close()
            print("{} \t Se cerró la conexión a la base de datos con éxito".format(datetime.now()))

    except (Exception, psycopg2.Error) as error:
        print("{} \t Error en el método close_connection".format(datetime.now()))
        print("Ocurrió un error cerrando la conexión - ", error)


def query_in_process(connection):
    """ Query to get in process designs """
    try:
        if(connection):
        
            connection.execute(IN_PROCESS_DESIGNS_QUERY)    
            record = connection.fetchall()

            print("{} \t Finaliza lectura de diseños a procesar".format(datetime.now()))

            return record

    except (Exception, psycopg2.Error) as error:
        print("{} \t Error en el método query_in_process".format(datetime.now()))
        print("Ocurrió un error consultando los diseños - ", error)


def update_processed_files(connection, cursor, image_pk, design_pk, file):
    """ Method to persist processed files in Database """
    try:
        if(connection):

            cursor.execute(UPDATE_IMAGE % (file, str(image_pk)))
            connection.commit()

            cursor.execute(UPDATE_DESIGN_STATUS % str(design_pk))
            connection.commit()
            
            print("{} \t Actualización de diseño correcta".format(datetime.now()))

    except (Exception, psycopg2.Error) as error:
        print("{} \t Error en el método update_processed_files".format(datetime.now()))
        print("Ocurrió actualizando el estado - ", error)
            