class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

    def get_count(self):
        return self.count

test = Counter()
test.increment()
test.increment()
test.reset()
a = test.get_count()
print(a)


