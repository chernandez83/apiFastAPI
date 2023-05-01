from typing import List, Tuple, Union, Dict

calificaciones: List[int] = [10, 9, 9, 10, 7, 8]

def promedio(calificaciones: List[int]) -> float:
    return sum(calificaciones) / len(calificaciones)

print(promedio(calificaciones))

config: Tuple[str, int] = ('localhost', 80)
print(config)

options: Tuple[Union[str, int]] = ('root', 'superuser', 8080, 'localhost')
print(options)

users: Dict[str, bool] = {
    'batman': True,
    'joker': False
}
print(users)