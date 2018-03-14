#coding: utf-8

### BONJOUR, ICI Jean-Hugues ###
### Comme toujours, mes notes et corrections sont précédées de trois dièses ###

### Bravo! Ton code est très bien commenté!

import csv
import requests 
from bs4 import BeautifulSoup

### Je modifie le nom du fichier CSV pour faire des tests

fichier = "profsUQAM_JHR.csv"

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

### Ici, c'est toujours une bonne habitude à prendre que d'enregistrer l'URL
### Ça peut être pratique pour régler des bogues
### Mais aussi pour faire des vérifications pour voir s'il n'y a pas d'erreurs dans nos données
		prof.append(url3)

		professeur = requests.get(url3)
		page3 = BeautifulSoup(professeur.text,"html.parser")

		nomprenom = page3.find("h1").text.strip()	
		print("*"*50)
		print(nomprenom)
		prof.append(nomprenom)

### Dans la section qui suit, tu assumes que le 3e <p> contient l'adresse courriel et le 4e le numéro de téléphone
### Ce n'est pas toujours le cas
### Il est important de mettre la bonne donnée à la bonne place
### S'il y a une adresse courriel, on la met dans la variable «adresse»
### S'il n'y en a pas, la variable «adresse» ne contient rien ou contient «?» ou «aucune».

### Voici une proposition de solution pour y parvenir

### En fait, il faut passer au travers de tous les <p> pour chacune des informations qu'on veut colliger
### Commençons mettre tous ces <p> dans une liste, comme tu le faisais déjà dans une version antérieure de ton script

		infos = page3.find_all("p")

### Puis, on vérifie si la première information qu'on cherche, le poste, s'y trouve
### Si elle y est, on sort de la boucle avec la commande «break», que je n'ai pas eu le temps de vous montrer (il y a tant de choses)
### Si elle n'y est pas, on met «?» dans la variable «poste»
### Après avoir tout vérifié, on ajoute le contenu de notre variable «poste» à la liste «prof» contenant toutes les infos sur le prof où on est rendu

		for info in infos:
			if "Poste :" in info.text:
				poste = info.text.split(":")
				poste = poste[1].strip()
				break
			else:
				poste = "?"
		prof.append(poste)

### Puis on recommence avec le courriel

		for info in infos:
			if "Courriel :" in info.text:
				courriel = info.text.split(":")
				courriel = courriel[1].strip()
				break
			else:
				courriel = "?"
		prof.append(courriel)

### Puis avec le numéro de téléphone

		for info in infos:
			if "Téléphone :" in info.text:
				tel = info.text.split(":")
				tel = tel[1].strip()
				break
			else:
				tel = "?"
		prof.append(tel)

### Puis avec le numéro de local

		for info in infos:
			if "Local :" in info.text:
				local = info.text.split(":")
				local = local[1].strip()
				break
			else:
				local = "?"
		prof.append(local)

### Certains profs ont un autre courriel; récoltons-le

		for info in infos:
			if "Autre courriel :" in info.text:
				autreCourriel = info.text.split(":")
				autreCourriel = autreCourriel[1].strip()
				break
			else:
				autreCourriel = "?"
		prof.append(autreCourriel)

### Certains extravagants affichent même un autre numéro de téléphone; récoltons-le également

		for info in infos:
			if "Autre téléphone :" in info.text:
				autreTel = info.text.split(":")
				autreTel = autreTel[1].strip()
				break
			else:
				autreTel = "?"
		prof.append(autreTel)

# 		#Cette ligne sert à rester dans la classe row. Comme ça, même si les <p> sont décalés, on ne collecte pas l'information de trop qui se trouve aussi dans des <p>, mais non dans la class row. 
# 		# for infos in page3.find_all("div",class_="row",limit=1):

# 		# infos = page3.find_all("p")
# 		# print(len(infos))

# 		# for info in infos:
# 			# print(info.text)
# 			# print(telephone)
# 			# print(courriel)


# #Aller chercher tout les éléments qui se trouvent dans de <p> dans le premier class row de la page où se trouvent les informations des professeurs. 

### Même si c'est théorique, puisque je te propose une autre solution
### Sache qu'on peut faire «find("p")» sur infos in non sur page3 puisqu'on se trouve dans une boucle
### où la variable «info» contient du HTML sur lequel on peut aussi faire des ".find()" avec BeautifulSoup

