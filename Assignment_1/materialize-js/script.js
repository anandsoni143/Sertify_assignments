$(document).ready(function(){
 
    $('.myreview').carousel({
        numVisible:7,
        shift:55,
        padding: 55,
    });
});

function toggleModal(){
    var instance = M.Modal.getInstance($('#modal3'));
    instance.open();
}




// search
