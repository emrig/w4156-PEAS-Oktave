
$(document).ready(function() {

	$(".loader").hide();

	$("#search-form-master").submit(function(event) {

		$('html,body').animate({
			scrollTop: $("#search-results").offset().top},
			'slow');

		if ($('#song-search-features-row').length) {
			document.getElementById("song-search-features-row").remove();
		}

		var tempo = $("#tempo-search-bar").val();
		var key = $("#key-list").val();
		var mode = $("#mode-list").val();
		var time_signature = $("#time-sig-list").val();

		if (!key && !mode && !time_signature && (tempo.length == 0)) {
			window.alert("You must input at least one musical characteristic.");
			return;
		}

		if (isNaN(tempo)) {
		    window.alert("Tempo must be a number.");
    		return;	
		}

		document.getElementById("myGrid").remove();
		$(".loader").show();

		var grid_element = $("<div id='myGrid' style='height: 600px;width:auto;' class='ag-theme-balham'>");
		$("#search-results").append(grid_element);

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

		$('html,body').animate({
			scrollTop: $("#search-results").offset().top},
			'slow');

		if ($('#song-search-features-row').length) {
			document.getElementById("song-search-features-row").remove();

		}

		var song_input = document.getElementById("song-search-bar").value; 
		if (song_input.length == 0)
    	{
    		window.alert("You must input a song title.");
    		return;
    	}

		document.getElementById("myGrid").remove();
    	$(".loader").show();

		var grid_element = $("<div id='myGrid' style='height: 600px;width:800px;' class='ag-theme-balham'>");
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
		{headerName: "Album Art", field: "album_art", suppressSizeToFit: true, width: 220, cellRenderer: function(params) {
      return '<img src="'+ params.value + '" height="200" width="200">'
  }, autoHeight:true},
  	
		{headerName: "Song", field: "name", suppressSizeToFit: true, width: 200, cellStyle: {'white-space': 'normal'}},
		{headerName: "Artist Name", field: "artist_name", suppressSizeToFit: true, width: 200, cellStyle: {'white-space': 'normal'}},
		{headerName: "Album", field: "album_name", suppressSizeToFit: true, width: 200, cellStyle: {'white-space': 'normal'}},
		{headerName: "Song ID", field: "id", hide:true}
		];

		// let the grid know which columns and what data to use
    	var gridOptions = {
    		columnDefs: columnDefs,
    		enableSorting: true,
    		enableFilter: true,
    		rowSelection: 'single',
    		overlayLoadingTemplate: '<span class="ag-overlay-loading-center">Please wait while your rows are loading</span>',
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
			var grid_element = $("<div id='myGrid' class='ag-theme-balham' style='margin: auto; height: 600px; width: 100%; margin-top: -120px;'>");
			$("#search-results").append(grid_element);

    	   // Encode JSON string
    	   var json_string = JSON.stringify(json_object);

    	   var json = $.get("/id_search", json_object, function(json) {parse(json);});
		}
	}

	function parse(json)
	{

		if ( (json["data"]["search_song_features"]) !== null) {
			var name = json["data"]["search_song_features"].name;
			var artist_name = json["data"]["search_song_features"].artist_name;
			var tempo = json["data"]["search_song_features"].tempo;
			var key = json["data"]["search_song_features"].key;
			var time_signature = json["data"]["search_song_features"].time_signature;

			var new_row = $("<div class='row' id='song-search-features-row'>");

			var col1 = $("<div class='col-xs-2'>");
			$(col1).text("Selected song:");
			
			var col2 = $("<div class='col-xs-2'>");
			$(col2).text("Song: " + name);

			var col3 = $("<div class='col-xs-2'>");
			$(col3).text("Artist: " + artist_name);

			var col4 = $("<div class='col-xs-2'>");
			$(col4).text("Tempo: " + tempo);			

			var col5 = $("<div class='col-xs-2'>");
			$(col5).text("Key: " + key);	

			var col6 = $("<div class='col-xs-2'>");
			$(col6).text("Time Signature: " + time_signature);	

			$(new_row).append(col1);
			$(new_row).append(col2);
			$(new_row).append(col3);
			$(new_row).append(col4);
			$(new_row).append(col5);
			$(new_row).append(col6);
			$("#song-search-features").append(new_row);
		}

		// specify the columns
		var columnDefs = [

		{headerName: "Album Art", field: "album_art", suppressSizeToFit: true, width:200, cellRenderer: function(params) {
      return '<img src="'+ params.value + '" height="200" width="200">'
  }, autoHeight:true},
  		
  		{headerName: "", field: "preview_url", suppressSizeToFit: true, width: 45, cellRenderer: function(params) {
      return '<audio id="player" controls="false" name="media"><source src="'+ params.value +'" type="audio/mpeg"></audio>'
  }, autoHeight:true},

		{headerName: "Song", field: "name", cellStyle: {'white-space': 'normal'}},
		{headerName: "Artist Name", field: "artist_name"},
		{headerName: "Tempo", field: "tempo", width: 80, headerTooltip: "The speed or pace of a given piece. Measured in beats per minute (BPM)."},
		{headerName: "Key", field: "key", width: 90, headerTooltip: "The group of pitches, or scale, that forms the basis of a musical composition."},
		{headerName: "Time Signature", width: 130, field: "time_signature", headerTooltip: "The number of beats contained in each measure (bar)."},
		{headerName: "Acousticness", width: 120, field: "acousticness", headerTooltip: "A confidence measure from 0 to 100 of whether the track is acoustic.", cellStyle: function(params) {
			if (params.value > 0 && params.value < 0.33) {
				return {color: 'red', backgroundColor: 'green'};
			}
		}
	},

		{headerName: "Danceability", field: "danceability", width: 115, headerTooltip: "Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity."},
		{headerName: "Energy", field: "energy", width: 90, headerTooltip: "A measure from 0 to 100 that represents a perceptual measure of intensity and activity."},
		{headerName: "Instrumentalness", field: "instrumentalness", width: 135, headerTooltip: "Predicts whether a track contains no vocals. Confidence is higher as the value approaches 100."},
		{headerName: "Liveness", field: "liveness", width: 100, headerTooltip: "Detects the presence of an audience in the recording. A value above 80 provides strong likelihood that the track is live."},
		{headerName: "Loudness", field: "loudness", width: 100, headerTooltip: "The overall loudness of a track in decibels (dB). Values typical range between -60 and 0 db."},
		{headerName: "Speechiness", field: "speechiness", width: 120, headerTooltip: "Detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 100 the attribute value."},
		{headerName: "Positivity", field: "valence", width: 120, headerTooltip: "A measure from 0 to 100 describing the musical positiveness conveyed by a track. Tracks with high positivity sound more cheerful or euphoric, while tracks with low positivity sound more sad, depressed, or angry."},
		{headerName: "Length", width: 85, field: "duration_ms"}

	    ];

	    // let the grid know which columns and what data to use
    	var gridOptions = {
    		columnDefs: columnDefs,
    		enableSorting: true,
    		enableFilter: true,
    		overlayLoadingTemplate: '<span class="ag-overlay-loading-center">Please wait while your rows are loading</span>',
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
