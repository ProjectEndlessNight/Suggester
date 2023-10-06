# Suggester

A simple suggestion system for your media library

## Features

- Absurdly simple and lightweight
- Easy-ish to use
- No database required
- No JS required (via the magic of forms)
- Pretty okay looking

## Installation

Should work anywhere Python does, but I've used it exclusively on Linux. For a quick and easy install on Linux:

```sh
git clone https://github.com/ProjectEndlessNight/Suggester.git
cd Suggester
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python serve.py
```

Very similar commands should work on Windows:

```bat
git clone https://github.com/ProjectEndlessNight/Suggester.git
cd Suggester
python3 -m venv env
env\Scripts\activate
pip install -r requirements.txt
python serve.py
```

WARNING: Make sure to change the default config at the top of `serve.py` before running the server - specifically, change the admin password!

## Usage

The server will run on port 5000 by default. You can change this by setting the `PORT` variable in the config. You can access the server by going to `http://localhost:5000` (or whatever port you set it to) in your browser. The default admin password is `password` - you should change this immediately! 

### Adding a suggestion (End user)

All the end user needs to do is head to the main page on the site and enter their desired media. The site will then check for duplicates in name and URL/URI, and if it finds none, will add the suggestion to the database for further review. If `ALLOWPUBLICVIEW` is set to `True` in the configuration, the user will be able to watch the progress of their suggestion on the site.

### Reviewing suggestions (Admin)

The admin can view all suggestions by going to the `/admin` page on the site. They can then approve or deny suggestions, and a queue will be created for all approved suggestions to manually add them to the library.
