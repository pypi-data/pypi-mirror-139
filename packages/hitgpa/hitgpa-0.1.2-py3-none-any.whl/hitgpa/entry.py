from hit import score
from gpalib import convert_to_4
from gpalib.arithmetic import arithmetic
import pandas as pd
import argparse
from hit import ids
from hit import score


def main():
    arith_choices = arithmetic['hundred']
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='输出文件路径',
                        required=False, default='result.csv')
    parser.add_argument('-i', '--input',
                        help='输入成绩单文件的路径，CSV格式，如果你想通过jwes查询数据，不要使用这个参数',
                        required=False,
                        default='jwes')
    parser.add_argument('-u', '--username',
                        help='如果你想查询jwes成绩，需要提供你的学工号', default=None)
    parser.add_argument('-p', '--password',
                        help='如果你想查询jwes成绩，需要提供你的学工密码', default=None)
    parser.add_argument('--no-convert', action='store_true',
                        help="""不转换成绩，直接输出结果，这对你想从jwes中查到成绩后再改比较有用""")
    parser.add_argument('--no-average', action='store_true',
                        help='不计算与学分的加权平均值，直接输出结果')
    parser.add_argument('--from-converted',
                        action='store_true', help='从已经转换为4分制的数据计算加权均值')
    args = parser.parse_args()

    if args.from_converted:
        converted = pd.read_csv(args.input)
    else:
        if args.input != 'jwes':
            transcript = pd.read_csv(args.input)
        else:
            username = args.username
            password = args.password
            if username is None or password is None:
                if username is None:
                    print('你没有通过文件输入你的成绩，必须使用学号和密码来查询，你没输学号')
                    print('你可以加上 --username [你的学号] 来解决这个问题')
                if password is None:
                    print('你没有通过文件输入你的成绩，必须使用学号和密码来查询，你没输密码')
                    print('你可以加上 --password [你的学工密码] 来解决这个问题')
                print('你也可以通过 --input [文件名]来提供你的成绩单文件')
                print('你可以通过 -h 获取一些帮助信息')
                exit(-1)
            s = ids.idslogin(username, password)
            transcript = score.query(s)

        if args.no_convert:
            transcript.to_csv(args.output)
            exit(0)
        converted = {}
        for arith in arith_choices:
            try:
                converted[arith] = convert_to_4(
                    transcript['总成绩'], score_type='hundred', arith=arith)
            except TypeError as e:
                print("我们遇到了一些问题：{}".format(str(e)))
                print("你可能需要手动清理你的“总成绩”中不是一个有效数字的地方，例如“旷考”， “取消成绩”")
                print("可以先得到CSV，再进行修改，使用--no-convert")
                print("然后使用 --input 来用文件输入数据")
                exit(0)

        converted = pd.DataFrame(converted)
        converted['学分'] = transcript['学分']

    if args.no_average:
        converted['课程名称'] = transcript['课程名称']
        converted.to_csv(args.output)

    else:
        final_result = {}
        for arith in arith_choices:
            final_result[arith] = converted[arith].dot(
                converted['学分']) / converted['学分'].sum()
        final_result = pd.DataFrame(final_result, index=['平均学分绩'])
        final_result.to_csv(args.output)


if __name__ == '__main__':
    main()
