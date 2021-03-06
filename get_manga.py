from bs4 import BeautifulSoup
import requests
import os

def get_name() :
	page = requests.get("http://www.mangapanda.com/alphabetical").text
	soup = BeautifulSoup(page,"lxml")

	ul_li = soup.find_all("ul",{"class":"series_alpha"})

	name_dic = {}
	countr = 1
	for ul in ul_li :
		names = ul.find_all("li")
		for name in names :
			n = name.find("a").get("href")
			name_dic[countr] = str(n).strip().replace("/","")
			countr += 1
	return name_dic

def crawl() :

	# f = open('names.json').read()
	# name_dic = eval(f)
	name_dic = get_name()
	print name_dic

	alpha = str(raw_input("Enter 1st alphabet of Manga Name or 0 for others : ")).lower()

	temp_dic = {}
	ctr = 1
	if alpha == '0' :
		for i in name_dic.values() :
			if ord(i[0]) < 97 or ord(i[0]) > 122 :
				temp_dic[ctr] = i
				ctr += 1
	else :
		for i in name_dic.values() :
			if ord(i[0]) == ord(alpha) :
				temp_dic[ctr] = i
				ctr += 1

	for i in range(1,len(temp_dic.keys())) :
		print str(i)+" : "+str(temp_dic[i])

	print "\n"
	mnga = raw_input("Enter Manga No. : ")
	print "\n"
	print "Getting manga... " + temp_dic[int(mnga)] + "\n"

	url_temp = "http://mangapanda.com/" + temp_dic[int(mnga)]
	t = requests.get(url_temp).text
	s = BeautifulSoup(t,"lxml")
	tbl_li = s.find('table',{'id':'listing'}).find_all("a")

	print "No. of chapters = " + str(len(tbl_li)) + "\n\nNOTE : If only one chapter to Download, enter START and END as same\n\n"
	strt = int(raw_input("Enter starting chapter : "))
	end = int(raw_input("Enter ending chapter : "))
	print "\n"

	for c in range(strt,end+1) :

		dir_path = temp_dic[int(mnga)] + "/" + str(c)
		os.system("mkdir -p "+dir_path)

		for chpt in range(1,100000) :
			url = url_temp + "/" + str(c) + "/" + str(chpt)
			page = requests.get(url)
			if page.status_code == 404 :
				break
			else :
				soup = BeautifulSoup(page.text,"lxml")
				img_url = soup.find("div",{"id":"imgholder"}).find("a").find("img").get("src")
				os.system("wget "+str(img_url)+" -O "+dir_path+"/"+str(chpt))

crawl()
