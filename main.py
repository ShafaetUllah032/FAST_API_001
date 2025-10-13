import json
from fastapi import FastAPI, Path, HTTPException, Query

app = FastAPI()

def load_data():
    with open('paitents.json','r') as f:
        data=json.load(f)
    return data

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