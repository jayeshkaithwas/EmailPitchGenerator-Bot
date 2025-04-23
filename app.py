from flask import Flask, request, make_response,render_template, Response
from google import genai
from pydantic import BaseModel
import json
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def verify_api(apikey):
    if apikey.isalnum():
        try:
            client = genai.Client(api_key=apikey)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="Hello, Gemini!!"
            )
            #print(response.text)
            message = "Valid Key"
        except Exception as e:
            #print(f"Error={e}")
            message = e.message
        return message
    else:
        message = "API key not valid. Please pass a valid API key."
        return message

@app.route('/', methods=['GET', 'POST'])
def get_gemini_api():
    if request.method == 'POST':
        api = request.form.get('apikey')
        validity = verify_api(api)
        if validity == 'Valid Key':
            resp = make_response(render_template('answer.html',saved_input=api))
            resp.set_cookie('api',api,max_age=60*60*24*30)
        else:
            resp = make_response(render_template('index.html',message=validity))        
        return resp
    #     if num.strip() == '':   # Empty input
    #         return "<h1>Invalid number</h1>"
    #     square = int(num) ** 2
    #     return render_template('answer.html', squareofnum=square, num=num)
    else:
        return render_template('index.html')
    
def generate_queries(apikey, target):
    client = genai.Client(api_key=apikey)
    prompt = f"""
            You are an AI assistant that writes concise search queries for market research.

            Create 4 short search queries based on the given target industry or company:
            01. Biggest pain points faced by this avatar
            02. Biggest companies in this industry
            03. How companies in this industry get clients
            04. Where to find companies in this industry online

            Here's the industry / company to perform market research on: #### {target} ####
            """
    class queries_structure(BaseModel):
        queries : list[str]

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': list[queries_structure],
        }
    )
    data = json.loads(response.text)
    return data

def web_search_agent(query, apikey):
    client = genai.Client(api_key=apikey)
    prompt = f"""
            You are a web search assistant. Provide a concise summary of the search results.

            Search the web for: {query}
            """
    response = client.models.generate_content(
    model="gemini-2.0-flash",  # or gemini-1.5-pro if you're using Gemini 1.5
    contents=prompt
    )
    #print(response.text)
    return response.text

def cold_email_agent(api, target, search_results):
    client = genai.Client(api_key=api)
    combined_results = "\n".join(search_results)
    prompt = f"""
    You are an expert cold email writer.

    Your task is to write concise and personalized cold emails based on the Market Research given to you.

    Make sure to utilize all 4 areas of the research (pain points, companies, clients, and online sources).

    Focus on describing what the target company will get, and add an appealing guarantee.

    Keep the email concise and use plain English.

    DO NOT OUTPUT ANY OTHER TEXT — ONLY THE COLD EMAIL ITSELF!

    ---

    Here is the target company: {target}

    Here is the market research:
    #### {combined_results} ####
    """
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
    )
    print(response)
    return response.text

@app.route('/email', methods=['GET', 'POST'])
def generate_email():
    # if request.method == 'POST':
    #     num = request.form.get('num')
    #     if num.strip() == '':   # Empty input
    #         return "<h1>Invalid number</h1>"
    #     square = int(num) ** 2
    #     return render_template('answer.html', squareofnum=square, num=num)
    if request.method == 'POST':
        target = request.form.get('target')
        api = request.cookies.get('api')
        #print(api)
        validity = verify_api(api)
        if validity == "Valid Key":
            data = generate_queries(api,target)
            search_results=[]
            for item in data:
                for query in item["queries"]:
                    print(query.strip('"'))
                    result = web_search_agent(query.strip('"'),api)
                    search_results.append(result)
            email = cold_email_agent(api, target, search_results)
            resp = make_response(render_template('answer.html',saved_input=api,email=email))
        else:
            resp = make_response(render_template('index.html',message=validity))  
        return resp      
    else:        
        return render_template('answer.html')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
