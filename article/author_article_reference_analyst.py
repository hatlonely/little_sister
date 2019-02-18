#!/usr/bin/env python3

import xlrd
import xlwt
import os
import argparse
import json


def accumulate(li):
    li2 = [0 for i in li]
    li2[0] = li[0]
    for i in range(1, len(li)):
        li2[i] = li2[i-1] + li[i]
    return li2


def to_excel(result, output):
    dirname = os.path.dirname(output)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    wwb = xlwt.Workbook()
    wws = wwb.add_sheet("sheet1")
    i = 0

    for key in ["author", "找到的结果数", "被引频次总计", "h-index"]:
        wws.write(i, 0, key)
        wws.write(i, 1, result[key])
        i += 1

    i += 1
    for key in ["年份", "当年发文篇数", "累计发文量", "当年被引次数", "累计被引次数", "篇均被引1", "年均被引", "篇均被引2", "h指数"]:
        wws.write(i, 0, key)
        for j in range(len(result["年份"])):
            wws.write(i, j+1, result[key][j])
        i += 1
    wwb.save(output)


def analysis(input, output):
    for filename in os.listdir(input):
        if not filename.endswith(".xls"):
            continue
        items = []
        path = os.path.join(input, filename)
        rwb = xlrd.open_workbook(path)
        rws = rwb.sheet_by_index(0)

        result = {}
        result["author"] = ":".join(
            rws.cell(0, 0).value.split(":")[1:]
        ).strip()
        result["找到的结果数"] = rws.cell(22, 1).value
        result["被引频次总计"] = rws.cell(23, 1).value
        result["每项平均引用次数"] = rws.cell(24, 1).value
        result["h-index"] = rws.cell(25, 1).value

        header = []
        for j in range(0, rws.ncols):
            header.append(rws.cell(27, j).value)
        header = [
            int(i) if not isinstance(i, str) else i for i in header
        ]
        years = []
        keys = [i for i in header if isinstance(i, int)]
        year_article_refers = [[] for i in keys]
        for j in range(28, rws.nrows):
            item = {}
            for i in range(0, rws.ncols):
                item[header[i]] = rws.cell(j, i).value
            items.append(item)
            years.append(int(item["出版年"]))
            for i in range(len(keys)):
                year_article_refers[i].append(int(item[keys[i]]))
        year_article_sum_refers = [[0 for j in years] for i in keys]
        year_article_avg_refers = [[0 for j in years] for i in keys]
        year_article_sum_refers[0] = year_article_refers[0]
        for i in range(1, len(keys)):
            for j in range(0, len(years)):
                year_article_sum_refers[i][j] = year_article_refers[i][j] + \
                    year_article_sum_refers[i-1][j]
        for i in range(len(year_article_refers)):
            y1 = keys[i]
            year_article_avg_refers[i] = [0 for i in years]
            for j in range(len(years)):
                y2 = years[j]
                if y1 >= y2:
                    year_article_avg_refers[i][j] = year_article_sum_refers[i][j] / \
                        (y1 - y2 + 1)
        result["当年被引次数"] = [0 for i in keys]
        result["当年发文篇数"] = [0 for i in keys]
        result["篇均被引1"] = [0 for i in keys]
        result["年均被引"] = [0 for i in keys]
        result["h指数"] = [0 for i in keys]
        for i in range(len(keys)):
            result["当年被引次数"][i] = sum(year_article_refers[i])
            result["年均被引"][i] = sum(year_article_avg_refers[i])
            result["当年发文篇数"][i] = len([y for y in years if y == keys[i]])
            refers = sorted(year_article_sum_refers[i], reverse=True)
            for idx in range(len(refers)):
                if refers[idx] >= idx + 1:
                    result["h指数"][i] = idx + 1
                else:
                    break
        result["累计被引次数"] = accumulate(result["当年被引次数"])
        result["累计发文量"] = accumulate(result["当年发文篇数"])
        result["篇均被引1"] = [
            0 if result["当年被引次数"][i] == 0 else result["当年被引次数"][i] /
            result["累计发文量"][i]
            for i in range(len(keys))
        ]
        result["篇均被引2"] = [
            0 if result["年均被引"][i] == 0 else result["年均被引"][i] /
            result["累计发文量"][i]
            for i in range(len(keys))
        ]
        result["年份"] = keys
        to_excel(result, os.path.join(output, filename[:-4]+"_analyst.xls"))


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Example:
            python3 author_article_reference_analyst.py -i 2008 -o 2008_analyst
        """
    )
    parser.add_argument(
        "-i", "--input", type=str,
        help="input directory", default="data"
    )
    parser.add_argument(
        "-o", "--output", type=str,
        help="output filename", default="data_analyst"
    )
    args = parser.parse_args()
    analysis(args.input, args.output)


if __name__ == "__main__":
    main()
