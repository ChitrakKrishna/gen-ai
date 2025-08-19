# main.py

from fastapi import FastAPI, Request, Form
from retrieval import get_response
from admin import get_department

# === FastAPI app ===
app = FastAPI()

global departmentg
departmentg = None

@app.get('/login')
def login(request: Request, email: str, id: str):
    global departmentg
    # departmentg = None
    if email and id:
        department = get_department(email, id)
    else:
        return "Enter Both Email and Id"

    if department == None:
        return "Wrong email or id"

    else:
        departmentg = department
        return department


@app.get('/chat')
def chat(request: Request, query: str):
    global departmentg

    if departmentg == None:
        return "You need to login first"
    respose = get_response(departmentg, query)

    return respose


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)