
$(document).ready(function() {

	$("#search-form-master").submit(function(event) {
		var tempo_input = $("#tempo-search-bar").val();
		if (isNaN(tempo_input)) {
		    window.alert("Tempo must be a number.");
    		return;	
		}

		document.getElementById("myGrid").remove();
		var grid_element = $("<div id='myGrid' style='height: 600px;width:auto;' class='ag-theme-balham'>");
		$("#search-results").append(grid_element);

		var tempo = $("#tempo-search-bar").val();
		var key = $("#key-list").val();
		var mode = $("#mode-list").val();
		var time_signature = $("#time-sig-list").val();

		// Create empty array
		var array = [];

		// Create JSON object with property "genre_label"
		var json_object = {};

		if (tempo.length !== 0) {
			json_object['tempo'] = tempo;
		}

		if (key != null) {
			json_object['key'] = key;
		}	

		if (mode != null) {
			json_object['mode'] = mode;
		}				

		if (time_signature != null) {
			json_object['time_signature'] = time_signature;
		}	

		// var json_object = {
		// 	tempo: tempo,
		// 	key: key,
		// 	mode: mode,
		// 	time_signature: time_signature
		// }

		// Add object to array
		array.push(json_object);

		// Encode JSON string
		var json_string = JSON.stringify(array);

		var json = $.get("/attribute_search", json_object, function(json) {parse(json);});
	});

	$("#song-search-form-master").submit(function(event) {
		var song_input = document.getElementById("song-search-bar").value; 
		if (song_input.length == 0)
    	{
    		window.alert("You must input a song title.");
    		return;
    	}

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
    		onSelectionChanged: onSelectionChanged,
    		 onGridReady: function(params) {
        params.api.sizeColumnsToFit();
    }
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
    	   //console.log(selectedRowsString);
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

		{headerName: "Album Art", field: "album_art", suppressSizeToFit: true, cellRenderer: function(params) {
      return '<img src="'+ params.value + '" height="200" width="200">'
  }, autoHeight:true},
  		
  		{headerName: "Song Preview", field: "preview_url", suppressSizeToFit: true, cellRenderer: function(params) {
      return '<audio id="player" controls="false" name="media"><source src="'+ params.value +'" type="audio/mpeg"></audio>'
  }, autoHeight:true},

		{headerName: "Song", field: "name"},
		{headerName: "Artist Name", field: "artist_name"},
		{headerName: "Tempo", field: "tempo", headerTooltip: "The speed or pace of a given piece. Measured in beats per minute (BPM)."},
		{headerName: "Key", field: "key", headerTooltip: "The group of pitches, or scale, that forms the basis of a musical composition."},
		{headerName: "Time Signature", field: "time_signature", headerTooltip: "The number of beats contained in each measure (bar)."},
		{headerName: "Acousticness", field: "acousticness", headerTooltip: "A confidence measure from 0 to 100 of whether the track is acoustic.", cellStyle: function(params) {
			if (params.value > 0 && params.value < 0.33) {
				return {color: 'red', backgroundColor: 'green'};
			}
		}
	},

		{headerName: "Danceability", field: "danceability", headerTooltip: "Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity."},
		{headerName: "Energy", field: "energy", headerTooltip: "A measure from 0 to 100 that represents a perceptual measure of intensity and activity."},
		{headerName: "Instrumentalness", field: "instrumentalness", headerTooltip: "Predicts whether a track contains no vocals. Confidence is higher as the value approaches 100."},
		{headerName: "Liveness", field: "liveness", headerTooltip: "Detects the presence of an audience in the recording. A value above 80 provides strong likelihood that the track is live."},
		{headerName: "Loudness", field: "loudness", headerTooltip: "The overall loudness of a track in decibels (dB). Values typical range between -60 and 0 db."},
		{headerName: "Speechiness", field: "speechiness", headerTooltip: "Detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 100 the attribute value."},
		{headerName: "Positivity", field: "valence", headerTooltip: "A measure from 0 to 100 describing the musical positiveness conveyed by a track. Tracks with high positivity sound more cheerful or euphoric, while tracks with low positivity sound more sad, depressed, or angry."},
		{headerName: "Length (ms)", field: "duration_ms"}

	    ];

	    // let the grid know which columns and what data to use
    	var gridOptions = {
    		columnDefs: columnDefs,
    		enableSorting: true,
    		enableFilter: true,
    		 onGridReady: function(params) {
        // params.api.sizeColumnsToFit();
    }
    	};

		// lookup the container we want the Grid to use
		var eGridDiv = document.querySelector('#myGrid');
	

		// create the grid passing in the div to use together with the columns & data we want to use
		new agGrid.Grid(eGridDiv, gridOptions);
		gridOptions.api.setRowData(json["data"]["results"]);
		gridOptions.rowHeight = 600;
	}

});
