from MLdriver import *
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/", methods = ["POST", "GET"])
def index():
    project = str(request.args.get("project"))
    return "Request finished status: " + str(main(project))

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
