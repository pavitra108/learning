class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

d = Animal("cats")
print(d.speak())
a= Dog("Tuffle")
print(a.speak())
