awk 'BEGIN{ print "id,name,artists,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,duration_ms,time_signature"; getline;}
{
	split($0, fields, ",")
	gsub(/with/, "feat.")
	# Feat case
	if (fields[2]~"\(feat."){
		split(fields[2], names, "\(feat. ")
		split(names[2], names, "&" )
		for (jx in names){
			if (names[jx]~"\)\""){
				names[jx] = substr(names[jx], 1, length(names[jx]) - 2)
			}
			print fields[1]","fields[2]","names[jx]","fields[4]","fields[5]","fields[6]","fields[7]","fields[8]","fields[9]","fields[10]","fields[11]","fields[12]","fields[13]","fields[14]","fields[15]","fields[16]

		}
	}
	print $0
	
}' data/top2018.csv >> data/top2018-q11.csv