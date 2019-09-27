awk 'BEGIN{ print "Date|Artist|Song|Album|Label|Show|DJ";}
{
	split($1, date, ":")
	da = date[2]" "substr($2, 1, length($2)-1)" "$3

	getline;
	split($1, artist, ":")
	art = artist[2]
	for (ix = 2; ix <= NF; ++ix){
		art = art" "$ix
	}

	getline;
	split($1, song, ":")
	sg = song[2]
	for (ix = 2; ix <= NF; ++ix){
		sg = sg" "$ix
	}

	getline;
	split($1, album, ":")
	alb = album[2]
	for (ix = 2; ix <= NF; ++ix){
		alb = alb" "$ix
	}

	getline;
	split($1, label, ":")
	lab = label[2]
	for (ix = 2; ix <= NF; ++ix){
		lab = lab" "$ix
	}

	getline;
	split($1, show, ":")
	sh = show[2]
	for (ix = 2; ix <= NF; ++ix){
		sh = sh" "$ix
	}

	getline;
	split($1, dj, ":")
	d = dj[2]
	for (ix = 2; ix <= NF; ++ix){
		d = d" "$ix
	}

	line = da"|"art"|"sg"|"alb"|"lab"|"sh"|"d
	gsub(/Nick Edit/, "Nick Bike Edit", line)
	gsub(/ocean eyes/, "Ocean Eyes", line)
    gsub(/bad guy/, "Bad Guy", line)
    gsub(/my boy/, "My Boy", line)
    gsub(/watch/, "Watch", line)
    gsub(/Barefoot in the Park/, "Barefoot In The Park", line)
    gsub(/live/, "Live", line)
    gsub(/@/, "at", line)
    gsub(/wmbr/, "WMBR", line)
    gsub(/HiiJack/, "HiiiJack", line)
    gsub(/Ellish/, "Eilish", line)
    gsub(/billie eilish/, "Billie Eilish", line)
    gsub(/James Black/, "James Blake", line)
    gsub(/bury a friend/, "Bury A Friend", line)
    gsub(/&/, "and", line)

    print line
	

}' data/wmbr.txt > data/wmbr-awk.txt

