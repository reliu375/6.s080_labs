awk -F '|' 'BEGIN{ print "Date|Artist|Song|Album|Label|Show|DJ"; getline;}
{
	split($0, fields, "|")
	# Feat case
	# print fields[3]~"\(feat."
	if (fields[3]~"\(feat."){
		split(fields[3], names, "\(feat. ")
		name = substr(names[2], 1, length(names[2]) - 1)
		print fields[1]"|"name"|"fields[3]"|"fields[4]"|"fields[5]"|"fields[6]"|"fields[7]
	}

	# Split author
	if (fields[2]~","){
		split(fields[2], names, ", ")
		for (jx in names){
			print fields[1]"|"names[jx]"|"fields[3]"|"fields[4]"|"fields[5]"|"fields[6]"|"fields[7]
		}
	}

	else if (fields[2]~"and"){
		split(fields[2], names, " and ")
		for (jx in names){
			print fields[1]"|"names[jx]"|"fields[3]"|"fields[4]"|"fields[5]"|"fields[6]"|"fields[7]
		}
	} else {
		print $0
	}
}' data/wmbr-awk.txt >> data/wmbr-11-awk.txt