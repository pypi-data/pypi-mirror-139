=====================
positions_backtester
=====================

.. image:: https://img.shields.io/github/last-commit/stas-prokopiev/positions_backtester
   :target: https://img.shields.io/github/last-commit/stas-prokopiev/positions_backtester
   :alt: GitHub last commit

.. image:: https://img.shields.io/github/license/stas-prokopiev/positions_backtester
    :target: https://github.com/stas-prokopiev/positions_backtester/blob/master/LICENSE.txt
    :alt: GitHub license<space><space>

.. image:: https://img.shields.io/pypi/v/positions_backtester
   :target: https://img.shields.io/pypi/v/positions_backtester
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/positions_backtester
   :target: https://img.shields.io/pypi/pyversions/positions_backtester
   :alt: PyPI - Python Version


.. contents:: **Table of Contents**

Short Overview.
=========================
positions_backtester is a python package (**py>=3.7**) to backtest trading strategies (dataframe with positions) with execution costs modeling

| This package is trying to solve problem of slow trading with fast data.
| Let's say that you want to update your trading position once in a hour, day, week, ...
| But you have data with much higher resolution - minutes, seconds, miliseconds
| Then you can give the wanted positions dataframe with the tick with which you want to trade
| And higher resolution will be used to calculate approximate execution prices
| Which will be just mean price over execution time period

Installation via pip:
======================

.. code-block:: bash

    pip install positions_backtester

How to use it
===========================

Create Backtester
----------------------

.. code-block:: python

    from positions_backtester import Backtester

    backtester = Backtester(float_percent_const_trading_fees=0.01,)

How to backtest your dataframe with positions
-----------------------------------------------

.. code-block:: python

    from positions_backtester import Backtester

    df_backtest_res = backtester.backtest(
        df_positions_short,
        df_prices_full,
        is_to_neutralize=True,
        td_trading_delay=None,
        td_execution_duration=None,
    )

Arguments:

#. **df_positions_short**:
    | pd.DataFrame
    | Positions we want to take with the frequency with which we want to change our positions
#. **df_prices_full**:
    | pd.DataFrame
    | Prices of assets in higher resolution
    | Higher resolution needed for better execution evaluation
#. **is_to_neutralize=True,**:
    | Flag if to have long-short equal positions
#. **td_trading_delay=None**:
    | datetime.timedelta
    | Delay needed to calculate the wanted positions
#. **td_execution_duration**:
    | datetime.timedelta
    | How long should the execution take
    | Execution price will be the mean price over execution time period


Inputs:
-----------------------------------------------

df_positions_short
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..
    raw:: html

    <embed>
        <table border="1" class="dataframe">
        <thead>
            <tr style="text-align: right;">
            <th></th>
            <th>asset_1</th>
            <th>asset_2</th>
            <th>asset_3</th>
            </tr>
            <tr>
            <th>Close datetime</th>
            <th></th>
            <th></th>
            <th></th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <th>2021-07-06 22:00:00+00:00</th>
            <td>0.285602</td>
            <td>NaN</td>
            <td>NaN</td>
            </tr>
            <tr>
            <th>2021-07-06 23:00:00+00:00</th>
            <td>0.296204</td>
            <td>NaN</td>
            <td>NaN</td>
            </tr>
            <tr>
            <th>2021-07-07 00:00:00+00:00</th>
            <td>0.294426</td>
            <td>NaN</td>
            <td>NaN</td>
            </tr>
        </tbody>
        </table>
    </embed>


