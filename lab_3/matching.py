import pandas as pd
import argparse
import sklearn as skl
import score
import os
import pdb
import textdistance

# You can add functions, and imports as neccesary for your ER algorithm
# you may find the scoring code useful for training and running locally

def run(directory):
    r1 = pd.read_csv(os.path.join(directory, "retailer1.csv"))
    r2 = pd.read_csv(os.path.join(directory, "retailer2.csv"))
    # TODO: This function should produce a csv file in the lab_3
    # directory using the name given by the follwing variable
    # e.g. "test_output.csv" for the test set. with the same format 
    # as data/train/matches.csv including the header
    # Please do not modify the output_filename

    replace_brand(r1, r2)
    replace_title(r1, r2)
    replace_desc(r1, r2)
    replace_shipment(r1, r2)

    r2["shortdescr"] = r2["proddescrshort"]
    fields = ["custom_id", "brand", "title", "price", "shortdescr", "modelno", "shipweight", "dimensions"] # , "price", "proddescrshort", "dimensions"]
    r1, r2 = r1[fields + ["groupname", "longdescr"]], r2[fields + ["category1", "proddescrlong", "Weight", "listprice"]]

    col1, col2 = [], []

    companyMatch = {}
    for br1 in r1['brand'].sort_values().unique():
        for br2 in r2['brand'].unique():
            if jaccard(br1, br2) >= 1/10:
                if br1 in companyMatch:
                    companyMatch[br1].append(br2)
                else:
                    companyMatch[br1] = [br2]

    for brand in companyMatch:
        # pdb.set_trace()
        for ix, row1 in r1[r1.brand == brand].iterrows():
            for jx, row2 in r2[r2.brand.isin(companyMatch[brand])].iterrows():
                c1 = jaccard(row1["title"], row2["title"])
                c2 = jaccard(row1['shortdescr'], row2['shortdescr'])
                c3 = edit_distance(row1["modelno"], row2["modelno"])
                c4 = abs(row1['price'] - row2['price']) <= 0.5 or abs(row1['price'] - row2['listprice']) <= 0.5
                c5 = edit_distance(row1['dimensions'], row2['dimensions'])
                c6 = abs(row1['shipweight'] - row2['Weight']) <= 1
                if c1 >= 0.6 or c2 >= 0.6 or c3 == 0:
                    col1.append(row1["custom_id"])
                    col2.append(row2["custom_id"])
                elif (c1 >= 0.2 or c2 >= 0.2) and (c3 <= 1 and c4 and c6):
                    col1.append(row1["custom_id"])
                    col2.append(row2["custom_id"])

    matches = pd.DataFrame({"id1": col1, "id2": col2})

    output_filename = "test_output.csv"

    matches.to_csv(output_filename, index = False)

def train(directory):
    train_matches = pd.read_csv(os.path.join(directory, "matches.csv"))
    r1 = pd.read_csv(os.path.join(directory, "retailer1.csv"))
    r2 = pd.read_csv(os.path.join(directory, "retailer2.csv"))

    replace_brand(r1, r2)
    replace_title(r1, r2)
    replace_desc(r1, r2)
    replace_shipment(r1, r2)
    replace_groupname(r1, r2)

    r2["shortdescr"] = r2["proddescrshort"]
    fields = ["custom_id", "brand", "title", "price", "shortdescr", "modelno", "shipweight", "dimensions"] # , "price", "proddescrshort", "dimensions"]
    r1, r2 = r1[fields + ["groupname", "longdescr"]], r2[fields + ["category1", "proddescrlong", "Weight", "listprice", "pcategory1", "category2", "pcategory2"]]
    
    col1, col2 = [], []

    companyMatch = {}
    for br1 in r1['brand'].sort_values().unique():
        for br2 in r2['brand'].unique():
            if jaccard(br1, br2) >= 1/10:
                if br1 in companyMatch:
                    companyMatch[br1].append(br2)
                else:
                    companyMatch[br1] = [br2]

    for brand in companyMatch:
        # pdb.set_trace()
        for ix, row1 in r1[r1.brand == brand].iterrows():
            for jx, row2 in r2[r2.brand.isin(companyMatch[brand])].iterrows():
                c1 = jaccard(row1["title"], row2["title"])
                c2 = jaccard(row1['shortdescr'], row2['shortdescr'])
                c3 = edit_distance(row1["modelno"], row2["modelno"])
                c4 = abs(row1['price'] - row2['price']) <= 0.5 or abs(row1['price'] - row2['listprice']) <= 0.5
                c5 = row1['groupname'] == row2['category1']
                c6 = abs(row1['shipweight'] - row2['Weight']) <= 1
                if c1 >= 0.6 or c2 >= 0.6 or c3 == 0:
                    col1.append(row1["custom_id"])
                    col2.append(row2["custom_id"])
                elif (c1 >= 0.2 or c2 >= 0.2) and (c3 <= 1 and c4 and c6):
                    col1.append(row1["custom_id"])
                    col2.append(row2["custom_id"])

    matches = pd.DataFrame({"id1": col1, "id2": col2})
    
    output_filename = "train_output.csv"

    matches.to_csv(output_filename)

