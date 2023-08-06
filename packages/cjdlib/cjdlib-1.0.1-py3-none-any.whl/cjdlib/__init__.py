name = "cjdlib"


def print_individual_income_tax(salary):
    # 计算个人所得税
    point = 3500
    yanglao_rate = 0.08
    hospital_rate = 0.02
    losejob_rate = 0.01
    basemoney_rate = 0.2
    five_one_money = salary * (yanglao_rate + hospital_rate + losejob_rate + basemoney_rate)
    rest_money = salary - five_one_money - point
    res_money = salary - five_one_money
    if rest_money <= 1500:
        res_money -= rest_money * 0.03
    elif 1500 < rest_money <= 4500:
        tax_money = rest_money * 0.1
        res_money -= (tax_money - 105)
    elif 4500 < rest_money <= 9000:
        tax_money = rest_money * 0.2
        res_money -= (tax_money - 555)
    elif 9000 < rest_money <= 35000:
        tax_money = rest_money * 0.25
        res_money -= (tax_money - 1005)
    elif 35000 < rest_money <= 55000:
        tax_money = rest_money * 0.3
        res_money -= (tax_money - 2755)
    elif 55000 < rest_money <= 80000:
        tax_money = rest_money * 0.35
        res_money -= (tax_money - 5505)
    else:
        tax_money = rest_money * 0.45
        res_money -= (tax_money - 13505)
    print('税前工资为：{0},税后工资为：{1}'.format(salary, res_money))


def print_the_time():
    import time
    while True:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        time.sleep(1)


def decomposed_prime_factor(num):
    m = []
    while num != 1:  # n==1时，已分解到最后一个质因数
        for i in range(2, int(num + 1)):
            if num % i == 0:
                m.append(str(i))  # 将i转化为字符串再追加到列表中，便于使用join函数进行输出
                num = num / i
        if num == 1:
            break  # n==1时，循环停止
    print('×'.join(m))


class bcolors:
    # 颜色输出
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_disk_space(path):
    import psutil
    from psutil._common import bytes2human
    usage = psutil.disk_usage(path)
    space_total = bytes2human(usage.total)
    space_used = bytes2human(usage.used)
    space_free = bytes2human(usage.free)
    print(f"总容量：{space_total}\n已用：{space_used}\n剩余：{space_free}")
    return  space_total, space_used, space_free

def get_os_info():
    import platform
    def showinfo(tip, info):
        print("{}:{}".format(tip,info))
    showinfo("操作系统及版本信息",platform.platform())
    showinfo('获取系统版本号',platform.version())
    showinfo('获取系统名称', platform.system())
    showinfo('系统位数', platform.architecture())
    showinfo('计算机类型', platform.machine())
    showinfo('计算机名称', platform.node())
    showinfo('处理器类型', platform.processor())
    showinfo('计算机相关信息', platform.uname())
    showinfo('python相关信息', platform.python_build())
    showinfo('python版本信息:', platform.python_version())

def get_time_of_the_year(year,month,day):
    import time
    read_time=year+'-'+month+'-'+day
    stru_time=time.strptime(read_time,r'%Y-%m-%d')
    print('这一天是这一年的第',stru_time.tm_yday,'天')

def print_all(string,times=0.1):
    from time import sleep
    for strs in string:
        sleep(times)
        print(string, end='', flush=True)
