
$(document).ready(function() {

	$("#search-form-master").submit(function(event) {
		document.getElementById("myGrid").remove();
		var grid_element = $("<div id='myGrid' style='height: 600px;width:auto;' class='ag-theme-balham'>");
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

	$("#song-search-form-master").submit(function(event) {
		document.getElementById("myGrid").remove();
		var grid_element = $("<div id='myGrid' class='ag-theme-balham'>");
		$("#search-results").append(grid_element);

		var track_name = $("#song-search-bar").val();

		// Create JSON object with property "genre_label"
		var json_object = {
			track_name: track_name,
		}

		// Encode JSON string
		var json_string = JSON.stringify(json_object);

		var json = $.get("/track_search", json_object, function(json) {parse_song(json);});
		//console.log(json);
	});

	function parse_song(json) 
	{
		// specify the columns
		var columnDefs = [
		{headerName: "Album Art", field: "album_art", cellRenderer: function(params) {
      return '<img src="'+ params.value + '" height="200" width="200">'
  }, autoHeight:true},
		{headerName: "Song", field: "name"},
		{headerName: "Artist Name", field: "artist_name"},
		{headerName: "Album", field: "album_name"},
		{headerName: "Song ID", field: "id", hide:true}
		];

		// let the grid know which columns and what data to use
    	var gridOptions = {
    		columnDefs: columnDefs,
    		enableSorting: true,
    		enableFilter: true,
    		rowSelection: 'single',
    		onSelectionChanged: onSelectionChanged
    	};

    	// lookup the container we want the Grid to use
		var eGridDiv = document.querySelector('#myGrid');

		// create the grid passing in the div to use together with the columns & data we want to use
		new agGrid.Grid(eGridDiv, gridOptions);
		gridOptions.api.setRowData(json["data"]);
		gridOptions.rowHeight = 600;

		var selectedRows = gridOptions.api.getSelectedRows();

    	function onSelectionChanged() {
    	    var selectedRows = gridOptions.api.getSelectedRows();
    	    var selectedRowsString = '';
    	    selectedRows.forEach( function(selectedRow, index) {
    	        if (index!==0) {
    	            selectedRowsString += ', ';
    	        }
    	        selectedRowsString += selectedRow.id;
    	    });
    	   
    	   // Create JSON object with property "genre_label"
    	   console.log(selectedRowsString);
    	   var json_object = {
    	   track_id: selectedRowsString
    	}

    		document.getElementById("myGrid").remove();
			var grid_element = $("<div id='myGrid' class='ag-theme-balham' style='margin: auto; height: 600px; width: 100%;'>");
			$("#search-results").append(grid_element);

    	   // Encode JSON string
    	   var json_string = JSON.stringify(json_object);

    	   var json = $.get("/id_search", json_object, function(json) {parse(json);});
		}
	}


	function parse(json)
	{
		// specify the columns
		var columnDefs = [

		{headerName: "Album Art", field: "album_art", cellRenderer: function(params) {
      return '<img src="'+ params.value + '" height="200" width="200">'
  }, autoHeight:true},
  		
  		{headerName: "Preview Song", field: "preview_url", cellRenderer: function(params) {
      return '<audio id="player" controls="false" name="media"><source src="'+ params.value +'" type="audio/mpeg"></audio>'
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
		gridOptions.api.setRowData(json["data"]["results"]);
		gridOptions.rowHeight = 600;
	}

});
