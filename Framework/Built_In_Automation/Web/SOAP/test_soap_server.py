import logging
from spyne import (
    Application,
    rpc,
    ServiceBase,
    Integer,
    Unicode,
    Float,
    Boolean,
    Iterable,
    ComplexModel,
    Array,
)
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware


# Define the Item type
class Item(ComplexModel):
    item_id = Unicode
    quantity = Integer
    price = Float


# Define the Order type
class Order(ComplexModel):
    order_id = Unicode
    customer_name = Unicode
    items = Array(Item)
    shipping_address = Unicode


# Define the SOAP service
class CalculatorService(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def add(ctx, num1, num2):
        """Adds two numbers."""
        return num1 + num2

    @rpc(Order, Boolean, _returns=Iterable(Unicode))
    def process_order(ctx, order, priority):
        """Processes an order."""
        # Calculate total cost
        total_cost = sum(item.quantity * item.price for item in order.items)
        # Generate item descriptions
        item_descriptions = [
            f"Item {item.item_id}: {item.quantity} x ${item.price}"
            for item in order.items
        ]

        # Include priority information
        priority_note = (
            "Priority order processing enabled."
            if priority
            else "Standard order processing."
        )
        return [f"Total Cost: ${total_cost:.2f}", *item_descriptions, priority_note]


# Create the SOAP application
soap_app = Application(
    [CalculatorService],
    tns="zeuz.ai.soap",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

# WSGI Application
soap_wsgi_app = WsgiApplication(soap_app)

# Flask application
app = Flask(__name__)

# Attach the SOAP application to Flask
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/soap": soap_wsgi_app})


@app.route("/", methods=["GET"])
def index():
    return "Welcome to the SOAP API! Use /soap for SOAP requests."


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    app.run(host="0.0.0.0", port=5000)
