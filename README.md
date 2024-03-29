This project is now archived and not maintained. Even more so than the usual MIT License:

THE SOFTWARE IS **ARCHIVED AND NOT MAINTAINED** “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

# ANTS

## Continuous Integration Build
[![Build Status](https://travis-ci.com/buckbaskin/notess.svg?token=ASNKRRcpZXw2vpqjSCDX&branch=master)](https://travis-ci.com/buckbaskin/notess)

## Code Coverage
[![codecov](https://codecov.io/gh/buckbaskin/notess/branch/master/graph/badge.svg?token=vZ02TTtbOA)](https://codecov.io/gh/buckbaskin/notess)


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
