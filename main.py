import consts
import exceptions

import requests, json
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode

class PrintfulPy:

    VERSION = "0.0.0.1a"

    _store = {
        'base_url': consts.API_BASE_URL,
        'connection': None,
        'auth': None,
        'last_response': None,
        'last_response_raw': None,
        'auth_user': None,
        'auth_pass': None
    }

    def __init__(self, api_key: str = None, connect: bool = True) -> None:
        """
        Printful API class. Initializes the connection to the API server.

        :param key: API Key (Get it from your store's dashboard). Note that this
            is not the consumer key and secret found under store info. Rather,
            the API key can be found under Store > API and will be two strings
            separated by a ':'.
        :param connect: Boolean that sets if to actually connect to Printful API server.

        :return: A stateful object with an authenticated connection.
        """
        self.api_key = api_key
        self.__verify_api_key()

        self._store['auth_user'], self._store['auth_pass'] = self.api_key.split(":")

        if connect:
            self.__connect()

    def __verify_api_key(self) -> None:
        """
        CheckWall that makes sure the API key is in a valid format.

        :return: None
        """
        if not self.api_key:
            raise exceptions.PrintfulApiKeyException('No Printful API Key Provided', 'error code: 0.1')
        
        if not ':' in self.api_key:
            raise exceptions.PrintfulApiKeyException('Invalid Printful API Key', 'error code: 0.2')
        
    def __connect(self) -> None:
        """
        Configures the connection to the API server.
        
        :return: None
        """
        self._store['connection']: requests.Session = requests.Session()
        self._store['connection'].auth = HTTPBasicAuth(self._store['auth_user'], self._store['auth_pass'])
        self._store['connection'].headers['User-Agent'] = 'PrinfulPy (Python API wrapper for Prinful API)'
        self._store['connection'].headers['Content-Type'] = 'application/json'

    def get_product_list(self):
        """
        Get all product list
        """
        return self.__do_get('products')

    def get_variant_info(self, pk=None):
        """
        Get info about a variant

        :param pk: The Printful identifier for the variant.
        """
        return self.__do_get('products/variant/' + pk)

    def get_product_info(self, pk=None):
        """
        Get product's variant list

        :param pk: The Printful identifier for the variant.
        """
        return self.__do_get('products/' + pk)

    def get_order_list(self):
        """
        Get order list
        """
        return self.__do_get('orders')

    def put_order_new(self, data=None):
        """
        Create new order
        """
        return self.__do_post("orders", data=data)

    def get_order_info(self, pk=None):
        """
        Get order data
        """
        return self.__do_get('orders/' + pk)

    def put_order_cancel(self, pk=None):
        """
        Cancel an order
        """
        return self.__do_delete("orders/" + pk)

    def put_order_update(self, pk=None, data=None):
        """
        Update order data
        """
        return self.__do_put("orders/" + pk, data=data)

    def put_order_confirm(self, pk=None):
        """
        Confirm draft for fulfillment
        """
        return self.__do_post('orders/' + pk + "/confirm")

    def get_file_list(self):
        """
        Get list of files
        """
        return self.__do_get('files')

    def put_file_new(self, data):
        """
        Add new file
        """
        return self.__do_post('/files', data=data)

    def get_file_info(self, pk=None):
        """
        Get file info
        """
        return self.__do_get('files/' + pk)

    def get_shippingrate_calc(self, data):
        """
        Calculate shipping rates
        """
        return self.__do_post("shipping/rates", data=data)

    def get_syncproduct_list(self):
        """
        Get list of sync products
        """
        return self.__do_get('sync/products')

    def get_syncproduct_info(self, pk=None):
        """
        Get info about sync product
        """
        return self.__do_get('sync/products/' + pk)

    def put_syncproduct_remove(self, pk=None):
        """
        Unlink all synced variants of this product
        """
        return self.__do_delete('sync/products/' + pk)

    def get_syncvariant_info(self, pk=None):
        """
        Get info about sync variant
        """
        return self.__do_get('sync/variant/' + pk)

    def get_countries_list(self):
        """
        Retrieve country list
        """
        return self.__do_get('countries')

    def get_tax_geos(self):
        """
        Retrieve state list that requires state tax calc
        """
        return self.__do_get('tax/rates')

    def get_tax_calc(self, data=None):
        """
        Calculate tax rate
        """
        return self.__do_post("tax/rates", data=data)

    def get_webhooks_info(self):
        """
        Get webhook configuration
        """
        return self.__do_get('webhooks')

    def put_webhooks_update(self, data=None):
        """
        Set up webhook configuration
        """
        return self.__do_post("webhooks", data=data)

    def put_webhooks_disable(self):
        """
        Disable webhook support. No data param, because the API doesn't
        require it.
        """
        return self.__do_delete("webhooks")

    def get_store_info(self):
        """
        Get store info
        """
        return self.__do_get('store')

    def put_store_packingslip(self, data=None):
        """
        Change store packing slip
        """
        return self.__do_post('store/packing-slip', data=data)

    def get_item_count(self):
        """
        Returns total available item count from the last request if it supports
        paging (e.g order list) or nil otherwise
        """
        if(self._store['last_response'] and 'paging' in self._store['last_response']):
            return self._store['last_response']['paging']['total']
        else:
            None

    
    def __do_get(self, path: str, params: dict = None) -> str:
        """
        Perform a GET request to the API

        :param path: Request path (ex. 'orders' or 'orders/123')
        :param params: Additional GET parameters as a dictionary

        :return: The json result param
        """
        return self.__request('GET', path, params)
    
    def __do_delete(self, path: str, params: dict = None) -> str:
        """
        Perform a DELETE request to the API
        
        :param path: Request path (ex. 'orders' or 'orders/123)
        :param params: Additional DELETE parameters as a dictionary

        :return: The json result param
        """
        return self.__request('DELETE', path, params)
    
    def __do_post(self, path: str, data: dict = None, params: dict = None) -> str:
        """
        Perform a POST request to the API
        
        :param path: Request path (ex. 'orders' or 'orders/123)
        :param data: Request body data as a dictionary
        :param params: Additional POST parameters as a dictionary

        :return: The json result param
        """
        return self.__request('POST', path, params, data)
    
    def __do_put(self, path: str, data: dict = None, params: dict = None) -> str:
        """
        Perform a PUT request to the API
        
        :param path: Request path (ex. 'orders' or 'orders/123)
        :param data: Request body data as a dictionary
        :param params: Additional PUT parameters as a dictionary

        :return: The json result param
        """
        return self.__request('PUT', path, params, data)
    
    def __request(self, method: str, path: str, params: dict = None, data: dict = None) -> dict:
        """
        General request function

        :param method: The HTTP(S) methods: GET, POST, PUT and DELETE.
        :param path: The request path (ex: api.printful.com/products).
        :param params: The url params (ex: api.printful.com/products?offset=10).
        :param data: The json to give the api data with.

        :return: The result
        """
        self._store['last_response'] = None
        self._store['last_response_raw']: requests.Response = None

        # Let's allow full URI in requests, if only the /path is given, then add the API_BASE_URL as prefix
        if path.startswith('http'):
            url = path
        else:
            url = self._store['base_url'] + path

        if params:
            url += "?" + urlencode(params)

        if data:
            body = json.dumps(data)
        else:
            body = None

        try:
            request = self._store['connection'].request(
                method,
                url,
                data=body
            )
            self._store['last_response_raw'] = request

        except Exception as e:
            raise exceptions.PrintfulApiFailException('Printful API request failed: {}'.format(e), '1.0')
        
        self._store['last_response_raw']: requests.Response = self._store['last_response_raw']
        if (self._store['last_response_raw'].status_code < 200 or self._store['last_response_raw'].status_code >= 300):
            raise exceptions.PrintfulApiFailException('Invalid Printful API reponse', '1.1')
        
        # Now let's decode the response
        try:
            data = json.loads(
                self._store['last_response_raw'].content.decode('utf-8')
            )
            self._store['last_response'] = data
        except ValueError as e:
            raise exceptions.PrintfulApiFailException('Printful API sent a non json response', '1.2')
        
        return data['result']

PrintfulPy()