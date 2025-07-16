from flask import Flask, render_template, request

class PaviStack:

    """
    Abitlity to add and pop an element, it should be FILO
    """

    def __init__(self):
        self.names = []
        pass

    def __str__(self):
        return f"The current list: {self.names}"

    def add(self, element):
        self.names.append(element)
        print(self.names)
        return self.names

    def pop(self):
        while self.names:
            element_to_pop = self.names.pop()
            print(element_to_pop)
            return element_to_pop
        else:
            print("list is empty")

app = Flask(__name__)
name_stack = PaviStack()  # A stack for names

@app.route('/')
def home():
    return render_template('template.html')

@app.route('/get_name', methods=['POST'])
def get_name():
    action = request.form['action']
    full_name = request.form['name']

    if action == 'add_name':
        name_stack.add(full_name)
        message = f"Name {full_name} added to the stack."
    else:
        return "Invalid action"

    return render_template('template.html', message=message)

@app.route('/process_name', methods=['POST'])
def process_name():
    process = request.form['process']
    if process == 'process_name':
        result = name_stack.pop()
        message = f"Next order to process: {result}"
    else:
        message = "No names to process"

    return render_template('template.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

'''if __name__ == '__main__':
    stack = PaviStack()
    stack.add("pavi")
    stack.add("viswesh")
    elem = stack.pop()
    stack.add("vihaan")
    print(stack)'''

