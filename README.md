# Networking Microservice

Microservice Backend Prototype with Dynamic Dashboard Integration

This project implements a modular microservice capable of handling multiple actions such as math operations, string manipulation, file reading, and system information retrieval. The microservice communicates through a TCP bridge and is connected to a dynamic frontend panel inside my portfolio dashboard, allowing real‑time interaction, testing, and visualization of responses.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Install Node.js and Python 3.
2. Navigate to the project folder and install dependencies with `npm install`.
3. Run the Python microservice by executing `python server.py`. This starts the TCP server that listens for incoming instructions.
4. (Optional) Run `python client.py` in a separate terminal if you want to manually send commands to the microservice and read the responses directly.

Instructions for using the software:

1. Start the microservice by running `python server.py`.
2. Use `client.py` to send instructions such as math operations, string transformations, or file read requests. You can run two or more `client.py` and start a conversation.
3. The microservice will process each instruction and return a structured response that the client displays in the terminal.

## Development Environment

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Node.js 18+
* Python 3.11+
* Express.js
* WebSocket library
* Custom TCP bridge scripts

## Useful Websites to Learn More

I found these websites useful in developing this software:

* Node.js Documentation: https://nodejs.org
* Python Official Docs: https://docs.python.org
* WebSockets Guide (MDN): https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Add real-time logs from the microservice into the dashboard
* [ ] Implement syntax highlighting for JSON responses
* [ ] Deploy the microservice to a cloud environment for online testing