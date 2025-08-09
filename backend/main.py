from fastapi import FastAPI, Request, Response, status, HTTPException, Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
from pydantic import BaseModel,EmailStr,ConfigDict
import datetime
import util,otha2
from fastapi.middleware.cors import CORSMiddleware




# -----------------------------
# Database Models
# -----------------------------
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str =Field(index=True, sa_column_kwargs={"unique": True})
    password: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


  

# -----------------------------
# Pydantic Schemas
# -----------------------------
class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str



class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    created_at: datetime.datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"    

# -----------------------------
# Database Setup
# -----------------------------
DATABASE_URL = "databasetype://nameofDBMS:password@ip_address/databasen" #fill your database deatail
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session



# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/signup', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def new_user(user_data: UserSignup, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    hased_password=util.hash(user_data.password)

    # Create new user
    new_user = User( username=user_data.username,
                    email=user_data.email,
                    password=hased_password  
                    ) 
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user



@app.post('/login/' ,response_model=Token)
async def login_user(user_login: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_login.email)).first()

    if not user or not util.verify(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token=otha2.create_access_token(data={'sub':str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}
