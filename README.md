# PrintfulPy
## Printful API Wrapper for Python

This Python package provides a convenient wrapper for interacting with the [Printful API](https://developers.printful.com/docs) within your Python applications. It simplifies the process of integrating Printful's services into your projects, enabling seamless management of products, orders, shipments, and more.

## Installation

You can install the package via pip:

###WORK IN PROGRESS

## Usage

### Initialization

First, import the `PrintfulPy` class and initialize it with your API key:

```python
from printfulpy import PrintfulPy

api_key = 'YOUR_PRINTFUL_API_KEY'
client = PrintfulPy(api_key)
```

### Examples

#### Get Product Catalog

Retrieve the list of available products in the Printful catalog:

```python
products = client.get_product_list()
print(products)
```

#### Create an Order

Create a new order with specific items and details:

```python
order_data = {
    # Add order details here
}
order = client.put_order_new(order_data)
print(order)
```

#### Retrieve Order Information

Retrieve information about a specific order:

```python
order_id = 'YOUR_ORDER_ID'
order_info = client.get_order_info(order_id)
print(order_info)
```

## Documentation

For detailed information on available methods and their parameters, refer to the [Printful API documentation](https://developers.printful.com/docs).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to expand on each section, add code snippets, or customize it further based on your specific implementation or additional functionalities.
