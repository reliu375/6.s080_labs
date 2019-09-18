--replace this with your query
SELECT candidate.CAND_NAME, CAND_PTY_AFFILIATION, TTL_INDIV_CONTRIB, TTL_RECEIPTS, TTL_INDIV_CONTRIB/TTL_RECEIPTS AS CONT_PER_RECEIPT
FROM candidate, cand_summary
WHERE candidate.CAND_ID = cand_summary.CAND_ID
AND candidate.CAND_OFFICE = 'H'
AND candidate.CAND_STATUS in ('C', 'N')
AND candidate.CAND_ELECTION_YR = 2016
AND cand_summary.TTL_RECEIPTS>= 100000
ORDER BY CONT_PER_RECEIPT ASC
LIMIT 10;
