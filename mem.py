import sys

import spacy
from spacy.parts_of_speech import *
import spacy.en

import myra.v2.global_data as global_data

from flask import Flask
app = Flask(__name__)

nlp = None

@app.route("/")
def hello():
    global nlp
    nlp = global_data.G.English()
    return "Hello World!"

if __name__ == "__main__":
    port=5000
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)
