import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3 as sql
import pandas as pd
import argparse

def runSQL(query_num):
	with sql.connect("lab1.sqlite") as conn, open("queries/q{}.sql".format(query_num)) as in_query:
		cur = conn.cursor()
		df = pd.read_sql_query(in_query.read(), conn)
		return df

def Q1Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    candidate = pd.read_csv('data/candidate.txt', delimiter = '|')

    condition = (candidate.CAND_ELECTION_YR == 2016) & (candidate.CAND_OFFICE_ST == "US")
    condition = condition & ((candidate.CAND_STATUS == 'C') | (candidate.CAND_STATUS == 'N' ))
    fields = ["CAND_ELECTION_YR", "CAND_OFFICE_ST", "CAND_NAME"]
    pres_2016_cand = candidate[condition]
    pres_2016_cand = pres_2016_cand[fields]

    res = pres_2016_cand.groupby(fields[:2]).count()

    return res

def Q2Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    candidate = pd.read_csv('data/candidate.txt', delimiter = '|')

    condition = (candidate.CAND_PTY_AFFILIATION != "REP") & (candidate.CAND_PTY_AFFILIATION != "DEM") & (candidate.CAND_PTY_AFFILIATION != "IND") & (candidate.CAND_OFFICE == "S")
    condition = condition & ((candidate.CAND_STATUS == 'C') | (candidate.CAND_STATUS == 'N' ))
    condition = condition & (candidate.CAND_ELECTION_YR == 2016)
    fields = ["CAND_PTY_AFFILIATION", "CAND_NAME"]
    senate_candidates = candidate[condition]
    res = senate_candidates[fields].groupby(fields[:1]).count().rename({"CAND_NAME":"NUM_CANDIDATES"}, axis="columns").sort_values(
          'NUM_CANDIDATES', ascending = False)

    return res

def Q3Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    pac = pd.read_csv('data/pac_summary.txt', delimiter = '|')

    condition = pac.CMTE_TP == "O" # Super-PACs only.

    fields = ["CMTE_ID", "CMTE_NM", "TTL_RECEIPTS"]

    super_pac = pac[condition]
    return super_pac[fields].sort_values(["TTL_RECEIPTS"], ascending = False)[:10]

def Q4Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    candidate = pd.read_csv('data/candidate.txt', delimiter = '|')
    committee = pd.read_csv('data/committee.txt', delimiter = '|')

    condition = (candidate.CAND_ELECTION_YR == 2016)
    condition = condition & ((candidate.CAND_STATUS == 'C') | (candidate.CAND_STATUS == 'N' ))
    condition = condition & (candidate.CAND_OFFICE == 'P')

    candidate = candidate[condition]
    fields = ["CAND_NAME", "CMTE_NM", "CMTE_ST1"]
    cand_fields = ["CAND_NAME", "CAND_PCC"]
    cmte_fields = ["CMTE_ID", "CMTE_NM" ,"CMTE_ST1"]

    candidate = candidate[cand_fields]
    committee = committee[cmte_fields]

    joined = pd.merge(left = candidate, right = committee,
                      left_on = ["CAND_PCC"],
                      right_on = ["CMTE_ID"])

    huck = joined.CAND_NAME.str.contains('HUCK')
    joined = joined[huck]
    fields = ["CAND_NAME", "CMTE_NM", "CMTE_ST1"]

    return joined[fields]

def Q5Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    candidate = pd.read_csv('data/candidate.txt', delimiter = '|')
    cand_summary = pd.read_csv('data/cand_summary.txt', delimiter = '|')
    committee = pd.read_csv('data/committee.txt', delimiter = '|')
    dist_pop = pd.read_csv('data/dist_pop.txt', delimiter = '|')

    state_pop = dist_pop[['state', 'population']].groupby('state').sum()

    cand_filter = (candidate.CAND_OFFICE == 'S') & ((candidate.CAND_STATUS == 'C') | (candidate.CAND_STATUS == 'N' ))
    cand_filter = cand_filter & (candidate.CAND_ELECTION_YR == 2016)
    candidate = candidate[cand_filter]

    cand_fields = ["CAND_ID","CAND_NAME", "CAND_PCC", "CAND_OFFICE_ST"]
    candidate = candidate[cand_fields]

    cand_sum_fields = ["CAND_ID", "TTL_RECEIPTS"]
    cand_summary = cand_summary[cand_sum_fields]

    committee_fields = ["CMTE_ID", "CMTE_NM"]
    committee = committee[committee_fields]

    joined = pd.merge(left = candidate, right = cand_summary,
                      left_on = ["CAND_ID"], right_on = ["CAND_ID"])
    joined = pd.merge(left = joined, right = committee, 
                      left_on = ["CAND_PCC"], right_on = ["CMTE_ID"])
    joined = pd.merge(left = joined, right = state_pop,
                      left_on = ["CAND_OFFICE_ST"], right_on = ["state"])

    joined["PER_CAPITA_REC"] = joined.TTL_RECEIPTS / joined.population

    fields = ["CMTE_NM", "CAND_OFFICE_ST", "TTL_RECEIPTS","PER_CAPITA_REC"]

    res = joined.sort_values(["PER_CAPITA_REC"], ascending = False)[:20]

    return res[fields]


