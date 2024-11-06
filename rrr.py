import threading

def test(word):
    print(word)

threading.Thread(target=test, args=("hello",)).start()