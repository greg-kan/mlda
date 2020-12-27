# Функция, которая обращает все строки в числа и подставляет значение по умолчанию, если встречает пропуск.  
def digitize_values(collection, default=0):  
    no_missed = [value if value else default for value in collection]   
    return [float(value) for value in no_missed]  
  
# Мы передаём на вход произвольные параметры и смотрим, что функция корректно работает с ними   
# Проверим, что функция корректно обращает список строк в список чисел  
def test_digitize_convert_to_float():  
    assert digitize_values(["10", "50"])  == [10, 50]  
    assert digitize_values(["70.2", "33.4"]) == [70.2, 33.4]  
      
# Хорошей практикой считается покрывать разные аспекты функции в разных тестах  
# Здесь мы проверим, что функция закрывает пропуски   
def test_digitize_restore_missed():  
    assert digitize_values([""], 10) == [10]  
    assert digitize_values(["20", None], 50) == [20, 50]  
      
# Ещё стоит проверять, что наша функция корректно работает на граничных значениях  
# Например, на пустых данных  
def test_digitize_empty():  
    assert digitize_values([]) == []