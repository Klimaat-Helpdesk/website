import Controller from '../modules/controller';

export default class NavigationController extends Controller {

    init() {
        this.initializeButtons();
        this.initializeCheckboxes();

        this.selectedCategories = [];
    }

    initializeButtons() {
    var continueButton = document.getElementById('form-step__continue');
    var backButton = document.getElementById('form-step__back');

    if(!continueButton || !backButton){
      return;
    }

    continueButton.addEventListener("click", this.activateStepTwo.bind(this));
    backButton.addEventListener("click", this.activateStepOne.bind(this));
  }

  initializeCheckboxes() {
    var categoriesField = document.querySelector('.form-field__categories');

    if(!categoriesField) {
      return;
    }

    // Whenever a change is detected, show relevant tips
    var checkboxes = categoriesField.querySelectorAll('input');
    var thisRef = this;
    checkboxes.forEach(function(e) {
        e.addEventListener('change', function() {
          if(this.checked) {
            thisRef.selectedCategories.push(this.value);
            thisRef.showSuggestionCategory(this.value);
          }
          else {
            thisRef.selectedCategories.pop(this.value);
            thisRef.hideSuggestionCategory(this.value);
          }

          // Check whether to show suggestions at all
          var tipsDiv = document.querySelector('.form__tip');
          if(tipsDiv) {
            if (thisRef.selectedCategories.length === 0) {
              tipsDiv.classList.add('is-hidden');
              tipsDiv.classList.add('is-visible');
            } else {
              tipsDiv.classList.add('is-visible');
              tipsDiv.classList.add('is-hidden');
            }
          }
        });
    });
  }

  showSuggestionCategory(category) {
    var idName = category.replaceAll(' ', '_');
    var suggestionDiv = document.querySelector('#suggestion-answers__' + idName);
    if (!suggestionDiv) {
      return;
    }

    suggestionDiv.classList.remove('is-hidden');
    suggestionDiv.classList.add('is-visible');

    // Move to top
    var parent = suggestionDiv.parentNode;
    if (parent) {
      suggestionDiv.parentNode.insertBefore(suggestionDiv, parent.firstChild);
    }
  }

  hideSuggestionCategory(category) {
    var idName = category.replaceAll(' ', '_');
    var suggestionDiv = document.querySelector('#suggestion-answers__' + idName);
    if (!suggestionDiv) {
      return;
    }

    suggestionDiv.classList.remove('is-visible');
    suggestionDiv.classList.add('is-hidden');
  }

  activateStepTwo() {
    document.querySelectorAll(".form-step__one").forEach(e => e.classList.add('is-hidden'));
    document.querySelectorAll(".form-step__one").forEach(e => e.classList.remove('is-visible'));

    document.querySelectorAll(".form-step__two").forEach(e => e.classList.remove('is-hidden'));
    document.querySelectorAll(".form-step__two").forEach(e => e.classList.add('is-visible'));

    // Set the category tags/buttons in step 2
    var categoriesSpan = document.getElementById("form-step__selected-categories");
    categoriesSpan.innerHTML = this.getSelectedCategoriesHTML();

    // Categories in step 2 function as a back button
    var selectedCategoryButtons = document.querySelectorAll('.selected_category');
    if(selectedCategoryButtons) {
      var thisRef = this;
      selectedCategoryButtons.forEach(function(e){
        e.addEventListener('click', thisRef.activateStepOne);
      });
    }
  }

  activateStepOne() {
    document.querySelectorAll(".form-step__two").forEach(e => e.classList.add('is-hidden'));
    document.querySelectorAll(".form-step__two").forEach(e => e.classList.remove('is-visible'));

    document.querySelectorAll(".form-step__one").forEach(e => e.classList.remove('is-hidden'));
    document.querySelectorAll(".form-step__one").forEach(e => e.classList.add('is-visible'));
  }

  getSelectedCategoriesHTML() {
    var htmlString = '';
    // Im not sure this is best practice :D
    if (this.selectedCategories.length > 0) {
      this.selectedCategories.forEach(e => (htmlString += `<span class="tag selected_category">${e}</span>`));
    }
    else {
      htmlString = '<span class="tag selected_category">een nieuwe categorie</span>';
    }
    return htmlString;
  }
}
