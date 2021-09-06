import sqlite3

import datetime
from typing import Text
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

db_counter = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`


def get_db_connection() -> None:
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global db_counter
    db_counter += 1
    app.logger.debug(
        f'Connection to Database Successful through {request.user_agent.browser} on {request.user_agent.platform}')

    return connection


# Function to get a post using its ID
def get_post(post_id: int) -> Text:
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    return post


# Function to get a post using its ID
def get_time_stamp(logging: bool = False) -> str:
    datetime_now = datetime.datetime.now()
    date, time = str(datetime_now).split(" ")
    if logging:

        log_time_stamp = date.replace(
            "-", "_") + "_" + time.split(".")[0].replace(":", "_")
        return log_time_stamp
    else:
        return date, time.split(".")[0]


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application
@app.route('/')
def index() -> Text:
    app.logger.debug(
        f'{index.__name__} page is accessed through {request.user_agent.browser} on {request.user_agent.platform}')

    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id: int) -> Text:
    app.logger.debug(
        f'{get_post.__name__} page is accessed through {request.user_agent.browser} on {request.user_agent.platform}')

    post = get_post(post_id)
    if post is None:
        app.logger.error(f'Article with id {post_id} Not Found')
        return render_template('404.html'), 404
    else:
        app.logger.info(f' Article "{post[2]}" retrieved!')
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about() -> Text:
    app.logger.debug(
        f'{about.__name__} page is accessed through {request.user_agent.browser} on {request.user_agent.platform}')
    app.logger.info(' "About Us" page is retrieved!')
    return render_template('about.html')


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create() -> Text:
    app.logger.debug(
        f'{create.__name__} page is accessed through {request.user_agent.browser} on {request.user_agent.platform}')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f' A new article "{title}" created.')
            return redirect(url_for('index'))

    return render_template('create.html')


# Define the Health Page for the Website
@app.route('/healthz')
def healthz() -> json:
    app.logger.debug(
        f'{healthz.__name__} page is accessed through {request.user_agent.browser} on {request.user_agent.platform}')

    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('"Status" is accessed.')
    return render_template('status.html', healthz=response)


# Define the Health Page for the Website
@app.route('/metrics')
def metrics() -> json:
    app.logger.debug(
        f'{metrics.__name__} page is accessed through {request.user_agent.browser} on {request.user_agent.platform}')

    connection = get_db_connection()
    posts = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
    connection.close()

    response = app.response_class(
        response=json.dumps(
            {"db_connection_count": db_counter, "post_count": posts[0]}),
        status=200,
        mimetype='application/json'
    )
    app.logger.info('"Metrics" is accessed')
    return render_template('metrics.html', metrics=response)


# start the application on port 3111
if __name__ == "__main__":

    logging.basicConfig(
        filename=f'logs/app_{get_time_stamp(True)}.log', level=logging.INFO, format='%(levelname)s:%(name)s:%(asctime)s, %(message)s', datefmt='%d/%m/%Y, %H:%M:%S')
    app.run(host='0.0.0.0', port='3111')
