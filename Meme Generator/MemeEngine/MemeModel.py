"""This code is created to generate meme from a random picture by adding a random quote to it."""

from PIL import Image, ImageDraw, ImageFont
import os
import time
import random
import requests
from QuoteEngine import Importer


class MemeEngine():
    """Genereate a meme with a random quote."""

    def __init__(self,  img_path, text=None, author=None, width=500):
        """
        Initialize a Meme object.

        Parameters:
        - img_path (str): The file path to the background image for the meme.
        - text (str, optional): The text to be added to the meme. Default is None.
        - author (str, optional): The author or source of the meme text. Default is None.
        - width (int, optional): The width of the meme image in pixels. Default is 500.

        Note:
        - If 'text' and 'author' are both None, the meme will have no text.
        - If 'text' is provided but 'author' is None, the meme will display only the 'text'.
        - If both 'text' and 'author' are provided, the meme will display 'text' with an attribution to 'author'.
        - 'width' determines the width of the resulting meme image, while the height is adjusted proportionally.
        """
        self.img_path = img_path
        self.text = text
        self.author = author
        self.width = width

    def create_new_path(self, path):
        """Generate a unique filename based on a timestamp."""
        timestamp = int(time.time())
        base_filename = os.path.basename(path)
        file_name, file_extension = os.path.splitext(base_filename)

        directory = "_data/Memes/"
        new_filename = f"{file_name}_{timestamp}{file_extension}"
        new_path = os.path.join(directory, new_filename)
        absolute_path = os.path.abspath(new_path)
        print(absolute_path)
        return absolute_path

    def make_meme(self, img_path, text, author, width=500):
        """Make a meme by manipulating an image and adding a random quote."""
        current_directory = os.path.dirname(os.path.abspath(__file__))
        directory_path = os.path.join(current_directory, '..', '_data', 'DogQuotes')
        files = os.listdir(directory_path)
        random_file = random.choice(files)
        random_file_path = os.path.join(directory_path, random_file)

        # Get a random quote from a random file from the given directory.
        if text is None and author is None:
            quote_list = Importer.Ingestor.parse(random_file_path)
            print(quote_list)
            quote = random.choice(quote_list)
            print(f"quote {quote}, type is {type(quote)}")
            text = quote.body
            author = quote.author

        # open file
        meme_img = Image.open(img_path, mode='r', formats=None)



        if width is not None:
            ratio = width / float(meme_img.size[0])
            height = int(ratio * float(meme_img.size[1]))
            resized_img = meme_img.resize((width, height), Image.NEAREST)
            resized_img_path = self.create_new_path(img_path)
            resized_img.save(resized_img_path)

            # Ppen resized image to add text
            opened_img = Image.open(resized_img_path)

            # Add text to the image
            font_path = "/Library/Fonts/Arial.ttf"
            meme_image = ImageDraw.Draw(opened_img)
            font = ImageFont.truetype(font_path, 20)
            meme_image.text((50, 50), text=f"{text} - {author}", fill=(255, 255, 255), font=font)
            meme_path = resized_img_path
            opened_img.save(meme_path)
            return meme_path