def Q6Pandas():
    """
    TODO: Write your Pandas query here, return a dataframe to answer the question
    """
    cand_summary = pd.read_csv('data/cand_summary.txt', delimiter = '|')
    candidate = pd.read_csv('data/candidate.txt', delimiter = '|')


    cand_summary['CONT_PER_RECEIPT'] = cand_summary.TTL_INDIV_CONTRIB / cand_summary.TTL_RECEIPTS 
    cand_filter = (candidate.CAND_OFFICE == 'H') & ((candidate.CAND_STATUS == 'C') | (candidate.CAND_STATUS == 'N' ))
    cand_filter = cand_filter & (candidate.CAND_ELECTION_YR == 2016)
    sum_filter = cand_summary.TTL_RECEIPTS >= 100000

    candidate = candidate[cand_filter]
    cand_summary = cand_summary[sum_filter]

    candidate_fields = ["CAND_ID", "CAND_NAME", "CAND_PTY_AFFILIATION"]
    cand_summary_fields = ["CAND_ID", "TTL_INDIV_CONTRIB", "TTL_RECEIPTS", "CONT_PER_RECEIPT"]

    candidate = candidate[candidate_fields]
    cand_summary = cand_summary[cand_summary_fields]

    joined = pd.merge(left = candidate, right = cand_summary,
                      left_on = ["CAND_ID"], right_on = ["CAND_ID"])

    joined = joined.sort_values(["CONT_PER_RECEIPT"], ascending = True)

    fields = ["CAND_NAME", "CAND_PTY_AFFILIATION", "TTL_INDIV_CONTRIB", "TTL_RECEIPTS", "CONT_PER_RECEIPT"]

    return joined[:10][fields]

def Q7Pandas():
    cand_summary = pd.read_csv('data/cand_summary.txt', delimiter = '|')
    candidate = pd.read_csv('data/candidate.txt', delimiter = '|')

    cand_filter = (candidate.CAND_OFFICE == 'S') & ((candidate.CAND_STATUS == 'C') | (candidate.CAND_STATUS == 'N' ))
    cand_filter = cand_filter & (candidate.CAND_ELECTION_YR == 2016)

    candidate = candidate[cand_filter]

    candidate_fields = ["CAND_ID", "CAND_NAME", "CAND_PTY_AFFILIATION"]
    cand_summary_fields = ["CAND_ID", "TTL_INDIV_CONTRIB", "TTL_RECEIPTS"]

    candidate = candidate[candidate_fields]
    cand_summary = cand_summary[cand_summary_fields]

    joined = pd.merge(left = candidate, right = cand_summary,
                      left_on = ["CAND_ID"], right_on = ["CAND_ID"])

    fields = ["CAND_PTY_AFFILIATION", 'TTL_INDIV_CONTRIB', "TTL_RECEIPTS"]

    joined = joined[fields].groupby("CAND_PTY_AFFILIATION").sum()

    joined["CONT_PER_RECEIPT"] = joined.TTL_INDIV_CONTRIB / joined.TTL_RECEIPTS

    joined = joined.sort_values('CONT_PER_RECEIPT', ascending = False)
    
    return joined[:10]
    

pandas_queries = [Q1Pandas, Q2Pandas, Q3Pandas, Q4Pandas, Q5Pandas, Q6Pandas, Q7Pandas]
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", "-q", help="Run a specific query", type=int)
    args = parser.parse_args()

    queries = range(1, 12)
    if args.query != None:
        queries = [args.query]
    for query in queries:
        print("\nQuery {}".format(query))
        if query <= 7:
            print("\nPandas Output")
            print(pandas_queries[query-1]())
        print("\nSQLite Output")
        print(runSQL(query))
    

	
