$(function() {
    $("#Queform").submit(function() {
        $("#searchloader").addClass("linear-activity");
        $("#automplete-1").blur();
    });
    setTimeout(function() {
        $("#anim").html("Hear the answer");
        $('#anim').addClass("anima");
    }, 3000);
    setTimeout(function() {
        $("#anim").fadeOut();
    }, 10000);
    //Email
    $('#askq').click(function() {
        $.ajax({
            url: '/askquestion',
            type: 'GET',
            data: { 'phnumber': $('#ph').val(), 'mailaddress': $('#mailid').val(), 'mes': $('#mes').val() },
            success: function(response) {
                alert("Thank you for contacting us we will get back to you shortly");
            },
            error: function(response) { alert("Something went wrong,Please try after some time"); }
        });
    });
    //save suggested answer to file
    $('#suggestanswer').click(function() {
        $.ajax({
            url: '/saveans',
            type: 'GET',
            data: { 'question': $('#accurate').html(), 'answer': $('#suganswer').val() },
            success: function(response) {
                if (response.content.result < 0) {
                    alert("Enter data");
                } else {
                    alert("Thanks for your response");
                }
            },
            error: function(response) { alert("Something went wrong,Please try after some time"); }
        });
    });
    //load suggestion words
    setTimeout(function() { $("#automplete-1").focus(); }, 3000);
    var words_arr = [];
    $('#spi').addClass("spinner");
    $.ajax({
        url: '/getwords',
        type: 'GET',
        success: function(response) {
            var arr = response.content.result;
            i = -1;
            while (++i < arr.length) {
                words_arr.push(arr[i]);
            }
        },
        error: function(response) {}
    }).always(function() {
        setTimeout(function() { $('#spi').removeClass("spinner"); }, 2000);
    });
    $("#automplete-1").autocomplete({
        maxResults: 10,
        minLength: 3,
        multiple: true,
        multipleSeparator: " ",
        source: words_arr
    });
    $.ui.autocomplete.filter = function(array, term) {
        var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(term), "i");
        return $.grep(array, function(value) {
            return matcher.test(value.label || value.value || value);
        });
    };
    //text to speech
    $('#soundbutton').click(function() {
        $("#anim").fadeOut();
        $('#soundbutton').addClass("SoundPluse");
        $('#soundbutton').css("pointer-events", "none");
        $.ajax({
                url: '/playsnd',
                type: 'GET',
                success: function(response) {},
                error: function() { alert("Something went wrong,Please try after some time"); }
            })
            .always(function(jqXHROrData, textStatus, jqXHROrErrorThrown) {
                $('#soundbutton').removeClass("SoundPluse");
                $('#soundbutton').css("pointer-events", "");
            });
    });
    //speech to text
    $('#mic').click(function() {
        $("#automplete-1").val("Listening...");
        $("#automplete-1").css("pointer-events", "none");
        $('#mic').addClass("Rec");
        $.ajax({
            url: '/openmic',
            type: 'GET',
            success: function(response) {
                if (response.content.result === "NO") {
                    alert("Please check your microphone and audio levels");
                    $("#automplete-1").val("");
                } else {
                    var query = response.content.result;
                    query = query.toLowerCase();
                    $("#automplete-1").val(query);
                    setTimeout(function() { $("#Queform").trigger("submit"); }, 1000);
                }
            },
            error: function() {
                $("#automplete-1").val("");
                alert("please check your microphone and audio levels");
            }
        }).always(function() {
            $('#mic').removeClass("Rec");
            $("#automplete-1").css("pointer-events", "");
        });
    });
});