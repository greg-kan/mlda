# �������, ������� �������� ��� ������ � ����� � ����������� �������� �� ���������, ���� ��������� �������.  
def digitize_values(collection, default=0):  
    no_missed = [value if value else default for value in collection]   
    return [float(value) for value in no_missed]  
  
# �� ������� �� ���� ������������ ��������� � �������, ��� ������� ��������� �������� � ����   
# ��������, ��� ������� ��������� �������� ������ ����� � ������ �����  
def test_digitize_convert_to_float():  
    assert digitize_values(["10", "50"])  == [10, 50]  
    assert digitize_values(["70.2", "33.4"]) == [70.2, 33.4]  
      
# ������� ��������� ��������� ��������� ������ ������� ������� � ������ ������  
# ����� �� ��������, ��� ������� ��������� ��������   
def test_digitize_restore_missed():  
    assert digitize_values([""], 10) == [10]  
    assert digitize_values(["20", None], 50) == [20, 50]  
      
# ��� ����� ���������, ��� ���� ������� ��������� �������� �� ��������� ���������  
# ��������, �� ������ ������  
def test_digitize_empty():  
    assert digitize_values([]) == []