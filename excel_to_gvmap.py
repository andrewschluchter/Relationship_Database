import os, pandas, openpyxl

# open excel file
input_file = "relations.xlsx"
cwd = os.getcwd()
input_file_path = cwd+os.sep+input_file
entries_sheet = "entries"
relationships_sheet = "relationships"
codes_sheet = "codes"
theWorkbook = openpyxl.load_workbook(input_file_path)
#print(theWorkbook)
#print(theWorkbook[entries_sheet]['A1'].value)  #'Test1'
#print(theWorkbook.sheetnames)  #'Test1'

# gather all data from each sheet of the spreadsheet and store as dataframes
ws1 = theWorkbook[entries_sheet]
df1 = pandas.DataFrame(ws1.values)
#make the columns from the first row
columnNames = df1.iloc[0]
df1 = df1[1:]
df1.columns = columnNames
#print(df1)
ws2 = theWorkbook[relationships_sheet]
df2 = pandas.DataFrame(ws2.values)
#make the columns from the first row
columnNames = df2.iloc[0]
df2 = df2[1:]
df2.columns = columnNames
#print(df2)
ws3 = theWorkbook[codes_sheet]
df3 = pandas.DataFrame(ws3.values)
#make the columns from the first row
columnNames = df3.iloc[0]
df3 = df3[1:]
df3.columns = columnNames
#print(df3)

# use the codes worksheet to update all dataframes fully
for index, row in df1.iterrows():
    #print(row)
    for index1, row1 in df3.iterrows():
        if str(row1['status']) == str(row['status']):
            #print("entry found!")
            #print(index1)
            replace_val = str(df3.iloc[index1-1]['status code'])
            #print("replace_val:")
            #print(replace_val)
            #print(df3['status'][1])
            df1['status'][index] = replace_val
            #print("replaced values for status: ")
            #print(df1['status'])
    for index1, row1 in df3.iterrows():
        if str(row1['area']) == str(row['area']):
            replace_val = str(df3.iloc[index1-1]['area code'])
            df1['area'][index] = replace_val
for index, row in df2.iterrows():
    for index1, row1 in df3.iterrows():
        if str(row1['edge']) == str(row['edge']):
            replace_val = str(df3.iloc[index1-1]['edge code'])
            df2['edge'][index] = replace_val
    for index1, row1 in df3.iterrows():
        if str(row1['arrow']) == str(row['arrow']):
            replace_val = str(df3.iloc[index1-1]['arrow code'])
            df2['arrow'][index] = replace_val
#print(df1['status'])
#print(df1['area'])

# create and/or open the .gv file
output_file = "relations_data_gen.gv"
output_file_path = cwd+os.sep+output_file
outfile = open(output_file_path, 'w')
#df1.to_string(outfile)

