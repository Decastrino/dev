from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schema
from .database import get_db, mongodb_db
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import and_

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

import logging
import datetime

from . import schema, oauth2, models, utils
import stripe

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, models
from sqlalchemy.orm import Session

from . import schema, oauth2, models, utils
# from .. import utils, oauth2, schema
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


app = FastAPI()

# CORS middleware to allow frontend to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post('/login', response_model=schema.Token)
async def login(loginInfo: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
# async def login(loginInfo: schema.Login, db: Session = Depends(get_db)):
    print(f"The login info is: {loginInfo}")
    print(f"OAuth2PasswordRequestForm is {OAuth2PasswordRequestForm.__str__}")
    email = loginInfo.username
    user_password = loginInfo.password
    
    # get the user from the database
    user = db.query(models.User).filter(models.User.email == email).first()
    print("Found user!!!!)")
    
    if not user:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Invalid credentials")
    
    # verify user provided password with the user's password stored in the database.
    if not utils.verify_password(user_password, user.password):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Invalid Credentials")
        
    # Create Token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    # Return Token
    return {"access_token": access_token, "token_type": "bearer"}


#############################################################################################################################################
# Users
#############################################################################################################################################

# Create User
@app.post('/admin/createuser', status_code=status.HTTP_201_CREATED, response_model=schema.UserCreate)
async def create_admin_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # db_user = await db.query(models.User).filter(models.User.username == user.username,
    #                                        models.User.email == user.email).first()
    # if db_user:
    #     raise HTTPException(status_code=400, detail="User already registered")
    
    # Create and save new user object
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    user.is_admin = True
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh object to get newly generated ID
    
    print("***********************************************")
    print(f"{new_user}")

    return new_user  # Return the created child object with response details


@app.post('/createuser', status_code=status.HTTP_201_CREATED, response_model=schema.UserCreate)
async def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # db_user = await db.query(models.User).filter(models.User.username == user.username,
    #                                        models.User.email == user.email).first()
    # if db_user:
    #     raise HTTPException(status_code=400, detail="User already registered")
    
    # Create and save new user object
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh object to get newly generated ID
    
    print("***********************************************")
    print(f"{new_user}")

    return new_user  # Return the created child object with response details


# Update User info
@app.put("/users/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.UserCreate)
async def update_user(id: int, updated_user: schema.UserCreate, current_user: int, db: Session = Depends(get_db)):
    user_query = await db.query(models.User).filter(models.User.id == int(id))
    user = user_query.first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"User with id {id} not found")

    if current_user.id != id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized to update post")

    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    
    return user
    

# Get all users
@app.get("/admin/users", response_model=List[schema.UserResponse])
#@app.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    # print(f"All users: {temp_db}")
    # return temp_db
    users = db.query(models.User).all()
    return users


# Get a user
@app.get("/users/id/{id}", response_model=schema.UserResponse, status_code=status.HTTP_200_OK)
async def get_one_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == int(id)).first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"User with id {id} not found")
        
    return user


@app.get("/users/email/{email}")
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email {email} not found")
    return user


# Delete a user
@app.delete("/user/{id}", status_code=status.HTTP_404_NOT_FOUND)
async def delete_user(id: int, current_user: int, db: Session = Depends(get_db)):
    
    user_query = await db.query(models.User).filter(models.User.id == int(id))
    user = user_query.first()

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Entry with id {id} not found")

    if current_user.id != int(id):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized to delete")

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



#############################################################################################################################################
# Child
#############################################################################################################################################

@app.post('/createchild', response_model=schema.ChildCreate, status_code=status.HTTP_201_CREATED)
async def create_child(child: schema.ChildCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    # Access current user ID
    parent_id = current_user.id
    
    # Check for existing child with same name and parent (optional)
    child_query = db.query(models.Child).filter(models.Child.name == child.name, models.Child.parent_id == parent_id)
    found_child = child_query.first()
    
    if found_child:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Child with name: {child.name} and parent id: {current_user.id} already exists")
    
    # Add parent_id to child dictionary
    child_dict = child.dict()  # Convert schema data to dictionary
    child_dict["parent_id"] = parent_id
    
    # Create and save new child object
    new_child = models.Child(**child_dict)
    db.add(new_child)
    db.commit()
    db.refresh(new_child) # Refresh object to get newly generated ID
    
    return new_child # Return the created child object with response details


# Get all children by admin
@app.get("/admin/children", response_model=List[schema.ChildResponse], status_code=status.HTTP_200_OK)
async def get_children(request: Request, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                       skip: int = 0, limit: int = 10):
    
    print(f"Current user with details: {current_user.email}, {current_user.id}, {current_user.is_admin}")

    if not current_user.is_admin:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized for retrieval")
    
    children = db.query(models.Child).offset(skip).limit(limit).all()

    if not children:
         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"No Children found")
    return children


