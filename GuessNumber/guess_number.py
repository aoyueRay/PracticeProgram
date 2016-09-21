#-*- coding:utf-8 -*-

import random
import MySQLdb


# 未完成项：
# 1）用户注册及登录操作，区分用户记录战绩
# 2）使用数据库记录每个用户的战绩数据
# 3）使用数据库查询显示用户的战绩数据
class GuessNumber(object):

    def __init__(self):
        """
        在初始化中连接数据库
        数据库名：GuessNumber
        """
        try:
            self.conn = MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='433280',
                db='GuessNumber',
                charset='utf8',
                use_unicode=True
            )
            self.cur = self.conn.cursor()
        except MySQLdb.Error as err:
            print('唉呀，连接数据库出错了！')
            print('Error %d : %s ' % (err.args[0], err.args[1]))

    def close_DB(self):
        """
        关闭数据库，将__init__中打开的数据库连接和游标关闭
        :return: None
        """
        self.cur.close()
        self.conn.close()
        return None

    def ui(self):
        """
        主界面目录
        :return:用户选择的功能码，func:string
        """
        print('*' * 80)
        print('*\t\t\t\t猜数小游戏\t\t\t')
        print('*' * 80)
        print('*\t\t\t\t1）开始游戏')
        print('*\t\t\t\t2）我的战绩')
        print('*\t\t\t\tq）离开游戏')
        print('*' * 80)
        while True:
            func = raw_input('想要干啥：')
            if func not in ('1', '2', 'q'):
                print('没有这个选项啊，换一个呗～')
            else:
                break
        return func

    def start_game_ui(self):
        """
        难度选择界面
        :return:用户选择的功能码，func:string
        """
        print('*' * 80)
        print('*\t\t\t\t选择游戏难度\t\t\t')
        print('*' * 80)
        print('*\t\t\t\t1）简单(0 - 10)')
        print('*\t\t\t\t2）一般(0 - 1000)')
        print('*\t\t\t\t3）困难(0 - 100000)')
        print('*\t\t\t\tq）不玩了～')
        print('*' * 80)
        while True:
            func = raw_input('选个难度呗：')
            if func not in ('1','2','3','q'):
                print('没有这个选项啊，换一个呗～')
            else:
                break
        return func

    def guess(self,func):
        """
        猜数函数，根据输入的难度，随机生成一个数，并根据用户输入判断是否猜中
        :param func: 用户输入的难度选择，string
        :return: 本次猜数所使用的次数，count:num
        """
        start = 0    # 下限
        # 根据选择难度定义随机数上限
        if func == '1':
            end = 10    # 上限
            file_difficulty = '简单'
        elif func == '2':
            end = 1000    # 上限
            file_difficulty = '一般'
        else:
            end = 100000    # 上限
            file_difficulty = '困难'
        target = random.randint(start,end)    # 生成目标值
        count = 0    # 记录猜测的次数
        print('target = %d' % target)
        while True:
            input_num = int(raw_input('来来来猜一个：'))
            count += 1
            if input_num == target:
                print('居然猜中了！')
                print('答案就是%d！！！' % target)
                break
            elif input_num > target:
                print('大了大了～～')
            else:
                print('小了小了～～')
        print('猜了%d次终于猜对咯，不容易不容易。。' % count)
        file_record = '难度：%s \t 目标数：%d \t 猜测次数：%d\n' % (file_difficulty,target,count)
        with open('my_record.txt','a') as f:
            f.write(file_record)
        return count

    def one_more_try(self):
        """
        选择是否再猜一次
        :return: 用户选择的功能码，func:bool
        """
        print('*' * 80)
        print('*\t\t\t\t再来一次？\t\t\t')
        print('*' * 80)
        print('*\t\t\t\t1）来来来，再战三百回！')
        print('*\t\t\t\tq）累了累了。。。。')
        while True:
            func = raw_input('怎么说？')
            if func not in ('1','q'):
                print('没有这个选项啊，换一个呗～')
            else:
                break
        if func == '1':
            return(True)
        else:
            return(False)

if __name__ == '__main__':
    guess_number = GuessNumber()

    round_number = 0    # 猜测的轮数
    round_count = 0    # 每轮猜测的次数

    while True:
        main_func = guess_number.ui()
        if main_func == 'q':    # 退出游戏
            break
        elif main_func == '1':    # 开始游戏
            more_times = True    # 再来一次，初始化为True
            while more_times:
                round_number += 1
                start_func = guess_number.start_game_ui()    # 选择难度
                if start_func != 'q':
                    round_count += guess_number.guess(start_func)
                    more_times = guess_number.one_more_try()    # 再来一次
        elif main_func == '2':    # 我的战绩
            with open('my_record.txt','r') as f:
                records = f.readlines()
                for each in records:
                    print(each),     # ','用来去掉print自带的换行符
        else:    # 离开游戏
            break
    if round_count:
        round_average = float(round_count) / round_number    # 转换为浮点数计算平均每轮猜测的次数
        round_average = round(round_average,2)    # 四舍五入
    else:
        round_average = 0
    print('本次游戏共猜了%d轮，平均每轮%f次猜中！' % (round_number,round_average))

    guess_number.close_DB()    # 关闭数据库
    print('游戏结束～')
