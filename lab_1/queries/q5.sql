--replace this with your query

SELECT committee.CMTE_NM, candidate.CAND_OFFICE_ST, cand_summary.TTL_RECEIPTS, cand_summary.TTL_RECEIPTS/state_pop.population AS PER_CAPITA_REC
FROM committee, candidate, cand_summary, (
	SELECT state, sum(population) AS population
    FROM dist_pop
    GROUP BY state) state_pop
WHERE candidate.CAND_ID = cand_summary.CAND_ID
AND committee.CMTE_ID = candidate.CAND_PCC
AND state_pop.state = candidate.CAND_OFFICE_ST
AND candidate.CAND_OFFICE = "S"
AND candidate.CAND_ELECTION_YR = 2016
AND candidate.CAND_STATUS in ('C', 'N')
ORDER BY PER_CAPITA_REC DESC
LIMIT 20
;
