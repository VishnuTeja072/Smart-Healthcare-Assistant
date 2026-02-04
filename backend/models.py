



from pydantic import BaseModel, Field
from typing import List, Optional

class TriageData(BaseModel):
    urgency: str
    summary: str 
    possible_conditions: List[str]
    advice: List[str]
    specialist: str
    emergency: bool

class HospitalResponse(BaseModel):
    name: str
 
    lat: float
    lon: float
    address: str
    rating: float
    maps_url: str
    distance_km: float
  
    available_specialist: str 

class FinalResponse(BaseModel):
    triage: TriageData
    hospitals: List[HospitalResponse]
    latency_ms: float = 0.0

class HospitalRequest(BaseModel):
    latitude: float
    longitude: float
    symptoms: str