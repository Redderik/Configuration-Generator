    document.addEventListener('submit', function (event) {
    var zone = document.getElementById("Zone");
    var zoneval = zone.options[zone.selectedIndex].value;
  // if the zone field is Zone 1, we let the form submit

  if(zoneval!=="Zone 1") {
    // If it isn't, we display an appropriate error message
    alert("This zone template is not yet implemented.")
    // Then we prevent the form from being sent by canceling the event
    event.preventDefault();
  }
});

$(document).ready(function(){
    var maxField = 10; //Input fields increment limitation
    var addButton = $('.add_button'); //Add button selector
    var wrapper = $('.field_wrapper'); //Input field wrapper
    var x = 1; //Initial field counter is 1
    var fieldHTML= '<div><table><tr><label for="vlan_num[]">Vlan Number: &nbsp&nbsp</label><input type="text" id="vlan_num[]" name="vlan_num[]" value=""/></tr><tr>&nbsp&nbsp<label for="vlan_name[]">Vlan Name: &nbsp&nbsp</label><input type="text" id="vlan_name[]" name="vlan_name[]" value=""/>&nbsp&nbsp<a href="javascript:void(0);" class="remove_button"><img width="16" height="16" src="static/images/remove.png"/></a></tr></table></div>'; //New input field html


    //Once add button is clicked
    $(addButton).click(function(){
        //Check maximum number of input fields
        if(x < maxField){
         var fieldHTML= '<div><table><tr><label for="vlan_num[]">Vlan Number: &nbsp&nbsp</label><input type="text" id="vlan_num[]" name="vlan_num[]" value=""/></tr>&nbsp&nbsp<tr><label for="vlan_name[]">Vlan Name: &nbsp&nbsp</label><input type="text" id="vlan_name[]" name="vlan_name[]" value=""/>&nbsp&nbsp<a href="javascript:void(0);" class="remove_button"><img width="16" height="16" src="static/images/remove.png"/></a></tr></table></div>'; //New input field html

            x++; //Increment field counter
            $(wrapper).append(fieldHTML); //Add field html
        }
    });

    //Once remove button is clicked
    $(wrapper).on('click', '.remove_button', function(e){
        e.preventDefault();
        $(this).parent('div').remove(); //Remove field html
        x--; //Decrement field counter
    });
});