from chessmanager.views.home import HomeView
from chessmanager.controllers.home import HomeCtrl


def main():
    home_view = HomeView()
    ctrl = HomeCtrl(home_view)
    ctrl.run()


if __name__ == '__main__':
    main()
