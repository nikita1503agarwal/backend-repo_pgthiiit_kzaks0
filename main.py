import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict

from database import db, create_document, get_documents
from schemas import Barber, Service, Appointment, Testimonial, ShopInfo

app = FastAPI(title="Barbershop API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Barbershop backend running"}

@app.get("/api/schema")
def get_schema():
    # Expose schema classes for the Flames DB viewer
    return {
        "collections": [
            "barber",
            "service",
            "appointment",
            "testimonial",
            "shopinfo",
        ]
    }

@app.get("/test")
def test_database():
    response: Dict[str, Any] = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Seed endpoint to quickly create some base content if empty
@app.post("/api/seed")
def seed_content():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    # Seed barbers
    if db["barber"].count_documents({}) == 0:
        create_document("barber", Barber(name="Jax", bio="Master of modern fades.", avatar=None, specialties=["Fades", "Beards"], experience_years=8).model_dump())
        create_document("barber", Barber(name="Mila", bio="Classic cuts & razor finishes.", avatar=None, specialties=["Classics", "Razor"], experience_years=10).model_dump())

    # Seed services
    if db["service"].count_documents({}) == 0:
        create_document("service", Service(name="Skin Fade", description="Precision skin fade with style", duration_minutes=45, price=35, popular=True).model_dump())
        create_document("service", Service(name="Classic Cut", description="Timeless cut and style", duration_minutes=40, price=30, popular=True).model_dump())
        create_document("service", Service(name="Beard Trim", description="Shape and line-up", duration_minutes=20, price=18).model_dump())

    # Seed testimonials
    if db["testimonial"].count_documents({}) == 0:
        create_document("testimonial", Testimonial(author="Andre", message="Best fade in the city.", rating=5, featured=True).model_dump())
        create_document("testimonial", Testimonial(author="Luis", message="Clean lines, great vibe.", rating=5).model_dump())

    # Seed shop info
    if db["shopinfo"].count_documents({}) == 0:
        create_document("shopinfo", ShopInfo().model_dump())

    return {"status": "ok"}

# Create appointment endpoint
@app.post("/api/appointments")
def create_appointment(payload: Appointment):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    appt_id = create_document("appointment", payload)
    return {"id": appt_id, "status": "created"}

# Public endpoints to fetch content
@app.get("/api/barbers")
def list_barbers():
    docs = get_documents("barber")
    for d in docs:
        d["_id"] = str(d["_id"])  # convert for JSON
    return docs

@app.get("/api/services")
def list_services():
    docs = get_documents("service")
    for d in docs:
        d["_id"] = str(d["_id"])  # convert for JSON
    return docs

@app.get("/api/testimonials")
def list_testimonials():
    docs = get_documents("testimonial")
    for d in docs:
        d["_id"] = str(d["_id"])  # convert for JSON
    return docs

@app.get("/api/shop")
def get_shop_info():
    docs = get_documents("shopinfo", limit=1)
    if docs:
        d = docs[0]
        d["_id"] = str(d["_id"])  # convert for JSON
        return d
    return ShopInfo().model_dump()


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
