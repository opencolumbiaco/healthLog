var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
    });
}

function menu() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}

var slider=document.getElementById("mood");
var emoji=document.getElementById("emoji");
var emoticons=["mood_bad", "sentiment_very_dissatisfied", 
    "sentiment_satisfied","sentiment_satisfied_alt",
    "sentiment_very_satisfied"
	];
slider.oninput=function(){
    emoji.innerHTML=emoticons[slider.value];
}
