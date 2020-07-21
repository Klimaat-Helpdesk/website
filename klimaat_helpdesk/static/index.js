//MKR  to compile opur scss import it once here
import './stylesheets/main.scss';

function setupControllers(container) {

  // Initialize all controllers defined on nodes
  Array.from(container.querySelectorAll(
    '[data-controller]:not([data-initialized])')
  ).map((el) => {
    el.dataset.initialized = true;

    // Allow multiple controllers with whitespace between
    return [
      ...el.dataset.controller.trim().replace(/\s+/, ' ').trim().split(' ')
    ].map((controller) => {
      if (! controller) {
        return;
      }


      try {
        let Controller = require(`controllers/${controller}.js`).default;
        el.__controller__ = new Controller(el);
        return el.__controller__;
      } catch(e) {
        console.log(`Error loading controller "${controller}"`);
        throw e;
      }
    });
  });
}


document.addEventListener('DOMContentLoaded', function (event) {
  const container = event.target;
  setupControllers(container);
});


window.setupControllers = setupControllers;
