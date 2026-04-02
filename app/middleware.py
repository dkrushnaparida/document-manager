from flask import request


def register_middleware(app):
    @app.before_request
    def before_request_func():
        print(f"[REQUEST] {request.method} {request.path}")

    @app.after_request
    def after_request_func(response):
        response.headers["X-App-Name"] = "Document Manager"
        return response
