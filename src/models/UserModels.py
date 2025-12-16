from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(Base):
    __tablename__ = "users" 
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]  
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)