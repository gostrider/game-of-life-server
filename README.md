# A Game of Life Server written in Python using Tornado

## Requirement:

**Python version**

Python 3+  
Project version 3.6.0

### Project dependency  
- Tornado web server

To install tornado web server  

For python3 as default version  
`pip install tornado`

For python2 as default version  
`pip3 install tornado`

## Build:

Run  
`python3 main.py`

## Description:

This project is aim to implement Conway's Game of Life server using python.

This project uses [Tornado web framework](http://www.tornadoweb.org/en/stable/) as the skeleton of the server.

## Features completed:
- Implementation logic of Game of Life
- Server is able to accepts web socket connection
- Server is able to store each individual connection
- Server is able to update all connection by given time

## TODO Features:
- Synchronise result during currently non-blocking natural of the code
- Provide unqiue color for each connected user
- Averaging color cell from rule #4 
