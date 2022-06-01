class YearResults:

    def __init__(self, file, isRoundsPresent):
        self.placeToStud = {}
        self.countryToStud = {}
        self.path = file
        self.isRoundsPresent = isRoundsPresent

    def parse(self, file):
        file = open(file, 'r').readlines()
        arifcount = len(file)
        for it in range(0, arifcount, 5):
        	place = file[it]
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
            countryToScore[country] = sum([student['score'] for student in students])
        
        scores = list(countryToScore.values())
        scores.sort(reverse=True)
        
        placeToCountry, countryToPlace = {}, {}
        for i, score in enumerate(scores):
            for country, val in countryToScore.items():
                if score == val:
                    break
            # print(f'#{i+1}. {country}. {val}')
            placeToCountry[i+1] = country
            countryToPlace[country] = i+1
        return placeToCountry, countryToPlace
        
    def main(self):
        # self.parse_html('data/2021.html')
        # self.parse_html('data/2020.html')
        # self.parse_html('data/2019.html')
        # self.parse_html_rounds('data/2018.html')
        # self.parse_html_rounds('data/2017.html')
        # self.parse_html_rounds('data/2016.html')
        # self.parse_html('data/2015.html')
        # self.parse_html_rounds('data/2014.html')
        # self.parse_html_rounds('data/2013.html')
        # self.parse_html_rounds('data/2010.html')
        self.parse(self.path)
        return self.build_rating_based_on_score()

def export_ratings_based_on_score(countries):
    BASE = 'data/informatics/'
    YEARS = '2021|T 2020|T 2019|T 2018|T 2017|T 2016|T 2015|T 2014|T 2013|T 2012|T 2011|T 2010|T'
    # YEARS = '2018'
    yearToPlace = {}
    for year_and_bool in YEARS.split(' '):
        year, prebool = year_and_bool.split('|')
        if prebool == 'T': actbool = True
        else: actbool = False
        yr = YearResults(BASE + f'{year}.out', 1)
        placeToCountry, countryToPlace = yr.main()
        yearToPlace[year] = {}
        for country in countries:
            if country in countryToPlace:
                yearToPlace[year][country] = countryToPlace[country]
        yearToPlace[year]['total'] = len(countryToPlace.keys())
    return yearToPlace


#o = export_ratings_based_on_score(('KZ', 'UZ', 'RU'))
#print(o)