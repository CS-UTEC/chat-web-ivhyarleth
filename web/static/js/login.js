function login() {
  console.log("Login User");
  var username = $('#username').val();
  var password = $('#password').val();
  console.log("Data",username,password);
  var credentials ={
    'username':username,
    'password':password
  };
  $.post({
    url: '/authenticate',
    type: 'post',
    dataType: 'json',
    contentType: 'application/json',
    success: function(data){
      if (data['message'] == 'ok'){
        alert("authenticate:)");
        window.location="/static/html/chat.html";
      }
      else {
        alert("incorrecto");
      }
    },
    data: JSON.stringify(credentials)
  });

}
