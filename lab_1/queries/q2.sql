--replace this with your query
SELECT CAND_PTY_AFFILIATION, count(CAND_ID) AS NUM_CANDIDATES
FROM candidate 
WHERE CAND_OFFICE="S"
AND CAND_PTY_AFFILIATION!="REP"
AND CAND_PTY_AFFILIATION!="DEM"
AND CAND_PTY_AFFILIATION!="IND"
AND CAND_STATUS in ('C', 'N')
AND CAND_ELECTION_YR=2016
GROUP BY CAND_PTY_AFFILIATION
ORDER BY NUM_CANDIDATES DESC;
