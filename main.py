from src.extensive_games import Daruma
from src.model import Model
from src.solvers import CFR
#from strategy import Strategy
from src.visualizers import DarumaVisualizer

game = Daruma(10, 10, 5, 1)
model = Model(game)

model.search(game)
result = CFR(model)
#strategy = Strategy.from_model(model)