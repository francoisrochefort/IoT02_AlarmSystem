from fuzzywuzzy import process

#https://github.com/seatgeek/thefuzz

phrases = [u"quelle heure est-il?", 
           u"il est quelle heure?", 
           u"quel temps fait-il?", 
           u"quelles sont les prévision météo?", 
           u"quelles sont les prévisions de la météo?"]

maPhrase = u"quel temps il fait?"

(modele, score) = process.extractOne(maPhrase, phrases)
print(modele, score)



