# 收益率
import numpy as np


def return_rate(current_nav, last_section_nav):
    """
    收益率 =（结束日累计净值-起始日期前一日累计净值）/起始日前一日单位净值

    :param current_nav: 计算日期的净值或复权累计净值
    :param last_section_nav: 上一区间末对应日期的净值或复权累计净值
    :return: 收益率
    """
    return current_nav / last_section_nav - 1


# 年化收益率
def return_annualized(section_return, year_days, days: int):
    """
    年化收益率的年度日期统计，有按交易日和按自然日两种计算方式，计算公式有所不同。

    按交易日计算：
        年化收益率=（1+区间收益率）**（252/区间交易天数）-1
        年度内交易天数一般取 252 天，也有客户要求设定为 250 天情况。

    按自然日计算：
        年化收益率=（1+区间收益率）**（365/区间自然日天数）-1

    :param section_return: 区间收益率
    :param year_days: 年化天数
    :param days: 区间天数
    :return: 年化收益率
    """
    if days <= 0:
        return np.NaN
    else:
        return (1 + section_return) ** (year_days / days) - 1


def return_stdev_a(stdev, sections: int = 52):
    """
    计算年化波动率，一般使用周收益率测算

    年化波动率=stdev(区间周收益率)*sqrt（52）

    :param stdev: 固定周期区间收益率生成的标准差

    :param sections: 一年内的周期数量

    """

    return stdev * np.sqrt(sections)
