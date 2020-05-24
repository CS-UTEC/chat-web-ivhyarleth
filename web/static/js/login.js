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
      console.log("authenticate:)");
      alert("200");
    },
    data: JSON.stringify(credentials)
  });

}
