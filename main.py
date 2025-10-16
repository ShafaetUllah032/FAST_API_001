import json
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal


app = FastAPI()


class Patient(BaseModel):
    id : Annotated[str, Field(..., description=" Unique ID of the patient", example="P001")]
    name : Annotated[str, Field(..., description=" Full name of the patient", example="Donald Trump")]
    city :Annotated[str, Field(..., description=" City of the patient", example="New York")]
    age : Annotated[int, Field(..., gt=0, lt=113, description=" Age of the patient", example=23)]
    gender : Annotated[Literal['male', "female"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description=" Height of the patient in m")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg")]

    @computed_field
    @property

    def bmi(self)-> float:
        return round(self.weight/(self.height**2), 2)
    

    @computed_field
    @property

    def verdict(self)-> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"



def load_data():
    with open('paitent.json','r') as f:
        data=json.load(f)
    return data


def save_data(data):
    with open('paitent.json','w') as f:
        # print(data)
        json.dump(data, f)

@app.get("/")
def read_root():
    return {"message": "Patient Management System"}

@app.get("/about")
def read_about():
    return {
        'message': 'Fully functional Patient Management System',
        'author': 'Safaet Ullah',
        'version': '1.0.0'
    }

@app.get("/view/{patient_id}")
def view_patients(patient_id: str= Path(..., description=" ID of the patient in the DB", example="P001")):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str= Query(..., description="Sort on the basis of height, weight or bmi"), order: str=Query("asc", description="Sort in asc or desc order")):
    valid_fields=["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid field to sort. Select from{valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="invalid order value. Select from ['asc', 'desc']")
    
    data=load_data()
    sort_order= True if order=="desc" else False
    sorted_data=sorted(data.values(), key=lambda x:x[sort_by], reverse=sort_order)
    return sorted_data



@app.post("/create", status_code=201)

def create_patient(patient: Patient):

    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400 , detail="Data already exsist")
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    print(data[patient.id])
    save_data(data)
    return JSONResponse(status_code=201, content=("Successfully ! created new patient"))

                   