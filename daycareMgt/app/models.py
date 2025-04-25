from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy import  DateTime, Boolean, Time, Date, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, time
import enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Weekday(enum.Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

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
    children = relationship("Child", back_populates="parent")
    
    payments = relationship("Payment", back_populates="user")
    notifications = relationship("Notification", back_populates="recipient")


class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    parent = relationship("User", back_populates="children")
    bookings = relationship("Booking", back_populates="child")
    billings = relationship("Billing", back_populates="child")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    activity_name = Column(String, nullable=False)
    booking_datetime = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    operational_hours_id = Column(Integer, ForeignKey("operational_hours.id"), nullable=True)

    child = relationship("Child", back_populates="bookings")
    operational_hours = relationship("OperationalHours")

class OperationalHours(Base):
    __tablename__ = "operational_hours"
    
    id = Column(Integer, primary_key=True, index=True)
    weekday = Column(SQLEnum(Weekday))
    specific_datetime = Column(DateTime, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    __table_args__ = (UniqueConstraint('weekday', 'specific_datetime', name='_weekday_specific_datetime_uc'),)

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_name = Column(String)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    weekday = Column(SQLEnum(Weekday), nullable=False)
    # capacity = Column(Integer, default=0)

    
class Billing(Base):
     __tablename__ = "billing"

     id = Column(Integer, primary_key=True, index=True)
     child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
     amount = Column(Float, nullable=False)
     billing_date = Column(DateTime, default=datetime.utcnow)
     
     child = relationship("Child", back_populates="billings")

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

    user = relationship("User", back_populates="payments")
    
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(String(255), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    recipient = relationship("User", back_populates="notifications")

    
