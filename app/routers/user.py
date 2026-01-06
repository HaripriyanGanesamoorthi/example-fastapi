from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : schemas.Usercreate, db:Session = Depends(get_db)):
    # Truncate password to 72 bytes BEFORE hashing
    password_bytes = str(user.password).encode("utf-8")[:72]  # ensures <=72 bytes
    hashed_password = utils.hash(password_bytes)

    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id : int, db:Session = Depends(get_db),):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user