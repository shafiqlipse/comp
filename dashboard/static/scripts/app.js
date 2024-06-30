// const Theme = document.querySelector(".theme-toggler");

// const Theme = document.querySelector(".theme-toggler");
const icon = document.getElementById("iconed");
const wrapper = document.querySelector(".dashboard-wrapper");

const Toggletheme = () => {
  const isLightTheme = wrapper.classList.contains("light");

  if (isLightTheme) {
    icon.innerHTML = '<i class="fa fa-moon"></i>';
    wrapper.classList.remove("light");
    wrapper.classList.add("dark");
    localStorage.setItem("theme", "dark");
  } else {
    icon.innerHTML = '<i class="fa fa-sun"></i>';
    wrapper.classList.remove("dark");
    wrapper.classList.add("light");
    localStorage.setItem("theme", "light");
  }
};

// Check the theme in local storage when the page is loaded
document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem("theme");

  // If there's a saved theme, apply it
  if (savedTheme === "dark") {
    icon.innerHTML = '<i class="fa fa-sun"></i>';

    wrapper.classList.remove("light");
    icon.innerHTML = '<i class="fa fa-sun"></i>';

    wrapper.classList.add("dark");
  } else {
    icon.innerHTML = '<i class="fa fa-sun"></i>';

    wrapper.classList.remove("dark");
    icon.innerHTML = '<i class="fa fa-sun"></i>';

    wrapper.classList.add("light");
  }
});

// toggle menu avvount
// toggle menu avvount
const account = document.querySelector(".account-toggle");

const ToggleAccount = () => {
  if (account.classList.contains("account-off")) {
    account.classList.remove("account-off");
    account.classList.add("account-on");
  } else {
    account.classList.add("account-off");
    account.classList.remove("account-on");
  }
  console.log(account.classList);
  // When the user clicks anywhere outside of the modal, close it
};

// Event delegation to add "account-off" when clicking outside the account element
// document.addEventListener("click", (event) => {
//   if (!event.target.closest(".account-toggle")) {
//     ToggleAccount();
//   }accordion for sidebar
const accordionItems = document.querySelectorAll(".item-head");

for (const item of accordionItems) {
  item.addEventListener("click", () => {
    const answer = item.nextElementSibling;
    // const tog = document.querySelector(".tog");
    if (answer.classList.contains("menu-on")) {
      answer.classList.remove("menu-on");
      answer.classList.add("menu-off");
    } else {
      answer.classList.add("menu-on");
      answer.classList.remove("menu-off");
    }
  });
}

// });

function displayImage(input) {
  var reader = new FileReader();
  reader.onload = function (e) {
    document.getElementById("image-preview").src = e.target.result;
  };
  reader.readAsDataURL(input.files[0]);
}

//.tabs for profiles

const tabsContainer = document.querySelector(".tabs-container");
const tabButtons = tabsContainer.querySelectorAll(".tab");
const tabPanels = Array.from(tabsContainer.querySelectorAll(".tabpanel"));

function tabClickHandler(e) {
  const { id } = e.currentTarget;

  // Hide all panels
  tabPanels.forEach((panel) => {
    panel.hidden = true;
  });

  // Deselect all tab buttons
  tabButtons.forEach((button) => {
    button.setAttribute("aria-selected", "false");
  });

  // Mark the selected tab button
  e.currentTarget.setAttribute("aria-selected", "true");

  // Show the corresponding panel
  const currentTab = tabPanels.find(
    (panel) => panel.getAttribute("aria-labelledby") === id
  );
  currentTab.hidden = false;
}

tabButtons.forEach((button) => {
  button.addEventListener("click", tabClickHandler);
});

// controls modal
// // Get the modal
// const modal = document.getElementById("contoggle");

// // Get the button that opens the modal
// const btn = document.getElementById("cwontrols");

// // Get the <span> element that closes the modal
// const span = document.getElementsByClassName("close")[0];

// // When the user clicks on the button, open the modal
// btn.onclick = function () {
//   modal.style.display = "block";
// };

// // When the user clicks on <span> (x), close the modal
// span.onclick = function () {
//   modal.style.display = "none";
// };

// // When the user clicks anywhere outside of the modal, close it
// window.onclick = function (event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// };
