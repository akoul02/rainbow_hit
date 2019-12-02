from dataclasses import dataclass

@dataclass
class Bot:
    x: int
    name: str

    # def throw_yield(func):
    #     def wrapper(*args, **kwargs):
    #         func(*args, **kwargs)
    #     return wrapper

    # @throw_yield
    def step(self, n: int):
        self.x += n
        print(f'{self.name} Making {n} steps')
        print(f'{self.name}\'s Current coordinate: {self.x}\n')

    def sleep(self):
        print(f'{self.name} is sleeping')