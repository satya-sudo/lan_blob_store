#!/bin/bash
echo runing lint check before
pylint src

echo auto fixing lint
black ./src

echo running lint check after 
pylint src
