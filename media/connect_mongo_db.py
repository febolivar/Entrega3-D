""" Batch database connection module from mongo """

# Mongo Database Imports

import pymongo
from pymongo import MongoClient
import boto3

# Util

from datetime import datetime

# Global variables

HOST = '18.210.47.72'
PORT = 27017
DB_NAME = 'proyecto1'
CLIENT = MongoClient( host = HOST)

# SQS queue configuration
APP_AWS_QUEUE = {
  'region_name': 'us-east-1',
  'aws_access_key_id': 'AKIAWMDWJXRQEMTXLLHF',
  'aws_secret_access_key': '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',
  'sqs_queue_url': 'https://sqs.us-east-1.amazonaws.com/438334766176/queuse_design_std'
}

# Methods

def query_in_process():
    imagenes_por_procesar = False
    # create SQS client
    sqs_client = boto3.client('sqs',
                              region_name=APP_AWS_QUEUE['region_name'],
                              aws_access_key_id=APP_AWS_QUEUE['aws_access_key_id'],
                              aws_secret_access_key=APP_AWS_QUEUE['aws_secret_access_key']
                              )

    # Read Queue
    msg = sqs_client.receive_message(QueueUrl=APP_AWS_QUEUE['sqs_queue_url'],
                                     MaxNumberOfMessages=1
                                     )

    #print("{} \t Inicia la lectura de la cola".format(datetime.now()))
    
    msg_receipt_handle = extract_values(msg, 'ReceiptHandle')

    try:
        msg_receipt_handle = msg_receipt_handle[0]
        imagenes_por_procesar = True
    except:
        msg_receipt_handle=''
        #print("{} \t No se encontraron elementos en la cola".format(datetime.now()))

    if imagenes_por_procesar:
        image_to_process = extract_values(msg, 'Body')
        design_id = str(image_to_process).replace('[', '')
        design_id = design_id.replace(']', '')
        design_id = design_id.replace('\'', '')
    else:
        design_id = '0'

    try:
        
        #print("{} \t Inicia la lectura de la base de datos".format(datetime.now()))

        db = CLIENT[DB_NAME]
        
        designs = db['designs_design']
        images = db['designs_image']
        designers = db['auth_user']

        projects = db['designs_project']
        enterprises = db['users_enterprise']

        designs_to_process = list()
        
        for item in designs.find({'id': int(design_id)}):
            
            designs_to_process.append(
                {
                    'id': item['id'],
                    'design_create_date': item['design_create_date'],
                    'design_creator_id': item['design_creator_id'],
                    'design_project_id' : item['design_project_id'],
                }
            )

        for item in designs_to_process:
            image = images.find_one({'image_design_id': item['id']})
            
            designer = designers.find_one({'id': item['design_creator_id']})

            project = projects.find_one({'id': item['design_project_id']})
            enterprise = enterprises.find_one({'id' : project['project_enterprise_id'] })
            #print(image)
            #print(designer)
            #print(project)
            #print(enterprise)
            item['image_original'] = image['image_original']
            item['image_id'] = image['id']
            item['first_name'] = designer['first_name']
            item['email'] = designer['email']
            item['url'] = enterprise['enterprise_url']

        #print(desings_to_process)

        if design_id != "0":
            # Delete Queue
            print("{} \t Borrador de mensaje de la cola".format(datetime.now()))
            sqs_client.delete_message(QueueUrl=APP_AWS_QUEUE['sqs_queue_url'],
                                      ReceiptHandle=msg_receipt_handle)

        return designs_to_process

    except Exception as e:
        print(str(e))
        print("{} \t Error en la lectura de diseños a procesar".format(datetime.now()))


def update_processed_files(imagen_pk, design_pk, file):
    try:

        db = CLIENT[DB_NAME]

        designs = db['designs_design']
        images = db['designs_image']

        update_image = {'id': imagen_pk}
        processed_image = { '$set': { 'image_processed': file } }

        images.update_one(update_image,processed_image)

        update_desing = { 'id' : design_pk }
        processed_design = { '$set': { 'design_state_id': 2 } }

        designs.update_one(update_desing,processed_design)

        print("{} \t Actualización de diseño correcta".format(datetime.now()))

    except:
        print("{} \t Error en el método update_processed_files".format(datetime.now()))


def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
