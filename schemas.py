"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

# Barbershop domain schemas

class Barber(BaseModel):
    name: str = Field(..., description="Barber's full name")
    bio: Optional[str] = Field(None, description="Short bio about the barber")
    avatar: Optional[str] = Field(None, description="Image URL for the barber")
    experience_years: Optional[int] = Field(5, ge=0, le=60, description="Years of experience")
    specialties: Optional[list[str]] = Field(default_factory=list, description="List of specialties")
    rating: Optional[float] = Field(4.9, ge=0, le=5, description="Average rating out of 5")

class Service(BaseModel):
    name: str = Field(..., description="Service name")
    description: Optional[str] = Field(None, description="Service description")
    duration_minutes: int = Field(..., ge=10, le=240, description="Duration in minutes")
    price: float = Field(..., ge=0, description="Price in USD")
    popular: bool = Field(False, description="Whether this is a popular service")

class Appointment(BaseModel):
    customer_name: str = Field(..., description="Customer full name")
    customer_email: Optional[EmailStr] = Field(None, description="Customer email")
    customer_phone: Optional[str] = Field(None, description="Customer phone number")
    service_id: Optional[str] = Field(None, description="Selected service ID")
    barber_id: Optional[str] = Field(None, description="Selected barber ID")
    date: str = Field(..., description="Date in YYYY-MM-DD")
    time: str = Field(..., description="Time in HH:MM")
    notes: Optional[str] = Field(None, description="Additional notes")
    status: str = Field("pending", description="Status of the appointment")

class Testimonial(BaseModel):
    author: str
    message: str
    rating: int = Field(5, ge=1, le=5)
    avatar: Optional[str] = None
    featured: bool = False

class ShopInfo(BaseModel):
    name: str = Field("Blue Flame Barbers", description="Shop name")
    address: str = Field("123 Fade Ave, Suite 7, Your City", description="Street address")
    phone: str = Field("(555) 123-4567", description="Public phone")
    email: Optional[EmailStr] = None
    hours: dict = Field(
        default_factory=lambda: {
            "Mon-Fri": "9:00 AM - 8:00 PM",
            "Sat": "9:00 AM - 6:00 PM",
            "Sun": "Closed",
        }
    )
    about: Optional[str] = Field(
        "Precision fades, classic cuts, and warm vibes. Book your seat and leave sharp.",
        description="About the shop",
    )

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
