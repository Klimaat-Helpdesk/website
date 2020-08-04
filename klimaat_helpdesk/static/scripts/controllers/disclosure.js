import Controller from '../modules/controller';

export default class DisclosureController extends Controller {

  init() {
    this.link = this.element.querySelector('.disclosure__title-button')
    this.region = this.element.querySelector('.disclosure__disclosure-content')

    if (!this.link || !this.region) {
      return
    }

    this.link.addEventListener('click', () => this.toggleRegion())
  }

    toggleRegion () {
      if (this.link.getAttribute('aria-expanded') === 'true') {
        this.region.setAttribute('hidden', 'hidden')
        this.link.setAttribute('aria-expanded', false)
        this.element.classList.remove('disclosure--expanded')
      } else {
        this.region.removeAttribute('hidden')
        this.link.setAttribute('aria-expanded', true)
        this.element.classList.add('disclosure--expanded')

        const rect = this.region.getBoundingClientRect()
        window.scroll({ top: (window.pageYOffset + rect.top) - (window.innerHeight / 3), left: 0, behavior: 'smooth' })

        this.link.blur()
      }
    }
}
