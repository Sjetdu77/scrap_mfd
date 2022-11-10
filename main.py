import requests as rq
from bs4 import BeautifulSoup as bs
from flask import *
from pandas import DataFrame

mfd = "https://meleeframedata.com/"

app = Flask(__name__)

@app.route("/")
def index():
	list_stats = {
		"Name": [],
		"Weight" : [],
		"Fast Fall Speed" : [],
		"Dash Speed" : [],
		"Run Speed": [],
		"Wavedash Length (Rank)": [],
		"PLA Intangibility Frames": [],
		"Jump Squat": [],
		"Wall Jump": []
	}


	specifics = {}
	site_mfd = rq.get(mfd).text
	general = bs(site_mfd, "html.parser")
	allChars = general.find("div", {"class" : "char-grid"}).findAll("a")

	for c in allChars:
		page_spe = bs(rq.get(mfd + "/" + c.attrs["href"]).text, "html.parser")
		specifics[c.attrs["href"]] = page_spe

		stats = page_spe.find("div", {"class" : "misc-container"})
		stats = stats.findAll("div")

		for aStat in stats:
			s = aStat.string.split(": ")
			if s[0] == "Wall Jump":
				if s[1].strip() == "Yes":
					list_stats["Wall Jump"].append(True)
				else:
					list_stats["Wall Jump"].append(False)
			else:
				try:
					list_stats[s[0]].append(int(s[1]))
				except:
					list_stats[s[0]].append(float(s[1]))


		parts = c.attrs["name"]. split(",")[0].split()
		for p in range(len(parts)):
			parts[p] = parts[p].capitalize()

		list_stats["Name"].append(" ".join(parts))

	df_mfd = DataFrame.from_dict(list_stats).to_html(classes='data', header='true')
	print(df_mfd)
	return render_template("index.html", tables=df_mfd)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')