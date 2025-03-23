from flask import Flask, render_template, request
from exa_py import Exa
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Initialize Exa client
api_key = input("Enter your Exa API key: ")
exa = Exa(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")

    if not query:
        return render_template("index.html", error="Please enter a search query.", results=[])

    try:
        # Perform a search using Exa
        response = exa.search(query, num_results=5)  # Use 5 for quick testing

        results = []
        for result in response.results:            
            # Extract description correctly for each result
            description = getattr(result, "description", "No description available")
            
            results.append({
                "url": result.url,
                "title": result.title,
                "description": description
            })

        return render_template("index.html", results=results, query=query)

    except Exception as e:
        return render_template("index.html", error=f"Search failed: {str(e)}", results=[])

if __name__ == "__main__":
    app.run(debug=True)
