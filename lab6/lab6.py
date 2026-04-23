class Employee:
    def __init__(self, name, hours, rate, bonus_coef):
        self.name = name
        self.hours = hours
        self.rate = rate
        self.bonus_coef = bonus_coef

    def calculate_bonus(self):
        return round(self.hours * self.rate * self.bonus_coef)

    def salary_per_hour(self):
        return (self.hours * self.rate + self.calculate_bonus()) / self.hours

    def salary(self):
        return self.hours * self.rate + self.calculate_bonus()

    def __add__(self, other):
        if type(self) is type(other):
            return type(self)(
                name=f'{self.name} & {other.name}',
                hours=self.hours + other.hours,
                rate=self.rate + other.rate,
                bonus_coef=self.bonus_coef + other.bonus_coef
            )
        raise TypeError('Объекты должны принадлежать одному классу')


class Senior(Employee):
    def calculate_bonus(self):
        return round(self.hours * self.rate * self.bonus_coef * 1.5)


class Director(Employee):
    def calculate_bonus(self):
        return round(self.hours * self.rate * self.bonus_coef * 2.0)


e1 = Employee('Дима', 30, 20, 0.1)
print('Имя, Часы, Ставка, Коэф премии:', 
      e1.name, e1.hours, e1.rate, e1.bonus_coef)
print('Премия:', e1.calculate_bonus())
print('Зарплата в час:', e1.salary_per_hour())
print('Зарплата:', e1.salary())

s1 = Senior('Иван', 40, 10, 0.2)
print('Имя, Часы, Ставка, Коэф премии:',
      s1.name, s1.hours, s1.rate, s1.bonus_coef)
print('Премия:', s1.calculate_bonus())
print('Зарплата в час:', s1.salary_per_hour())
print('Зарплата:', s1.salary())

d1 = Director('Анна', 40, 20, 0.25)
d2 = Director('Мария', 30, 22, 0.3)
d3 = d1 + d2
print('Имя, Часы, Ставка, Коэф премии:',
      d3.name, d3.hours, d3.rate, d3.bonus_coef)
print('Премия:', d3.calculate_bonus())
print('Зарплата в час:', d3.salary_per_hour())
print('Зарплата:', d3.salary())
