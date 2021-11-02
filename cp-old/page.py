a=open("jpg.html", mode="r").readlines()
b=open("page.html", mode="a+")
for line  in a:
        line=line.split("|")
        b.write("<a href=\'"+line[2]+"\'>"+ line[1]+"</a><h1>"+line[0]+"</h1><br>\n")
        print(line)

