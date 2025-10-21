from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI
from typing import Annotated, List, Literal
from fastapi.responses import JSONResponse
import pandas as pd
import pickle



app=FastAPI()

with open('model.pkl','rb') as f:
    model=pickle.load(f)


class PredictionRequest(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=113, description='age of the client')]
    height: Annotated[float, Field(..., gt=0, description='height of the client in meters')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the clident in kgs')]
    income_lpa: Annotated[float, Field(..., gt=0, description='income of the client in lakhs per annum')]
    smoker: Annotated[bool, Field(..., description='Whether the client is a smoker or not')]
    city: Annotated[str, Field(..., description='city of the client')]
    occupation: Annotated[Literal['retired', 'unemployed', 'government_job', 'student', 'freelancer',
       'business_owner', 'private_job'], Field(..., description='occupation of the client')]


    @computed_field
    @property 
    def bmi(self)-> float:
        return round(self.weight/(self.height**2), 2)


    @computed_field
    @property
    def age_level(self)-> str:
        if(self.age<=10):
            return 'child'
        elif(self.age>10 & self.age<=23):
            return 'youth'
        elif(self.age>23 & self.age<60):
            return "adult"
        else:
            return 'senior'

    @computed_field
    @property
    def city_level(self)-> str:
        tier_1_cities = ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune']
        if self.city in tier_1_cities:
            return 'Tier_1'
        else:
            return 'Tier_2'


    @computed_field
    @property

    def health_condition(self)-> str:
        if (self.bmi>=30) & (self.smoker==True) & (self.age_level=='senior'):
            return 'serious'
        elif (self.bmi>=30) & (self.smoker==True) & (self.age_level=='adult'):
            return 'medium'
        elif (self.bmi>25) & (self.bmi<30) & (self.smoker==True) &(self.age_level=='adult'):
            return 'mild'
        elif (self.bmi>=30) & (self.smoker==False) & (self.age_level=='senior'):
            return 'little_risk'
        else:
            return 'no_issue'



@app.post("/predict")
def prediction(data: PredictionRequest):
    input=pd.DataFrame([
        {
            "income_lpa":data.income_lpa,
            "occupation":data.occupation,
            "bmi":data.bmi,
            "age_level":data.age_level,
            "city_level":data.city_level,
            "health_condition":data.health_condition
        }
    ])
    print(input)
    pred=model.predict(input)
    return JSONResponse(status_code=200, content=f"The predicted insurance type is {pred[0]}")














