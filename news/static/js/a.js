function displayImage(input) {
  var reader = new FileReader();
  reader.onload = function (e) {
    document.getElementById("image-preview").src = e.target.result;
  };
  reader.readAsDataURL(input.files[0]);
}
