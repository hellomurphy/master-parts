from fastapi import FastAPI, HTTPException
from openpyxl import Workbook
from tempfile import NamedTemporaryFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from typing import List, Union

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.post("/generate_excel")
async def generate_excel(data: List[List[Union[str, int]]]):
    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active

    # Add data to the workbook
    for row in data:
        ws.append(row)

    # Save the workbook to a temporary file
    with NamedTemporaryFile(delete=False) as tmp:
        file_path = tmp.name
        wb.save(file_path)

        # Return the Excel file as a streaming response
        return StreamingResponse(open(file_path, "rb"), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
