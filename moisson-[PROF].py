#coding: utf-8

import csv
import requests 
from bs4 import BeautifulSoup 

fichier = "Moisson_profuqam2.csv"

#Ici, j'ai essayé de créer une première ligne en haut de mon fichier csv pour que cahcune de mes colonnes aient un titre. Finalement, je n'ai pas réussi à bien le faire. Je me suis dit que je pourrais le faire à la main vu le peu de colonnes que j'ai.

#titre = ["nom prénom", "département", "poste", "courriel", "téléphone", "local", "domaines d'expertise"]
#titre.append
#next(lignes)

# Il y a une boucle dans une boucle pour que l'on puisse aller chercher tous les professeurs du répertoires et toutes les informations que l'on veut sur eux. 

url = "http://professeurs.uqam.ca/listeunite"
contenu = requests.get(url)
page = BeautifulSoup(contenu.text,"html.parser")

for ligne in page.find("div", id="contenu").find_all("li"):
	#print(ligne.a)

	
	url2 = "http://professeurs.uqam.ca" + ligne.a["href"]
	print(url2)

	donnees = requests.get(url2)
	page2 = BeautifulSoup(donnees.text,"html.parser")

	nomDesProfs = page2.find_all("td",class_="nom_professeur")
	#print(len(NomDesProfs))

	for nomProf in nomDesProfs:
		prof =[]
		#print(nomProf)

		url3 = "http://professeurs.uqam.ca" + nomProf.a["href"]
		#print(url3)

		professeur = requests.get(url3)
		page3 = BeautifulSoup(professeur.text,"html.parser")

		nomprenom = page3.find("h1").text.strip()	
		#print("*"*50)
		#print(nomprenom)
		prof.append(nomprenom)

		#Cette ligne sert à rester dans la classe row. Comme ça, même si les <p> sont décalés, on ne collecte pas l'information de trop qui se trouve aussi dans des <p>, mais non dans la class row. 
		for infos in page3.find_all("div",class_="row",limit=1):
		

		#infos = page3.find_all("p")
		
		#for info in infos:

			#if "Courriel" in info.text.strip():
				#courriel = info
			#else: 
				#courriel = "?"
		#print(telephone)
		#print(courriel)

#Aller chercher tout les éléments qui se trouvent dans de <p> dans le premier class row de la page où se trouvent les informations des professeurs. 
			departement = page3.find("p").text.strip()
			#print(departement) 
			prof.append(departement)

			poste = page3.find("p").find_next("p").text.strip()
			#print(poste)
			prof.append(poste[8:])

			courriel = page3.find("p").find_next("p").find_next("p").text.strip()
			#print(courriel)
			prof.append(courriel[10:])

			telephone = page3.find("p").find_next("p").find_next("p").find_next("p").text.strip()
			#print(telephone)
			prof.append(telephone[11:])

			local = page3.find("p").find_next("p").find_next("p").find_next("p").find_next("p").text.strip()
			#print(local)
			prof.append(local[7:])
#Je vais chercher des carathères en particulier pour que dans chque case de nom fichier csv, on ne voit pas toujours Téléphone: ou Courriel: 

			#p = soup.find_all('p')
			#paragraphs = []
			#for x in p:
    		#paragraphs.append(str(x))
			ldomaines = []
			for domaines in infos.find_all("ul"):
				#domaines.get_text()
				#print(domaines.text.strip())
				#domaines1 = domaines.encode(encoding='utf-8')
				#domaines.text.strip() = expertises
				ldomaines.append(domaines.text.strip())
				for element in ldomaines: 
					element.replace("\n",",")
			#print(ldomaines)

			prof.append(ldomaines)
#Ici, j'ai essayé d'enlever les \n qui n'arrêtaient pas d'apparaître dans mon texte. 

		#info = page3.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").text.strip()
		#print(info)

		#if page3.find("p").find_next("p").find_next("p").find_next("p").text.strip() == "Téléphone :":
			#print(telephone)

		#else:
			#print(...)
			print(prof)


			poupou = open(fichier,"a",encoding='utf-8')
			chat = csv.writer(poupou)
			chat.writerow(prof)



