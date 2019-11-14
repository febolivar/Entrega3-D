#!/usr/bin/python3

""" Process designs module for process designs
    with a batch model.
    Parameters:
        1 -> Resizing width in pixels (e.g 800)
        2 -> Resizing height in pixels (e.g 600)
        3 -> Resizing strategy. (T) for thumbnail, otherwise for resize 
        4 -> Email Password
 """
# Future and GET Library

from __future__ import print_function

# Util and OS

import os, sys
# sys.path.append('/usr/local/lib64/python3.6/site-packages/')
from pathlib import Path

# Datetime and start loggin

from datetime import datetime

print("{} \t Inicia Proceso Batch"
    .format(datetime.now())
    )

print("\t Python version: {}"
    .format(sys.version)
    )

# Pillow

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# Connection module

from connect_mongo_db import (
    query_in_process, 
    update_processed_files
)

# Email module
 
from send_mail import send_email

# S3 
import logging
import boto3
from botocore.exceptions import ClientError

# Global varaibles
SIZE = (800, 600)
SIZING_METHOD = 'T'
EMAIL_PASSWORD = os.getenv('AWS_EMAIL_PASS')

WA_URL = os.environ['WA_URL']


BASE_DIR = Path()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FONT_SELECTION = "/app/media/font/arial.ttf"  # FONT_SELECTION = "font/arial.ttf"
FONT_SIZE = 24
RECTANGLE_COLOR = (255,255,255)
FONT_COLOR = (0,0,0)


def processing(test = False):
    # Database Connection and get image to process from queue

    designs_to_process = query_in_process()

    data = {}

    if designs_to_process is not None:

        for design in designs_to_process:
            try:
                # print("-"*110)
                # print("{} \t Inicia procesamiento de la imagen {} -> {}"
                #    .format(datetime.now(),
                #       design['image_id'],
                #        design['id'])
                #    )

                # print("\t {} \t Inicial {}" .format(datetime.now(), design['image_id']))
                print("\t Procesamiento \t Comienzo {} \t {}".format(datetime.now(), design['image_id']))

                data['creator'] = design['first_name']
                data['email'] = design['email']
                data['date'] = design['design_create_date'].strftime(DATE_FORMAT)
                data['image'] = design['image_original']
                data['image_pk'] = design['image_id']
                data['design_pk'] = design['id']
                data['url'] =  WA_URL + design['url']

                # print("{} \t Inicia lectura de imagen en S3"
                #    .format(datetime.now()))


                # print(os.getenv('AWS_ACCESS_KEY_ID'))
                # print(os.getenv('AWS_SECRET_ACCESS_KEY'))
                s3_session = boto3.Session(
                    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
                )


                s3_manager = s3_session.resource('s3')

                s3_bucket = s3_manager.Bucket(os.getenv('AWS_STORAGE_BUCKET_NAME'))
                # print(os.getenv('AWS_STORAGE_BUCKET_NAME'))

                name_simple = data['image'].replace('originals/','')

                s3_bucket.download_file( data['image'], name_simple )
                im = Image.open( BASE_DIR / name_simple )

                default_width = SIZE[0]
                default_height = SIZE[1]

            # try:
                # PASO 1: Cambia de tamaño la imagen

                if SIZING_METHOD == 'T':
                    im.thumbnail(SIZE, Image.ANTIALIAS)
                else:
                    im = im.resize(SIZE, Image.ANTIALIAS)

                # PASO 2: Dibuja la marca de la imagen procesadas

                draw = ImageDraw.Draw(im)

                font = ImageFont.truetype(FONT_SELECTION, FONT_SIZE)

                width, height = im.size

                if height < default_height:
                    default_height = height

                if width < default_width and height == default_height:
                    default_width = width

                draw.rectangle(
                    [0, default_height - 30, default_width, default_height],
                    fill=RECTANGLE_COLOR
                )

                draw.text(
                    (10, default_height - 30),
                    ("{} - {} ".format(data['creator'],data['date'])),
                    FONT_COLOR,
                    font=font
                )

                # PASO 3: Almacena la imagen generada en formato PNG

                name_file = data['image'].replace('originals/','')

                name_file = 'processed_' + name_file[:name_file.index('.')]

                name_file =  name_file + '.png'

                output = BASE_DIR / name_file

                im.save(output)

                output_file = 'processed/' + name_file

                upload_file_s3(name_file, s3_bucket)
                # PASO 4: Cambia el estado de la imagen procesada en la base de datos

                update_processed_files(
                    data['image_pk'],
                    data['design_pk'],
                    output_file)

                # PASO 5: Envía el email de la imagen procesada
                if not test:
                    # print('Enviar email a: ')
                    # print(data['email'])
                    send_email(
                        EMAIL_PASSWORD,
                        data['email'],
                        data['creator'],
                        name_file,
                        data['url']
                    )

                # print(
                #    '{} \t Diseño: "{}" procesado con exito en [{}] con ({},{})px'.format(
                #        datetime.now(), data['image'], SIZING_METHOD, default_width, default_height
                #    ))

                # print("{} \t Fin {}".format(datetime.now(), design['image_id']))
                print("\t Procesamiento \t Finaliza {} \t {}".format(datetime.now(), design['image_id']))

                # PASO 6: Eliminar temporal
                os.remove(BASE_DIR / name_simple)
                os.remove(output)
            except Exception as error:
                print("{} \t Error en diseño: {} -> {}"
                    .format(datetime.now(), data['image'], error))


def upload_file_s3(file_name, bucket):
    with open(file_name, 'rb') as upload:
        try:
            upload_key = 'processed/' + file_name

            bucket.put_object(
                Key = upload_key,
                Body = upload
            )
        except ClientError as e:
            print("{} \t Proceso S3 Fallo {}".format(
                datetime.now(),logging.error(e))) 
            return False
        return True


def run():
    while True:
        processing()


if __name__ == "__main__":
    run()
