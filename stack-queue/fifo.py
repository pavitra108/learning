from flask import Flask, render_template, request


class PaviQueue:

    """
    Queue that adds and pops order numbers in FIFO order.
    """

    def __init__(self):
        self.orders = []
        pass

    def __str__(self):
        return f"The current orders in queue: {self.orders}"

    def add(self, order_number):
        self.orders.append(order_number)
        print(self.orders)
        return self.orders

    def pop(self):
        while self.orders:
            element_to_pop = self.orders.pop(0)
            return element_to_pop
        else:
            print("All orders sre processed.")


app = Flask(__name__)
order_queue = PaviQueue()  # A global queue for order numbers

@app.route('/')
def home():
    return render_template('template.html')

@app.route('/get_order', methods=['POST'])
def get_orders():
    action = request.form['action']
    order_number = request.form['order_number']

    if action == 'place_order':
        order_queue.add(order_number)
        message = f"Order {order_number} added to the queue."
    else:
        return "Invalid action"

    return render_template('template.html', message=message)

@app.route('/process_order', methods=['POST'])
def process_orders():
    process = request.form['process']
    if process == 'process_order':
        result = order_queue.pop()
        message = f"Next order to process: {result}"
    else:
        message = "No orders to process"

    return render_template('template.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

"""if __name__ == '__main__':
    queue = PaviQueue()
    queue.add("pavi")
    queue.add("viswesh")
    elem = queue.pop()
    print(elem)
    queue.add("vihaan")
    print(queue)"""

