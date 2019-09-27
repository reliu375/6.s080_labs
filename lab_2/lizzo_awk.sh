awk -F '},{' 'BEGIN{ }
{
    for (ix = 1; ix <= NF; ++ix){
    	line = ""
    	split($ix, fields, ",")
    	for (jx in fields){
    		n = split(fields[jx], subfields, ":")
    		if (n > 1){
  				for (kx = 2; kx <= n; ++kx)
    				line = line", "subfields[kx]
    		}
    		if (n == 1){
    			line = line", "subfields[1]
    		}
    	}
    	line = substr(line, 3)
    	print line
    }

}' data/lizzo_appearances.json > lizzo_awk.txt

awk -F '", "' 'BEGIN{ print "Year|Title|Notes" }
{
	line = ""

    for (ix = 1; ix <= NF; ++ix)
    	# print $ix
    	if (substr($ix, 1, 1) == "\""){
    		year = substr($ix, 2)
    		if (year == "2017,  2018"){
    			line = line"|"substr($ix, 1, 5)
    		}
    		else{
    			line = line"|"substr($ix, 1)
    		}
    		
    	}
    	else if (substr($ix, length($ix)) == "\""){
    		line = line"|"substr($ix, 1, length($ix) - 1)
    	}
    	else {
    		line = line"|"$ix
    	}

    gsub(/\\/, "", line)
    gsub(/\"}]/, "", line)
    line = substr(line, 3)
    print line

    if ($1~","){
    	newline = "2018"substr(line, 5)
    	print newline
    } 
     
}' lizzo_awk.txt > lizzo_awk_final.txt
