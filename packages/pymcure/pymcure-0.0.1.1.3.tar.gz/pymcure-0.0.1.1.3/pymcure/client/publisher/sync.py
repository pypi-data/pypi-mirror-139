# -*- coding: utf-8 -*-
""" 
@author: Vianney ADOU <adoujmv@gmail.com>
"""
import requests

from ..message import Message
from ..exceptions import PublishRejectedError, UnauthorizedPublishedError
from .publisher import Publisher

class SyncPublisher(Publisher):
    def publish(self, message: Message) -> str:
        # check the parameters of the request
        self._check_parameters(message)
        print(self.mercure_hub)
        # Create the request
        response = requests.post(
            self.mercure_hub,
            Publisher._get_form_data(message),
            headers=self._get_request_headers()
        )

        if response.status_code == 403:
            raise PublishRejectedError(response.text)
        
        if response.status_code == 401:
            raise UnauthorizedPublishedError(response.text)

        return str(response.text)