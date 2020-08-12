import Controller from '../modules/controller';

export default class NavigationController extends Controller {

  init() {
    this.openButton = this.el.querySelector('.menu-bar__icon-button');
    this.closeButton = this.el.querySelector('.menu-overlay__close-button');
    this.overlay = this.el.querySelector('.menu-overlay');

    if (!this.openButton || !this.closeButton || !this.overlay) {
      return;
    }

    this.openButton.addEventListener('click', this.onOpenClick.bind(this));
    this.closeButton.addEventListener('click', this.onCloseClick.bind(this));

  }

  onOpenClick(e) {

    e.stopPropagation();
    this.open();
  }

  onCloseClick(e) {

    e.stopPropagation();
    this.close();
  }

  open() {
    this.overlay.classList.add('is-visible');

    document.documentElement.classList.add('prevent-scrolling');

  }

  close() {
    this.overlay.classList.remove('is-visible');

    document.documentElement.classList.remove('prevent-scrolling');

  }
}
