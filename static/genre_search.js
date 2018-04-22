
$(document).ready(function() {

	$("#search-form-master").submit(function(event) {
		document.getElementById("myGrid").remove();
		var grid_element = $("<div id='myGrid' style='height: 600px;width:100%;' class='ag-theme-balham'>");
		$("#search-results").append(grid_element);

		var tempo = $("#tempo-search-bar").val();
		var key = $("#key-list").val();
		var time_signature = $("#time-sig-list").val();

		// Create empty array
		var array = [];

		// Create JSON object with property "genre_label"
		var json_object = {
			tempo: tempo,
			key: key,
			time_signature: time_signature
		}

		// Add object to array
		array.push(json_object);

		// Encode JSON string
		var json_string = JSON.stringify(array);

		var json = $.get("/attribute_search", json_object, function(json) {parse(json);});
	});

	function parse(json)
	{
		// specify the columns
		var columnDefs = [
		{headerName: "Album Art", field: "album_art", cellRenderer: function(params) {
      return '<img src="'+ params.value + '" height="200" width="200">'
  }, autoHeight:true},
		{headerName: "Song", field: "name"},
		{headerName: "Artist Name", field: "artist_name"},
		{headerName: "Tempo", field: "tempo"},
		{headerName: "Key", field: "key"},
		{headerName: "Time Signature", field: "time_signature"},
		{headerName: "Acousticness", field: "acousticness"},
		{headerName: "Danceability", field: "danceability"},
		{headerName: "Energy", field: "energy"},
		{headerName: "Instrumentalness", field: "instrumentalness"},
		{headerName: "Liveness", field: "liveness"},
		{headerName: "Loudness", field: "loudness"},
		{headerName: "Speechiness", field: "speechiness"},
		{headerName: "Happiness", field: "valence"},
		{headerName: "Length (ms)", field: "duration_ms"}

	    ];

	    // let the grid know which columns and what data to use
    	var gridOptions = {
    		columnDefs: columnDefs,
    		enableSorting: true,
    		enableFilter: true,
    	};

		// lookup the container we want the Grid to use
		var eGridDiv = document.querySelector('#myGrid');
	

		// create the grid passing in the div to use together with the columns & data we want to use
		new agGrid.Grid(eGridDiv, gridOptions);
		gridOptions.api.setRowData(json["results"]);
		gridOptions.rowHeight = 600;
	}

});
