import csv
import operator

def csv_to_list(csv_file, delimiter=','):
    """
    读取csv文件内容，以list形式返回,
    每一行都是一个子list
    """
    with open(csv_file, 'r',encoding='UTF-8') as csv_con:
        reader = csv.reader(csv_con, delimiter=delimiter)
        return list(reader)

def print_csv(csv_content):
    """ 打印csv文件到标准输出."""
    print(50 * '-')
    for row in csv_content:
        row = [str(e) for e in row]
        print('\t'.join(row))
    print(50 * '-')


csv_cont = csv_to_list('./info.csv')
def sort_by_column(csv_cont):
    header = csv_cont[0]
    body = csv_cont[1:]

    bj = open('./bj.csv','w',encoding='UTF-8')
    bj = csv.writer(bj)
    bj.writerow(header)

    cd = open('./cd.csv', 'w', encoding='UTF-8')
    cd = csv.writer(cd)
    cd.writerow(header)

    cq = open('./cq.csv', 'w', encoding='UTF-8')
    cq = csv.writer(cq)
    cq.writerow(header)

    gz = open('./bj.csv', 'w', encoding='UTF-8')
    gz = csv.writer(gz)
    gz.writerow(header)

    hz = open('./bj.csv', 'w', encoding='UTF-8')
    hz = csv.writer(hz)
    hz.writerow(header)

    sh = open('./bj.csv', 'w', encoding='UTF-8')
    sh = csv.writer(sh)
    sh.writerow(header)

    su = open('./bj.csv', 'w', encoding='UTF-8')
    su = csv.writer(su)
    su.writerow(header)

    tj = open('./bj.csv', 'w', encoding='UTF-8')
    tj = csv.writer(tj)
    tj.writerow(header)

    for items in body:
        if len(items) > 0:
            if items[0] == '北京':
                bj.writerow(items)
            elif items[0] == '天津':
                tj.writerow(items)
            elif items[0] == '成都':
                cd.writerow(items)
            elif items[0] == '重庆':
                cq.writerow(items)
            elif items[0] == '广州':
                gz.writerow(items)
            elif items[0] == '杭州':
                hz.writerow(items)
            elif items[0] == '苏州':
                su.writerow(items)
            elif items[0] == '上海':
                sh.writerow(items)

csv_sorted = sort_by_column(csv_cont)  # 按col3排序
# print_csv(csv_sorted)

