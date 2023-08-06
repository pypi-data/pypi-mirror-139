import pandas as pd
import numpy as np
from pandas.tseries.offsets import BDay

class PortfolioAnalysis:
    def __init__(self, daily_return, outputname='./Unnamed'):
        # 포트폴리오 일별 수익률
        self.daily_return = daily_return
        # 포트폴리오 복리수익률
        self.cum_ret_cmpd = self.daily_return.add(1).cumprod()
        # 포트폴리오 단리수익률
        self.cum_ret_smpl = self.daily_return.cumsum()

        # 분석 기간
        self.num_years = self.get_num_year(self.daily_return.index.year.unique())

        # 각종 포트폴리오 성과지표
        self.cagr = self._calculate_cagr(self.cum_ret_cmpd, self.num_years)
        self.std = self._calculate_std(self.daily_return,self.num_years)
        self.sharpe = self.cagr/self.std
        self.sortino = self.cagr/self._calculate_downsiderisk(self.daily_return,self.num_years)
        self.drawdown = self._calculate_dd(self.cum_ret_cmpd)
        self.average_drawdown = self.drawdown.mean()
        self.mdd = self._calculate_mdd(self.drawdown)

        try:
            self.R1Y_HPR, self.R1Y_HPR_WR = self._holding_period_return(self.cum_ret_cmpd, self.num_years)
        except:
            pass


        # Bokeh Plot을 위한 기본 변수 설정
        from bokeh import palettes
        self.color_list = ['#ec008e','#0086d4', '#361b6f',  '#8c98a0'] + list(palettes.Category20_20)
        self.outputname = outputname
    def basic_report(self, simple=False, display = True, toolbar_location='above'):
        from bokeh.plotting import figure, output_file, show, curdoc, save
        from bokeh.layouts import column
        from bokeh.models import ColumnDataSource, Legend, Column
        from bokeh.models.widgets import DataTable, TableColumn
        from bokeh.models import NumeralTickFormatter, LogTickFormatter

        def to_source(df):
            df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
            return ColumnDataSource(df)

        curdoc().clear()
        output_file(self.outputname + '.html')


        try:
            static_data = pd.concat([self.cum_ret_cmpd.iloc[-1]-1, self.cagr, self.sharpe, self.sortino, self.std, self.mdd, self.average_drawdown,self.R1Y_HPR_WR], axis=1)
            static_data.columns = ['Compound_Return', 'CAGR', 'Sharpe Ratio', 'Sortino Ratio', 'Standard Deviation',
                                   'MDD',
                                   'Average Drawdown', 'HPR(1Y)']
        except:
            static_data = pd.concat([self.cum_ret_cmpd.iloc[-1]-1, self.cagr, self.sharpe, self.sortino, self.std, self.mdd, self.average_drawdown], axis=1)
            static_data.columns = ['Compound_Return', 'CAGR', 'Sharpe Ratio', 'Sortino Ratio', 'Standard Deviation', 'MDD', 'Average Drawdown']
        for col in static_data.columns:
            if col in ['Compound_Return', 'CAGR', 'MDD', 'Average Drawdown', 'Standard Deviation','HPR(1Y)']:
                static_data.loc[:, col] = static_data.loc[:, col].apply(lambda x: str(np.around((x * 100), decimals=2)) + "%")
            else:
                static_data.loc[:, col] = static_data.loc[:, col].apply(lambda x: np.around(x, decimals=4))
        static_data.reset_index(inplace=True)
        static_data.rename(columns={'index': 'Portfolio'}, inplace=True)
        source = ColumnDataSource(static_data)
        columns = [TableColumn(field=col, title=col) for col in static_data.columns]
        data_table_obj = DataTable(source=source, columns=columns, width=1500, height=200,index_position=None)


        if simple==True:
            # Plot 단리
            source_for_chart = to_source(self.cum_ret_smpl)
            return_TS_obj = figure(x_axis_type='datetime',
                        title='Simple Return' + f'({self.cum_ret_cmpd.index[0].strftime("%Y-%m-%d")} ~ {self.cum_ret_cmpd.index[-1].strftime("%Y-%m-%d")})',
                        plot_width=1500, plot_height=400, toolbar_location=toolbar_location)
        elif simple=='log':
            # Plot 로그
            source_for_chart = to_source(self.cum_ret_cmpd)
            return_TS_obj = figure(x_axis_type='datetime', y_axis_type='log', y_axis_label=r"$$\frac{P_n}{P_0}$$",
                        title='Cumulative Return(LogScaled)' + f'({self.cum_ret_cmpd.index[0].strftime("%Y-%m-%d")} ~ {self.cum_ret_cmpd.index[-1].strftime("%Y-%m-%d")})',
                        plot_width=1500, plot_height=450, toolbar_location=toolbar_location)
        else:
            # Plot 복리
            source_for_chart = to_source(self.cum_ret_cmpd-1)
            return_TS_obj = figure(x_axis_type='datetime',
                        title='Cumulative Return' + f'({self.cum_ret_cmpd.index[0].strftime("%Y-%m-%d")} ~ {self.cum_ret_cmpd.index[-1].strftime("%Y-%m-%d")})',
                        plot_width=1500, plot_height=450, toolbar_location=toolbar_location)

        return_TS_lgd_list = []
        for i, col in enumerate(self.cum_ret_cmpd.columns):
            return_TS_line = return_TS_obj.line(source=source_for_chart, x=self.cum_ret_cmpd.index.name, y=col, color=self.color_list[i], line_width=2)
            return_TS_lgd_list.append((col, [return_TS_line]))
        return_TS_lgd = Legend(items=return_TS_lgd_list, location='center')
        return_TS_obj.add_layout(return_TS_lgd, 'right')
        return_TS_obj.legend.click_policy = "hide"
        return_TS_obj.yaxis.formatter = NumeralTickFormatter(format='0 %')

        # Plot drawdown
        dd_TS_obj = figure(x_axis_type='datetime',
                    title='Drawdown',
                    plot_width=1500, plot_height=170, toolbar_location=toolbar_location)
        source_dd_TS = to_source(self.drawdown)
        dd_TS_lgd_list = []
        for i, col in enumerate(self.drawdown.columns):
            dd_TS_line = dd_TS_obj.line(source=source_dd_TS, x='date', y=col, color=self.color_list[i], line_width=2)
            dd_TS_lgd_list.append((col, [dd_TS_line]))
        dd_TS_lgd = Legend(items=dd_TS_lgd_list, location='center')
        dd_TS_obj.add_layout(dd_TS_lgd, 'right')
        dd_TS_obj.legend.click_policy = "hide"
        dd_TS_obj.yaxis.formatter = NumeralTickFormatter(format='0 %')

        try:
            source_R1Y_HPR = to_source(self.R1Y_HPR)
            R1Y_HPR_obj = figure(x_axis_type='datetime',
                        title='Rolling Holding Period Return',
                        plot_width=1500, plot_height=170, toolbar_location=toolbar_location)
            R1Y_HPR_lgd_list = []
            for i, col in enumerate(self.R1Y_HPR.columns):
                p_line = R1Y_HPR_obj.line(source=source_R1Y_HPR, x='date', y=col, color=self.color_list[i], line_width=2)
                R1Y_HPR_lgd_list.append((col, [p_line]))
            R1Y_HPR_lgd = Legend(items=R1Y_HPR_lgd_list, location='center')

            R1Y_HPR_obj.add_layout(R1Y_HPR_lgd, 'right')
            R1Y_HPR_obj.legend.click_policy = "hide"
            R1Y_HPR_obj.yaxis.formatter = NumeralTickFormatter(format='0 %')
        except:
            pass

        if display == True:
            try:
                show(column(return_TS_obj, dd_TS_obj, R1Y_HPR_obj, Column(data_table_obj)))
            except:
                show(column(return_TS_obj, dd_TS_obj, Column(data_table_obj)))
        else:
            try:
                save(column(return_TS_obj, dd_TS_obj, R1Y_HPR_obj, Column(data_table_obj)))
            except:
                save(column(return_TS_obj, dd_TS_obj, Column(data_table_obj)))
    def report(self, display = True, toolbar_location='above'):
        from bokeh.plotting import output_file, show, curdoc, save
        from bokeh.layouts import column
        from bokeh.models import Column

        curdoc().clear()
        output_file(self.outputname + '.html')

        data_table_obj = self.get_table_obj()
        cmpd_return_TS_obj = self.get_cmpd_rtn_obj(toolbar_location)
        logscale_return_TS_obj = self.get_logscale_rtn_obj(toolbar_location)
        dd_TS_obj = self.get_dd_obj(toolbar_location)
        R1Y_HPR_obj = self.get_R1Y_HPR_obj(toolbar_location)

        if display == True:
            try:
                show(column(cmpd_return_TS_obj, logscale_return_TS_obj, dd_TS_obj, R1Y_HPR_obj, Column(data_table_obj)))
            except:
                show(column(cmpd_return_TS_obj, logscale_return_TS_obj, dd_TS_obj, Column(data_table_obj)))
        else:
            try:
                save(column(cmpd_return_TS_obj, logscale_return_TS_obj, dd_TS_obj, R1Y_HPR_obj, Column(data_table_obj)))
            except:
                save(column(cmpd_return_TS_obj, logscale_return_TS_obj, dd_TS_obj, Column(data_table_obj)))

    def to_source(self, df):
        from bokeh.models import ColumnDataSource
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
        return ColumnDataSource(df)
    def get_table_obj(self):
        from bokeh.models import ColumnDataSource
        from bokeh.models.widgets import DataTable, TableColumn

        try:
            static_data = pd.concat(
                [self.cum_ret_cmpd.iloc[-1] - 1, self.cagr, self.sharpe, self.sortino, self.std, self.mdd,
                 self.average_drawdown, self.R1Y_HPR_WR], axis=1)
            static_data.columns = ['Compound_Return', 'CAGR', 'Sharpe Ratio', 'Sortino Ratio', 'Standard Deviation',
                                   'MDD',
                                   'Average Drawdown', 'HPR(1Y)']
        except:
            static_data = pd.concat(
                [self.cum_ret_cmpd.iloc[-1] - 1, self.cagr, self.sharpe, self.sortino, self.std, self.mdd,
                 self.average_drawdown], axis=1)
            static_data.columns = ['Compound_Return', 'CAGR', 'Sharpe Ratio', 'Sortino Ratio', 'Standard Deviation',
                                   'MDD', 'Average Drawdown']
        for col in static_data.columns:
            if col in ['Compound_Return', 'CAGR', 'MDD', 'Average Drawdown', 'Standard Deviation', 'HPR(1Y)']:
                static_data.loc[:, col] = static_data.loc[:, col].apply(
                    lambda x: str(np.around((x * 100), decimals=2)) + "%")
            else:
                static_data.loc[:, col] = static_data.loc[:, col].apply(lambda x: np.around(x, decimals=4))
        static_data.reset_index(inplace=True)
        static_data.rename(columns={'index': 'Portfolio'}, inplace=True)
        source = ColumnDataSource(static_data)
        columns = [TableColumn(field=col, title=col) for col in static_data.columns]
        data_table_fig = DataTable(source=source, columns=columns, width=1500, height=200, index_position=None)
        return data_table_fig
    def get_inputtable_obj(self, input_tbl):
        from bokeh.models import ColumnDataSource
        from bokeh.models.widgets import DataTable, TableColumn
        # input_tbl = metric_table_decile.copy()

        # input_tbl.columns
        # input_tbl.filter(like='Alpha')

        pct_display = ['CAGR', 'std', 'MDD', 'Alpha CAGR', 'Tracking Error', 'Hit', 'R-Hit', 'Hit(alpha)', 'R-Hit(alpha)']
        for col in input_tbl.columns:
            if col in pct_display:
                input_tbl.loc[:, col] = input_tbl.loc[:, col].apply(
                    lambda x: str(np.around((x * 100), decimals=2)) + "%")
            else:
                input_tbl.loc[:, col] = input_tbl.loc[:, col].apply(lambda x: np.around(x, decimals=4))
        input_tbl.reset_index(inplace=True)
        input_tbl.rename(columns={'index': 'Portfolio'}, inplace=True)
        source = ColumnDataSource(input_tbl)
        columns = [TableColumn(field=col, title=col) for col in input_tbl.columns]
        data_table_fig = DataTable(source=source, columns=columns, width=1500, height=200, index_position=None)
        return data_table_fig
    def get_smpl_rtn_obj(self, toolbar_location):
        from bokeh.plotting import figure
        from bokeh.models import NumeralTickFormatter, Legend

        # Plot 단리
        source_for_chart = self.to_source(self.cum_ret_smpl)
        return_TS_obj = figure(x_axis_type='datetime',
                    title='Simple Return' + f'({self.cum_ret_cmpd.index[0].strftime("%Y-%m-%d")} ~ {self.cum_ret_cmpd.index[-1].strftime("%Y-%m-%d")})',
                    plot_width=1500, plot_height=400, toolbar_location=toolbar_location)
        return_TS_lgd_list = []
        for i, col in enumerate(self.cum_ret_cmpd.columns):
            return_TS_line = return_TS_obj.line(source=source_for_chart, x=self.cum_ret_cmpd.index.name, y=col, color=self.color_list[i], line_width=2)
            return_TS_lgd_list.append((col, [return_TS_line]))
        return_TS_lgd = Legend(items=return_TS_lgd_list, location='center')
        return_TS_obj.add_layout(return_TS_lgd, 'right')
        return_TS_obj.legend.click_policy = "hide"
        return_TS_obj.yaxis.formatter = NumeralTickFormatter(format='0 %')
        return return_TS_obj
    def get_cmpd_rtn_obj(self, toolbar_location):
        from bokeh.plotting import figure
        from bokeh.models import NumeralTickFormatter, Legend
        # Plot 복리
        source_for_chart = self.to_source(self.cum_ret_cmpd - 1)
        return_TS_obj = figure(x_axis_type='datetime',
                               title='Cumulative Return' + f'({self.cum_ret_cmpd.index[0].strftime("%Y-%m-%d")} ~ {self.cum_ret_cmpd.index[-1].strftime("%Y-%m-%d")})',
                               plot_width=1500, plot_height=450, toolbar_location=toolbar_location)

        return_TS_lgd_list = []
        for i, col in enumerate(self.cum_ret_cmpd.columns):
            return_TS_line = return_TS_obj.line(source=source_for_chart, x=self.cum_ret_cmpd.index.name, y=col,
                                                color=self.color_list[i], line_width=2)
            return_TS_lgd_list.append((col, [return_TS_line]))
        return_TS_lgd = Legend(items=return_TS_lgd_list, location='center')
        return_TS_obj.add_layout(return_TS_lgd, 'right')
        return_TS_obj.legend.click_policy = "hide"
        return_TS_obj.yaxis.formatter = NumeralTickFormatter(format='0 %')
        return return_TS_obj
    def get_logscale_rtn_obj(self, toolbar_location):
        from bokeh.plotting import figure
        from bokeh.models import NumeralTickFormatter, Legend
        # Plot 로그
        source_for_chart = self.to_source(self.cum_ret_cmpd)
        return_TS_obj = figure(x_axis_type='datetime', y_axis_type='log', y_axis_label=r"$$\frac{P_n}{P_0}$$",
                               title='Cumulative Return(LogScaled)' + f'({self.cum_ret_cmpd.index[0].strftime("%Y-%m-%d")} ~ {self.cum_ret_cmpd.index[-1].strftime("%Y-%m-%d")})',
                               plot_width=1500, plot_height=450, toolbar_location=toolbar_location)
        return_TS_lgd_list = []
        for i, col in enumerate(self.cum_ret_cmpd.columns):
            return_TS_line = return_TS_obj.line(source=source_for_chart, x=self.cum_ret_cmpd.index.name, y=col,
                                                color=self.color_list[i], line_width=2)
            return_TS_lgd_list.append((col, [return_TS_line]))
        return_TS_lgd = Legend(items=return_TS_lgd_list, location='center')
        return_TS_obj.add_layout(return_TS_lgd, 'right')
        return_TS_obj.legend.click_policy = "hide"
        return_TS_obj.yaxis.formatter = NumeralTickFormatter(format='0 %')
        return return_TS_obj
    def get_dd_obj(self, toolbar_location):
        from bokeh.plotting import figure
        from bokeh.models import NumeralTickFormatter, Legend
        # Plot drawdown
        dd_TS_obj = figure(x_axis_type='datetime',
                    title='Drawdown',
                    plot_width=1500, plot_height=170, toolbar_location=toolbar_location)
        source_dd_TS = self.to_source(self.drawdown)
        dd_TS_lgd_list = []
        for i, col in enumerate(self.drawdown.columns):
            dd_TS_line = dd_TS_obj.line(source=source_dd_TS, x='date', y=col, color=self.color_list[i], line_width=2)
            dd_TS_lgd_list.append((col, [dd_TS_line]))
        dd_TS_lgd = Legend(items=dd_TS_lgd_list, location='center')
        dd_TS_obj.add_layout(dd_TS_lgd, 'right')
        dd_TS_obj.legend.click_policy = "hide"
        dd_TS_obj.yaxis.formatter = NumeralTickFormatter(format='0 %')
        return dd_TS_obj
    def get_R1Y_HPR_obj(self, toolbar_location):
        from bokeh.plotting import figure
        from bokeh.models import NumeralTickFormatter, Legend
        try:
            source_R1Y_HPR = self.to_source(self.R1Y_HPR)
            R1Y_HPR_obj = figure(x_axis_type='datetime',
                                 title='Rolling Holding Period Return',
                                 plot_width=1500, plot_height=170, toolbar_location=toolbar_location)
            R1Y_HPR_lgd_list = []
            for i, col in enumerate(self.R1Y_HPR.columns):
                p_line = R1Y_HPR_obj.line(source=source_R1Y_HPR, x='date', y=col, color=self.color_list[i],
                                          line_width=2)
                R1Y_HPR_lgd_list.append((col, [p_line]))
            R1Y_HPR_lgd = Legend(items=R1Y_HPR_lgd_list, location='center')

            R1Y_HPR_obj.add_layout(R1Y_HPR_lgd, 'right')
            R1Y_HPR_obj.legend.click_policy = "hide"
            R1Y_HPR_obj.yaxis.formatter = NumeralTickFormatter(format='0 %')
            return R1Y_HPR_obj
        except:
            return None

    def deciles_bar_color_list(self,bar_num,bench_num):
        # Spectral6 컬러 목록
        # #['#3288bd', '#99d594', '#e6f598', '#fee08b',, '#d53e4f']
        deciles_bar_color_list = []
        for i in range(0, bar_num):
            deciles_bar_color_list.append('#fc8d59')
        for i in range(0, bench_num):
            deciles_bar_color_list.append('#e6f598')
        return deciles_bar_color_list

    def get_CAGR_bar_obj(self):
        from scipy.stats import linregress
        from bokeh.plotting import figure
        from bokeh.models import ColumnDataSource, NumeralTickFormatter

        CAGR_values=self.cagr.values
        CAGR_index=self.cagr.index

        slp, itrct, rval, pval, stderr = linregress(range(1,len(CAGR_index)), CAGR_values[:-1])
        title_text = f'10분위 연환산 수익률(r_value:{round(rval,2)}, p_value:{round(pval,2)}, std_err:{round(stderr,2)})'

        qun_sourse = ColumnDataSource(data = dict(분위=list(CAGR_index), CAGR =CAGR_values, color=self.deciles_bar_color_list(10, 1)))
        qun = figure(x_range=list(CAGR_index), plot_height=440, title=title_text, plot_width=390)
        qun.vbar(x='분위', top='CAGR', width=0.9,  source=qun_sourse, color='color')
        qun.line(range(1,len(CAGR_index)), [x*slp + itrct for x in range(0,len(CAGR_index))], color='black', line_width=2)
        qun.xgrid.grid_line_color = None
        qun.toolbar.logo = None
        qun.toolbar_location = None
        qun.yaxis[0].formatter = NumeralTickFormatter(format="0.00%")
        return qun

    def _array_to_df(self, arr):
        try:
            return pd.DataFrame(arr,
                              index=self.daily_return.index.values,
                              columns=self.daily_return.columns.values).rename_axis("date")
        except:
            return pd.DataFrame(arr,
                                index=self.cum_ret_cmpd.index.values,
                                columns=self.cum_ret_cmpd.columns.values).rename_axis("date")

    def get_num_year(self, num_years):
        num_years = len(num_years)
        if num_years ==2 :
            # 기간이 1년 이상이면, 1년이란 길이의 기준은 데이터의 갯수로 한다.
            start_date = self.daily_return.index[0]
            end_date = start_date + pd.DateOffset(years=1)

            date_list = self.daily_return.loc[start_date:end_date].index
            num_days = len(date_list)

        elif num_years==1:
            # 기간이 1년 미만이면, 1년이란 길이의 기준은 다음해까지의 영업일 기준으로 가상으로 확장시킨다.
            start_date = self.daily_return.index[0]
            end_date = self.daily_return.index[-1]
            end_date_ = start_date + pd.DateOffset(years=1)

            # 1년이란 기준의 날짜 수 정의
            date_list = pd.date_range(start=start_date, end=end_date_, freq=BDay())
            date_list2 = pd.date_range(start=start_date, end=end_date, freq=BDay())
            num_days = len(date_list)/len(date_list2) * len(self.daily_return.index)

        else:
            # 3년 이상이면, input된 데이터의 첫해와 마지막 해를 제외하고 한 해의 날짜수의 평균으로 한다.
            num_days = self.daily_return.groupby(pd.Grouper(freq='Y')).count().iloc[1:-1].mean()[0]
        return num_days
    def _calculate_dd(self, df):
        # df = self.cum_ret_cmpd.copy()
        # df = t_df.pct_change().copy()
        max_list = df.iloc[0].values
        out_list = [np.array([0]*len(max_list))]

        for ix in range(1, len(df.index)):
            max_list = np.max([max_list, df.iloc[ix].values], axis=0)
            out_list.append((df.iloc[ix].values - max_list) / max_list)

        out = self._array_to_df(out_list)
        return out

    @staticmethod
    def _calculate_cagr(df, num_days):
        return ((df.iloc[-1]) ** (1 / len(df.index))) ** num_days - 1
    @staticmethod
    def _calculate_std(df, num_days):
        return df.std() * np.sqrt(num_days)
    @staticmethod
    def _calculate_mdd(df):
        return df.min()
    @staticmethod
    def _calculate_downsiderisk(df,num_days):
        return df.applymap(lambda x: 0 if x >= 0 else x).std() * np.sqrt(num_days)
    @staticmethod
    def _holding_period_return(df, num_days):
        Rolling_HPR_1Y = df.pct_change(int(num_days.round())).dropna()
        HPR_1Y_mean = Rolling_HPR_1Y.mean()
        HPR_1Y_max = Rolling_HPR_1Y.max()
        HPR_1Y_min = Rolling_HPR_1Y.min()
        Rolling_HPR_1Y_WR = (Rolling_HPR_1Y > 0).sum() / Rolling_HPR_1Y.shape[0]
        return Rolling_HPR_1Y, Rolling_HPR_1Y_WR