df_prices_full
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..
    raw:: html

    <embed>
        <table border="1" class="dataframe">
        <thead>
            <tr style="text-align: right;">
            <th></th>
            <th>asset_1</th>
            <th>asset_2</th>
            <th>asset_3</th>
            </tr>
            <tr>
            <th>Close datetime</th>
            <th></th>
            <th></th>
            <th></th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <th>2021-07-06 23:57:59+00:00</th>
            <td>317.86</td>
            <td>57.00</td>
            <td>15.488</td>
            </tr>
            <tr>
            <th>2021-07-06 23:58:59+00:00</th>
            <td>317.11</td>
            <td>57.04</td>
            <td>15.480</td>
            </tr>
            <tr>
            <th>2021-07-06 23:59:59+00:00</th>
            <td>316.49</td>
            <td>57.01</td>
            <td>15.459</td>
            </tr>
        </tbody>
        </table>
    </embed>


Output: df_backtest_res
-----------------------------------------------

..
    raw:: html

    <embed>
        <table border="1" class="dataframe">
        <thead>
            <tr style="text-align: right;">
            <th></th>
            <th>PNL_before_costs</th>
            <th>execution_fee_pnl</th>
            <th>trading_volume</th>
            <th>const_trading_fee_pnl</th>
            <th>PNL_after_costs</th>
            <th>PNL_half_costs</th>
            <th>booksize</th>
            </tr>
            <tr>
            <th>Close datetime</th>
            <th></th>
            <th></th>
            <th></th>
            <th></th>
            <th></th>
            <th></th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <th>2021-07-06 20:00:00+00:00</th>
            <td>-0.002108</td>
            <td>-0.004361</td>
            <td>0.034720</td>
            <td>0.000003</td>
            <td>0.002250</td>
            <td>0.000071</td>
            <td>1.0</td>
            </tr>
            <tr>
            <th>2021-07-06 21:00:00+00:00</th>
            <td>-0.005282</td>
            <td>-0.000222</td>
            <td>0.053568</td>
            <td>0.000005</td>
            <td>-0.005065</td>
            <td>-0.005174</td>
            <td>1.0</td>
            </tr>
            <tr>
            <th>2021-07-06 22:00:00+00:00</th>
            <td>0.000466</td>
            <td>0.002673</td>
            <td>0.044552</td>
            <td>0.000004</td>
            <td>-0.002212</td>
            <td>-0.000873</td>
            <td>1.0</td>
            </tr>
            <tr>
            <th>2021-07-06 23:00:00+00:00</th>
            <td>-0.000614</td>
            <td>-0.003834</td>
            <td>0.072116</td>
            <td>0.000007</td>
            <td>0.003212</td>
            <td>0.001299</td>
            <td>1.0</td>
            </tr>
            <tr>
            <th>2021-07-07 00:00:00+00:00</th>
            <td>0.000000</td>
            <td>0.000000</td>
            <td>0.032531</td>
            <td>0.000003</td>
            <td>-0.000003</td>
            <td>-0.000002</td>
            <td>1.0</td>
            </tr>
        </tbody>
        </table>
    </embed>


Formulas
===========================

| PNL_before_costs = (previous_position) * (price_change_%)
| trading_volume = abs(new_wanted_position - previous_position)
| const_trading_fee_pnl = trading_volume * broker_commision
| execution_fee_pnl = (new_wanted_position - previous_position) * (execution_price - current_price)
| PNL_after_costs = PNL_before_costs - (const_trading_fee_pnl + execution_fee_pnl)
| PNL_half_costs = PNL_before_costs - (const_trading_fee_pnl + execution_fee_pnl) / 2.0

Links
=====

    * `PYPI <https://pypi.org/project/positions_backtester/>`_
    * `GitHub <https://github.com/stas-prokopiev/positions_backtester>`_

Project local Links
===================

    * `CHANGELOG <https://github.com/stas-prokopiev/positions_backtester/blob/master/CHANGELOG.rst>`_.
    * `CONTRIBUTING <https://github.com/stas-prokopiev/positions_backtester/blob/master/CONTRIBUTING.rst>`_.

Contacts
========

    * Email: stas.prokopiev@gmail.com
    * `vk.com <https://vk.com/stas.prokopyev>`_
    * `Facebook <https://www.facebook.com/profile.php?id=100009380530321>`_

License
=======

This project is licensed under the MIT License.