# modules/Tools/Internet_Tools/Browser/csp.py

from flask import Flask, request, Response

app = Flask(__name__)

# Define the Content-Security-Policy directives
CSP_DIRECTIVES = {
    "default-src": "'self'",
    "script-src": "'self' 'unsafe-inline' 'unsafe-eval'",
    "style-src": "'self' 'unsafe-inline'",
    "img-src": "'self' data:",
    "frame-ancestors": "'self'",
    "connect-src": "'self'",
    "font-src": "'self' data:",
    "object-src": "'none'",
    "media-src": "'self'",
    "child-src": "'self'",
    "form-action": "'self'",
    "frame-src": "'self'"
}

@app.after_request
def apply_csp(response):
    csp_policy = "; ".join([f"{key} {value}" for key, value in CSP_DIRECTIVES.items()])
    response.headers["Content-Security-Policy"] = csp_policy
    return response

@app.route('/')
def home():
    return "Content-Security-Policy is set!"