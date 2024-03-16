from typing import List
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
import pickle
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
with open('./Drug_craetedH1.pkl', 'rb') as file:
    loaded_model = pickle.load(file)


    from typing import List

from pydantic import BaseModel



class Drugclass(BaseModel):
    disease: str
    age: int
    gender: str

app = FastAPI()

@app.post("/predict")
def func(s: Drugclass):
    # Convert disease to number format
    disease_mapping = {
        'Diarrhea': 0,
        'cold_and_flue': 1,
        'Stomachae': 2,
        'Dengue': 3,
        'Malaria': 4,
        'Pneumonia': 5,
        'Allergy': 6
    }
    s.disease = disease_mapping.get(s.disease, -1)  # -1 if disease not found

    # Convert gender to number format
    gender_mapping = {
        'Male': 0,
        'Female': 1
    }
    s.gender = gender_mapping.get(s.gender, -1)  # -1 if gender not found

    # Convert age group
    if 5 <= s.age <= 14:
        s.age = 0
    elif 15 <= s.age <= 100:
        s.age = 1
    else:
        s.age = -1


    input_data = [[s.disease, s.gender,s.age,]]  # Prepare input data for prediction
    drugs = loaded_model.predict(input_data)  # Predict drugs based on input data

    # Regular expression to match the items
    


    # Input NumPy array containing bytes-like objects
    

# Convert bytes-like objects to strings
    input_strings = drugs.tolist()

    output_list = [sentence.strip() for drug in input_strings for sentence in drug.split(',')]

    # Return the predicted drugs as a list of strings
    return {"predicted_drugs": output_list}






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3003)
    
