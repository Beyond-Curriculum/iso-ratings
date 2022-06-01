from numpy import place


class YearResults:

    def __init__(self, file):
        self.placeToStud = {}
        self.countryToStud = {}
        self.path = file

    def parse(self, file):
        file = open(file, 'r').readlines()
        arifcount = len(file)
        for it in range(1, arifcount, 5):
            place = int(file[it].split('\n')[0])
            country = file[it + 1].split('\n')[0]
            name = file[it + 2].split('\t')[0]
            score = float(file[it + 3])
            medal = file[it + 4].split('\n')[0]
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
        
    def main(self):
        self.parse(self.path)
        return self.build_rating_based_on_score()

def export_ratings_based_on_score(countries):
    BASE = 'data/informatics/'
    YEARS = '2021 2020 2019 2018 2017 2016 2015 2014 2013 2012 2011 2010'
    yearToPlace = {}
    for year in YEARS.split(' '):
        yr = YearResults(BASE + f'{year}.txt')
        placeToCountry, countryToPlace = yr.main()
        yearToPlace[year] = {}
        for country in countries:
            if country in countryToPlace:
                yearToPlace[year][country] = countryToPlace[country]
        yearToPlace[year]['total'] = len(countryToPlace.keys())
    return yearToPlace


o = export_ratings_based_on_score(('KZ', 'UZ', 'RU'))
#print(o)