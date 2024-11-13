#!/bin/bash

echo Creating/Starting Database 
python src/create_db.py 

echo Starting the server
python src/server.py
