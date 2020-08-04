export default class Controller {

  constructor(el, options = {}) {

    // can be reduced to one at some point
    this.el = el;
    this.element = el;

    this.init()
  }

  init() {
    throw Error(`Initialization method must be defined for ${this}.`)
  }
}
