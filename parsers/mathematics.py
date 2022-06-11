
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
        i = 0
        for row in rows:
            elts = row.split('<td>')
            # print(elts)
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
            # print(student)
            # i += 1
            # if i == 10: break
            self.countryToStud[country].append(student)
            self.placeToStud[place] = student
    
    def _build_rating(self, data, reverse):
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
        # print(len(countryToPlace), len(list(placeToCountry.values())))
        return placeToCountry, countryToPlace

    def build_rating_based_on_score(self):
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = sum([student['score'] for student in students])
        return self._build_rating(countryToScore, True)
    
    def build_rating_based_on_position(self):
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = sum([student['place'] for student in students])
        return self._build_rating(countryToScore, False)
    
    def build_rating_based_on_medals(self):
        translate = {'золото': 'gold', 'серебро': 'silver', 'бронза': 'bronze'}
        countryToScore = {}
        for country, students in self.countryToStud.items():
            countryToScore[country] = {'gold': 0, 'silver': 0, 'bronze': 0}
            for student in students:
                medal = student['medal']
                if medal:
                    medal = translate[medal.lower()]
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
        
    def get_medal_statistics(self):
        placeToCountry, countryToPlace = self.build_rating_based_on_medals()
        KZ_place = countryToPlace['KZ']
        max_place = max(list(placeToCountry.keys()))
        total = len(countryToPlace)
        above = 0
        for i in range(1, KZ_place):
            above += len(placeToCountry[i])
        
        data_quant = {'kz_place': KZ_place, 'max_place': max_place, 'above': above, 'total': total}
        return data_quant
        
    def main(self):
        if self.isRoundsPresent:
            self.parse_html_rounds(self.path)
        else:
            self.parse_html(self.path)
    
    def plot(self, mode):
        if mode == 'score':
            return self.build_rating_based_on_score()
        elif mode == 'medals':
            return self.build_rating_based_on_medals()
        elif mode == 'position':
            return self.build_rating_based_on_position()

def create_ratings(countries, mode, years):
    BASE = 'data/mathematics/'
    # YEARS = '2021|T'
    yearToPlace = {}
    for year_and_bool in years.split(' '):
        year, prebool = year_and_bool.split('|')
        if prebool == 'T': actbool = True
        else: actbool = False
        yr = YearResults(BASE + f'{year}.txt', actbool)
        yr.main()
        placeToCountry, countryToPlace = yr.plot(mode)
        yearToPlace[year] = {}
        for country in countries:
            if country in countryToPlace:
                yearToPlace[year][country] = countryToPlace[country]
        yearToPlace[year]['total'] = len(countryToPlace.keys())
    return yearToPlace

YEARS = '2021|T 2020|T 2019|T 2018|T 2017|T 2016|T 2015|T 2014|T 2013|T 2012|T 2011|T 2010|T'

def export_ratings_based_on_score(countries):
    return create_ratings(countries, 'score', YEARS)

def export_ratings_based_on_medals(countries):
    return create_ratings(countries, 'medals', YEARS)

def export_ratings_based_on_position(countries):
    return create_ratings(countries, 'position', YEARS)
# o = export_ratings_based_on_score(('KZ', 'HK', 'IN'))
# print(o)

def export_medal_statistics():
    BASE = 'data/mathematics/'
    yearToData = {}
    for year_and_bool in YEARS.split(' '):
        year, prebool = year_and_bool.split('|')
        if prebool == 'T': actbool = True
        elif prebool == 'F': actbool = False
        yr = YearResults(BASE + f'{year}.txt', actbool)
        yr.main()
        data_elt = yr.get_medal_statistics()
        yearToData[year] = data_elt
    return yearToData        

# o = export_medal_statistics()
# print(o)