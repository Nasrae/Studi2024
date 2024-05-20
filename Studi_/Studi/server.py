#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request
import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51PBYAfRuwrgHlaAj4tHujPBfYMJ9uABu8L5pMxFnxN1OKLLDrPWY80rrFJUb0IAabz0UtgshNkaAdBtUJICfMy6T00N0MAlS4W'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:8000'

if __name__ == '__main__':
    app.run(port=4242)