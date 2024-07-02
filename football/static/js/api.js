// get teams for a specific sport age and gender
function get_fteams() {
  var gender_select = document.getElementById("id_gender");
  var age_select = document.getElementById("id_age");
  var sport_select = document.getElementById("id_sport");
  var team_select = document.getElementById("id_teams");

  var gender = gender_select.value;
  var sport = sport_select.value;
  var age = age_select.value;

  const url = `/get_fteams/?sport=${sport}&gender=${gender}&age=${age}`;
  console.log("Fetching URL:", url);

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log("Received data:", data);
      team_select.innerHTML = "Athletes";

      if (data.teams.length === 0) {
        team_select.innerHTML = "<p>No teams found.</p>";
      } else {
        data.teams.forEach((team) => {
          var div = document.createElement("div");
          var label = document.createElement("label");
          var input = document.createElement("input");
          input.type = "checkbox";
          input.value = team.id;
          input.name = "teams";
          label.innerText = team.school_name;
          div.appendChild(input);
          div.appendChild(label);
          team_select.appendChild(div);
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching teams:", error);
      team_select.innerHTML = "<p>Error fetching teams. Please try again.</p>";
    });
}

function get_gteams() {
  var gender_select = document.getElementById("id_gender");
  var age_select = document.getElementById("id_age");
  var sport_select = document.getElementById("id_sport");
  var team_select = document.getElementById("id_teams");

  var gender = gender_select.value;
  var sport = sport_select.value;
  var age = age_select.value;

  const url = `/get_fteams/?sport=${sport}&gender=${gender}&age=${age}`;
  console.log("Fetching URL:", url);

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      //console.log("Received data:", data);
      team_select.innerHTML = "Athletes";

      if (data.teams.length === 0) {
        team_select.innerHTML = "<p>No teams found.</p>";
      } else {
        data.teams.forEach((team) => {
          var div = document.createElement("div");
          var label = document.createElement("label");
          var input = document.createElement("input");
          input.type = "checkbox";
          input.value = team.id;
          input.name = "teams";
          label.innerText = team.school_name;
          div.appendChild(input);
          div.appendChild(label);
          team_select.appendChild(div);
        });
      }
    })
    .catch((error) => {
      // console.error("Error fetching teams:", error);
      team_select.innerHTML = "<p>Error fetching teams. Please try again.</p>";
    });
}

// Attach the get_teams function to the onchange events of the sport, gender, and age elements
// document.getElementById("id_sport").onchange = get_teams;
document.getElementById("id_sport").onchange = get_fteams;
document.getElementById("id_gender").onchange = get_fteams;
document.getElementById("id_age").onchange = get_fteams;

// Attach the get_teams function to the onchange events of the sport, gender, and age elements
// document.getElementById("id_sport").onchange = get_teams;


