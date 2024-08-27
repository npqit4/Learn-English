import json
import os
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

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

gsheet = "1iUBDMtB7aoOoRjHPQe-VD181Fevw3YqpMf1UphBcWjs"
vocabulary = get_data_gsheets(gsheet, "Vocabulary")
phrase = get_data_gsheets(gsheet, "Phrase")
question = get_data_gsheets(gsheet, "Question")


# question = get_data_gsheets("Question")


@app.get("/")
async def root():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")

    # Đọc nội dung file HTML
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)


@app.get("/update")
async def root():
    file_path = os.path.join(os.path.dirname(__file__), "update.html")

    # Đọc nội dung file HTML
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)


class Info(BaseModel):
    gsheet: str = None
    token: str = None


@app.post("/update-info")
async def update_info(
        info: Info = None,
):
    global gsheet
    gsheet = info.gsheet
    token = json.loads(info.token)
    # save token to file
    with open("token.json", "w") as f:
        json.dump(token, f)
    return {"status": "success"}


@app.get("/refresh")
async def refresh():
    global vocabulary, phrase, question, gsheet
    vocabulary = get_data_gsheets(gsheet, "Vocabulary")
    phrase = get_data_gsheets(gsheet, "Phrase")
    question = get_data_gsheets(gsheet, "Question")
    return {"status": "success"}


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


@app.get("/question")
async def random_question():
    random_question = random.choice(question)
    return {
        "question": random_question[0],
        "answer": random_question[1],
    }
