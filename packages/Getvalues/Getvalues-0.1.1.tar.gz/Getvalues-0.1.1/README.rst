===================
Getvalues
===================
在python中，轻松获取json中某个key的值。

In Python, it's easy to get the value of a key in JSON

- get属性
 - a = {'a': 1,'b': {[{'c':2}]}}
 - g = Getvalues.get('c', a)
 - print(g)  // [2]


author: puyihd@gmail.com