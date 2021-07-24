from vnpy.app.cta_strategy import (
    CtaTemplate,
    BarGenerator,
    ArrayManager,
    TradeData,
    OrderData,
    BarData,
    TickData,
    StopOrder
)


class DemoStrategy(CtaTemplate):
    author = "Simon"

    # 定义参数, 可以界面上进行修改的
    fast_window = 10
    slow_window = 20

    # 定义变量
    fast_ma0 = 0
    fast_ma1 = 0

    slow_ma0 = 0
    slow_ma1 = 0

    parameters = ['fast_window', 'slow_window']
    variables = ['fast_ma0', 'fast_ma1', 'slow_ma0', 'slow_ma1']

    def __init__(
            self,
            cta_engine: Any,
            strategy_name: str,
            vt_symbol: str,
            setting: dict,
    ):
        super(DemoStrategy, self).__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.bg = BarGenerator(self.on_bar)

        self.am = ArrayManager()

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略开始")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略结束")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        self.am.update_bar(bar)

        if not self.am.inited:
            return

        # 快速均线
        self.fast_ma0 = self.am.sma(self.fast_window, array=True)[-1]
        self.fast_ma1 = self.am.sma(self.fast_window, array=True)[-2]

        # 慢速均线
        self.slow_ma0 = self.am.sma(self.slow_window, array=True)[-1]
        self.slow_ma1 = self.am.sma(self.slow_window, array=True)[-2]

        if self.pos == 0:

            # \  /
            #  \/
            #  /\
            # /  \
            # 金叉
            if self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1:
                self.buy(bar.close_price, 1)

            elif self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1:
                self.short(bar.close_price, 1)

        # 更新图表
        self.put_event()

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        self.put_event()
