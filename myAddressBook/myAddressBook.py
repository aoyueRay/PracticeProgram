#-*- coding:utf-8 -*-

import MySQLdb
import chardet

class myAddressBook():

    # 在初始化中连接数据库
    # 数据库名：myAddressBook
    # 表名：contactinfos
    def __init__(self):
        try:
            self.conn = MySQLdb.connect(
                host = 'localhost',
                user = 'root',
                passwd = '433280',
                db = 'myAddressBook',
                charset = 'utf8',
                use_unicode = True
            )
            self.cur = self.conn.cursor()
        except MySQLdb.Error as err:
            print('唉呀，连接数据库出错了！')
            print('Error %d : %s ' % (err.args[0], err.args[1]))

    # 首页目录
    # 打印首页的目录项
    # 输入：无
    # 输出：用户选择的功能码，字符串的形式返回
    def UI(self):
        print('*' * 80)
        print('*\t\t\t\t我的通讯录\t\t\t')
        print('*' * 80)
        print('*\t\t\t\t1）新增联系人信息')
        print('*\t\t\t\t2）查询联系人信息')
        print('*\t\t\t\t3）修改联系人信息')
        print('*\t\t\t\t4）删除联系人信息')
        print('*\t\t\t\t5）显示所有联系人')
        print('*\t\t\t\t6）清空我的通讯录')
        print('*\t\t\t\t7）批量导入通讯录')
        print('*\t\t\t\tq）退出我的通讯录')
        print('*' * 80)
        while True:
            func = raw_input('想要干啥：')
            if func not in ('1','2','3','4','5','6','7','q'):
                print('没有这个选项啊，换一个呗～')
            else:
                break
        return func

    # 新增联系人页面
    # 打印提示，获取用户输入的各项信息
    # 输入：无
    # 输出：联系人明细信息，以元组的形式返回
    def addUI(self):
        while True:
            print('*' * 80)
            print('*\t\t\t\t新增联系人信息\t\t\t')
            print('*' * 80)
            id = int(raw_input('请输入联系人ID：'))
            name = raw_input('请输入联系人姓名：')
            phone = raw_input('请输入联系人座机号码：')
            mobilephone = raw_input('请输入联系人手机号码：')
            email = raw_input('请输入联系人邮箱地址：')
            print('-' * 35 + '我是分割线' + '-' * 35)
            print('确认一下信息呗：')
            print('\tID：%d' % id)
            print('\t姓名：%s' % name)
            print('\t座机号码：%s' % phone)
            print('\t手机号码：%s' % mobilephone)
            print('\t邮箱地址：%s' % email)
            print('-' * 35 + '我是分割线' + '-' * 35)
            choice = raw_input('没问题的话就保存一下？（Y/N）：')
            if choice == 'Y' or choice == 'y':
                return id,name,phone,mobilephone,email

    # 新增联系人记录
    # 将输入的信息保存至数据库中
    # 输入：联系人信息，以元组的形式输入
    # 输出：无
    def addRecord(self,infos):
        sql = 'insert into contactinfos (id,name,phone,mobilephone,email)' \
              ' values (%d,"%s","%s","%s","%s")' % (infos[0],infos[1],infos[2],infos[3],infos[4])
        try:
            count = self.cur.execute(sql)
            self.conn.commit()
        except MySQLdb.Error as err:
            print('新增记录的时候出错了。。。')
            print('Error %d : %s' % (err.args[0],err.args[1]))

        if count == 0:
            print('居然没有添加成功。。。')
        else:
            print('新增了%d条记录。' % count)
        return None

    # 查找联系人页面
    # 打印提示，获取用户输入的功能码与查询信息，可支持模糊查询
    # 输入：无
    # 输出：功能码和查询信息，以元组的形式返回
    def queryUI(self):
        print('*' * 80)
        print('*\t\t\t\t查询联系人信息\t\t\t')
        print('*' * 80)
        print('\t\t\t\t1)通过ID查询联系人')
        print('\t\t\t\t2)通过姓名查询联系人')
        print('\t\t\t\t3)通过座机号码查询联系人')
        print('\t\t\t\t4)通过手机号码查询联系人')
        print('\t\t\t\t5)通过邮箱地址查询联系人')
        print('\t\t\t\tq)返回目录')
        print('*' * 80)
        func = raw_input('请选择需要的查询方式：')
        if func == '1':
            data = raw_input('请输入联系人ID：')
        elif func == '2':
            data = raw_input('请输入联系人姓名：')
        elif func == '3':
            data = raw_input('请输入联系人座机号码：')
        elif func == '4':
            data = raw_input('请输入联系人手机号码：')
        elif func == '5':
            data = raw_input('请输入联系人邮箱地址：')
        elif func == 'q':
            data = None
        else:
            func = None
            data = None
        return func, data

    # 查找联系人记录（条件查询）
    # 根据输入的功能码和信息，模糊查询记录。
    # 输入：功能码和查询信息，以元组的形式输入，（功能码，信息）
    # 输出：无
    def queryRecord(self,infos):
        func = infos[0]
        data = infos[1]
        count = 0
        query_dict = {}
        if func == '1':
            query_dict['1'] = 'select * from contactinfos where id like "%' + data + '%"'
        else:
            query_dict['2'] = 'select * from contactinfos where name like "%' + data +'%"'
            query_dict['3'] = 'select * from contactinfos where phone like "%' + data +'%"'
            query_dict['4'] = 'select * from contactinfos where mobilephone like "%' + data +'%"'
            query_dict['5'] = 'sekect * from contactinfos where email like "%' + data +'%"'
        sql = query_dict.get(func)
        try:
            count = self.cur.execute(sql)
            self.conn.commit()
            results = self.cur.fetchall()
            for each in results:
                print('\tID:%d' % each[0])
                print('\t姓名:%s' % each[1].encode('utf-8'))
                print('\t座机号码:%s' % each[2].encode('utf-8'))
                print('\t手机号码:%s' % each[3].encode('utf-8'))
                print('\t邮箱地址:%s' % each[4].encode('utf-8'))
                print('-' * 35 + '我是分割线' + '-' * 35)
        except MySQLdb.Error as err:
            print('查询记录的时候出错了。。。')
            print('Error %d : %s' % (err.args[0],err.args[1]))

        if count == 0:
            print('什么都没有找到。。。')
        else:
            print('找到%d条记录。。。' % count)
        return None

    # 删除联系人页面
    # 打印提示，获取用户输入的功能码与删除信息，不支持模糊删除
    # 输入：无
    # 输出：功能码与删除信息，以元组的形式返回
    def deleteUI(self):
        print('*' * 80)
        print('*\t\t\t\t删除联系人')
        print('*' * 80)
        print('*\t\t\t\t1）通过ID删除联系人')
        print('*\t\t\t\t2）通过姓名删除联系人')
        print('*\t\t\t\t3）通过座机号码删除联系人')
        print('*\t\t\t\t4）通过手机号码删除联系人')
        print('*\t\t\t\t5）通过邮箱地址删除联系人')
        print('*\t\t\t\tq）返回目录')
        print('*' * 80)
        func = raw_input('请选择删除联系人的方式：')
        if func == '1':
            data = raw_input('请输入联系人ID：')
        elif func == '2':
            data = raw_input('请输入联系人姓名：')
        elif func == '3':
            data = raw_input('请输入联系人座机号码：')
        elif func == '4':
            data = raw_input('请输入联系人手机号码：')
        elif func == '5':
            data = raw_input('请输入联系人邮箱地址：')
        elif func == 'q':
            data = None
        else:
            func = None
            data = None
        return func,data

    # 删除联系人记录
    # 根据输入的功能码与信息，删除库表记录
    # 输入：功能码和删除信息，以元组的形式输入，（功能码，信息）
    # 输出：无
    def deleteRecord(self,infos):
        func = infos[0]
        data = infos[1]
        count = 0
        delete_dict = {}
        if func == '1':
            delete_dict['1'] = 'delete from contactinfos where id = %d' % int(data)
        else:
            delete_dict['2'] = 'delete from contactinfos where name = "%s"' % data
            delete_dict['3'] = 'delete from contactinfos where phone = "%s"' % data
            delete_dict['4'] = 'delete from contactinfos where mobilephone = "%s"' % data
            delete_dict['5'] = 'delete from contactinfos where email = "%s"' % data
        sql = delete_dict.get(func)
        try:
            count = self.cur.execute(sql)
            self.conn.commit()
        except MySQLdb.Error as err:
            print('删除记录的时候出错了。。。')
            print('Error %d : %s' % (err.args[0], err.args[1]))

        if count == 0:
            print('没有记录被删除是什么鬼。。。')
        else:
            print('%d条记录被删除。。。' % count)
        return None

    # 修改联系人页面
    # 打印提示，获取用户输入的信息，目前只支持通过联系人ID查找相关信息，并单个修改
    # 输入：无
    # 输出：功能码，联系人ID，需要修改的信息，以元组的形式返回
    def modifyUI(self):
        print('*' * 80)
        print('*\t\t\t\t删除联系人')
        print('*' * 80)
        print('*\t\t\t\t1)修改姓名')
        print('*\t\t\t\t2)修改座机号码')
        print('*\t\t\t\t3)修改手机号码')
        print('*\t\t\t\t4)修改邮箱地址')
        print('*\t\t\t\tq)返回目录')
        print('*' * 80)
        func = raw_input('请选择需要的修改方式：')
        if func == '1':
            data = raw_input('请输入联系人姓名：')
            contact_id = raw_input('请输入联系人的ID：')
        elif func == '2':
            data = raw_input('请输入联系人座机号码：')
            contact_id = raw_input('请输入联系人的ID：')
        elif func == '3':
            data = raw_input('请输入联系人手机号码：')
            contact_id = raw_input('请输入联系人的ID：')
        elif func == '4':
            data = raw_input('请输入联系人邮箱地址：')
            contact_id = raw_input('请输入联系人的ID：')
        elif func == 'q':
            data = None
            contact_id = None
        else:
            func = None
            data = None
            contact_id = None
        return func,contact_id,data

    # 修改联系人记录
    # 通过用户输入的信息，修改相关联系人的信息。通过联系人ID定位要修改的联系人。目前仅支持单个字段修改。
    # 输入：功能码，联系人ID，需要修改的信息，以元组的形式输入
    # 输出：无
    def modifyRecord(self,infos):
        func = infos[0]
        contact_id = int(infos[1])
        data = infos[2]
        modify_dict = {}
        count = 0
        modify_dict['1'] = 'update contactinfos set name = "%s" where id = %d' % (data,contact_id)
        modify_dict['2'] = 'update contactinfos set phone = "%s" where id = %d' % (data,contact_id)
        modify_dict['3'] = 'update contactinfos set mobilephone = "%s" where id = %d' % (data,contact_id)
        modify_dict['4'] = 'update contactinfos set email = "%s" where id = %d' % (data,contact_id)
        sql = modify_dict.get(func)
        try:
            count = self.cur.execute(sql)
            self.conn.commit()
        except MySQLdb.Error as err:
            print('修改记录的时候出错了。。。')
            print('Error %d : %s' % (err.args[0], err.args[1]))

        if count == 0:
            print('没有记录被修改是什么鬼。。。')
        else:
            print('%d条记录被修改。。。' % count)
        return None

    # 显示全部联系人记录（全部查询）
    # 全表查询，将库表中所有的记录查询出来，并格式化显示。
    # 输入：无
    # 输出：无
    def showRecord(self):
        print('*' * 80)
        print('所有联系人信息：')
        sql = 'select * from contactinfos'
        try:
            count = self.cur.execute(sql)
            results = self.cur.fetchall()
            for each in results:
                print('\tID:%d' % each[0])
                print('\t姓名:%s' % each[1].encode('utf-8'))
                print('\t座机号码:%s' % each[2].encode('utf-8'))
                print('\t手机号码:%s' % each[3].encode('utf-8'))
                print('\t邮箱地址:%s' % each[4].encode('utf-8'))
                print('-' * 35 + '我是分割线' + '-' * 35)
            print('*' * 80)
        except MySQLdb.Error as err:
            print('查询记录的时候出错了。。。')
            print('Error %d : %s' % (err.args[0], err.args[1]))

        if count == 0:
            print('什么都没找到。。。')
        else:
            print('找到%d条记录。。。' % count)
        return None

    # 清空我的通讯录
    # 将数据表中所有的记录全部删除，目前暂无确认提示
    # 输入：无
    # 输出：无
    def clearRecord(self):
        print('*' * 80)
        print('*\t\t\t\t清空我的通讯录')
        print('*' * 80)
        sql = 'delete from contactinfos'
        try:
            count = self.cur.execute(sql)
            self.conn.commit()
            print('%d条记录被删除。。。' % count)
        except MySQLdb.Error as err:
            print('清空记录的时候出错了。。。')
            print('Error %d : %s' % (err.args[0], err.args[1]))
        return None

    # 批量导入通讯录
    # 将yibu.txt中的数据批量导入库表中
    # 输入：无
    # 输出：无
    def importRecord(self):
        print('*' * 80)
        print('\t\t\t批量导入通讯录\t\t\t')
        print('*' * 80)
        with open('yibu.txt','rb') as f:
            records = f.readlines()
        for each in records:
            info = each.split('|')
            id = int(info[0])
            name = info[4]
            phone = info[2]
            mobilephone = info[3]
            email = info[4]
            sql = 'insert into contactinfos (id,name,phone,mobilephone,email)' \
                  ' values (%d,"%s","%s","%s","%s")' % (id,name,phone,mobilephone,email)
            try:
                self.cur.execute(sql)
                self.conn.commit()
                print('ID为%d的记录导入完毕。' % id)
            except MySQLdb.Error as err:
                print('新增记录的时候出错了。。。')
                print('Error %d : %s' % (err.args[0], err.args[1]))
        return None

    # 关闭数据库
    # 将__init__中打开的数据库连接和游标关闭
    # 输入：无
    # 输出：无
    def closeDB(self):
        self.cur.close()
        self.conn.close()
        return None



