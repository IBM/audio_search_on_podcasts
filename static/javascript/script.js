const uploading2 = document.getElementById("uploading2");
const error2 = document.getElementById("error2");
const uploaded2 = document.getElementById("uploaded2");
const audio = document.getElementById("audio");

$(document).ready(function() {

    uploaded2.style.display = "none";
    error2.style.display = "none";
    uploading2.style.display = "none";

});

function isEmpty(el) {
    return !$.trim(el.html())
}

$('#Upload').on('click', function() {
    uploading2.style.display = "block";
    if (isEmpty($('#myFiles'))) {
        uploading2.style.display = "none";
        error2.style.display = "block";
    } else {
        error2.style.display = "none";
        $.ajax({
            url: '/uploader',
            type: 'POST',
            data: new FormData($('form')[0]),
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            success: function(response) {
                var res = response.filepath.split("/");
                window.location = "/query/"+res[2];
                uploading2.style.display = "none";
                uploaded2.style.display = "block";
                audioPlayer = '<br/><a><video controls> <source src="' +
                    response.filepath + '" type="video/mp4"> Your browser does not support the audio element. </video></a>';

                audio.innerHTML = audioPlayer;
            },
            error: function() {
                error2.style.display = "block";
            }
        });
    }

});