import GD_utils as gdu
import pandas as pd
def basic_report(base_price, name='./Unnamed', display=True, toolbar_location='above'):
    # base_price = df.copy()
    b_price = base_price.sort_index().rename_axis('date', axis=0).dropna()

    daily_return = b_price.pct_change().fillna(0)
    if type(daily_return) == pd.core.series.Series:
        daily_return = pd.DataFrame(daily_return.rename("price")).rename_axis('date', axis=0)


    PA = gdu.portfolio_calculator.PortfolioAnalysis(daily_return, outputname=name)
    PA.report(display=display, toolbar_location=toolbar_location)