if __name__ == '__main__':
    addressbook = myAddressBook()

    while True:
        main_func = addressbook.UI()
        if main_func == '1':    # 新增联系人信息
            add_infos = addressbook.addUI()
            addressbook.addRecord(add_infos)
        elif main_func == '2':    # 查找联系人信息
            while True:
                query_infos = addressbook.queryUI()
                if query_infos[0] == 'q':
                    break
                elif query_infos[0] == None:
                    print('没有这种方式，重新选一个呗。')
                else:
                    addressbook.queryRecord(query_infos)
        elif main_func == '3':    # 修改联系人信息
            while True:
                modify_infos = addressbook.modifyUI()
                if modify_infos[0] == 'q':
                    break
                elif modify_infos[0] == None:
                    print('没有这种方式，重新选一个呗。')
                else:
                    addressbook.modifyRecord(modify_infos)
        elif main_func == '4':    # 删除联系人信息
            while True:
                delete_infos = addressbook.deleteUI()
                if delete_infos[0] == 'q':
                    break
                elif delete_infos[0] == None:
                    print('没有这种方式，重新选一个呗。')
                else:
                    addressbook.deleteRecord(delete_infos)
        elif main_func == '5':    # 显示所有联系人
            addressbook.showRecord()
        elif main_func == '6':    # 清空我的通讯录
            addressbook.clearRecord()
        elif main_func == '7':    # 批量导入通讯录
            addressbook.importRecord()
        else:    # 退出我的通讯录
            print('要走了么。。。再见～')
            addressbook.closeDB()
            break