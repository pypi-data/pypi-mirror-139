import datetime

import pyqtgraph as pg
from pyqtgraph.Qt import QT_LIB, PYQT6
from pglive.kwargs import Axis

if QT_LIB == PYQT6:
    from PyQt6.QtGui import QPen
else:
    from PyQt5.QtGui import QPen

from pyqtgraph import debug as debug


class LiveAxis(pg.AxisItem):

    def __init__(self, orientation, pen=None, textPen=None, axisPen=None, linkView=None, parent=None, maxTickLength=-5,
                 showValues=True, text='', units='', unitPrefix='', **kwargs):
        super().__init__(orientation, pen=pen, textPen=textPen, linkView=linkView, parent=parent,
                         maxTickLength=maxTickLength, showValues=showValues, text=text, units=units,
                         unitPrefix=unitPrefix, **kwargs)
        # Fixing pyqtgraph bug, not setting textPen properly
        if textPen is None:
            self.setTextPen()
        else:
            self.setTextPen(textPen)
        # Set axisPen
        if axisPen is not None and not isinstance(axisPen, QPen):
            axisPen = pg.mkPen(color=axisPen)
        self.axisPen = axisPen
        if self.axisPen is None:
            self.axisPen = self.pen()
        # Tick format
        self.tick_format = kwargs.get(Axis.TICK_FORMAT, None)

    def tickStrings(self, values, scale, spacing):
        if self.tick_format == Axis.DATETIME:
            # Convert tick to Datetime
            return [datetime.datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S") for value in values]
        elif self.tick_format == Axis.TIME:
            # Convert tick to Time
            return [datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S") for value in values]
        else:
            # No specific format
            return super().tickStrings(values, scale, spacing)

    def drawPicture(self, p, axisSpec, tickSpecs, textSpecs):
        profiler = debug.Profiler()

        p.setRenderHint(p.RenderHint.Antialiasing, False)
        p.setRenderHint(p.RenderHint.TextAntialiasing, True)

        # draw long line along axis
        pen, p1, p2 = axisSpec
        # Use axis pen to draw axis line
        p.setPen(self.axisPen)
        p.drawLine(p1, p2)
        # Switch back to normal pen
        p.setPen(pen)
        # p.translate(0.5,0)  ## resolves some damn pixel ambiguity

        # draw ticks
        for pen, p1, p2 in tickSpecs:
            p.setPen(pen)
            p.drawLine(p1, p2)
        profiler('draw ticks')

        # Draw all text
        if self.style['tickFont'] is not None:
            p.setFont(self.style['tickFont'])
        p.setPen(self.textPen())
        bounding = self.boundingRect().toAlignedRect()
        p.setClipRect(bounding)
        for rect, flags, text in textSpecs:
            p.drawText(rect, int(flags), text)

        profiler('draw text')
