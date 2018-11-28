1. input_csvs(has all the csvs needed to run the code)

	* bats_details.csv : contains batsman_name and his strike_rate, average
          Format : Batsman, strike_rate, average


	* bowl_details.csv : contains bowler_name and his strike_rate, economy
	  Format : Bowler, strike_rate, economy

	* FinalDataSet4.csv : is the dataset used to train the model
	  Format : Overs, team_no, striker_no, non-striker_no, bowler_no, venue_no, 
		striker's strike_rate, striker's aavg, non-striker's stike_rate, non-striker's avg,
	        bowler's economy, bowler's strike_rate, confidence_value, runs(0/1/2/3/4/6) or wicket(7)

	* match.csv : has batting and bowling order of both the teams for which match has to be simulated.
	  Format : batord_team1, batord_team2, bowlord_team1, bowlord_team2

	* PlayerMapping.csv : has the mapping of distinct number associated with each of the players.
	  Format : player_name, player_number

	* TeamMapping : has the mapping of distinct number associated with each team.
	  Format : Teamname(short form like RCB), team_number

	* VenueMapping : has he mapping of distinct number associated with each venue.
	  Format : venue_name, venue_number
	  
2. run.txt has steps to run the code			