def replace_brand(r1, r2):
    r1['brand'].replace('Avery Personal Creations', 'Avery', inplace=True)
    r2['brand'].replace('Avery Personal Creations', 'Avery', inplace=True)
    r1['brand'].replace('Diamond Crystal', 'Diamond', inplace=True)
    r2['brand'].replace('Diamond Crystal', 'Diamond', inplace=True)
    r1['brand'].replace('Elite Screens', 'Elite', inplace=True)
    r2['brand'].replace('Elite Screens', 'Elite', inplace=True)
    r1['brand'].replace('Encore Software', 'Encore', inplace=True)
    r2['brand'].replace('Encore Software', 'Encore', inplace=True)
    r1['brand'].replace('General Electric', 'GE', inplace=True)
    r2['brand'].replace('General Electric', 'GE', inplace=True)
    r1['brand'].replace('MOTOROLA', 'Motorola', inplace=True)
    r2['brand'].replace('MOTOROLA', 'Motorola', inplace=True)
    r1['brand'].replace('Royal Consumer', 'Royal', inplace=True)
    r2['brand'].replace('Royal Consumer', 'Royal', inplace=True)
    r1['brand'].replace('Rubbermaid Commercial', 'Rubbermaid', inplace=True)
    r2['brand'].replace('Rubbermaid Commercial', 'Rubbermaid', inplace=True)
    r1['brand'].replace('Team ProMark', 'Team Pro Mark', inplace=True)
    r2['brand'].replace('Team ProMark', 'Team Pro Mark', inplace=True)

    r1['brand'] = r1['brand'].str.lower()
    r2['brand'] = r2['brand'].str.lower()

    r1['modelno'] = r1['modelno'].str.lower()
    r2['modelno'] = r2['modelno'].str.lower()


def replace_title(r1, r2):
    r1['title'] = r1['title'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()
    r2['title'] = r2['title'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()

    r1['modelno'].fillna('', inplace=True)
    r2['modelno'].fillna('  ', inplace=True)

def replace_desc(r1, r2):
    r1['shortdescr'] = r1['shortdescr'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()
    # r1['shortdescr'].fillna('', inplace=True)
    r2['proddescrshort'] = r2['proddescrshort'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()
    # r2['proddescrshort'].fillna(' ', inplace=True)

    r1['longdescr'] = r1['shortdescr'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()
    r2['proddescrlong'] = r2['proddescrlong'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()

def replace_shipment(r1, r2):
    r2[['Weight', 'Units']] = r2['shipweight'].str.split(' ', n=1, expand=True)
    r2['Weight'] = r2['Weight'].astype(float)
    r2.loc[r2['Units'] == 'ounces', 'Weight'] = r2.loc[r2['Units'] == 'ounces', 'Weight']/16

def replace_groupname(r1, r2):
    r1['groupname'] = r1['groupname'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()
    r2['category1'] = r2['category1'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()
    r2['category2'] = r2['category2'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()
    r2['pcategory1'] = r2['pcategory1'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()
    r2['pcategory2'] = r2['pcategory2'].str.replace('[^a-zA-Z0-9 ]', '').str.lower()

def partition(df, field):
    return pd.unique(df[field])

def edit_distance(s1, s2):
    if str(s1) == 'nan' or str(s2) == 'nan':
        return float('inf')

    try:
        m, n = len(s1), len(s2)
    except:
        pdb.set_trace()
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
  
    # Fill d[][] in bottom up manner 
    for i in range(m+1): 
        for j in range(n+1): 
  
            # If first string is empty, only option is to 
            # insert all characters of second string 
            if i == 0: 
                dp[i][j] = j    # Min. operations = j 
  
            # If second string is empty, only option is to 
            # remove all characters of second string 
            elif j == 0: 
                dp[i][j] = i    # Min. operations = i 
  
            # If last characters are same, ignore last char 
            # and recur for remaining string 
            elif s1[i-1] == s2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
  
            # If last character are different, consider all 
            # possibilities and find minimum 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert 
                                   dp[i-1][j],        # Remove 
                                   dp[i-1][j-1])    # Replace 
  
    return dp[m][n]

def jaccard(s1, s2):
    if str(s1) == 'nan' or str(s2) == 'nan':
        return 0
    l1, l2 = set(s1.lower().strip().split(" ")), set(s2.lower().strip().split(" "))
    return len(l1 & l2) / len(l1 | l2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_directory")
    parser.add_argument("--train", action="store_true")
    args = parser.parse_args()
    if args.train:
        train(args.input_directory)
    else:
        run(args.input_directory)



