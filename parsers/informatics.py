from numpy import place


class YearResults:

    def __init__(self, file):
        self.placeToStud = {}
        self.countryToStud = {}
        self.path = file

    def parse(self, file):
        file = open(file, 'r').readlines()
        arifcount = len(file)
        for it in range(0, arifcount, 1):
        	file[it] = file[it].split('\t')[0].split('\n')[0]
        for it in range(0, arifcount, 5):
        	place = int(file[it])
        	country = file[it + 1]
        	name = file[it + 2]
        	score = float(file[it + 3])
        	medal = file[it + 4]
        	if country not in self.countryToStud:
        		self.countryToStud[country] = []
        	student = {'place': place, 'name': name, 'country': country, 'score': score, 'medal': medal}
        	self.countryToStud[country].append(student)
        	self.placeToStud[place] = student
    
    def build_rating_based_on_score(self):
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = sum([student['score'] for student in students])/len(students)

        scores = list(set(countryToScore.values()))
        scores.sort(reverse=True)
        
        placeToCountry, countryToPlace = {}, {}
        for i, score in enumerate(scores):
            for country, val in countryToScore.items():
                if score == val:
                    if i+1 not in placeToCountry:
                        placeToCountry[i+1] = []
                    placeToCountry[i+1].append(country)
                    countryToPlace[country] = i+1
        return placeToCountry, countryToPlace
    
    def build_rating_based_on_place(self):
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = sum([student['place'] for student in students])/len(students)

        scores = list(set(countryToScore.values()))
        scores.sort(reverse=False)

        placeToCountry, countryToPlace = {}, {}
        for i, score in enumerate(scores):
            for country, val in countryToScore.items():
                if score == val:
                    if i+1 not in placeToCountry:
                        placeToCountry[i+1] = []
                    placeToCountry[i+1].append(country)
                    countryToPlace[country] = i+1
        return placeToCountry, countryToPlace
        
    def mainPlace(self):
        self.parse(self.path)
        return self.build_rating_based_on_place()
        
    def mainScore(self):
        self.parse(self.path)
        return self.build_rating_based_on_score()
	
def export_ratings_based_on_score(countries):
	BASE = 'data/informatics/'
	YEARS = '2021 2020 2019 2018 2017 2016 2015 2014 2013 2012 2011 2010'
	yearToPlace = {}
	for year in YEARS.split(' '):
		yr = YearResults(BASE + f'{year}.txt')
		placeToCountry, countryToPlace = yr.mainScore()
		yearToPlace[year] = {}
		for country in countries:
			if country in countryToPlace:
				yearToPlace[year][country] = countryToPlace[country]
		yearToPlace[year]['total'] = len(countryToPlace.keys())
	return yearToPlace

def export_ratings_based_on_place(countries):
	BASE = 'data/informatics/'
	YEARS = '2021 2020 2019 2018 2017 2016 2015 2014 2013 2012 2011 2010'
	yearToPlace = {}
	for year in YEARS.split(' '):
		yr = YearResults(BASE + f'{year}.txt')
		placeToCountry, countryToPlace = yr.mainPlace()
		yearToPlace[year] = {}
		for country in countries:
			if country in countryToPlace:
				yearToPlace[year][country] = countryToPlace[country]
		yearToPlace[year]['total'] = len(countryToPlace.keys())
	return yearToPlace


#o = export_ratings_based_on_score(('KZ', 'UZ', 'RU'))
#o = export_ratings_based_on_place(('KZ', 'UZ', 'RU'))
#print(o)