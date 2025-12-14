from pydantic import Field, BaseModel


class TaskADDshema(BaseModel):
    name:str = Field(max_length =40)
    text:str = Field(max_length =250) 
    status:str= Field(max_length=30) 
    deadline:str=Field(max_length=40)

class TaskSchema(TaskADDshema):
    pass