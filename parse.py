
class YearResults:

    def __init__(self):
        self.placeToStud = {}
        self.countryToStud = {}
        pass

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
            print(place, country, name, score, medal)
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
                print(place, country, name, score, medal)
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
        
        for i, score in enumerate(scores):
            for country, val in countryToScore.items():
                if score == val:
                    break
            print(f'#{i+1}. {country}. {val}')
        
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
        self.parse_html_rounds('data/2010.html')
        self.build_rating_based_on_score()

yr = YearResults()
yr.main()

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
