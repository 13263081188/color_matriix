fo = open("1.txt", "w")
print("文件名: ", fo.name)

V = [2,2,3]
for i in V:
        # 在文件末尾写入一行
        fo.seek(0, 2)
        # print("IIII",int(i[0][0]))
        line = fo.write(" " + str(i))
fo.close()