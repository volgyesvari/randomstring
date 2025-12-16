# Installation Process
Run the following command from the project's root folder to install dependencies:
```bash
poetry install 
```
```bash
poetry run uvicorn app.main:app --reload --workers 1
```
If you encounter a "returned non-zero exit status 9009", run:
```bash
poetry config virtualenvs.use-poetry-python true
```
The virtual environment might need manual activation:
(Windows)
```bash
.\.venv\Scripts\activate.ps1
```
After successful run, the swagger UI is available on 
http://localhost:8000/docs

# Description
The service has 2 endpoints:  
POST /measurements  
With body structure:  
    {
      "sensorId": 0,
      "metricType": "windSpeed",
      "metricValue": 0,
      "timestamp": 0}  
GET /metrics  
With parameters:  
&nbsp;&nbsp;&nbsp;&nbsp; sensor_ids: list[int]  
&nbsp;&nbsp;&nbsp;&nbsp; metrics: list[Literal["windSpeed", "humidity", "pressure", "temperature"]]
&nbsp;&nbsp;&nbsp;&nbsp; statistic: Literal["min", "max", "sum", "average"]
&nbsp;&nbsp;&nbsp;&nbsp; start_date: datetime
&nbsp;&nbsp;&nbsp;&nbsp; end_date: datetime  

For simplicity the service uses a local SQLite database.
