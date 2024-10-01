from sys import path
from classes.upgrades import *

x = IncomeUpgrade("Lounge", 5000, 1.25)
print(x.bought)
x.purchase()
print(x.bought)
