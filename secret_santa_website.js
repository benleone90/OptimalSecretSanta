var size_init = 3;

$(document).ready(function() {
  for (var i = 1; i < size_init + 1; i++) {
    var name_input = $('<input type="text"><br/>');
    name_input.attr("name", "member");
    name_input.attr("placeholder", "Enter Member " + i + "'s Name");
    $("#group-entry").append(name_input);

    var email_input = $('<input type="text"><br/><br/>');
    email_input.attr("name", "email");
    email_input.attr("placeholder", "Enter Member " + i + "'s Email");
    $("#group-entry").append(email_input);
    // $("input").addClass("member");
  }

  $("#add-more").click(function() {
    size_init++;
    var name_input = $('<input type="text"><br/>');
    name_input.attr("name", "member");
    name_input.attr("placeholder", "Enter Member " + size_init + "'s Name");
    $("#group-entry").append(name_input);

    var email_input = $('<input type="text"><br/><br/>');
    email_input.attr("name", "email");
    email_input.attr("placeholder", "Enter Member " + size_init + "'s Email");
    $("#group-entry").append(email_input);
    //$("input").addClass("member");
  });
});