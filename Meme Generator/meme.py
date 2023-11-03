import os
import random
import argparse
from QuoteEngine.Importer import Ingestor
from MemeEngine.MemeModel import MemeEngine
from QuoteEngine.QuoteModel1 import QuoteModel
"""This is the main script."""

def generate_meme(path=None, body=None, author=None):
    """Generate a meme given a path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Generate memes')

    # Add command-line arguments
    parser.add_argument('--path', type=str, help='Path to an image file')
    parser.add_argument('--body', type=str, help='Quote body to add to the image')
    parser.add_argument('--author', type=str, help='Quote author to add to the image')

    # Parse the command-line arguments
    args = parser.parse_args()

    try:
        # Call the generate_meme function with the parsed arguments
        generated_meme_path = generate_meme(args.path, args.body, args.author)

        if generated_meme_path:
            print(f'Meme generated and saved at: {generated_meme_path}')
        else:
            print('Meme generation failed.')

    except Exception as e:
        raise e





