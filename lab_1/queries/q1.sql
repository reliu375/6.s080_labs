--replace this with your query
SELECT CAND_ELECTION_YR, CAND_OFFICE_ST, count(CAND_ID)
FROM candidate
WHERE CAND_OFFICE_ST="US"
AND CAND_STATUS in ('C', 'N')
AND CAND_ELECTION_YR=2016