from src.views.tourney import TourneyView
from src.views.home import HomeView
from src.controllers.tourney import TourneyCtrl
from src.controllers.home import HomeCtrl

HOME_VIEW = HomeView()
TOURNEY_VIEW = TourneyView()
CTRL = HomeCtrl(HOME_VIEW, TOURNEY_VIEW)
CTRL.run()