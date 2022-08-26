from main import get_type_structure
import datetime


t1 = datetime.datetime.now().time()

c = 0
while c != 300:
    print(get_type_structure('jpg', 'images/inv-000')