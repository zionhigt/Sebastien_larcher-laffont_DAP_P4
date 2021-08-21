from chessmanager.views.home import HomeView
from chessmanager.controllers.home import HomeCtrl



def main():
    HOME_VIEW = HomeView()
    CTRL = HomeCtrl(HOME_VIEW)
    CTRL.run()



if __name__ == '__main__':
    main()