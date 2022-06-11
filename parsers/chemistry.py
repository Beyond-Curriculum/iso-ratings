# парсинг идет со скорборда

from venv import create


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
        
    def _build_rating(self, data, reverse):
        # data - countryToScore
        scores = list(set(data.values()))
        scores.sort(reverse=reverse)
        
        placeToCountry, countryToPlace = {}, {}
        for i, score in enumerate(scores):
            for country, val in data.items():
                if score == val:
                    if i+1 not in placeToCountry:
                        placeToCountry[i+1] = []
                    placeToCountry[i+1].append(country)
                    countryToPlace[country] = i+1
        return placeToCountry, countryToPlace
    
    def build_rating_based_on_score(self):
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = sum([student['score'] for student in students])
        return self._build_rating(countryToScore, True)
        # scores = list(set(countryToScore.values()))
        # scores.sort(reverse=True)
        
        # placeToCountry, countryToPlace = {}, {}
        # for i, score in enumerate(scores):
        #     for country, val in countryToScore.items():
        #         if score == val:
        #             if i+1 not in placeToCountry:
        #                 placeToCountry[i+1] = []
        #             placeToCountry[i+1].append(country)
        #             countryToPlace[country] = i+1
        # return placeToCountry, countryToPlace

    def build_rating_based_on_medals(self):
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = {'gold': 0, 'silver': 0, 'bronze': 0}
            for student in students:
                medal = student['medal']
                if medal:
                    medal = medal.lower()
                    countryToScore[country][medal] +=1

        # print(countryToScore)
        # Medal Sort
        rank = sorted(list(countryToScore.keys()), key = lambda e: (countryToScore[e]['gold'], countryToScore[e]['silver'], countryToScore[e]['bronze']))
        total = len(rank)
        placeToCountry = {}
        place = 1
        prevCountry = None
        for i in range(1, total+1):
            country = rank[total-i]
            if i == 1:
                placeToCountry[place] = [country,]
                prevCountry = country
            else:
                cur = countryToScore[country]
                prev = countryToScore[prevCountry]
                # print(cur, prev, country, prevCountry)
                if cur['gold'] == prev['gold']:
                    if cur['silver'] == prev['silver']:
                        if cur['bronze'] == prev['bronze']:
                            placeToCountry[place].append(country)
                        else:
                            place += 1
                            placeToCountry[place] = [country,]
                    else:
                        place += 1
                        placeToCountry[place] = [country,]
                else:
                    place += 1
                    placeToCountry[place] = [country,]
                prevCountry = country

        countryToPlace = {}
        for place, countries in placeToCountry.items():
            for country in countries:
                countryToPlace[country] = place
        return placeToCountry, countryToPlace
        
    def build_rating_based_on_position(self):
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = sum([student['place'] for student in students])
        return self._build_rating(countryToScore, False)

    def main(self, mode):
        if self.isRoundsPresent:
            self.parse_html_rounds(self.path)
        else:
            self.parse_html(self.path)
        if mode == 'score':
            return self.build_rating_based_on_score()
        elif mode == 'medals':
            return self.build_rating_based_on_medals()
        elif mode == 'position':
            return self.build_rating_based_on_position()

def create_ratings(countries, mode):
    BASE = 'data/chemistry/'
    YEARS = '2021|F 2020|F 2019|F 2018|T 2017|T 2016|T 2015|F 2014|T 2013|T 2010|T'
    # YEARS = '2018'
    yearToPlace = {}
    for year_and_bool in YEARS.split(' '):
        year, prebool = year_and_bool.split('|')
        if prebool == 'T': actbool = True
        else: actbool = False
        yr = YearResults(BASE + f'{year}.txt', actbool)
        placeToCountry, countryToPlace = yr.main(mode)
        yearToPlace[year] = {}
        for country in countries:
            if country in countryToPlace: #funny - uzbekistan didn't participate in 2010
                yearToPlace[year][country] = countryToPlace[country]
        yearToPlace[year]['total'] = len(countryToPlace.keys())
    return yearToPlace

def export_ratings_based_on_score(countries):
    return create_ratings(countries, 'score')

def export_ratings_based_on_medals(countries):
    return create_ratings(countries, 'medals')

def export_ratings_based_on_position(countries):
    return create_ratings(countries, 'position')

# o = export_ratings_based_on_medals(('KZ', 'UZ', 'RU'))
# print(o)

# o = export_ratings_based_on_position(('KZ', 'UZ', 'RU'))
# print(o)

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