--replace this with your query

select total_cont.STATE, total_cont.TOTAL_AMT,
       total_cont.TOTAL_AMT / state_pop.TOTAL_POP as PER_CAPITA_DONATION 
from
	(select STATE, sum(TRANSACTION_AMT) as TOTAL_AMT
	from indiv_contrib
	where TRANSACTION_TP = '10'
	and ENTITY_TP = 'IND'
	group by STATE) total_cont,
	(select state, sum(population) as TOTAL_POP
	from dist_pop
	group by state) state_pop
where total_cont.STATE = state_pop.state
order by PER_CAPITA_DONATION desc
limit 5;
