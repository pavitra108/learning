import random
import requests
import os
from flask import Flask, render_template, abort, request, send_from_directory
from MemeEngine.MemeModel import MemeEngine
from QuoteEngine.Importer import Ingestor
from QuoteEngine.ImportInterface import IngestorInterface

# @TODO Import your Ingestor and MemeEngine classes

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quote_file = random.choice(quote_files)
    quotes_list = Ingestor.parse(quote_file)

    quotes = quotes_list

    images_path = "./_data/photos/dog/"
    images_path = os.path.abspath(images_path)
    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    images_list= [os.path.join(images_path, filename) for filename in os.listdir(images_path)]

    imgs = images_list

    print(quotes, imgs)
    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array
    global imgs
    global quotes
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    img_name = path.split("/")[-1]
    return render_template('meme.html', path=f"./_data/Memes/{img_name}")


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')

@app.route('/_data/Memes/<filename>')
def images(filename):
    images_directory = "./_data/Memes"  # Replace with the path to your images directory
    return send_from_directory(images_directory, filename)


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""

    def is_image_url(url):
        try:
            response = requests.head(url)
            content_type = response.headers.get('content-type')
            if content_type and content_type.startswith('image/'):
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            # Handle invalid URL exceptions here
            print(f"Invalid URL: {url}\nPlease check if the URL contains an image.")
            return False

    if 'image_url' in request.form:
        image_url = request.form['image_url']
        if is_image_url(image_url):

        # 1. Save the image from the image_url to a temporary local file
            response = requests.get(image_url)
            if response.status_code == 200:
                with open('temp_image.jpg', 'wb') as f:
                    f.write(response.content)

            # 2. Use the meme object to generate a meme using the temporary image
            #    file, the body, and author form parameters.
            body = request.form['body']
            author = request.form['author']
            meme = MemeEngine('./tmp').make_meme('temp_image.jpg', body, author)  # Implement this function

            # 3. Remove the temporary saved image
            os.remove('temp_image.jpg')
            img_name = meme.split("/")[-1]
            path = f"./_data/Memes/{img_name}"

            return render_template('meme.html', path=path)
        else:
            return f"Invalid URL: {image_url}<br> Please check if the URL contains an image."


if __name__ == "__main__":
    app.run()
