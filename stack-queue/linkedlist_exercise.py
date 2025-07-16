
# to create the pointers
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# to create a linked list
class LinkedList:
    # to create an empty list
    def __init__(self):
        self.head = None

    # to add a node (data & pointer) to the end of the list
    def add(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        # navigate with the "current" to get to the last node and add new node there
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def print_ll(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print ("end")


# use linked list - creating an instance of object
my_llist = LinkedList()
my_llist.add("Vish")
my_llist.add("Pavi")
my_llist.add("Vihaan")
my_llist.add("Nithin")

my_llist.print_ll()





