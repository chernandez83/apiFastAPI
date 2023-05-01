# Anotaciones
a: str = 'Hola'
b: int = 45
c: float = 3.1416
d: bool = True

# print(a, b, c, d)


def sumInt(num1: int, num2: int) -> int:
    return num1 + num2


val1: int = 20
val2: int = 50
val3: int

resultado: int = sumInt(val1, val2)
print(resultado)


class User():

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def saluda(self) -> str:
        return f'Hola {self.username}'


batman = User('Batman', 'Robin')
print(batman.saluda())