# output the starting information
outfile.write("strict digraph {\n")
outfile.write("\n")
outfile.write("    /*\n")
outfile.write("    *** Clusters\n")
outfile.write("    (semi-default) 0 = unknown\n")
outfile.write("    1 = Bay Area\n")
outfile.write("    2 = San Diego area\n")
outfile.write("    3 = LA area\n")
outfile.write("    4 = Oregon\n")
outfile.write("    5 = Ohio\n")
outfile.write("    6 = Illinois\n")
outfile.write("    7 = Virginia\n")
outfile.write("\n")
outfile.write("    *** Colors\n")
outfile.write("    (default) white = #ffffffbb = undeclared/unknown\n")
outfile.write("    palegreen = #22ff99bb = self\n")
outfile.write("    tan = coworkers\n")
outfile.write("    dodgerblue = #55aaffbb = safe but not open\n")
outfile.write("    violet = safe & open\n")
outfile.write("    cyan = #22ffffbb = good friends\n")
outfile.write("    lightyellow = caution: watch over\n")
outfile.write("    red = #ff4444bb = caution: dangerous\n")
outfile.write("    gray42 = #888888bb = dead\n")
outfile.write("\n")
outfile.write("    *** Edges\n")
outfile.write("    (default) style=solid = directly related\n")
outfile.write("    style=dashed = family, exact relation unknown\n")
outfile.write("    style=dotted = unknown or no relation\n")
outfile.write("\n")
outfile.write("    *** Arrows\n")
outfile.write("    (default) arrowhead=normal = a direct product of\n")
outfile.write("    arrowhead=none = partners\n")
outfile.write("    arrowhead=dot = cousin\n")
outfile.write("    arrowhead=tee = living with, but no relation\n")
outfile.write("    arrowhead=diamond = adoptive\n")
outfile.write("    */\n")
outfile.write("\n")
outfile.write("    /* Full entry format:\n")
outfile.write("    <node_name>\n")
outfile.write("    [label=<FULL NAME<BR/><FONT POINT-SIZE=\"8\">\n")
outfile.write("    PHONE NUMBER<BR/>\n")
outfile.write("    EMAIL<BR/>\n")
outfile.write("    BIRTHDAY<BR/>\n")
outfile.write("    ADDRESS LINE 1<BR/>\n")
outfile.write("    ADDRESS LINE 2<BR/>\n")
outfile.write("    Current: CURRENT DATE\n")
outfile.write("    </FONT>>shape=\"none\" style=\"filled\" fillcolor=\"white\" cluster=0];\n")
outfile.write("    */\n")
outfile.write("\n")
outfile.write("    graph [overlap_scaling=6 splines=true overlap=false];\n")
outfile.write("\n")
#outfile.write("    PROFESSIONAL [shape=\"none\" style=\"bold\" fillcolor=\"white\" shape=\"tab\" cluster=1]\n")
#outfile.write("    LAB [shape=\"none\" style=\"bold\" fillcolor=\"white\" shape=\"tab\" cluster=1]\n")
#outfile.write("    NONPROFESSIONAL [shape=\"none\" style=\"bold\" fillcolor=\"white\" shape=\"tab\" cluster=1]\n")
#outfile.write("\n")
print(df1)
print(df2)
print(df3)
for index, row in df3.iterrows():
    if str(row['context']) != 'None':
        outfile.write("    "+row['context']+" [shape=\"none\" style=\"bold\" fillcolor=\"white\" shape=\"tab\" cluster=1]\n")
outfile.write("\n")

# for each row in the entries sheet, output the information to the .gv file
    #<node_name>
    #[label=<FULL NAME<BR/><FONT POINT-SIZE="8">
    #PHONE NUMBER<BR/>
    #EMAIL<BR/>
    #BIRTHDAY<BR/>
    #ADDRESS LINE 1<BR/>
    #ADDRESS LINE 2<BR/>
    #Current: CURRENT DATE
    #</FONT>>shape="none" style="filled" fillcolor="white" cluster=0];
for index, row in df1.iterrows():
    node_name = row['full name'].replace(' ', '_')
    outfile.write("    <"+node_name+">\n")
    outfile.write("    [label=<"+row['full name']+"<BR/><FONT POINT-SIZE=\"8\">\n")
    try:
        outfile.write("    "+row['phone']+"<BR/>\n")
    except:
        pass
    try:
        outfile.write("    "+row['email']+"<BR/>\n")
    except:
        pass
    try:
        outfile.write("    "+row['address 1']+"<BR/>\n")
    except:
        pass
    try:
        outfile.write("    "+row['address 2']+"<BR/>\n")
    except:
        pass
    try:
        if str(row['current']) != 'None':
            outfile.write("    "+str(row['current'])+"<BR/>\n")
    except:
        pass
    outfile.write("    </FONT>>shape=\"none\" style=\"filled\" fillcolor=\""+str(row['status'])+"\" cluster="+str(row['area'])+"];\n")
    outfile.write("\n")

# for each row in the relationships sheet, output the information to the .gv file
for index, row in df1.iterrows():
    context = str(row['context'])
    #print(context)
    if context != "None":
        #from_node_name = df2['from node'][index].replace(' ', '_')
        to_node_name = df1['full name'][index].replace(' ', '_')
        outfile.write("    "+context+" -> "+to_node_name+" [style=solid arrowhead=normal]\n")
        #print("    "+context+" -> "+to_node_name+" [style=solid arrowhead=normal]")
for index, row in df2.iterrows():
    from_node_name = df2['from node'][index].replace(' ', '_')
    #print(from_node_name)
    to_node_name = df2['to node'][index].replace(' ', '_')
    outfile.write("    "+from_node_name+" -> "+to_node_name+" [style="+row['edge']+" arrowhead="+row['arrow']+"]\n")

# save and close the file and end the script
outfile.write("}\n")
outfile.close()
