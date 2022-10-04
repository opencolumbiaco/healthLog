var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "flex") {
        content.style.display = "none";
    } else {
        content.style.display = "flex";
        content.style.flexDirection = 'column';
    }
    });
}

function menu() {
    var x = document.getElementById("myLinks");
    if (x.style.display === "flex") {
        x.style.display = "none";
    } else {
        x.style.display = "flex";
        x.style.flexDirection = 'column';
    }
}
function auth() {
    var l = document.getElementById('login')
    var r = document.getElementById('reg')
    var t = document.getElementById('text')
    if (r.style.display === 'flex') {
        r.style.display = 'none'
        l.style.display = 'flex'
        l.style.flexDirection = 'column';
        t.innerHTML = 'Register'
    } else {
        l.style.display = 'none'
        r.style.display = 'flex'
        r.style.flexDirection = 'column';
        t.innerHTML = 'Login'
    }
}



$(document).ready(function(){
    $('#showMoods').click(function(){
        $('#hideMoods').animate( {
            width: 'toggle'
        })
    })
    $('#showMeds').click(function() {
        $('#hideMeds').animate( {
            width: 'toggle'
        })
    })
    $('#showSugars').click(function(){
        $('#hideSugars').animate( {
            width: 'toggle'
        })
    })
})