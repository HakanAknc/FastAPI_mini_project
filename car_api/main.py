from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Car(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    color: str
    mileage: int
    engine_power: int
    status: str

cars = []

@app.get("/cars", response_model=List[Car])
def get_cars():
    return cars

@app.post("/cars", response_model=Car)
def create_car(car: Car):
    for existing_car in cars:
        if existing_car.id == car.id:
            raise HTTPException(status_code=400, detail="Car with this ID already exists")
    cars.append(car)
    return car

@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, updated_car: Car):
    for index, car in enumerate(cars):
        if car.id == car_id:
            cars[index] = updated_car
            return updated_car
    raise HTTPException(status_code=404, detail="Car not found")


@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    for index, car in enumerate(cars):
        if car.id == car_id:
            cars.pop(index)
            return {"message" : "Car deleted successfully"}
    raise HTTPException(status_code=404, detail="Car not found")