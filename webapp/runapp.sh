#!/bin/bash

export FLASK_APP=flask_app
export FLASK_ENV=development
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000
