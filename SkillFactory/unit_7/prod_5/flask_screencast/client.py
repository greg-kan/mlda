import requests

if __name__ == '__main__':
    r = requests.post('http://localhost:5000/predict', json={'numbers': [1, 1, 1, 21.12]})
    print(r.status_code)
    if r.status_code == 200:
        print(r.json()['prediction'])  # print(r.json())
    else:
        print(r.text)

    # r = requests.post('http://localhost:5000/add', json={'num': 5})
    # print(r.status_code)
    # if r.status_code == 200:
    #     print(r.json()['result'])  # print(r.json())
    # else:
    #     print(r.text)
