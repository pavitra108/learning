<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>


  <p align="left">
    This is my README file that documents my Meme Generator project!
    <br />
  <br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#project_structure">Project Structure</a>
      <ul>
        <li><a href="#python_library_modules_used">Python Library Modules Used</a></li>
        <li><a href="#getting_started">Getting Started</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

This project is a Python-based meme generator that allows you to create memes by combining images and quotes. The project consists of a set of Python scripts and utilizes various libraries for image processing and text handling.

### Features

- **Meme Generation:** The core functionality of the project is to generate memes. You can either specify an image path, quote body, and author, or let the program choose a random image and quote for you.

- **Customizable Quotes:** The project supports various types of quote files, including TXT, DOCX, PDF, and CSV, making it easy to customize the content of your memes.

- **Command-Line Interface:** The project includes a command-line interface (CLI) for easy meme generation. You can provide arguments such as image path, quote, and author to create memes on the fly.

- **Web-based application:** This project also includes an app that uses the Quote Engine Module and Meme Generator Modules to generate a random captioned image.


### Project Structure

- `meme.py`: This script contains the core functionality for generating memes. It imports modules from `QuoteEngine` and `MemeEngine` to handle image and quote processing.

- `QuoteEngine`: This module contains functionality for parsing different quote file formats and managing quotes. It includes the `QuoteModel` class for representing quotes.
  - `Importer.py`: Provides functionality for ingesting quotes from various file formats.
  - `QuoteModel.py`: Defines the `QuoteModel` class to represent quotes.

- `MemeEngine`: This module provides image handling, image resizing, adding text and meme generation. The `MemeModel` class is used to add text to images.
  - `MemeModel.py`: Defines the `MemeModel` class used for resizing image and adding text to images.

- `app.py`: This script is the entry point for the meme generation process. It uses the command-line interface and also a simple web service to handle user input to generate memes.

### Getting Started

Use the `README.md` to get started.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Python Library Modules Used

The following Python Library Modules are used to complete this project.

* `Pillow`
* `Random`
* `Time`
* `OS`
* `Docx`
* `Pandas`
* `Xpdf`
* `Subprocess`
* `Argparse`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Getting Started

1. Clone this repository to your local machine.

2. Install the required dependencies (the modules mentioned above), including Pillow (PIL), if not already installed.

3. Run the `app.py` script with appropriate command-line arguments to create memes. You can specify the image path, quote, and author as needed.

### Usage

To create a meme with custom content, you can use the following command:
```shell
python generate_meme.py --path /path/to/image.jpg --body "Your quote goes here" --author "Author Name"
```
