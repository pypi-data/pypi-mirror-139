import datetime

import numpy as np
import pandas as pd

from mxmetric.calculate import calc as cc
from mxmetric.exc.mx_exc import BizException
from mxmetric.utils.date_util import calc_date


class CalcDataFrame(object):
    """
    基于pd.DataFrame的指标计算工具类
    """

    @staticmethod
    def get_fixed_return(data: pd.DataFrame, suffix: str = 'fixed_return', swanav_column: str = 'swanav'):
        """
        计算当前df周期性的收益率
        
        :param data: 一组周期性的复权累计净值数据，日期为索引，升序排列
        :param suffix: 返回列的后缀名
        :param swanav_column: 净值数据列名
        """
        ret = pd.DataFrame(data=cc.return_rate(data[swanav_column], data[swanav_column].shift()))
        ret.columns = [suffix]
        return ret

    @staticmethod
    def get_period_return(data: pd.DataFrame, period: [str, list], interval_insufficient: bool = True,
                          method: str = 'ffill', offset: int = -1, exacting: bool = True,
                          start_date: datetime.datetime = datetime.datetime(year=1990, month=1, day=1),
                          end_date: datetime.datetime = datetime.datetime.today(),
                          suffix: str = '_return', swanav_column: str = 'swanav', annualized: bool = False,
                          natural: bool = True):
        """
        获取某一时间段的收益率及年化收益率<br>

        Parameters
        ----------
        data:
            一组周期性的复权累计净值数据，日期为索引，升序排列

        period :
            时间区间或时间区间数组；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        method :
            计算上一区间末日期取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        exacting :
            是否和预期日期一致时时进行偏移 默认True，设置false时全部偏移

        start_date:
            计算数据开始日期

        end_date:
            计算数据结束日期

        offset :
            上一区间末日期取值与日期索引严格相等后取值后的偏移量 默认0 适用于获取区间外数据（如 本区间开始日收益 - 上一区间结束日收益的情况）

        suffix:
            返回列的后缀名

        swanav_column:
            净值数据列名

        annualized:
            是否同时计算年化收益率

        natural:
            年化时指定是否使用自然日，默认True，Fasle使用工作日

        """
        result = pd.DataFrame()
        cal_data = data[start_date:end_date]
        if isinstance(period, str):
            period = [period]

        if isinstance(period, list):
            for per in period:
                temp = cal_data.apply(CalcDataFrame.get_row_return,
                                      args=(
                                          data, per, interval_insufficient, method, offset, exacting, suffix,
                                          swanav_column,
                                          annualized, natural),
                                      axis=1)
                result = temp if len(result) == 0 else pd.merge(result, temp, how='left', left_index=True,
                                                                right_index=True)
        else:
            raise BizException("period类型错误")
        return result

    @staticmethod
    def get_row_return(row, data: pd.DataFrame, period: str, interval_insufficient: bool = True, method: str = 'ffill',
                       offset: int = -1,
                       exacting: bool = True,
                       suffix: str = '_return', swanav_column: str = 'swanav', annualized: bool = False,
                       natural: bool = True):
        """
        获取某一日期（row）对应的period的收益率及年化收益率

        Parameters
        ----------
        row:
            data中的某一行

        data:
            一组周期性的复权累计净值数据，日期为索引，升序排列

        period :
            时间区间；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        method :
            计算上一区间末日期取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        exacting :
            是否和预期日期一致时时进行偏移 默认True，设置false时全部偏移

        offset :
            上一区间末日期取值与日期索引严格相等后取值后的偏移量 默认0 适用于获取区间外数据（如 本区间开始日收益 - 上一区间结束日收益的情况）

        suffix:
            返回列的后缀名

        swanav_column:
            净值数据列名

        annualized:
            是否同时计算年化收益率

        natural:
            年化时指定是否使用自然日，默认True，Fasle使用工作日
        """
        result = pd.Series(dtype=float)
        curr_date = row.name
        curr_idx, per_date = CalcDataFrame.get_loc(data.index, curr_date, period=period, method=method, offset=offset,
                                                   exacting=exacting)
        if per_date < data.index[0] and not interval_insufficient:
            result[period + suffix] = np.nan
            if annualized:
                result[period + suffix + '_a'] = np.nan
            return result

        previous_date = data.index[curr_idx]
        result[period + suffix] = np.NaN if curr_date == previous_date else cc.return_rate(row[swanav_column],
                                                                                           data.iloc[curr_idx][
                                                                                               swanav_column])
        if annualized:
            # 计算年化收益
            if natural:
                year_days = 360
                days = (curr_date - previous_date).days
            else:
                year_days = 252
                days = len(pd.bdate_range(start=previous_date, end=curr_date)) - 1
            result[period + suffix + '_a'] = cc.return_annualized(result[period + suffix], year_days, days)
        return result

    @staticmethod
    def get_loc(index: pd.DataFrame.index, curr_date: datetime.datetime, period: str, method: str = 'nearest',
                offset: int = 0,
                exacting: bool = True):
        """
        获取某一日期curr_date 对应的period的在index中的另一日期 previous_date

        Parameters
        ----------
        index:
            一组日期索引

        curr_date:
            需计算的日期

        period :
            时间区间；取值参考date_util.ALL_DATE_PERIOD

        method :
            计算另一日期previous_date的取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        offset :
            偏移量，日期取值时是否进行偏移

        exacting :
            previous_date是否和预期日期expect_date一致时进行偏移 默认True，设置false时全部偏移

        """
        per_date = calc_date(curr_date, period, index[0])
        loc_old = index.get_indexer([per_date], method=method)[0]
        loc = loc_old if loc_old >= 0 else 0
        if (exacting and per_date == index[loc]) or not exacting:
            loc_temp = loc + offset
            if loc_temp > len(index):
                loc = len(index)
            elif loc_temp < 0:
                loc = 0
            else:
                loc = loc_temp
        return loc, per_date

    @staticmethod
    def get_period_stdev(data: pd.DataFrame, period: [str, list], interval_insufficient: bool = True,
                         method: str = 'bfill',
                         start_date: datetime.datetime = datetime.datetime(year=1990, month=1, day=1),
                         end_date: datetime.datetime = datetime.datetime.today(),
                         suffix: str = '_std', return_column: str = 'week_return', annualized: bool = False,
                         sections: int = 52):
        """
        计算年化标准差及其年化，年化标准差也就是年化波动率

        年化波动率=stdev(区间周收益率)*sqrt（52）；计算年化波动率一般使用周度收益率

        Parameters
        ----------
        data:
            一组时间为索引的收益率

        period:
            时间区间或时间区间数组；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        method:
            计算区间开始日期的取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        start_date:
            计算数据开始日期

        end_date:
            计算数据结束日期

        suffix:
            标准差后缀

        return_column:
            收益率列名

        annualized:
            是否同时计算年化波动率

        sections:
            年化周期数量

        """
        cal_data = data[start_date:end_date]
        if isinstance(period, str):
            period = [period]
        if isinstance(period, list):
            result = pd.DataFrame()
            for per in period:
                temp = cal_data.apply(CalcDataFrame.get_row_stdev,
                                      args=(
                                          data, per, interval_insufficient, method, suffix, return_column,
                                          annualized, sections),
                                      axis=1)
                result = pd.merge(temp, result, how='left', left_index=True, right_index=True)
        else:
            raise BizException("period类型错误")
        return result

    @staticmethod
    def get_row_stdev(row, data: pd.DataFrame, period: str, interval_insufficient: bool = True, method: str = 'nearest',
                      suffix: str = '_stdev',
                      return_column: str = 'week_return',
                      annualized: bool = False,
                      sections: int = 52):
        """
        获取某一日期（row）对应的period的收益率及年化收益率

        Parameters
        ----------
        row:
            data中的某一行

        data:
            一组时间为索引的收益率

        period:
            时间区间或时间区间数组；取值参考date_util.ALL_DATE_PERIOD

        interval_insufficient:
            时间区间数据不足是否仍计算

        method:
            计算区间开始日期的取值方式；'ffill'不存在则取前一个, 'bfill'不存在则后一个, 'nearest'取最近的

        suffix:
            标准差后缀

        return_column:
            收益率列名

        annualized:
            是否同时计算年化波动率

        sections:
            年化周期数量
        """
        result = pd.Series(dtype=float)
        curr_date = row.name
        curr_idx, per_date = CalcDataFrame.get_loc(data.index, curr_date, period=period, method=method)
        if per_date < data.index[0] and not interval_insufficient:
            result[period + suffix] = np.nan
            if annualized:
                result[period + suffix + '_a'] = np.nan
            return result
        previous_date = data.index[curr_idx]
        # 标准差
        result[period + suffix] = data[previous_date:curr_date][return_column].std()
        if annualized:
            # 年化波动率
            result[period + suffix + '_a'] = cc.return_stdev_a(result[period + suffix], sections)
        return result
