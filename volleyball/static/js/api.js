function get_fixteams() {
  var team_select = document.getElementById("id_team");
  //   var official_select = document.getElementById("id_officials");

  // Show loading indicators for teams and officials
  team_select.innerHTML = "<p>Loading teams...</p>";
  //   official_select.innerHTML = "<p>Loading officials...</p>";



  // Fetch teams
  fetch("/get_fixteams/")
    .then((response) => response.json())
    .then((data) => {
      // Hide the loading indicator for teams
      console.log(data);
      // Hide the loading indicator for teams
      team_select.innerHTML = "Team";

      // Update the 'team' checkbox list with the fetched data
      if (data.team.length === 0) {
        team_select.innerHTML = "<p>No teams found.</p>";
      } else {
        data.teams.forEach((team) => {
          var div = document.createElement("div");
          var label = document.createElement("label");
          var input = document.createElement("input");
          input.type = "checkbox";
          input.value = team.id;
          input.name = "teams"; // Ensure this is the correct name
          label.innerText = team.fname;
          div.appendChild(input);
          div.appendChild(label);
          team_select.appendChild(div);
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching teams:", error);
      team_select.innerHTML =
        "<p>Error fetching teams. Please try again.</p>";
    });

  // Fetch officials
}