# 			departement = infos.find("p").text.strip()
# 			# departement = page3.find("p").text.strip()
# 			#print(departement) 
# 			prof.append(departement)

# 			poste = infos.find("p").find_next("p").text.strip()
# 			# poste = page3.find("p").find_next("p").text.strip()
# 			#print(poste)
# 			prof.append(poste[8:])

# 			courriel = infos.find("p").find_next("p").find_next("p").text.strip()
# 			# courriel = page3.find("p").find_next("p").find_next("p").text.strip()
# 			#print(courriel)
# 			prof.append(courriel[10:])

# 			telephone = infos.find("p").find_next("p").find_next("p").find_next("p").text.strip()
# 			# telephone = page3.find("p").find_next("p").find_next("p").find_next("p").text.strip()
# 			#print(telephone)
# 			prof.append(telephone[11:])

# 			local = infos.find("p").find_next("p").find_next("p").find_next("p").find_next("p").text.strip()
# 			# local = page3.find("p").find_next("p").find_next("p").find_next("p").find_next("p").text.strip()
# 			#print(local)
# 			prof.append(local[7:])

### Tu as bien réussi d'aller chercher les domaines d'expertise.
### Mais ici, je vais ajuster ton code aux changements que j'ai effectués
### Et je vais aussi ajouter chaque expertise individuellement dans la liste «prof»
### Ainsi, chaque ligne de ton CSV aura le même nombre de colonnes

		h1 = page3.find_all("h1")
		# print(len(h1))

		if len(h1) > 1:
			expertise = h1[1].find_next("ul").find_all("li")
			if len(expertise) == 1:
				expertise1 = expertise[0].text
				expertise2 = "?"
				expertise3 = "?"
				expertise4 = "?"
				expertise5 = "?"
			if len(expertise) == 2:
				expertise1 = expertise[0].text
				expertise2 = expertise[1].text
				expertise3 = "?"
				expertise4 = "?"
				expertise5 = "?"
			if len(expertise) == 3:
				expertise1 = expertise[0].text
				expertise2 = expertise[1].text
				expertise3 = expertise[2].text
				expertise4 = "?"
				expertise5 = "?"
			if len(expertise) == 4:
				expertise1 = expertise[0].text
				expertise2 = expertise[1].text
				expertise3 = expertise[2].text
				expertise4 = expertise[3].text
				expertise5 = "?"
			if len(expertise) == 5:
				expertise1 = expertise[0].text
				expertise2 = expertise[1].text
				expertise3 = expertise[2].text
				expertise4 = expertise[3].text
				expertise5 = expertise[4].text
		else:
			expertise1 = "?"
			expertise2 = "?"
			expertise3 = "?"
			expertise4 = "?"
			expertise5 = "?"

		prof.append(expertise1)
		prof.append(expertise2)
		prof.append(expertise3)
		prof.append(expertise4)
		prof.append(expertise5)

		print(prof)

# #Je vais chercher des carathères en particulier pour que dans chque case de nom fichier csv, on ne voit pas toujours Téléphone: ou Courriel: 

# 			#p = soup.find_all('p')
# 			#paragraphs = []
# 			#for x in p:
#     		#paragraphs.append(str(x))
# 		ldomaines = []
# 		for domaines in infos.find_all("ul"):
# 			#domaines.get_text()
# 			#print(domaines.text.strip())
# 			#domaines1 = domaines.encode(encoding='utf-8')
# 			#domaines.text.strip() = expertises
# 			ldomaines.append(domaines.text.strip())
# 			for element in ldomaines: 
# 				element.replace("\n",",")
# 		print(len(ldomaines))

# 			prof.append(ldomaines)
# #Ici, j'ai essayé d'enlever les \n qui n'arrêtaient pas d'apparaître dans mon texte. 

# 		#info = page3.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").text.strip()
# 		#print(info)

# 		#if page3.find("p").find_next("p").find_next("p").find_next("p").text.strip() == "Téléphone :":
# 			#print(telephone)

# 		#else:
# 			#print(...)
# 			print(prof)

		poupou = open(fichier,"a",encoding='utf-8')
		chat = csv.writer(poupou)
		chat.writerow(prof)