import csv
import argparse

"""
示例
path/to/python path/to/this_file --input username.csv --output out.csv --output-keys "Age,Username"
以上命令会过滤username.csv中的行，写入out.csv中，只保留Age和Username两列。
过滤条件可以在filter_func中更改
"""


def main(input_filename: str, output_filename: str, output_keys: list):

    def filter_func(row_dict: dict):
        return float(row_dict["PRE_24H"]) != 0

    summary = {
        "input_total": 0,
        "output_total": 0,
    }

    with open(input_filename, "r", newline='') as csv_file: # 打开输入文件
        # 判断一下文件用的是哪种csv方言，比如判断一下分隔符是","还是";"
        dialect = csv.Sniffer().sniff(csv_file.read(102400))
        csv_file.seek(0)
        csv_reader = csv.DictReader(csv_file, dialect=dialect)
        with open(output_filename, "w", newline='') as new_file: # 打开输出文件
            csv_writer = csv.DictWriter(new_file, fieldnames=output_keys, dialect=dialect, extrasaction="ignore")
            csv_writer.writeheader() # 写入标题行
            for row_dict in csv_reader: # 遍历每一行
                if filter_func(row_dict): # 判断是否符合筛选条件
                    csv_writer.writerow(row_dict)
                    summary["output_total"] += 1
                summary['input_total']+=1

    return summary


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='处理csv文件')
    parser.add_argument('--input', type=str, required=True, help='输入文件')
    parser.add_argument('--output', type=str, required=True, help='输出文件')
    parser.add_argument('--output-keys', type=str, required=True, help='输出文件的字段名，逗号隔开，例如："Age,Name"')
    args = parser.parse_args()

    summary = main(args.input, args.output, args.output_keys.split(","))
    print(f"输入文件{args.input}中共有{summary['input_total']}行，输出文件{args.output}中共有{summary['output_total']}行")