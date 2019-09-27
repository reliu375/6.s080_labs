from wrangler import dw
import sys

if(len(sys.argv) < 3):
	sys.exit('Error: Please include an input and output file.  Example python script.py input.csv output.csv')

w = dw.DataWrangler()

# Split data repeatedly on '-n'  into  rows
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="row",
               update=False,
               insert_position="right",
               row=None,
               on="-\\n",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

# Split data repeatedly on '|'
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="column",
               update=False,
               insert_position="right",
               row=None,
               on="\\|",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

# Set  split1  name to  1
w.add(dw.SetName(column=["split1"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["1"],
                 header_row=None))

# Set  split2  name to  2
w.add(dw.SetName(column=["split2"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["2"],
                 header_row=None))

# Set  split3  name to  3
w.add(dw.SetName(column=["split3"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["3"],
                 header_row=None))

# Set  split4  name to  4
w.add(dw.SetName(column=["split4"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["4"],
                 header_row=None))

# Set  split5  name to  
w.add(dw.SetName(column=["split5"],
                 table=0,
                 status="active",
                 drop=True,
                 names=[""],
                 header_row=None))

# Fill   with values from below
w.add(dw.Fill(column=[""],
              table=0,
              status="active",
              drop=False,
              direction="up",
              method="copy",
              row=None))

# Drop 
w.add(dw.Drop(column=[""],
              table=0,
              status="active",
              drop=True))

# Fold 1, 2, 3, 4  using  header as a key
w.add(dw.Fold(column=["_1","_2","_3","_4"],
              table=0,
              status="active",
              drop=False,
              keys=[-1]))

# Drop split6
w.add(dw.Drop(column=["split6"],
              table=0,
              status="active",
              drop=True))

# Delete rows 1,2,3,4
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.RowIndex(column=[],
                  table=0,
                  status="active",
                  drop=False,
                  indices=[0,1,2,3])])))

# Split value repeatedly on ','  into  rows
w.add(dw.Split(column=["value"],
               table=0,
               status="active",
               drop=True,
               result="row",
               update=False,
               insert_position="right",
               row=None,
               on=",",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

w.apply_to_file(sys.argv[1]).print_csv(sys.argv[2])

