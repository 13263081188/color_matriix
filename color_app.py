import streamlit as st
import numpy as np
import pandas as pd
number = 16
MP = [[0.112,1.188,3.456,3.242,1.049,0.051,0.627,2.869,5.625,8.305,9.047,7.091,3.547,1.252,0.346,0.077],[0.003,0.035,0.228,0.669,1.525,3.342,7.040,9.425,9.415,7.886,5.374,3.162,1.386,0.463,0.126,0.028],[0.531,5.708,17.336,18.608,8.917,2.815,0.776,0.201,0.037,0.015,0.007,0.002,0.000,0.000,0.000,0.000]]
D = [[0 for _ in range(number)] for _ in range(number)]
V = [0, 0, 0, 0]
d_c = [[0],[0],[0]]
#染料k/s值
T = [] #矩阵
temp = [] #form
input_k_s = [] #input_text

#标准k/s值
F_s = np.mat([[0] for _ in range(number)])#向量

#基质k/s值
F_t = np.mat([[0] for _ in range(number)])#向量

#配方k/s值
Fm = np.mat([[0] for _ in range(number)]) #向量

for i in range(number):
        T.append([0 for _ in range(4)])
        temp.append([0 for _ in range(7)])
        input_k_s.append([0 for _ in range(7)])
# @st.cache
def main():
        # Wide mode
        st.set_page_config(layout="wide", page_title="计算机配色")
        st.write('\n')
        st.write("结果展示")
        test = st.beta_columns(4)
        for i in range(4):
                test[i].text("染料"+str(i+1)+"浓度")
        st.write("\n\n\n")
        st.write("k/s设置")
        # Sidebar
        st.sidebar.title("标准配方k/s值")
        zz = st.sidebar.form("计算")
        zz.write("最初解")
        three_dist = st.sidebar.beta_columns(3)
        d_x = three_dist[0].form("D_x")
        d_y = three_dist[1].form("D_y")
        d_z = three_dist[2].form("D_z")
        input_x = d_x.text_input("X的变化量")
        input_y = d_y.text_input("Y的变化量")
        input_z = d_z.text_input("Z的变化量")
        if d_x.form_submit_button("确认") and input_x:
                d_c[0][0] = float(input_x)
        if d_y.form_submit_button("确认") and input_y:
                d_c[1][0] = float(input_y)
        if d_z.form_submit_button("确认") and input_z:
                d_c[2][0] = float(input_z)
        zz_1 = st.sidebar.form("修正")
        zz_1.write("对浓度修正")
        # Disabling warning
        st.set_option('deprecation.showfileUploaderEncoding', False)

        k_s_number = [st.beta_columns(7) for _ in range(number)]

        for i in range(number):
                for j in range(7):
                        len = 400 + i *20
                        temp[i][j] = k_s_number[i][j].form('k'+str(j)+'_'+str(len))
                        if j == 0:
                                temp[i][j].write('波长' + str(len) + '    \n基质')
                        elif j == 5:
                                temp[i][j].write('波长' + str(len) + '    \n标准配方')
                        elif j == 6:
                                temp[i][j].write('波长' + str(len) + '    \n配方')
                        else:
                                temp[i][j].write('波长'+str(len)+'    \n染料'+str(j))
                        input_k_s[i][j] = temp[i][j].text_input('k/s')
                        if temp[i][j].form_submit_button("确认") and input_k_s[i][j]:
                                if j == 0:
                                        F_t[i] = float(input_k_s[i][j])
                                elif j == 5:
                                        F_s[i] = float(input_k_s[i][j])
                                elif j == 6:
                                        Fm[i] = float(input_k_s[i][j])
                                else:
                                        T[i][j-1] = float(input_k_s[i][j])
                                for m in input_k_s:
                                        print(m)
                                for m in F_t:
                                        print(m)
                                for m in F_s:
                                        print(m)
                                for m in F_t:
                                        print(m)
                                for m in T:
                                        print(m)
                                # zz.write(count_k_s[i][j])
        if zz.form_submit_button("计算初始浓度"):
                for i in range(number):
                        for j in range(7):
                                if j == 0:
                                        F_t[i] = float(input_k_s[i][j])
                                elif j == 5:
                                        F_s[i] = float(input_k_s[i][j])
                                elif j == 6:
                                        Fm[i] = float(input_k_s[i][j])
                                else:
                                        T[i][j - 1] = float(input_k_s[i][j])
                x = np.array(Fm)
                d_ = 1 - (x + 1) / ((1 + x) ** 2 - 1) ** 0.5
                d_ = list(d_)
                for i in range(number):
                        D[i][i] = d_[i][0]
                print("MP<D<T<F_s<F_t", MP, D, T, F_s,F_t)
                V = np.linalg.pinv(np.mat(MP)*np.mat(D)*np.mat(T))*np.mat(MP)*np.mat(D)*(np.mat(F_s)-F_t)
                print(V)
                # 打开文件
                fo = open("V.txt", "w")
                print("文件名: ", fo.name)
                print("TYPE",type(V))
                V = list(V)
                for i in V:
                        # 在文件末尾写入一行
                        fo.seek(0, 2)
                        print("IIII",int(i[0][0]))
                        line = fo.write(" " + str(float(i[0][0])))
                fo.close()
                for i in range(4):
                        test[i].write(V[i][0][0])
        if zz_1.form_submit_button("对浓度修正"):
                for i in range(number):
                        for j in range(7):
                                if j == 0:
                                        F_t[i] = float(input_k_s[i][j])
                                elif j == 5:
                                        F_s[i] = float(input_k_s[i][j])
                                elif j == 6:
                                        Fm[i] = float(input_k_s[i][j])
                                else:
                                        T[i][j - 1] = float(input_k_s[i][j])
                x = np.array(Fm)
                d_ = 1 - (x + 1) / ((1 + x) ** 2 - 1) ** 0.5
                d_ = list(d_)
                for i in range(number):
                        D[i][i] = d_[i][0]
                d_c[0][0] = float(input_x)
                d_c[1][0] = float(input_y)
                d_c[2][0] = float(input_z)
                print("MP<D<T<D_C",MP,D,T,d_c)
                d_v = np.linalg.pinv(np.mat(MP) * np.mat(D) * np.mat(T)) * np.mat(d_c)
                print("d_V",d_v)
                # 打开文件
                fo = open("V.txt", "r")
                print("文件名: ", fo.name)
                # print("TYPE", type(V))
                line = fo.readline()
                V = line.split(" ")
                del(V[0])
                print("V",V)
                for i in range(4):
                        V[i] = float(V[i]) + d_v[i]
                fo.close()
                # V = np.array(V) + np.array(d_v)
                # 打开文件
                fo = open("V.txt", "w")
                print("文件名: ", fo.name)
                print("TYPE", type(V),V)
                # V = list(V)
                for i in V:
                        # 在文件末尾写入一行
                        fo.seek(0, 2)
                        print("IIII", float(i[0][0]))
                        line = fo.write(" " + str(float(i[0][0])))
                fo.close()
                for i in range(4):
                        test[i].text(V[i])

if __name__ == '__main__':
    main()

