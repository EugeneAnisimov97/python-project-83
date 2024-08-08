from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == 'main':
    app.run()
