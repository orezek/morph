// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()


document.getElementById('no_guests').addEventListener('change', function() {
    var value = this.value;
    var guestFields = document.getElementById('guestFields');
    guestFields.innerHTML = '';
    var fields = '';
    for (var i = 2; i <= value; i++) {
        guestFields.innerHTML += '<div class="row field"><h3>Guest No. '+ i +'</h3><div class="col-md-4"><label for="title' + i + '">Title:</label><select class="form-control" id="title' + i + '" name="title' + i + '"><option value="mr">Mr</option><option value="mrs">Mrs</option><option value="ms">Ms</option><option value="mas">Master</option><option value="miss">Miss</option></select></div><div class="col-md-4"><label for="guest_ame' + i + '">Guest Name</label><input class="form-control" type="text" id="guest_name' + i + '" name="guest_name' + i + '" placeholder="First name" required></div><div class="col-md-4"><label for="guest_surname' + i + '">Guest Surname</label><input class="form-control" type="text" id="guest_surname' + i + '" name="guest_surname' + i + '" placeholder="Last name" required ></div></div><div class="row field"><div class="col-md-6"><div class="form-group"><label for="email' + i + '">Email</label><input class="form-control" type="email" id="email' + i + '" name="email' + i + '" placeholder="Please enter your email" required ></div></div><div class="col-md-6"><div class="form-group"><label for="tel' + i + '">Phone Number</label><input class="form-control" type="tel" id="tel' + i + '" name="tel' + i + '" placeholder="Enter your phone number" required ></div></div></div>';
    }
    console.log(guestFields)
});