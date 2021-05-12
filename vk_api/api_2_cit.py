import vk_api
from password import PASSWORD
vk_session = vk_api.VkApi('+79134636437', PASSWORD)
vk_session.auth()

vk = vk_session.get_api()
offset = 0
count = 100
j = 0
results = []
fac = 'ММФ'


for i in range(10):
    l = vk.wall.search(owner_id=-82490748, count=100, query="#ММФ", owners_only=1, offset=i*100)
    items = l['items']
    for i in items:
        j+=1
        text = i['text']
        for char in text:
            if char in "_":
                text.replace(char, '')
        text = str(text)
        list_text = text.split('#')
        citate = list_text[0]
        #print(citate)
        print(list_text)
        teacher = list_text[1]
        subject = ''
        if len(list_text) > 1:
            if fac in list_text[2] and len(list_text) > 3:
                subject = list_text[3]
            elif len(list_text) < 3:
                subject = list_text[2]

        result = {
            'Цитата': citate,
            'Препод': teacher,
            'Предмет': subject,
            'Фулл пост': i['text'],
        }
        print(j)
        results.append(result)
keys = results[0].keys()
import csv
with open('cit.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)