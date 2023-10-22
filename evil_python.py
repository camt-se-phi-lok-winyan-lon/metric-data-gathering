import re


header = "number,name,url,lint_score,test_coverage,document_score,activeness"
output = ""
# Read the content from the .txt file
with open('./text.txt', 'r') as file:
    next(file)
    content = file.read()
    content.strip()

lines = content.split('\n')


for line in lines :
    if len(line) == 0 : continue
    line_output = ""
    tokens = line.split('|')
    # print(tokens[0],tokens[1])
    line_output += tokens[0] + "," + tokens[1] + ","+ tokens[2] + ","

    rate_pattern = r'at (\d+\.\d+)/10'
    match = re.search(rate_pattern, tokens[3])
    if match:
        rating = match.group(1)
        line_output += f"{rating},"
    else:
        line_output += f"0,"

    
    coverage_pattern = r'(\d+%)'
    # print(tokens[2])
    match = re.search(coverage_pattern, tokens[4])
    if match:
        percentage = match.group(1)
        line_output += f"{percentage},"
    else:
        line_output += f"0%,"

    line_output += tokens[5] + ","
    line_output += tokens[6] + ","

    output += line_output + "\n"
    
with open('output.csv', 'w') as output_file:
    output_file.write(header + "\n")
    output_file.write(output)


print("Data has been converted and saved to output.csv")
