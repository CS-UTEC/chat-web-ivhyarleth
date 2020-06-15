function get_current(){
  console.log("Traer usuario logueado");
  $.getJSON("/current",function(data){
    console.log(data['username']);
    var div = '<div class="row userbox text-info mt-3 p-3 text-center">username</div>';
    div = div.replace('username', data['username']);
    $('#contacts').append(div);
    get_users(data['id']);
    });
}

function get_users(user_from) {
  $.getJSON("/users", function(data){
    let i = 0;
    $.each(data, function(){
    if (data[i]['id']!=user_from){
      var div = '<div class="row text-success p-3 mt-3 text-center userbox" id="div_id" onclick="getMessages(\'user_to\',\'user_from\')">username</div>';
      div = div.replace("username", data[i]['username']);
      div = div.replace("user_to", data[i]['id']);
      div = div.replace("user_from", user_from);
      div = div.replace("div_id", data[i]['username'].replace(".",""));
      //div = div.replace("div_id", data[i]['id']);
      $('#contacts').append(div);
    }
      i = i+1;
    })
  });
}

function saludar(name){
  alert("holaa " + name);
}

function getMessages(user_to,user_from){
  $('#chat').empty();
  console.log(user_to,user_from);
  $.getJSON('/messages/' + user_from + "/" + user_to, function(data){
    let i=0;
    $.each(data, function(){
      let div;
      if(data[i]['user_from_id']==user_from){
        div = '<div class="row"><div class="col-3 offset-9 text-primary shadow p-1 mb-1 bg-white rounded">Content</div></div>';
      }else{
        div = '<div class="row"><div class="col-3 text-success shadow p-1 mb-1 bg-white rounded">Content</div></div>';
      }
      div = div.replace("Content", data[i]['content']);
      $('#chat').append(div);
      i = i + 1;
    })
  });
  $('#botonMensaje').attr('onclick', 'sendMessages(' + user_to + ', ' + user_from + ')');
}

function sendMessages(user_to,user_from){
  var content = $('#textContent').val();
   $('#textContent').val("");
  var message = JSON.stringify({
      'content':content,
      'user_from_id':user_from,
      'user_to_id':user_to
  });
  $.ajax({
      url : '/sendMessages',
      type : 'POST',
      dataType : 'json',
      contentType : 'application/json',
      data : message,
      async : false
  });
  getMessages(user_to, user_from)
}


  /*  var content = $('#content').val();
    var message = JSON.stringify({
        'content':content,
        'user_from_id':user_from_id,
        'user_to_id':user_to_id
    });
    $.post({
        url : '/messages/chat',
        type : 'POST',
        dataType : 'json',
        contentType : 'application/json',
        data : message
    });
    get_messages(user_to, user_from)}*/

function logout(){
  $.getJSON('logout', function(data){
    alert(data['msg']);
  });
  window.location="/static/html/login.html";
}

function lookup(){
  //console.log($('#search').val());
  let value = $('#search').val();
  let parent = $('#contacts');
  let hijos = parent.children();
  for (var i = 1; i < hijos.length; i++){
    var id = '#' + hijos[i].id;
    if(hijos[i].id.startsWith(value)){
      $(id).removeClass('d-none');
      $(id).addClass('d-block');
    }else {
      $(id).removeClass('d-block');
      $(id).addClass('d-none');
    }
  }

}
