// Add smooth scrolling to all links in navbar + footer link
$(document).ready(function(){
    $(".navbar a, footer a[href='#myPage'], #home a[href='#python']").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {

        // Prevent default anchor click behavior
        event.preventDefault();

        // Store hash
        var hash = this.hash;

        // Using jQuery's animate() method to add smooth page scroll
        // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
        $('html, body').animate({
                scrollTop: $(hash).offset().top
                }, 900, function(){

                // Add hash (#) to URL when done scrolling (default click behavior)
                window.location.hash = hash;
            });
        } // End if
    });
    $("#todayDate").html( retDate() );
    $("#billDate").html( billDate(3));
})

// for collapsing navbar on small screen after clicking on a link
// $(document).ready(function() {
//     $("body").click(function(event) {
//             // only do this if navigation is visible, otherwise you see jump in navigation while collapse() is called
//              if ($(".navbar-collapse").is(":visible") && $(".navbar-toggle").is(":visible") ) {
//                 $('.navbar-collapse').collapse('toggle');
//             }
//       });
// });

// add sliding effect
$(window).scroll(function() {
    $(".slideanim").each(function(){
        var pos = $(this).offset().top;

        var winTop = $(window).scrollTop();
        if (pos < winTop + 600) {
            $(this).addClass("slide");
        }
    });
});

function retDate() {
    let d = new Date();
    let weekDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
    let monthNames= [ "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];
    return(weekDays[d.getDay() - 1] + ", " + monthNames[d.getMonth() - 1] + " " + d.getDate());
}

function billDate(i) {
    let d = new Date();
    let weekDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
    let monthNames= [ "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];
    return(weekDays[(d.getDay() + i - 1)%7] + ", " + monthNames[d.getMonth()] + " " + (d.getDate() + (i%30)));
}

