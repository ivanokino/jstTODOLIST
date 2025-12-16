from pydantic import Field, BaseModel



class UserSchema(BaseModel):
    name:str = Field(min_length=3, max_length=15)
    password:str = Field(min_length=4, max_length=25)
