#-*- coding:utf-8 -*-

# 功能：fibonacci数列，输入一个大于等于3的整数n，输出fibonacci数列的前n项
class FibonacciSequence(object):

    seq = [1,1]    # 定义全局变量列表，存放fibonacci数列，避免重复计算影响效率
    def fib(self,n):
        """
        计算第n项fibonacci数列的值
        :param n: 整数n
        :return: 数列第n项的值
        """
        if (n > 0) and (n - 1 < len(self.seq)):    # 检查列表中是否已经存在，避免重复计算
            number = self.seq[n - 1]
            return number
        else:
            number = self.fib(n - 1) + self.fib(n - 2)    # 递归计算第n项的值
            self.seq.append(number)
            return number

    def output_fib(self,n):
        """
        输出fibonacci数列的前n项
        :param n: 整数n
        :return: None
        """
        self.fib(n)
        for each in self.seq:
            print(each)
        return None

if __name__ == '__main__':
    fb = FibonacciSequence()
    while True:
        n = int(raw_input('请输入一个大于等于3的数：'))
        if n >= 3:
            fb.output_fib(n)
            break
        else:
            print('输入有误，请重新输入！')