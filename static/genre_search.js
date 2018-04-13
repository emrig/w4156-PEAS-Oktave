
$(document).ready(function() {

	//$("#search-results").hide();

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
		//console.log("Button clicked");
		//var genre = $("#genre-search-bar").val();
		var tempo = $("#tempo-search-bar").val();
		var key = $("#key-list").val();
		var time_signature = $("#time-sig-list").val();
		//console.log(genre);

		//console.log(key);

		// Create empty array
		var array = [];

		// Create JSON object with property "genre_label"
		var json_object = {
			//genre: genre,   
			tempo: tempo,
			key: key,
			time_signature: time_signature
		}

		console.log("JSON object");
		console.log(json_object);

		// Add object to array
		array.push(json_object);

		console.log("Array");
		console.log(array);

		// Encode JSON string
		var json_string = JSON.stringify(array);

		console.log("JSON string");
		console.log(json_string);


		//$("#search-results").show();
		//$("#search-results").hide();

		var data = $.get("/song_search_test_temp", json_object, parse(data));

	});

	function parse(data)
	{
		console.log(data);
	}


	// var artists = [];


});
