
$(document).ready(function() {

	var genres = [
	'adult standards',
	 'afrobeat',
	 'album rock',
	 'art rock',
	 'blues',
	 'blues-rock',
	 'brill building pop',
	 'chicago soul',
	 'christmas',
	 'classic funk rock',
	 'classic rock',
	 'country rock',
	 'dance pop',
	 'dance rock',
	 'deep funk',
	 'delta blues',
	 'disco',
	 'electric blues',
	 'folk rock',
	 'folk',
	 'funk',
	 'glam rock',
	 'hard rock',
	 'heavy christmas',
	 'hip pop',
	 'jazz blues',
	 'jazz christmas',
	 'jazz funk',
	 'lounge',
	 'melancholia',
	 'mellow gold',
	 'memphis blues',
	 'memphis soul',
	 'modern blues',
	 'motown',
	 'neo soul',
	 'new jack swing',
	 'new orleans blues',
	 'new romantic',
	 'new wave pop',
	 'new wave',
	 'northern soul',
	 'p funk',
	 'pop',
	 'post-disco',
	 'post-punk',
	 'protopunk',
	 'psychedelic rock',
	 'quiet storm',
	 'r&b',
	 'rock',
	 'rock-and-roll',
	 'rockabilly',
	 'roots rock',
	 'singer-songwriter',
	 'smooth jazz',
	 'soft rock',
	 'soul blues',
	 'soul christmas',
	 'soul jazz',
	 'soul',
	 'southern rock',
	 'southern soul',
	 'symphonic rock',
	 'synthpop',
	 'uk post-punk',
	 'urban contemporary',
	 'vocal jazz'
	 ];
	$( "#genre-search-bar" ).autocomplete({
	    source: genres
	});


	$("#search-form-master").submit(function(event) {
		document.getElementById("myGrid").remove();
		var grid_element = $("<div id='myGrid' style='height: 600px;width:100%;' class='ag-theme-balham'>");
		$("#search-results").append(grid_element);

		//console.log("Button clicked");
		//var genre = $("#genre-search-bar").val();
		var tempo = $("#tempo-search-bar").val();
		var key = $("#key-list").val();
		var time_signature = $("#time-sig-list").val();

		// Create empty array
		var array = [];

		// Create JSON object with property "genre_label"
		var json_object = {
			//genre: genre,   
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
		{headerName: "Duration (ms)", field: "duration_ms"}

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
		gridOptions.api.setRowData(json["data"]);
		gridOptions.rowHeight = 600;
	}

});
