$(document).ready(function(){
  $('ul.tabs').tabs();
  $(".button-collapse").sideNav();

  setTimeout(function(){
   window.location.reload(1);
}, 60000 );
});
