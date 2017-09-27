//attach auth header for every request.
// $.ajaxSetup({
//     beforeSend: function (xhr)
//     {
//      var authToken = getCookie("authToken");
//      if (authToken) {
//          xhr.setRequestHeader("Authorization","Token " + authToken);
//      }
//     }
// });

//function that is called when trying to login
function login() {
    var username = $("#loginEmailInput").val();
    var password = $("#loginPasswordInput").val();
    var loginUrl = "http://" + document.domain + "/login";
    var auth = make_base_auth(username, password);

    var request = new XMLHttpRequest();
    request.open("GET", loginUrl, false);
    request.setRequestHeader("Authorization", auth);
    request.send();

    token = JSON.parse(request.response)["token"];

    bake_cookie("authToken", token, 99);
    authCookie = read_cookie("authToken");

    return false
}

function make_base_auth(user, password) {
    var tok = user + ':' + password;
    var hash = btoa(tok);
    return "Basic " + hash;
}

var bake_cookie = function(name, value, days) {
    var expires;
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    }
    else {
        expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function read_cookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) {
                c_end = document.cookie.length;
            }
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}