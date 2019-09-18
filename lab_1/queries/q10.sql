--replace this with your query
select CAND_NAME, CAND_OFFICE_ST, sum(TRANSACTION_AMT) as TOTAL
from candidate
join indiv_contrib on candidate.CAND_PCC = indiv_contrib.CMTE_ID
where CAND_OFFICE_ST <> indiv_contrib.STATE
and CAND_ELECTION_YR = 2016
and CAND_OFFICE = 'S'
and CAND_STATUS in ('C', 'N')
group by candidate.CAND_ID
order by TOTAL desc
limit 5;
