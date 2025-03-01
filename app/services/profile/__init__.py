from random import randint
from pythondi import inject

from app.exceptions import AlreadyExists, InvalidConfirmationCodeError, NotValidEmail
from app.models.profile.repository import ProfileRepo
from app.models.profile.schema import FillProfileSchema
from app.models.user.repository import UserRepo
from app.models.user.schema import RegisterUserSchema

from utils.db.uow import UOW
from utils.deb import p
from utils.email import Email

from .email_text import email_confirmation_text

class ProfileService:
    def __init__(self):
        ...
        
    def is_bmstu_student_email(self, email: str) -> bool:
        return email.endswith("@student.bmstu.ru")
    
    def generate_email_confirmation_code(self, length: int = 6):
        return "q"
        return ''.join(str(digit) for digit in [randint(0, 9) for i in range(length)])
    
    def send_code_email(self, email: str, code: int):
        Email.send(
            email,
            email_confirmation_text.format(
                message='Добро пожаловать в BAUMAN.DATES! Чтобы начать пользоваться ботом, пожалуйста, подтвердите свою почту.',
                code=code),
            "Код подтверждения", True)
    
    @inject()
    def registered(self, id: int, repo: UserRepo):
        return repo.user_exists(id)
        
    @inject()
    def register(self, user_data: RegisterUserSchema, repo: UserRepo, uow: UOW):
        with uow(repo):
            repo.create(
                id=user_data.id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                username=user_data.username,
                role="user",
                banned=False,
                email="",
                verified=False
            )
            
            uow.commit()
    
    @inject()
    def process_email(self, user_id: int, email: str, repo: UserRepo, uow: UOW):
        if not self.is_bmstu_student_email(email) and False:
            raise NotValidEmail("Not Bauman student email.")
            
        if repo.email_exists(email):
            raise AlreadyExists("Email already exists.")
        
        with uow(repo):
            code = self.generate_email_confirmation_code()
            
            repo.process_email(user_id, email, code)
            self.send_code_email(email, code)
            
            uow.commit()
            
    
    @inject()
    def confirm_email(self, user_id: int, email: str, code: str, repo: UserRepo, uow: UOW):
        if not repo.get_email_confirmation_code(user_id, email) == code:
            raise InvalidConfirmationCodeError("Incorrect email confirmation code.")
        
        with uow(repo):
            repo.set_verified_email(user_id, email)
            
            uow.commit()
    
    @inject()
    def fill_profile(self, user_id: int, data: FillProfileSchema, repo: ProfileRepo, uow: UOW):
        with uow(repo):
            repo.create(user_id = user_id, name = data.name, age = data.age, sex=data.sex, description=data.description, photo='')
            
            uow.commit()