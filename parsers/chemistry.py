# парсинг идет со скорборда

class YearResults:

    def __init__(self, file, isRoundsPresent):
        self.placeToStud = {}
        self.countryToStud = {}
        self.path = file
        self.isRoundsPresent = isRoundsPresent

    def parse_html(self, file):
        file = open(file, 'r').readlines()[0]
        rows = file.split('<tr>')
        for row in rows:
            elts = row.split('<td>')
            if len(elts) == 1: 
                continue
            place = int(elts[1].split('</td>')[0])
            country = elts[2].split('.svg')[0][-2:]
            name = elts[3].split('</td>')[0]
            score = float(elts[4].split('</td>')[0])
            if 'medal' in elts[5]: 
                medal = elts[5].split('medal">')[-1].split('</div>')[0]
            else:
                medal = None
            # print(place, country, name, score, medal)
            if country not in self.countryToStud:
                self.countryToStud[country] = []
            student = {'place': place, 'name': name, 'country': country, 'score': score, 'medal': medal}
            self.countryToStud[country].append(student)
            self.placeToStud[place] = student

    def parse_html_rounds(self, file):
        file = open(file, 'r').readlines()[0]
        rows = file.split('<tr>')
        for row in rows:
            elts = row.split('<td>')
            if len(elts) == 1: 
                continue
            place = int(elts[1].split('</td>')[0])
            country = elts[2].split('.svg')[0][-2:]
            if "link" in elts[3]:
                name = elts[3].split('link">')[1].split('</span>')[0]
            else:
                name = elts[3].split('</td>')[0]
            score = float(elts[6].split('</td>')[0])
            if 'medal' in elts[7]: 
                medal = elts[7].split('medal">')[-1].split('</div>')[0]
            else:
                medal = None
            if place:
                # print(elts)
                # print(place, country, name, score, medal)
                pass
            if country not in self.countryToStud:
                self.countryToStud[country] = []
            student = {'place': place, 'name': name, 'country': country, 'score': score, 'medal': medal}
            self.countryToStud[country].append(student)
            self.placeToStud[place] = student
    
    def build_rating_based_on_score(self):
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = sum([student['score'] for student in students])
        
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
        if self.isRoundsPresent:
            self.parse_html_rounds(self.path)
        else:
            self.parse_html(self.path)
        return self.build_rating_based_on_score()

def export_ratings_based_on_score(countries):
    BASE = 'data/chemistry/'
    YEARS = '2021|F 2020|F 2019|F 2018|T 2017|T 2016|T 2015|F 2014|T 2013|T 2010|T'
    # YEARS = '2018'
    yearToPlace = {}
    for year_and_bool in YEARS.split(' '):
        year, prebool = year_and_bool.split('|')
        if prebool == 'T': actbool = True
        else: actbool = False
        yr = YearResults(BASE + f'{year}.txt', actbool)
        placeToCountry, countryToPlace = yr.main()
        yearToPlace[year] = {}
        for country in countries:
            if country in countryToPlace: #funny - uzbekistan didn't participate in 2010
                yearToPlace[year][country] = countryToPlace[country]
        yearToPlace[year]['total'] = len(countryToPlace.keys())
    return yearToPlace

# 2021 - 21/79
# 2020 - 27/59
# 2019 - 35/80
# 2018 - 34/76
# 2017 - 29/76
# 2016 - 16/67
# 2015 - 14/75
# 2014 - 33/75
# 2013 - 15/73
# 2012 - no scores
# 2011 - no scores
# 2010 - 31/68

# o = export_ratings_based_on_score(('KZ', 'UZ', 'RU'))
# print(o)