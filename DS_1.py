import pandas as pd

# Загрузка данных
df = pd.read_csv('dz.csv')

# Вывод информации о датафрейме
print("Информация о датафрейме:")
print(df.info())

# Вывод первых 12 строк датафрейма
print("\nПервые 12 строк датафрейма:")
print(df.head(12))

# Заполнение пропущенных значений
# Для столбца 'City' заменяем NaN на 'Не известно'
df['City'] = df['City'].fillna('Не известно')

# Для столбца 'Salary' заменяем NaN на 0
df['Salary'] = df['Salary'].fillna(0)

# Проверка результатов после заполнения
print("\nДатафрейм после заполнения пропущенных значений:")
print(df)

# Группировка данных по городам и вычисление средней зарплаты
group = df.groupby('City')[['Salary']].mean()
print("\nСредняя зарплата по городам:")
print(group)

average_salary = df['Salary'].mean()
print("\nСредняя зарплата в датафрейме:", round(average_salary,2))