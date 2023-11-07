from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session


from app import authentication, settings
from app.template_blog import schemas, crud
from app.template_blog.database import get_session
from app.template_blog.routes import router as template_blog_router

app = FastAPI(
    title="TEST"
)
app.include_router(template_blog_router)


@app.post("/login", response_model=schemas.Token)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)
):
    user = crud.authenticate_user(
        session,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authqwertyenticate": "Bearer"}
        )
    access_token = authentication.create_access_token(
        data={"sub": user.email},
        expires_delta=settings.ACCESS_TOKEN_EXPIRES
    )
    return {"access_token": access_token, "token_type": "bearer"}