# Get all children
@app.get("/children", response_model=List[schema.ChildResponse], status_code=status.HTTP_200_OK)
async def get_children(request: Request, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                       skip: int = 0, limit: int = 10):
    print(f"Request base url is {request.base_url}")
    print(f"Request headers is {request.headers}")
    logging.info(f"Request is {request.headers}")
    parent_id = current_user.id

    if not parent_id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized for retrieval")
        
    children = db.query(models.Child).filter(models.Child.parent_id == parent_id).offset(skip).limit(limit).all()

    if not children:
         return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                              detail=f"No Children found")
    return children


# Get a child by admin
@app.get("/admin/children/{id}", response_model=schema.ChildResponse, status_code=status.HTTP_200_OK)
async def get_one_child(request: Request, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    child = db.query(models.Child).filter(models.Child.id == int(id)).first()

    if not child:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Child with id {id} not found")

    if not current_user.is_admin:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized for retrieval")
        
    return child


# Get a child
@app.get("/children/{id}", response_model=schema.ChildResponse, status_code=status.HTTP_200_OK)
async def get_one_child(request: Request, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    child = db.query(models.Child).filter(models.Child.id == int(id)).first()

    if not child:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Child with id {id} not found")
        
    if current_user.id != child.parent_id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized to update child information")
        
    return child


# Update Child info
@app.put("/children/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.ChildCreate)
async def update_child(id: int, updated_child: schema.ChildCreate, current_user: int, db: Session = Depends(get_db)):
    
    child_query = await db.query(models.Child).filter(models.Child.id == int(id))
    child = child_query.first()

    if not child:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Child with id {id} not found")

    if current_user.id != child.parent_id and not current_user.is_admin:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized to update child information")

    child_query.update(updated_child.dict(), synchronize_session=False)
    db.commit()
    
    return child


#############################################################################################################################################
# Schedules
#############################################################################################################################################


@app.post('/createschedule')
async def create_schedule(schedule: schema.ScheduleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not current_user.is_admin:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized to create Schedules")
        
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


# Get all schedules
@app.get("/schedules/", response_model=List[schema.ScheduleResponse])
def get_schedules(db: Session = Depends(get_db)):
    schedules = db.query(models.Schedule).all()
    return schedules

# Get specific schedule by id
@app.get("/schedule/{schedule_id}", response_model=schema.ScheduleResponse)
async def get_specific_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = await db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Schedule not found")
    return schedule

# Update schedule by ID
@app.put("/schedules/{schedule_id}", response_model=schema.ScheduleResponse)
def update_schedule(schedule_id: int, schedule_update: schema.ScheduleUpdate, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Schedule not found")
    for key, value in schedule_update.dict(exclude_unset=True).items():
        setattr(schedule, key, value)
    db.commit()
    db.refresh(schedule)
    return schedule

@app.get("/schedule/today", response_model=schema.ScheduleResponse)
async def get_todays_schedule(db: Session = Depends(get_db)):
    today = datetime.date.today().strftime('%A')  # Get current day as string
    schedule = await db.query(models.Schedule).filter(models.Schedule.day == today).first()
    return schedule


#############################################################################################################################################
# Booking and operational hours
#############################################################################################################################################

@app.post("/bookings/{child_id}", response_model=schema.BookingCreate, status_code=status.HTTP_201_CREATED)
async def book_child(child_id: int, booking: schema.BookingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    booking_weekday = booking.booking_datetime.strftime('%A')
    
    # Find operational hours for the specific date or the weekday
    operational_hours = db.query(models.OperationalHours).filter(
        (models.OperationalHours.specific_datetime == booking.booking_datetime) | 
        (models.OperationalHours.weekday == booking_weekday)).first()
    
    if not operational_hours:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No operational hours defined for this day")
    
    # Check if the booking time falls within operational hours
    if not (operational_hours.start_time <= booking.start_time <= operational_hours.end_time and
            operational_hours.start_time <= booking.end_time <= operational_hours.end_time):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Booking time is outside of operational hours")
    
    # Check for capacity
    capacity = db.query(models.Booking).filter(and_(models.Booking.booking_datetime == booking.booking_datetime,
                                               models.Booking.start_time == booking.start_time,
                                               models.Booking.end_time == booking.end_time)).count()
    
    # Check for capacity
    if capacity >= 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No availability for the requested time slot, max capacity reached")
        
    child = db.query(models.Child).filter(models.Child.id == child_id).first()
    if not child:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Child with id {id} not found")
    
    if not current_user.is_admin and child.parent_id != current_user.id:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized to create bookings for child with id {child_id}")
        
    # Check if payment exists for this booking (simple example, could be extended)
    payment = db.query(models.Payment).filter(models.Payment.user_id == current_user.id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Payment is required before booking")

    db_booking = models.Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    # Trigger notification to parent about successful booking
    notification_message = f"Booking for {booking.booking_datetime} from {booking.start_time} to {booking.end_time} successfully created."
    create_message(current_user.id, notification_message, db)
    
    return db_booking

@app.get("/admin/bookings/", response_model=list[schema.AdminBookingResponse])
def read_operational_hours(skip: int = 0, limit: int = 7, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if not current_user.is_admin:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                             detail=f"Current user not authorized perform operation")

    return db.query(models.Booking).offset(skip).limit(limit).all()


@app.get("/bookings/", response_model=list[schema.BookingResponse])
def read_operational_hours(skip: int = 0, limit: int = 7, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    children_ids = db.query(models.Child.id).filter(models.Child.parent_id == current_user.id).all()
    children_ids = [id[0] for id in children_ids]
    print(f"Children_ids: {children_ids}")
    bookings =  db.query(models.Booking).filter(models.Booking.child_id.in_(children_ids)).offset(skip).limit(limit).all()
    
    return bookings


# Create or modify operational hours
@app.post("/admin/operational-hours/", response_model=schema.OperationalHoursCreate)
def create_or_update_operational_hours(operational_hours: schema.OperationalHoursCreate, weekday: schema.Weekday = None, db: Session = Depends(get_db)):
    existing_hours = db.query(models.OperationalHours).filter(models.OperationalHours.weekday == operational_hours.weekday).first()

    if existing_hours:
        existing_hours.weekday=operational_hours.weekday,
        existing_hours.specific_datetime=operational_hours.specific_datetime,
        existing_hours=operational_hours.end_time
        existing_hours.start_time=operational_hours.start_time,
        existing_hours.end_time = operational_hours.end_time
        
        db.commit()
        db.refresh(existing_hours)
        return existing_hours
    else:
        print("Helix: Creating new op hour")
        db_operational_hours = models.OperationalHours(**operational_hours.dict())
        db.add(db_operational_hours)
    db.commit()
    db.refresh(db_operational_hours)
    return db_operational_hours


@app.get("/admin/operational-hours/", response_model=list[schema.OperationalHoursCreate])
def read_operational_hours(skip: int = 0, limit: int = 7, db: Session = Depends(get_db)):
    return db.query(models.OperationalHours).offset(skip).limit(limit).all()


#############################################################################################################################################
# Payment
#############################################################################################################################################

# Create payment
@app.post("/payments/stripe", response_model=schema.PaymentResponse)
async def create_stripe_payment(payment: schema.PaymentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if payment.payment_method != "stripe":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid payment method for this endpoint")
        
    # Create a customer if one doesn't exist
    if not current_user.stripe_customer_id:
        customer = stripe.Customer.create(
            email=current_user.email,
            name=current_user.username,
        )
        current_user.stripe_customer_id = customer['id']
        db.commit()

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),  # Stripe uses the smallest currency unit
            currency=payment.currency,
            customer=current_user.stripe_customer_id,
            payment_method_types=["card"],
            setup_future_usage="off_session",
            payment_method=payment.payment_method_id,
            confirm=True,  # Confirm the payment immediately
            receipt_email=current_user.email,
        )
        # Handle other response statuses as needed
        if not intent.status == 'succeeded':
            raise HTTPException(status_code=400, detail="Payment failed")
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))

    db_payment = models.Payment(
        user_id=current_user.id,
        amount=payment.amount,
        currency=payment.currency,
        payment_method="stripe",
        payment_intent_id=intent['id'],
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    # Trigger notification to user (parent) about successful payment
    notification_message = f"Payment of ${payment.amount} successfully processed."
    create_message(current_user.id, notification_message, db)

    return db_payment

#############################################################################################################################################
# Notification
#############################################################################################################################################

def create_message(recipient_id: int, message: str, db: Session = Depends(get_db)):
    db_notification = models.Notification(
        recipient_id=recipient_id,
        message=message,
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


# Create notification
@app.post("/notifications/", response_model=schema.NotificationCreate)
def create_notification(notification: schema.NotificationCreate, db: Session = Depends(get_db)):
    
    recipient_id = notification.recipient_id
    message = notification.message
    create_message(recipient_id, message)
    return {"message": "Notification created"}


def create_a_notification(recipient_id: int, message: str):
    notification = {
        "recipient_id": recipient_id,
        "message": message,
        "sent_at": datetime.utcnow()
        }
    mongodb_db.notifications.insert_one(notification)
    
def get_notifications_for_user(user_id: int):
    return list(mongodb_db.notifications.find({"recipient_id": user_id}))

@app.post("/notifications/")
def create_notification_endpoint(recipient_id: int, message: str):
    create_notification(recipient_id, message)
    return {"message": "Notification created"}

@app.get("/notifications/{user_id}")
def get_notifications(user_id: int):
    notifications = get_notifications_for_user(user_id)
    return notifications

###################################################################################################

@app.get('/')
async def main():
    return {'message': 'welcome to the main page!!!'}
