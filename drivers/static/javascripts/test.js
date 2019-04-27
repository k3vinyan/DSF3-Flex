var script = document.createElement("SCRIPT");
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js';
script.type = 'text/javascript';
document.getElementsByTagName("head")[0].appendChild(script);


setTimeout(function(){

  //JSON Form
  var rosterJSON = {};

  var rosterArray = [];

  $('#pageRosterViewContent').prepend(
    optionButton('dlRoster', 'Roster Download', '#FFFFFF', '#cc0000', '5px')
  );

  let node = $('body');
  let roster = $(node).find('#cspDATable > tbody')[1].children;

  for(let i = 0; i < roster.length; i++){
    let driver = $(roster[i], 'tr')[0].children;
    let driverId = $(driver[0]).text();
    let driverName = $(driver[1]).text();
    let driverCurrentStatus = $(driver[2]).text();
    let driverBlockTime = $(driver[4]).text();
    let driverStartTime = $(driver[5]).text();
    let driverEndTime = $(driver[6]).text();


    if(rosterJSON[driverId]){
      rosterJSON[driverId].block.push({"time":driverBlockTime, "startTime":driverStartTime, "endTime":driverEndTime});
    } else {
      rosterJSON[driverId] = {"driverName":driverName, "block":[{"time":driverBlockTime, "startTime":driverStartTime, "endTime":driverEndTime}]};
    }

    rosterArray.push({driverName:driverName, driverId:driverId, driverBlockTime:driverBlockTime, driverStartTime:driverStartTime, driverEndTime:driverEndTime})

  };


  // $.ajax({
  //   type: "POST",
  //   url: "http://localhost:8000/drivers/addDrivers/",
  //   data: JSON.stringify(rosterArray),
  //   success: function(data){
  //     console.log(data)
  //   },
  //   error: function(data){
  //     console.log("no")
  //   }
  // });

  //create button with additonal options
  function optionButton(id, value, color, bgColor, padding){
    var id = id;
    var value = value;
    var color = color;
    var bgColor = bgColor;
    var padding = padding;
    var string;

    string = "<input id='" + id + "' type='button' value='" + value +
    "' style='" +"color: " + color + "; " + "background-color:" + bgColor +
    "; " + "padding: " + padding + "; border-style: none;'></button>";

    return string;
  };

}, 3000);
