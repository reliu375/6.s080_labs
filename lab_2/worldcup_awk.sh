awk 'BEGIN{ print "country,year,rank"; getline; getline;}
{
	country = $1; # Get country

	# Rank 1
	getline;
	if ($1 != "|0") {
		year1 = substr($1, 2)
		split(year1, years1, ",")
		for (ix in years1){
			print country","years1[ix]",1"
		}
	}

	# Rank 2
	getline;
	if ($1 != "|0"){
		year2 = substr($1, 2)
		split(year2, years2, ",")
		for (ix in years2){
			print country","years2[ix]",2"
		}
	}

	# Rank 3
	getline;
	if ($1 != "|0"){
		year3 = substr($1, 2)
		split(year3, years3, ",")
		for (ix in years3){
			print country","years3[ix]",3"
		}
	}	
	
	# Rank 4
	getline;
	if ($1 != "|0"){
		year4 = substr($1, 2)
		split(year4, years4, ",")
		for (ix in years4){
			print country","years4[ix]",4"
		}
	}
		
	getline;
	getline;


}' data/worldcup-semiclean.txt > data/worldcup-awk.txt