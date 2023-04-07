#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QDialog, QLabel, QGridLayout,
                             QDoubleSpinBox, QApplication, QLCDNumber)

import numpy as np
import pyqtgraph as pg

class Form(QDialog):

    def __init__(self):
        super().__init__()
        

        # inputs
        # x-values
        
        xLabel = QLabel("X values:")

        self.x1SpinBox = QDoubleSpinBox()
        self.x1SpinBox.setRange(-50., 50.)
        self.x1SpinBox.setValue(0)
        self.x1SpinBox.setSuffix("")
        self.x1SpinBox.setDecimals(2)
    

        self.x2SpinBox = QDoubleSpinBox()
        self.x2SpinBox.setRange(-50., 50.)
        self.x2SpinBox.setValue(0)
        self.x2SpinBox.setSuffix("")
        self.x2SpinBox.setDecimals(2)


        self.x3SpinBox = QDoubleSpinBox()
        self.x3SpinBox.setRange(-50., 50.)
        self.x3SpinBox.setValue(0)
        self.x3SpinBox.setSuffix("")
        self.x3SpinBox.setDecimals(2)
        
       # y-values

        yLabel = QLabel("Y values:")

        self.y1SpinBox = QDoubleSpinBox()
        self.y1SpinBox.setRange(-50., 50.)
        self.y1SpinBox.setValue(0)
        self.y1SpinBox.setSuffix("")
        self.y1SpinBox.setDecimals(2)
       

        self.y2SpinBox = QDoubleSpinBox()
        self.y2SpinBox.setRange(-50., 50.)
        self.y2SpinBox.setValue(0)
        self.y2SpinBox.setSuffix("")
        self.y2SpinBox.setDecimals(2)
       

        self.y3SpinBox = QDoubleSpinBox()
        self.y3SpinBox.setRange(-50., 50.)
        self.y3SpinBox.setValue(0)
        self.y3SpinBox.setSuffix("")
        self.y3SpinBox.setDecimals(2)
       
        

        # outputs
        
        alphaLabel = QLabel("Y-intercept: ")
        self.alpha = QLabel()
        betaLabel = QLabel("Slope: ")
        self.beta = QLabel()
        
        #self.lcd = QLCDNumber()
        
        
        
        # create a PlotWidget instance
        self.pw = pg.PlotWidget()

        # add scatter plot to the PlotWidget
        self.scatter = pg.ScatterPlotItem(x=[0], y=[0])
        self.pw.addItem(self.scatter)

        # add line to the PlotWidget
        self.line = pg.PlotCurveItem(x=[0,0], y=[0,0])
        self.pw.addItem(self.line)

        #set location and dimensions of box
        self.top = 0
        self.left = 0
        self.width = 800
        self.height = 600
        self.setGeometry(self.left, self.top, self.width, self.height)


        # setup the layout

        grid = QGridLayout()
        
        # x-inputs
        grid.addWidget(xLabel, 0, 0) 
        grid.addWidget(self.x1SpinBox, 1,0)
        grid.addWidget(self.x2SpinBox, 2, 0)
        grid.addWidget(self.x3SpinBox, 3, 0)
        
        # y-inputs

        grid.addWidget(yLabel, 0, 1)  
        grid.addWidget(self.y1SpinBox, 1, 1)
        grid.addWidget(self.y2SpinBox, 2, 1)
        grid.addWidget(self.y3SpinBox, 3, 1)

       
        # outputs
        grid.addWidget(alphaLabel, 4, 0)  # alpha
        grid.addWidget(self.alpha, 4, 1)
        grid.addWidget(betaLabel, 5, 0)  # beta
        grid.addWidget(self.beta, 5, 1)
        #grid.addWidget(self.lcd, 6,0)
        grid.addWidget(self.pw,6,2)
        self.setLayout(grid)
        

        # Set up event loop with signals & slots
        self.x1SpinBox.valueChanged.connect(self.updateUi)
        self.x2SpinBox.valueChanged.connect(self.updateUi)
        self.x3SpinBox.valueChanged.connect(self.updateUi)
        self.y1SpinBox.valueChanged.connect(self.updateUi)
        self.y2SpinBox.valueChanged.connect(self.updateUi)
        self.y3SpinBox.valueChanged.connect(self.updateUi)
        
        
        # Window title & initialize values of outputs
        self.setWindowTitle("Linear Regression Calculator")
        self.updateUi()

    def updateUi(self):
       
        x1 = self.x1SpinBox.value() 
        x2 = self.x2SpinBox.value()
        x3 = self.x3SpinBox.value()
        y1 = self.y1SpinBox.value() 
        y2 = self.y2SpinBox.value()
        y3 = self.y3SpinBox.value()

        # calculations to determine the coefficients for the line of best fit
        # y = alpha + beta * x

        x = [x1, x2, x3]
        y = [y1, y2, y3]
       

        xMean = sum(x)/len(x)
        yMean = sum(y)/len(y)
        
        numerator = 0
        denominator = 0

        for i in range(3):
            numerator += (x[i] - xMean)*(y[i] - yMean)
            denominator += (x[i] - xMean)**2

        try:
            beta = numerator/denominator
        
        except ZeroDivisionError:
            beta = 0
       
        alpha = yMean - xMean*beta

        #updating the regression line plot

        new_x = np.array([x1, x2, x3])
        new_y = np.array([y1, y2, y3])
        
        new_line_x = np.array([new_x.min(), new_x.max()])
        new_line_y = np.array([alpha + new_x.min() * beta, alpha + new_x.max() * beta ])

        self.scatter.setData(x=new_x, y=new_y)
        self.line.setData(x=new_line_x, y=new_line_y)

        self.alpha.setText("{:10.4f}".format(alpha))
        self.beta.setText("{:10.4f}".format(beta))
        #self.lcd.display(2023)
        #self.lcd.setStyleSheet('background-color:yellow')

        
        return


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())
