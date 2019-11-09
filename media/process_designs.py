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
sys.path.append('/home/SIS/da.salgadoc/.local/lib/python3.5/site-packages/')
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

from connect_db import (
    connect_to_data_base,
    close_connection,
    query_in_process, 
    update_processed_files
)

# Email module
 
from send_mail import send_email

# Global varaibles
SIZE = (800, 600)
SIZING_METHOD = 'T'
EMAIL_PASSWORD = 'Dsa123poi' 


BASE_DIR = Path()

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FONT_SELECTION = "font/arial.ttf"
FONT_SIZE = 24
RECTANGLE_COLOR = (255,255,255)
FONT_COLOR = (0,0,0)

# Database Connection and get "In Process" files

connection, cursor = connect_to_data_base()
designs_to_process = query_in_process(cursor)

data = {}

for key, design in enumerate(designs_to_process):
    print("-"*110)
    print("{} \t Inicia procesamiento de la imagen {} -> {}"
        .format(datetime.now(),
            design[4],
            design[5])
        )

    data['creator'] = design[0]
    data['email'] = design[1]
    data['date'] = design[2].strftime(DATE_FORMAT)
    data['image'] = design[3]
    data['image_pk'] = design[4]
    data['design_pk'] = design[5]
    
    im = Image.open( BASE_DIR / data['image'] )

    default_width = SIZE[0]
    default_height = SIZE[1]

    try:
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
        output = Path('processed') / name_file
        im.save(output)
        output_file = 'processed/' + name_file 

        # PASO 4: Cambia el estado de la imagen procesada en la base de datos

        update_processed_files(
            connection,
            cursor,
            data['image_pk'], 
            data['design_pk'],
            output_file)
        
        # PASO 5: Envía el email de la imagen procesada
        
        send_email(
            EMAIL_PASSWORD,
            data['email'],
            data['creator'],
            name_file
        )

        print(
            '{} \t Diseño: "{}" procesado con exito en [{}] con ({},{})px'.format(
                datetime.now(), data['image'], SIZING_METHOD, default_width, default_height
            )) 
         
    except Exception as error:
        
        print("{} \t Error en diseño: {} -> {}"
            .format(datetime.now(), data['image'], error))

close_connection(cursor)
