import logging

import requests


class PyLiphemAPI(object):
    """
    Basic object-oriented API wrapper

    :param object: _description_
    :type object: _type_
    """
    def __init__(self, token: str):
        self.token = token

    async def add_order(self, action: str, token: str, service: int=None, quantity: int=None, link: str=None):
        """
        Adds an order

        :param action: Action (from BigSMM API)
        :type action: str
        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :param service: Service number (from BigSMM API), defaults to None
        :type service: int, optional
        :param quantity: Number of executions, defaults to None
        :type quantity: int, optional
        :param link: Resource link, defaults to None
        :type link: str, optional
        :return: Success/error message
        :rtype: json/dict
        """

        response = requests.get(f'https://bigsmm.ru/api/v2/?action={action}&key={token}&service={service}&quantity='
                                f'{quantity}&link={link}')
        logging.info(response)

        if response.status_code == 200:
            return response.json()
        else:
            message = 'A request to the BIG SMM API was unsuccessful. The server returned HTTP {0} {1}.'
            return message.format(response.status_code, response.reason)

    async def service_list(self):
        """
        Shows a list of all services

        :return: list of services
        :rtype: dict
        """

        response = requests.get('https://bigsmm.ru/api/v2/?action=services')
        return response.json()

    async def check_balance(self, token: str):
        """
        Method for checking balance

        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :return: Json of received data
        :rtype: dict
        """

        response = requests.get(f"https://bigsmm.ru/api/v2/?action=balance&key={token}")
        return response.json()

    async def order_list(self, token: str):
        """
        Shows order list for token

        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :return: Json of received data
        :rtype: list
        """

        response = requests.get(f"https://bigsmm.ru/api/v2/?action=orders&key={token}")
        return response.json() 

    async def order_details(self, token: str, order_id: int):
        """
        Get current order details

        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :param order_id: Order ID
        :type order_id: int
        :return: Json of received data
        :rtype: list
        """

        response = requests.get(f"https://bigsmm.ru/api/v2/?action=order_details&key={token}6&order={order_id}")
        return response.json() 

    async def order_status(self, token: str, order_id: int):
        """Shows status of executing order

        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :param order_id: Order ID
        :type order_id: int
        :return: Json of received data
        :rtype: list
        """

        response = requests.get(f"https://bigsmm.ru/api/v2/?action=status&key={token}&order={order_id}")
        return response.json() 

    async def order_status_mass(self, token: str, orders_id: list):
        """Mass-checking for orders's statuses

        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :param orders_id: List of unfiltered orders's ids
        :type orders_id: list
        """
        formatted = ""
        for i in orders_id:
            if i != orders_id[-1]:
                formatted += i + ","
            else:
                formatted += i

        response = requests.get(f"https://bigsmm.ru/api/v2/?action=status&key={token}&orders={formatted}")
        return response.json() 

    async def order_cancel(self, token: str, order_id: int):
        """Cancer orders by their id

        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :param order_id: Order ID
        :type order_id: int
        """

        response = requests.get(f"https://bigsmm.ru/api/v2/?action=cancel&key={token}&order={order_id}")

    async def referreal_list(self, token: str):
        """List of referrals from current token

        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :return: Json of received data
        :rtype: list
        """
        response = requests.get(f"https://bigsmm.ru/api/v2/?action=referrals&key={token}")
        return response.json()

    async def referreals_total(self, token: str):
        """
        Income from all referrals for all time

        :param token: API TOKEN (from BigSMM API)
        :type token: str
        :return: Json of received data
        :rtype: dict
        """

        response = requests.get(f"https://bigsmm.ru/api/v2/?action=referrals_total&key={token}")
        return response.json()
