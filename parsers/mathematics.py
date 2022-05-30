
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
        file = open(file, 'r',encoding="utf8").readlines()[0]
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
        if self.isRoundsPresent:
            self.parse_html_rounds(self.path)
        else:
            self.parse_html(self.path)
        return self.build_rating_based_on_score()

def export_ratings_based_on_score(countries):
    BASE = 'data/mathematics/'
    YEARS = '2021|T 2020|T 2019|T 2018|T 2017|T 2016|T 2015|T 2014|T 2013|T 2012|T 2011|T 2010|T'
    # YEARS = '2018'
    yearToPlace = {}
    for year_and_bool in YEARS.split(' '):
        year, prebool = year_and_bool.split('|')
        if prebool == 'T': actbool = True
        else: actbool = False
        yr = YearResults(BASE + f'{year}.html', actbool)
        placeToCountry, countryToPlace = yr.main()
        yearToPlace[year] = {}
        for country in countries:
            if country in countryToPlace:
                yearToPlace[year][country] = countryToPlace[country]
        yearToPlace[year]['total'] = len(countryToPlace.keys())
    return yearToPlace

# 2021 - 
# 2020 - 
# 2019 - 
# 2018 - 
# 2017 - 
# 2016 - 
# 2015 - 
# 2014 - 
# 2013 - 
# 2012 - 
# 2011 - 
# 2010 - 

# o = export_ratings_based_on_score(('KZ', 'HK', 'IN'))
# print(o)