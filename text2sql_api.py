import os
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
import openai


openai.api_key = os.getenv("API_KEY")


app = FastAPI()

class UserRequest(BaseModel):
    request : str

@app.get("/")
def index() -> str:
    return "Hello, welcome to my API"


@app.post("/text2sql/")
def generate_sql(user_request: UserRequest):
    prompt_text = "### Postgres SQL tables, with their properties:\n#\n# asset(id, cost double, date_created, defects, model, name, serial_number, branch_id, brand_id, category_id, department_id, assigned_to, office_id, status, sub_category_id)\n# branch(id, branch_name)\n# brand (id, brand_name)\n# category(id, category_name)\n# department(id, department_name)\n# office(id, office_name, branch_id)\n# status(id, status)\n# sub_category(id, sub_category_name, category_id)\n#\n### {}. Give me the query only."
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_text.format(user_request.request),
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"] 
    )
    print(prompt_text)
    return response.choices[0].text.strip()
