BACKTEST VIEWER - ISSUES TO FIX
Last Updated: 2024-11-21

A. Python back test engine window:
1. the text fonts is unreadable. white text on a bit dark white background(no contrast on symbols, strategy, dates, highlighted/selected tab) 

B. MT5-Style Chart Viewer - JCAMP Back testing observation:
1. candle stick sit sill not showing. only EMA draws. 
2. Transparent trade boxes is location is way too off. 
	- the start/left side of the box is when the trade got entered or pending order. 
	- if pending order got triggered, the start/left side will be moved to the right to when it triggered.
	- the Transparent trade boxes should be ended/right-side of box when the trade was closed. 
	- on the chart viewport:
		-currently the columns shows below above the "TIME" is the Bar Numbers. this should be time and dates. instead of only bars number. maybe 		put this on the lines/rows. row1 = Time, row2 = Date 
3. bar slider is good. 
4. when the simulation is playing. the viewport is on not moving with the current price is. it should be moving with the current price. the current price must be on the right-side of the viewport.  
5. EMA should be like this: (and this is what the Jcamp_BacktestEA.mq5 v1.96 was using)
	-EMA fast is 20 and color RED
	-EMA Mid is 50 and color Orange
	-EMA slow is 100 and color blue


Note: 
lets focus first on this issues.