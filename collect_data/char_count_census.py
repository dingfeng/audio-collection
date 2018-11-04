# -*- coding: UTF-8 -*-
# filename: char_count_census date: 2018/11/2 16:39  
# author: FD
filename = './input_file_data/acoustic_introduction.txt'
f = open(filename, 'r',encoding='utf8')
content = f.read()
census_data = {}
for ch in content:
    ch=ch.lower()
    count = census_data.get(ch)
    if (count is None):
        count = 0
    count = count + 1
    census_data[ch] = count

for key in sorted(census_data.keys()):
    print('{} {}'.format(key,census_data[key]))