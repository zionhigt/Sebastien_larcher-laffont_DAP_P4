from chester.views.home import HomeView
from chester.controllers.home import HomeCtrl

HOME_VIEW = HomeView()
CTRL = HomeCtrl(HOME_VIEW)
CTRL.run()