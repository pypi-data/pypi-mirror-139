# -*- coding: utf-8 -*-
""" 
@author: Vianney ADOU <adoujmv@gmail.com>
"""

import urllib
from abc import ABC, abstractmethod, ABCMeta
import jwt
from ..message import Message

PAYLOAD = {
    "mercure": {
        "subscribe": [
        ],
        "publish": [
        ]
    }
}

#jwt header
HEADER = {
    "typ": "JWT",
    "alg": "HS256"
}


class Publisher(ABC):
    __metaclass__=ABCMeta

    mercure_hub = None
    mercure_jwt = None
    message = None
    secret = None
    payload = None
    header = None

    def __init__(self, mercure_hub, mercure_jwt, secret,payload=PAYLOAD,header=HEADER):
        self.mercure_hub = mercure_hub
    
        self.secret = secret
        self.payload = payload
        self.header = header

        if mercure_jwt == None:
            self.mercure_jwt = self._get_jwt()
        else:
            self.mercure_jwt = mercure_jwt

    @abstractmethod
    def publish(self, message: Message) -> str:
        """
        Publish an update to Mercure

        :param list topics: Topics to be published
        :param Message message: The message component with all the update details
        """ 
        pass

    def _check_parameters(self, message):
        """
        Check if the parameters has the right values
        :param Message: the message object
        """
        
        if len(self.mercure_hub) == 0:
            raise AttributeError('Please provide a mercure hub url')

        if len(self.mercure_jwt) == 0:
            raise AttributeError('Please provide a mercure jwt or got None')

        if len(self.secret) == 0:
            raise AttributeError('Please provide a mercure secret')

        #it has to have at last on topic
        if type(message.topics) is not list:
            raise TypeError('topics must be a list')
        elif len(message.topics) == 0:
            raise AttributeError('topics cannot be empty')

        # And data must be a string
        if type(message.data) is not str:
            raise TypeError('private must be a str')
        
        #if private is available, check if its string
        if message.private is not None and type(message.private) is not bool:
            raise TypeError('message_id must be a string')

        #if message_id is available, check if its string
        if message.message_id is not None and type(message.message_id) is not str:
            raise TypeError('message_id must be a string')

        #if event_type is available, check if its string
        if message.event_type is not None and type(message.event_type) is not str:
            raise TypeError('event_type must be a string')

        #if event_type is available, check if its integer
        if message.retry is not None and type(message.retry) is not int:
            raise TypeError('retry must be a integer')

    def _get_jwt(self):
        return jwt.encode(self.payload, self.secret, algorithm='HS256',headers=self.header)


    def _get_request_headers(self) -> object:
        """
        Return the headers needed by Mercure
        :return object
        """
        return {
            'Authorization': 'Bearer {}'.format(self.mercure_jwt),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    @staticmethod
    def _get_form_data(message) -> str:
        """
        Encode the message
        :param Message message
        :return str
        """
        form_data = {
            'topic': message.topics,
            'data': message.data
        }

        if message.private == True:
            form_data['private'] = "on"

        if message.message_id is not None:
            form_data['id'] = message.message_id

        if message.event_type is not None:
            form_data['type'] = message.event_type
        
        return urllib.parse.urlencode(form_data, True)