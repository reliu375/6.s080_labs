--replace this with your query
SELECT CAND_NAME, CMTE_NM, CMTE_ST1
FROM candidate, committee
WHERE committee.CMTE_ID = candidate.CAND_PCC
AND candidate.CAND_STATUS in ('C', 'N')
AND candidate.CAND_ELECTION_YR = 2016
AND candidate.CAND_OFFICE = 'P'
AND CAND_NAME like "%HUCK%";
