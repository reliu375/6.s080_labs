--replace this with your query
select STATE, sum(TRANSACTION_AMT) as TOTAL_CONTRI
from INDIV_CONTRIB
where ENTITY_TP = 'IND'
group by STATE
order by TOTAL_CONTRI desc
