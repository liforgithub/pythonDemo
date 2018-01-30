import pickle

table = pickle.load(open('./data.pkl', 'rb'))

for i in range(0, len(table)):
    for j in range(0, len(table[i]['children'])):
        for k in range(0, len(table[i]['children'][j]['children'])):
            num = table[i]['href'][0: table[i]['href'].index('.')]
            table[i]['children'][j]['children'][k]['href'] = num + '/' + table[i]['children'][j]['children'][k]['href']

pickle.dump(table, open('./data.pkl', 'wb'))