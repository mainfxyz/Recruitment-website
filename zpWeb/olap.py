import pymysql
import random

def K2():
    conn = pymysql.connect(host = "47.103.24.215",user = 'root',passwd = 'yesterday.1',db = 'zp',charset="utf8")

    cursor = conn.cursor()
    t = ['教育', '互联网', '管理', '文秘', '电子', '机械', '客服', '销售', '银行', '保险', '汽车', '采购', '化工', '设计']
    sql = 'SELECT K1,K2 FROM ZpModel_zp where jobType like %s'
    data1=[['product','1/4位点','3/4位点','平均薪资','薪资中位数']]
    data2=[['product','1/4位点','3/4位点','平均薪资','薪资中位数']]
    data3 = [['product', '3/4位点', '1/4位点', '平均薪资', '薪资中位数']]
    for tt in t:
        K2st = []
        K1st = []
        cursor.execute(sql,'%'+tt+'%')
        result = cursor.fetchall()
        conn.commit()

        for r in result:
            K2=r[-1]
            K1=r[-2]
            if K2<=0 or K1<=0:
                continue
            K2st.append(K2)
            K1st.append(K1)
        #K2
        K2s=sorted(K2st)
        l=len(K2st)

        K2_max = K2s[l//4]
        K2_min = K2s[l*3//4]
        K2_avg = sum(K2s)/l
        K2_z = K2s[l//2]
        tem=[tt,K2_max,K2_min,K2_avg,K2_z]
        data2.append(tem)

        # K1
        K1s = sorted(K1st)
        l = len(K1st)

        K1_max = K1s[l // 4]
        K1_min = K1s[l * 3 // 4]
        K1_avg = sum(K1s) / l
        K1_z = K1s[l // 2]
        tem = [tt, K1_max, K1_min, K1_avg, K1_z]
        data1.append(tem)

        #(K1+K2)/2
        K3st=[]
        for i in range(l):
            K3st.append(K1s[i]/2+K2s[i]/2)
        K3s = sorted(K3st)

        K3_max = K3s[l // 4]
        K3_min = K3s[l * 3 // 4]
        K3_avg = sum(K3s) / l
        K3_z = K1s[l // 2]
        tem = [tt, K3_max, K3_min, K3_avg, K3_z]
        data3.append(tem)

    conn.close()
    return data1,data2,data3

def W1():
    data=[
        ['product','教育', '互联网', '管理', '文秘', '电子', '机械', '客服', '销售', '银行', '保险', '汽车', '采购', '化工', '设计'],
        ['没有经验',6,4,4,4,5,6,6,7],
        ['1-3年',7,5,6,6,7,8],
        ['3-5年'],
        ['5-10年'],
        ['10年以上'],
    ]

    return data



if __name__=='__main__':
    w1=W1()
    print(w1)