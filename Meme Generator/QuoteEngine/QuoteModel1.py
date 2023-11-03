"""This code encapsulates the body and author of quotes."""


class QuoteModel:
    """This is a simple class that encapsulates the body and author of quotes."""

    def __init__(self, body, author):
        """Create a constructor method of a class. It takes three parameters: self, body, and author.

        Params:
        body: This is a parameter that is used to initialize the body attribute of the class.
        author: This is a parameter that is used to initialize the author attribute of the class.
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Define how an object of the class should be represented as a string."""
        return f'{self.body} - {self.author}'
