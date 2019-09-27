awk -F ',' 'BEGIN{ print "word, definition" }
{
    split($2, words, " ")
	for (ix in words) {
		print words[ix]", "$NF 
	}
}
END {
	print >> "synset_awk.txt"
	close("synset_awk.txt")
}' data/synsets.txt > synsets_awk.txt
