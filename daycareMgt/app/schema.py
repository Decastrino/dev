from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import time, date, datetime
from enum import Enum

class Weekday(str, Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

###############################################################
# User Schema
###############################################################

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., max_length=50)

class UserCreate(UserBase):
    password: str
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr]
    password: Optional[str]
    is_active: Optional[bool]
    is_admin: Optional[bool] = False
  
class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: Optional[bool]
    is_admin: Optional[bool]
    stripe_customer_id: Optional[int] = None
    
    
    class Config:
        orm_mode = True


###############################################################
# Child Schema
###############################################################

class ChildBase(BaseModel):
    name: str
    age: int
    parent_id: Optional[int] = None
    
class ChildCreate(ChildBase):
    pass

class ChildUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]

class ChildResponse(ChildBase):
    id: int
    created_at: datetime
    parent_id: int
    parent: UserResponse
    
    class Config:
        orm_mode = True
        

###############################################################
# Notification Schema
###############################################################

class NotificationCreate(BaseModel):
    recipient_id: int
    message: str

class NotificationResponse(BaseModel):
    id: int
    recipient_id: int
    message: str
    sent_at: datetime

    class Config:
        orm_mode = True

###############################################################
# Payment Schema
###############################################################

class PaymentCreate(BaseModel):
    user_id: int
    amount: float
    payment_method: str  # 'stripe' or 'google_pay'
    currency: str = 'usd'


class PaymentResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    payment_method: str
    created_at: datetime

    class Config:
        orm_mode = True
    
    
###############################################################
# Schedule Schema
###############################################################
        
class ScheduleCreate(BaseModel):
    # id: int
    # child_id: int
    activity_name: str
    start_time: str
    end_time: str
    start_time: time
    end_time: time
    weekday: Weekday
    
class ScheduleUpdate(BaseModel):
    activity_name: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]
    weekday: Optional[Weekday]


class ScheduleResponse(BaseModel):
    id: int
    # date: str
    activity_name: str
    start_time: time
    end_time: time
    weekday: Weekday
    
    class Config:
        orm_mode = True

###############################################################
# Booking Schema
###############################################################

class BookingCreate(BaseModel):
    # date: str
    # start_time: str
    # end_time: str
    child_id: int
    activity_name: str
    date: date
    start_time: time
    end_time: time
    
class BookingResponse(BaseModel):
    id: int
    activity_name: str
    date: date
    start_time: time
    end_time: time
    # start_time: datetime
    # end_time: datetime
    
    class Config:
        orm_mode = True

class OperationalHoursCreate(BaseModel):
    weekday: Weekday
    start_time: time
    end_time: time
    # opening_time: str
    # closing_time: str
    
class OperationalHoursResponse(BaseModel):
    weekday: Weekday
    start_time: time
    end_time: time
    
    class Config:
        orm_mode = True


###############################################################
#Login info Schema
###############################################################

class Login(BaseModel):
    email: EmailStr
    password: str
  
    class Config:
        orm_mode = True
        

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
