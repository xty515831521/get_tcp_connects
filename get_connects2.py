# -*- coding: UTF-8 -*-
# author=baird_xiang
import os
import sys
import time
import re
import copy

new_content = [] #去掉\n的浮点型连接数
nums = [] #连接数
connect_times = []  #连接数的时间
d_nums = [] #新增连接数
add_connect_times = [] #新增连接数的时间
new_connects = [] #加入了时间的连接数 格式'2018-05-02 16:50:18   ||  2.0'


#获取tcp连接数
def get_connects(ras_ip,end_time):
    
    while True:
        search_command = 'netstat -nat|grep "%s" |wc -l'%ras_ip
        num_connects = os.popen(search_command).read()
        print num_connects
        nums.append(num_connects)
        time.sleep(1)
        #avg_num = sum(nums)/len(nums)
        now_time = get_time()
        txt_time = get_time()
        connect_times.append(txt_time)
        
        if now_time == end_time:
            sys.exit()
        else:
            pass
        
 #数据输入文本保存并导出       
def in_out_txt():
    
    now_pwd = os.getcwd()
    file_name_time = get_time()
    file_name = now_pwd + '/tcp_connect_numbers_%s.txt'%file_name_time#tcp连接数的文本
    file_name_avage = now_pwd + '/avage_tcp_connects_%s.txt'%file_name_time  #平均连接数的文本
    #写入文本
    file1 = open(file_name,'w')
    for i in nums:
        i_num= re.findall('\d+', i)
        file1.write(i_num[0] + '\n')
    file1.close()
    #读出文本
    file2 = open(file_name,'r')
    content = file2.readlines()
    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]
    file2.close()
    #获得每秒新增连接数 
    get_add_file = open(file_name,'r')
    add_conn_content = get_add_file.readlines()
    for i in range(0,len(add_conn_content)):
        j = i+1
        if j < len(add_conn_content):
            d_value = int(add_conn_content[j]) - int(add_conn_content[i])
            d_nums.append(d_value)
    
    #将nums中'       2\n'转化为浮点数'2' 保存在new_content 中
    for i in content:
        ii = float(i)
        new_content.append(ii)
    #计算平均连接数 
    avg_number = round(sum(new_content)/len(new_content),4)

    #加入时间
    print len(nums)
    print len(connect_times)
    for i in range(0,len(nums)):
        new_connects_data = str(connect_times[i]) +  '   ||  '  + str(new_content[i]) 
        new_connects.append(new_connects_data)
        
    file3 = open(file_name,'w')
    for i in range(0,len(new_connects)):
        file3.write(new_connects[i] + '\n')
    file3.close()
    
    #平均连接数写入avage_tcp_connects.txt文本
   
    file_avage = open(file_name_avage,'w')
    
    file_avage.write(str(avg_number) + '\n')
    file_avage.close()
    return avg_number
    
#获取当前时间不split
def get_time():
    this_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return this_time        
#split时间    
def split_time(input_time):
    
    
    
    times = re.split("[a-z\-]|[a-z\:]|\s", input_time)
    
    out_time = times
    return out_time

if __name__ == '__main__':
    ras_ip = 'com.apple.net.utun_control' #获取连接数的进程或者端口
    end_time = '2018-05-03 15:40:00'  #脚本停止时间
    try :
        get_connects(ras_ip, end_time)
        
    except:
        avg_number = in_out_txt()
        print avg_number
