# 这人的笔记都写错了 https://www.jb51.net/article/166119.htm

s1 = 'today is a find day'
s1.replace('find', 'rainy')
print(s1)  # 它写的是 'today is a rainy day' 但是实际还是"today is a find day" 因为原先的变量没有接收新的字符串

print(id('today is a rainy day'))  # 40947976
print(id('today is a find day'))  # 40947904
print(id(s1))  # 40947904

# 原因:是会新生成一个字符串 'today is a rainy day'  但是没人来接收它
print('....................')
print(s1)  # today is a find day
print(id(s1))  # 40947904
s1 = s1.replace('find', 'rainy')
print(s1)
print(id(s1))  # 40948408   #★接收后 id发生变化
print(id('today is a rainy day'))  # 40947976
print(id('today is a find day'))  # 40947904
