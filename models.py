import datetime
import random
from typing import Literal

from pydantic import BaseModel, Field, field_validator, ValidationInfo, EmailStr, HttpUrl


def generate_random_name() -> str:
    names = ['Nikolay', 'Ivan']
    return random.choice(names)


class Phone(BaseModel):
    phone: str


class Address(BaseModel):
    country: str
    city: str
    phone: Phone


class User(BaseModel):  # Создаем класс, наследуя его от pydantic.BaseModel для того, чтобы параметры, передаваемые в
    # запрос post использовались в теле запроса (Request Body)
    name: str = Field(default_factory=generate_random_name)  # Динамически задаем имя
    age: int = Field(gt=0, lt=130)  # gt - greater than, lt - less than
    password: str
    password2: str
    non_required: str = Field(default=None)
    addresses: list[Address] = Field(default=None)
    locale: Literal['ru-RU', 'en-US']  # Таким образом задаем корректные значения
    create_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    avatar_url: HttpUrl
    # email: EmailStr

    @field_validator('password')  # Позволяет создавать отдельные, более сложные проверки для полей
    def validate_password(cls, password, values, **kwargs):
        if '!' not in password:
            raise ValueError('No ! in password')
        return password

    @field_validator('password2')
    def validate_password2(cls, password2, info: ValidationInfo):
        password = info.data['password']
        if password2 != password:
            raise ValueError(f'passwords not equal: {password2} != {password}')
        return password2


address = Address(city='Moscow', country='Russia', phone=Phone(phone='+7'))
user = User(age=26, password='123456!', password2='123456!', addresses=[address], locale='ru-RU',
            avatar_url='http://asd.ru', email='w@gmail.com')

user.addresses.append(address)

print(user.model_dump_json())

# # Наиболее часто используемые методы
# user = User(name='Nikolay', age=26, password='123456')
#
# print(user)
# print(user.model_dump_json(exclude={'password'}))  # exclude позволяет указать поля, которые не будут выводиться,
# # include - наоборот
#
# print(user.model_dump())
#
# user2 = User.model_validate({'name': 'Nikolay', 'age': 26, 'password': '123456'})
# user2.name = 'Ivan'
# print(user2)


class ResponseExample(BaseModel):
    message: str
    message3: str


