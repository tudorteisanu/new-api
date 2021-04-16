maxCols = 13;
maxRows = 13;

types = [
     {'name':'xs',"min": 0, "max": "576px" },
      {'name':'sm', "min": '540px', "max": "720px" },
     {'name':'md',"min": '720px', "max": "960px" },
     {'name':'lg',"min": '960px', "max": "1140px" },
     {'name':'xl', "min": '1140px', "max": "1320px" },
     {'name':'xxl',"min": '1320px', "max": "1400px" }
]
# @media (min-width: 576px) and (max-width: 940px) {
style = ''

for item in types:
    min = item['min']
    max = item['max']
    name = item['name']
    style += f'@media (min-width: {min}) '+'{'
    for row in range(1, maxRows):
        for col in range(1, maxRows):
            if ((col/row)*100) <= 100:
                style += f'\n*[cols="{row}"][{name}="{col}"]'+'{ display: inline-block;  max-width:'+ str(col*100/row)+'% !important; width: 100% !important; }'
           
    style += '\n}\n\n'


for i in range(30):
    style += f'\n .pa-{i+1} '+ '{ '+ f'padding: {i+1}px ' +'}'

for i in range(20):
    style += f'\n .py-{i+1} '+ '{ '+ f'padding-top: {i+1}px; padding-bottom: {i+1}px; ' +'}'

for i in range(20):
    style += f'\n .px-{i+1} '+ '{ '+ f'padding-left: {i+1}px; padding-right: {i+1}px; ' +'}'

for i in range(20):
    style += f'\n .pt-{i+1} '+ '{ '+ f'padding-top: {i+1}px ' +'}'

for i in range(20):
    style += f'\n .pb-{i+1} '+ '{ '+ f'padding-bottom: {i+1}px ' +'}'


for i in range(30):
    style += f'\n .ma-{i+1} '+ '{ '+ f'margin: {i+1}px ' +'}'

for i in range(20):
    style += f'\n .my-{i+1} '+ '{ '+ f'margin-top: {i+1}px; margin-bottom: {i+1}px; ' +'}'

for i in range(20):
    style += f'\n .mx-{i+1} '+ '{ '+ f'margin-left: {i+1}px; margin-right: {i+1}px; ' +'}'

for i in range(20):
    style += f'\n .mt-{i+1} '+ '{ '+ f'margin-top: {i+1}px ' +'}'

for i in range(20):
    style += f'\n .mb-{i+1} '+ '{ '+ f'margin-bottom: {i+1}px ' +'}'

for i in range(10):
    style += f'\n .br-{i+1} '+ '{ '+ f'border-radius: {i+1}px ' +'}'


with open('style.txt', 'w') as f:
    f.write(style)
print(style)