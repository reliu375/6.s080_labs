--replace this with your query
SELECT CAND_PTY_AFFILIATION, PTY_INDIV_CONTRIB, 
       PTY_TTL_RECEIPTS, PTY_INDIV_CONTRIB / PTY_TTL_RECEIPTS AS RATIO
FROM ( 
	SELECT CAND_PTY_AFFILIATION, sum(TTL_INDIV_CONTRIB) as PTY_INDIV_CONTRIB, 
	       sum(TTL_RECEIPTS) as PTY_TTL_RECEIPTS
	FROM candidate
	JOIN cand_summary ON candidate.CAND_ID = cand_summary.CAND_ID
	WHERE candidate.CAND_OFFICE = 'S'
	AND candidate.CAND_STATUS in ('C', 'N')
	AND candidate.CAND_ELECTION_YR = 2016
	GROUP BY CAND_PTY_AFFILIATION ) AGG
ORDER BY RATIO DESC
LIMIT 10;
