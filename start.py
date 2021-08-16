from chessmanager.views.home import HomeView
from chessmanager.controllers.home import HomeCtrl


HOME_VIEW = HomeView()
CTRL = HomeCtrl(HOME_VIEW)
CTRL.run()