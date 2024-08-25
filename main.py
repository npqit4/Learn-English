import os
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from get_data_gsheets import get_data_gsheets

app = FastAPI()

origins = [
    "*",  # Allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vocabulary = get_data_gsheets("Vocabulary")
phrase = get_data_gsheets("Phrase")


# question = get_data_gsheets("Question")


@app.get("/")
async def root():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")

    # Đọc nội dung file HTML
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)


@app.get("/vocabulary")
async def random_vocabulary():
    random_vocab = random.choice(vocabulary)
    return {
        "vocabulary": random_vocab[0],
        "type": random_vocab[1],
        "meaning": random_vocab[2],
    }


@app.get("/phrase")
async def random_phrase():
    random_phr = random.choice(phrase)
    return {
        "phrase": random_phr[0],
        "meaning": random_phr[1],
    }
