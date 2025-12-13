from pydantic import Field, BaseModel


class TaskADDshema(BaseModel):
    TaskName:str = Field(max_length =40)
    TaskText:str = Field(max_length =250)
    TaskStatus:str= Field(max_length=30) 
    TashDeadline:str=Field(max_length=40)

class TaskSchema(TaskADDshema):
    pass