#!/usr/bin/env python3

# 1. 打印 "hello world"（10分）

print("hello world")

# 2. 打印 1 到 100 的奇数 （20分）

for i in range(1, 100):
    if i % 2 == 1:
        print(i)

# 3. 给定一个 kvs = {
#     "c": 3,
#     "a": 8,
#     "b": 12,
# },
#     a) 打印它的键值对，顺序任意 （10分）
#     b) 按 key 的顺序输出键值对，期望输出: (a,8), (b,12), (c,3)  (20分)
#     c) 按 value 的顺序逆序输出，期望输出: (b,12), (a,8), (c,3)  (20分)

kvs = {
    "c": 3,
    "a": 8,
    "b": 12,
}

for k in kvs:
    print(k, kvs[k])

for k in sorted(kvs.keys()):
    print(k, kvs[k])

for kv in sorted(kvs.items(), key=lambda x: x[1], reverse=True):
    print(kv[0], kv[1])

# 4. 计算一个文件的行数 (20分)

count = 0
for file in open("syntax.py"):
    count += 1

print(count)
