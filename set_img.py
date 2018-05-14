# -*- coding: UTF-8 -*-
# author=baird_xiang
import os
import sys
import time
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import copy
d_nums = [] #新增连接数
nums = [] #连接数 
connect_times = []  #连接数的时间
add_connect_times = [] #新增连接数的时间
tick_spacing = 3 #绘图横坐标显示间隔
 #数据输入文本保存并导出       
def in_out_txt(file_name):
    
    
    
    #tcp连接数的文本
    #平均连接数的文本
   #读出文本
    file2 = open(file_name,'r')
    content = file2.readlines()
    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]
    file2.close()
    #读出文本，将时间和连接数分开到nums和connect——times两个列表
    for i in content:
        ll = re.split('\|\|',i)
        connect_times.append(ll[0])
        nums.append(float(ll[1]))
    
    #获得每秒新增连接数 

    for i in range(0,len(nums)):
        j = i+1
        if j < len(nums):
            d_value = float(nums[j]) - float(nums[i])
            d_nums.append(d_value)
    print 'd_nums   ',d_nums
   
#获取当前时间不split
def get_time():
    this_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return this_time        
#split时间    
def split_time(input_time):
    
    
    
    times = re.split("[a-z\-]|[a-z\:]|\s", input_time)
    
    out_time = times
    return out_time

#连接数绘图
def print_img1(end_time,cut_time,cut_tcpConn):
    now_pwd = os.getcwd()
    img_path = now_pwd + '/img_%s_tcpconn.png'%end_time#保存绘制好的图形到当前路径
    #连接数绘图
    plt.figure()
    ax1 = plt.subplot(1,1,1)
    ax1.plot(cut_time,cut_tcpConn)
    ax1.set_title('TCP Connects')
    ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.gcf().autofmt_xdate()
    plt.savefig(img_path)#保存图片
    plt.show()
    
#新增连接数绘图    
def print_img2(end_time,cut_add_time,cut_tcpAddConn):    
    now_pwd = os.getcwd()
    img_path = now_pwd + '/img_%s_addconn.png'%end_time#保存绘制好的图形到当前路径
    plt.figure()
    ax2 = plt.subplot(1,1,1)
    
    ax2.plot(cut_add_time,cut_tcpAddConn)
    ax2.set_title('Add TCP Connects per s')
    
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.gcf().autofmt_xdate()
    
    plt.savefig(img_path)#保存图片
    plt.show()
    
def cut_Conn_time(end_time):
    cut_tcpConn = [] #缩略的连接数
    cut_tcpAddConn = []  #缩略的新增连接数
    cut_time = [] #缩略的连接数时间
    cut_add_time = [] #缩略的新增连接数时间
    split_end_time = split_time(end_time) #split结束时间
    split_start_time = connect_times[0]  #获取开始时间
    split_start_time = split_time(split_start_time) #split 开始时间    
    for i in range(1,len(connect_times)):
        add_connect_times.append(connect_times[i])
    print 'add_connect_times',add_connect_times
    #大于一天，10分钟采样一次
    if float(split_end_time[2]) - float(split_start_time[2]) >=  1: #运行时间大于一天
        for i in range(0,len(nums),600):
            try:#处理越界
                avage_tcpConn = (nums[i] + nums[i+600])/2
                cut_tcpConn.append(avage_tcpConn)
            except:
                break
        for i in range(0,len(d_nums),600):
            try:#处理越界
                avage_addConn = (d_nums[i] + d_nums[i+600])/2
                cut_tcpAddConn.append(avage_addConn)
            except:
                break
        for i in range(0,len(add_connect_times),600): #处理新增连接数时间
            avage_add_ConnTime = add_connect_times[i]
            cut_add_time.append(avage_add_ConnTime)
        
        for i in range(0,len(connect_times),600):#处理连接数时间
            avage_ConnTime = connect_times[i]
            cut_time.append(avage_ConnTime)
        
        list_pop1=cut_add_time.pop(-1)
        list_pop2=cut_time.pop(-1)
        return cut_tcpConn,cut_tcpAddConn,cut_time,cut_add_time
    #大于一小时，3分钟采样一次
    elif float(split_end_time[3]) - float(split_start_time[3]) >=1 :
        for i in range(0,len(nums),180):
            try:#处理越界
                avage_tcpConn = (nums[i] + nums[i+180])/2
                cut_tcpConn.append(avage_tcpConn)
            except:
                break
        for i in range(0,len(d_nums),180):
            try:#处理越界
                avage_addConn = (d_nums[i] + d_nums[i+180])/2
                cut_tcpAddConn.append(avage_addConn)
            except:
                break
        for i in range(0,len(add_connect_times),180): #处理新增连接数时间
            avage_add_ConnTime = add_connect_times[i]
            cut_add_time.append(avage_add_ConnTime)
        for i in range(0,len(connect_times),180):#处理连接数时间
            avage_ConnTime = connect_times[i]
            cut_time.append(avage_ConnTime)
        list_pop=cut_add_time.pop(-1)
        list_pop2=cut_time.pop(-1)
        return cut_tcpConn,cut_tcpAddConn,cut_time,cut_add_time
    #3分钟以上，一小时以下
    elif float(split_end_time[4]) - float(split_start_time[4]) >= 3 :
        for i in range(0,len(nums),60):
            try:#处理越界
                avage_tcpConn = (nums[i] + nums[i+60])/2
                cut_tcpConn.append(avage_tcpConn)
            except:
                break
        for i in range(0,len(d_nums),60):
            try:#处理越界
                avage_addConn = (d_nums[i] + d_nums[i+60])/2
                cut_tcpAddConn.append(avage_addConn)
            except:
                break
        for i in range(0,len(add_connect_times),60): #处理新增连接数时间
            avage_add_ConnTime = add_connect_times[i]
            cut_add_time.append(avage_add_ConnTime)
        for i in range(0,len(connect_times),60):#处理连接数时间
            avage_ConnTime = connect_times[i]
            cut_time.append(avage_ConnTime)
        list_pop=cut_add_time.pop(-1)
        list_pop2=cut_time.pop(-1)
        return cut_tcpConn,cut_tcpAddConn,cut_time,cut_add_time
    #3分钟内
    else:
        cut_tcpAddConn = copy.deepcopy(d_nums)
        cut_tcpConn = copy.deepcopy(nums)
        cut_time = copy.deepcopy(connect_times)
        cut_add_time = copy.deepcopy(add_connect_times)
        
        return  cut_tcpConn,cut_tcpAddConn,cut_time,cut_add_time
    
if __name__ == '__main__':
    end_time = '2018-05-10 15:27:00'
    py_path = os.getcwd()
    file_name = '%s/tcp_connect_numbers_%s.txt'%(py_path,end_time)
   
    in_out_txt(file_name)
    print 'nums   ',nums
    cut_tcpConn,cut_tcpAddConn,cut_time,cut_add_time = cut_Conn_time(end_time)
    print 'cut_tcpConn ',cut_tcpConn
    print  'cut_tcpAddConn  ' ,cut_tcpAddConn
    print 'cut_time   ',cut_time
    print  'cut_add_time  ',cut_add_time
    print_img1(end_time,cut_time,cut_tcpConn)
    print_img2(end_time,cut_add_time,cut_tcpAddConn)