// Add Javascript here
alert("js loaded");

// function login() {
// 	alert("starting login");
// 	var username = $("#loginEmailInput").val(); 
// 	var password = $("#loginPasswordInput").val();
// 	var url = "http://192.168.99.100/login";
// 	var auth = make_base_auth(username, password);

// 	$.ajax({
// 	    url : url,
// 	    method : 'GET',
// 	    beforeSend : function(req) {
// 	        req.setRequestHeader('Authorization', auth);
// 	    }
// 	});
// }

// function make_base_auth(user, password) {
//   var tok = user + ':' + pass;
//   var hash = Base64.encode(tok);
//   return "Basic " + hash;
// }

// function completeFunction() {
// 	alert("login request completed");
// }