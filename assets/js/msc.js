// Instantiate MDC Drawer
if (document.querySelector(".mdc-text-field")) {
  document.querySelectorAll(".mdc-text-field").forEach(function (el) {
    new mdc.textField.MDCTextField(el);
  });
}

if (document.querySelector(".mdc-button")) {
  const buttonRipple = new mdc.ripple.MDCRipple(
    document.querySelector(".mdc-button")
  );
}

const opener = document.getElementById("mdc-drawer-opener");
const appBar = document.getElementById("app-bar");
if (opener) {
  const drawerEl = document.querySelector(".mdc-drawer");
  const drawer = new mdc.drawer.MDCDrawer.attachTo(drawerEl);
  opener.addEventListener("click", () => {
    if (drawer.open) {
      opener.innerText = "menu";
      drawer.open = false;
      setTimeout(function () {
        appBar.classList.remove("is-zindex-7");
      }, 1000);
    } else {
      opener.innerText = "close";
      drawer.open = true;
      appBar.classList.add("is-zindex-7");
    }
  });
}



const menuDrawers = document.getElementsByClassName("menu-button");

if (menuDrawers){
  Array.from(menuDrawers).forEach(function(menuDrawer) {
    menuDrawer.addEventListener('click', () => {
      const menu = new mdc.menu.MDCMenu(menuDrawer.parentElement.querySelector('.mdc-menu'));
      menu.open = true;

    });
  });
}

const msgBtns = document.getElementsByClassName("send_message");


if (msgBtns){
  Array.from(msgBtns).forEach(function(msgBtn) {
    msgBtn.addEventListener('click', () => {
      const dialog = new mdc.dialog.MDCDialog(msgBtn.closest('td').querySelector('.mdc-dialog'));
      dialog.open();
    });
  });
}


const axios = require('axios').default;

const reminderForms = document.getElementsByClassName('reminder_form');
if (reminderForms){
  Array.from(reminderForms).forEach(function(reminderForm) {
    reminderForm.addEventListener('submit', event => {
      event.preventDefault();
      let formData = new FormData(reminderForm);
      let action = reminderForm.action;
      const dialog = reminderForm.parentElement.closest('.mdc-dialog');

      const headers = {
        'X-CSRFToken': formData.get("csrfmiddlewaretoken")
      }

      axios.post(action, {
        questionnaire_id: formData.get("questionnaire_id"),
        msg: formData.get("msg"),
        selected_option: formData.get("selected_option"),
      }, { headers }).then(response => {
          data = response.data;
          dialog.classList.remove("mdc-dialog--open");
          if(data.status){
            alert("Email Sent successfully");
          } else {
            alert("There was some issue in sending emails. Please refresh and try again");
          }
      }).catch(error => {
        console.error('There was an error!', error);
      });
    });
  });
}

document.querySelectorAll('.parent_question input').forEach(item => {
  item.addEventListener('change', event => {
    checkForLogicImplementation(item);
  })
});

document.querySelectorAll('.parent_question select').forEach(item => {
  item.addEventListener('change', event => {
    checkForLogicImplementation(item);
  })
});

document.querySelectorAll('.parent_question textarea').forEach(item => {
  item.addEventListener('change', event => {
    checkForLogicImplementation(item);
  })
});

function checkForLogicImplementation (item){
  let parent = item.closest(".parent_question").parentElement;
  let itemVal = item.value;

  parent.querySelectorAll('.subquestion').forEach(subquestion => {
    var isLogicActive = subquestion.getAttribute('data-logic');

    if(isLogicActive === "True"){
      var showLogicWhen = subquestion.getAttribute('data-when');
      if(showLogicWhen === "any" ||  showLogicWhen === itemVal){
        subquestion.classList.remove("mdc-hide");
        subquestion.classList.add("mdc-show");
      } else {
          subquestion.classList.remove("mdc-show");
          subquestion.classList.add("mdc-hide");
      }
    }
  });
}