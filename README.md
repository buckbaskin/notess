# ANTS

## Continuous Integration Build
[![Build Status](https://travis-ci.org/buckbaskin/notess.svg?branch=master)](https://travis-ci.org/buckbaskin/notess)

## Code Coverage
[![codecov](https://codecov.io/gh/buckbaskin/notess/branch/master/graph/badge.svg)](https://codecov.io/gh/buckbaskin/notess)

## Code Health
[![Code Health](https://landscape.io/github/buckbaskin/notess/master/landscape.svg?style=flat)](https://landscape.io/github/buckbaskin/notess/master)


## Dependencies
- Python3
- Chrome Web Browser

## Run
Execute `python3 run.py`
Go to your browser and navigate to [localhost:5000](localhost:5000)

## Code

### knowledge.js
This module is our knowledge engine. It does a lot of the front end work
involved in communicating with gwscore.js (speech-to-text), Watson, 
and DBPedia. It also handles highlighting keywords and linking keywords to
outside contextual information. Communication with Watson and DBPdeia is 
done via AJAX calls to our Python Flask server. The Flask server routes 
each call to a specific endpoint (i.e. Watson, DBPedia).  

### gwscore.js
This is google source code used to transcribe speech. This script was wrapped 
using the common Javascript module pattern. In addition, we added a few of
our own functions to this code that allow us to modify the behavior of 
how the transcriptions are presented to the user (i.e interim transcription 
refresh rate, number of service calls).

### index.html
This is the main view for our web application. It initializes the knowledge
engine, and it is the where the user will take/record notes.