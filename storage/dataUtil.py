import os
from flask import Flask, request
from aes import AES
import database

server = Flask(__name__)

