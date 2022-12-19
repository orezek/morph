
// progress bar setter - sets width to zero
function setWidth() {
    for (const x of skill_bar_elements) {
        document.getElementById(x).style.width = "0%"
    }
}

// moves the progress bar at rate to a limit
function move(element, limit) {
  document.getElementById(element).style.width = "0%"
  var i = 0;
  if (i == 0) {
    i = 1;
    var elem = document.getElementById(element);
    var width = 0;
    var id = setInterval(frame, 10);
    function frame() {
      if (width >= limit) {
        clearInterval(id);
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
      }
    }
  }
}

// progress bar id's to fill
const skill_bar_elements = ["AWS Cloud", "Windows Server", "Networking",
"Python", "HTML", "Linux", "Problem Solving", "VM Ware", "Veeam", "MS Sharepoint"];

// fills the progress bar for each skill list element
function skills(elements) {
// note "elements" parameter should be used in the "for" loop instead of "skill_bar_elements" parameter
    for (const x of skill_bar_elements) {
      if (x == "AWS Cloud") {
        const aws = 70;
        move(x, aws)
        console.log(move(x, aws), x)
      } else if (x == "Windows Server") {
        const windows = 80;
        move(x, windows)
        console.log(move(x, windows), x)
      } else if (x == "Networking") {
        const networking = 65;
        move(x, networking)
        console.log(move(x, networking), x)
      } else if (x == "Python") {
        const python = 60;
        move(x, python)
        console.log(move(x, python), x)
      } else if (x == "HTML") {
        const html = 55;
        move(x, html)
        console.log(move(x, html), x)
      } else if (x == "Linux") {
        const linux = 55;
        move(x, linux)
        console.log(move(x, linux), x)
      } else if (x == "Problem Solving") {
        const problem = 90;
        move(x, problem)
        console.log(move(x, problem), x)
      } else if (x == "VM Ware") {
        const skill = 63;
        move(x, skill)
        console.log(move(x, skill), x)
      } else if (x == "Veeam") {
        const skill = 40;
        move(x, skill)
        console.log(move(x, skill), x)
      } else if (x == "MS Sharepoint") {
        const skill = 60;
        move(x, skill)
        console.log(move(x, skill), x)
        }
    }
}

// run skill function on every page load
skills(skill_bar_elements)





