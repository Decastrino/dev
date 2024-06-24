from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Time, Date, Enum as SQLEnum
# from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, time
import enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Weekday(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    stripe_customer_id = Column(String, unique=True)
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    #child_id = Column(Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False)
    # children = relationship("Child")

    
    
class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    parent = relationship("User")
    bookings = relationship("Booking")



class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    activity_name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)



class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_name = Column(String)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    weekday = Column(SQLEnum(Weekday), nullable=False)

    
class Billing(Base):
     __tablename__ = "billing"

     id = Column(Integer, primary_key=True, index=True)
     child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
     amount = Column(Float, nullable=False)
     billing_date = Column(DateTime, default=datetime.utcnow)
     
     children = relationship("Child")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="usd", nullable=False)
    payment_method = Column(String, nullable=False)
    payment_intent_id = Column(String, unique=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    user = relationship("User")
    
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    recipient = relationship("User")


class OperationalHours(Base):
    __tablename__ = "operational_hours"

    # start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    # end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    weekday = Column(SQLEnum(Weekday), primary_key=True)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    
    
    
    
    