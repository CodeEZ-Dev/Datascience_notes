from flask import Flask, jsonify, render_template, request
from fordbot.retrieval_generation import generation
from fordbot.data_ingestion import data_ingestion
from flasgger import Swagger

vstore = data_ingestion("done")
chain = generation(vstore)


app = Flask(__name__)
# app = Flask(__name__)
# swagger = Swagger(app)

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/get", methods = ["POST", "GET"])
def chat():
   
   if request.method == "POST":
      msg = request.form["msg"]
      input = msg

      result = chain.invoke(
         {"input": input},
    config={
        "configurable": {"session_id": "murali"}
    },
)["answer"]

      return str(result)

if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=5050, debug= True)