awk -F ',' 'BEGIN{ print "word, definition" }
{
	# Split the group of words into an array of words
	# Print the same definition for each word
    split($2, words, " ")
	for (ix in words) {
		print words[ix]", "$NF 
	}
}' data/synsets.txt > data/synsets-awk.txt
