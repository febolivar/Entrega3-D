# Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import time

from django.conf import settings
import logging
import boto3
from botocore.exceptions import ClientError


def send_sqs_message(msg_body):
    """
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    print("region name: " + settings.APP_AWS_QUEUE['region_name'])
    print("aws_access_key_id: " + settings.APP_AWS_QUEUE['aws_access_key_id'])
    print("aws_secret_access_key: " + settings.APP_AWS_QUEUE['aws_secret_access_key'])
    print("sqs_queue_url: " + settings.APP_AWS_QUEUE['sqs_queue_url'])

    sqs_client = boto3.client('sqs',
                              region_name=settings.APP_AWS_QUEUE['region_name'],
                              aws_access_key_id=settings.APP_AWS_QUEUE['aws_access_key_id'],
                              aws_secret_access_key=settings.APP_AWS_QUEUE['aws_secret_access_key']
                              )

    msg = sqs_client.send_message(QueueUrl=settings.APP_AWS_QUEUE['sqs_queue_url'],
                                  MessageBody=msg_body)

    print("Mensaje enviado a SQS exitosamente")
    '''
    try:

    except ClientError as e:
        logging.error(e)
        return None
    '''
    return msg