a1 = ['FOF', 'Wind', 'S']
s = 'FOF业绩也可圈可点。Wind统计数据显示，截至9月8日，偏股混合型FOF今年以来平均收益率为4.01%，近两年平均收益率为35.39%，近三年平均收益率为43.25%，为投资者贡献了稳中有升的回报。'

d1 = any(word if word in s else False for word in a1)
print(d1)
