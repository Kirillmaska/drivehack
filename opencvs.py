import os

for file in os.listdir('images'):
    with open(os.path.join('images', file), 'rb') as x:
        i = x.read()
        print(i)
