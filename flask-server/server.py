#pip install openai, langchain

from flask import Flask

app = Flask(__name__)

# Members API route
# Testing only for now
@app.route("/members")
def members():
    return {"members": ["member1", "member2", "member3"]}

if __name__ == "__main__":
    app.run(debug=True)