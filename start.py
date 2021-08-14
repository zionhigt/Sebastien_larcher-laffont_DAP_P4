from chessmanager.views.home import HomeView
from chessmanager.controllers.home import HomeCtrl


print("Chess manager")
HOME_VIEW = HomeView()
CTRL = HomeCtrl(HOME_VIEW)
CTRL.run()