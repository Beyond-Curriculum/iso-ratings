import parsers.chemistry
import parsers.mathematics
import parsers.informatics
import parsers.physics
import parsers.biology
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

class SubjectRating:

    def __init__(self, parser, subject):
        self.modeToParser = {
            'score': parser.export_ratings_based_on_score,
            'medals': parser.export_ratings_based_on_medals,
            'position': parser.export_ratings_based_on_position
        }
        self.parser = parser
        self.subject = subject
        self.subjToOl = {'chemistry': 'IChO', 'mathematics': 'IMO', 'informatics': 'IOI', 'biology': 'IBO', 'physics': 'IPhO'}
        self.showPlaces = True

    def _update_fig(self, figure, title, xAxis, yAxis, row=None, col=None, autorange='reversed'):
        if not row:
            figure.update_layout(
                xaxis=dict(
                    title=xAxis,
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='rgb(51, 51, 51)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Helvetica',
                        size=12,
                        color='rgb(51, 51, 51)',
                    ),
                ),
                yaxis=dict(
                    autorange=autorange,
                    # range=[120,-15],
                    title=yAxis,
                    showgrid=False,
                    zeroline=False,
                    showline=True,
                    showticklabels=True,
                    mirror=True,
                    dtick=10,
                    linecolor='rgb(51, 51, 51)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Helvetica',
                        size=12,
                        color='rgb(51, 51, 51)',
                    ),
                ),
            )

        figure.update_layout(autosize=False,
                width = 1080,
                height = 480,
                margin=dict(
                    # autoexpand=True,
                    l=100,
                    r=20,
                    t=110,
                ),
                # showlegend=False,
                plot_bgcolor='white')

        figure.update_layout(
            barmode='stack',
            title={
                'text': title,
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(color='#333333'), })
    
        if row:
            figure.update_xaxes(title=xAxis,
                    showline=True,
                    showgrid=False,
                    mirror=True,
                    showticklabels=True,
                    linecolor='rgb(51, 51, 51)',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                        family='Helvetica',
                        size=12,
                        color='rgb(51, 51, 51)',
                    ), row=row, col=col)
            figure.update_yaxes(
                # autorange='reversed',
                title=yAxis,
                range=[120, -20],
                showgrid=False,
                zeroline=False,
                showline=True,
                showticklabels=True,
                mirror=True,
                dtick=10,
                linecolor='rgb(51, 51, 51)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Helvetica',
                    size=12,
                    color='rgb(51, 51, 51)',
                ), row=row, col=col)
            figure.update_layout(
                title={
                    'text': f"<b>{title}</b>",
                    'y':0.97,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': dict(color='#333333'), })
            
            # figure.update_annotations(font=dict(size=16, color='#333333'),
            #     x=0.5, y=0.99, yanchor='top')


    def _create_trace(self, xVals, yVals, country, color, showlegend=True):
        if country in {'KZ', 'total'} and self.showPlaces:
            return go.Scatter(x=xVals, y=yVals, mode='markers+lines+text', name=country, text=yVals, marker_color=color, textposition="top center", showlegend=showlegend)
        else:
            return go.Scatter(x=xVals, y=yVals, mode='markers+lines', name=country, text=yVals, marker_color=color, showlegend=showlegend)

    def plot(self, countries, mode):
        # ---- тупой костыль (нужен чтобы на пдфках не было текста о непрогрузке mathjax)
        ran_fig = go.Figure(data = go.Scatter(x=[0,1,2,3], y=[0,1,4,9]))
        ran_fig.write_image('random.pdf')
        time.sleep(2) 
        # ---- конец тупого костыля
        colors = ['#090C9B', '#09814A', '#EF3E36', '#242423']
        yearToPlace = self.modeToParser[mode](countries)
        fig = go.Figure()
        traces = []
        for country in countries:
            xVals, yVals = [], []
            for year, data in yearToPlace.items():
                if country in data:
                    xVals.append(int(year))
                    yVals.append(data[country])
            trace = self._create_trace(xVals, yVals, country, colors)
            traces.append(trace)
        
        for trace in traces: fig.add_trace(trace)
        self._update_fig(fig, f'Командный рейтинг на {self.subjToOl[self.subject]}', 'Год', 'Место в рейтинге')
        with open(f'exports/html/{self.subject}-{mode}.html', 'w') as f:
            f.write(fig.to_html(include_plotlyjs='cdn'))
        fig.write_image(f'exports/svg/{self.subject}-{mode}.svg')
        fig.write_image(f'exports/pdf/{self.subject}-{mode}.pdf')
        fig.write_image(f'exports/jpg/{self.subject}-{mode}.jpg', scale=5.0)

    def _create_bar_trace(self, xVals, yVals, color, name, showlegend=True):
        return go.Bar(x=xVals, y=yVals, marker_color=color, name=name, showlegend=showlegend)
    
    def _create_scatter_trace(self, xVals, yVals, color, name, showlegend=True):
        return go.Scatter(x=xVals, y=yVals, marker_color=color, name=name, showlegend=showlegend)

    def medal_stats(self):
        # ---- тупой костыль (нужен чтобы на пдфках не было текста о непрогрузке mathjax)
        ran_fig = go.Figure(data = go.Scatter(x=[0,1,2,3], y=[0,1,4,9]))
        ran_fig.write_image('random.pdf')
        time.sleep(2) 
        # ---- конец тупого костыля
        yearToStats = self.parser.export_medal_statistics()
        fig = go.Figure()
        keyToData = {}

        for key in {'kz_place', 'max_place', 'above', 'total'}:
            xVals, yVals = [], []
            # for year, stats in yearToStats.items():
            for year in sorted(yearToStats):
                stats = yearToStats[year]
                xVals.append(year)
                yVals.append(stats[key])
            keyToData[key] = xVals, yVals
        
        colors = ['#BBBDF6', '#6A4C93', '#DAFFED', '#63ADF2']
        fig.add_trace(self._create_bar_trace(keyToData['total'][0], keyToData['total'][1], colors[0], 'Кол-во стран-участниц'))
        fig.add_trace(self._create_bar_trace(keyToData['above'][0], keyToData['above'][1], colors[1], 'Кол-во стран, выше РК в рейтинге'))
        fig.add_trace(self._create_scatter_trace(keyToData['kz_place'][0], keyToData['kz_place'][1], colors[2], 'Место РК в рейтинге'))
        fig.add_trace(self._create_scatter_trace(keyToData['kz_place'][0], keyToData['max_place'][1], colors[3], 'Общее кол-во мест в рейтинге'))


        self._update_fig(fig, f'Медальный зачет на {self.subjToOl[self.subject]}', 'Год', '',  ) #autorange=True
        fig.update_layout(barmode='overlay')
            
        with open(f'exports/html/{self.subject}-medal-stats.html', 'w') as f:
            f.write(fig.to_html(include_plotlyjs='cdn'))
        fig.write_image(f'exports/svg/{self.subject}-medal-stats.svg')
        fig.write_image(f'exports/pdf/{self.subject}-medal-stats.pdf')
        fig.write_image(f'exports/jpg/{self.subject}-medal-stats.jpg', scale=5.0)




# chemObj = SubjectRating(parsers.chemistry, 'chemistry')
# # chemObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# # chemObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# # chemObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')
# chemObj.medal_stats()

# mathObj = SubjectRating(parsers.mathematics, 'mathematics')
# # mathObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# # mathObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# # mathObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')
# mathObj.medal_stats()

# csObj = SubjectRating(parsers.informatics, 'informatics')
# # csObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# # csObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# # csObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')
# csObj.medal_stats()

# physObj = SubjectRating(parsers.physics, 'physics')
# # physObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# # physObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# # physObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')
# physObj.medal_stats()

# bioObj = SubjectRating(parsers.biology, 'biology')
# # bioObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# # bioObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# # bioObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')
# bioObj.medal_stats()


class CombinedPlot(SubjectRating):

    def __init__(self):
        self.parsers = {'score' : {'chem': parsers.chemistry, 'cs': parsers.informatics, 'math': parsers.mathematics,  'bio': parsers.biology},
            'medals' : {'chem': parsers.chemistry, 'cs': parsers.informatics, 'math': parsers.mathematics, 'bio': parsers.biology, 'phys': parsers.physics},
            'position' : {'chem': parsers.chemistry, 'cs': parsers.informatics, 'math': parsers.mathematics, 'bio': parsers.biology}}
        # self.subjToData = {}
        self.subplotTitles = {'chem': 'Командный рейтинг на IChO',
                                'math': 'Командный рейтинг на IMO',
                                'cs': 'Командный рейтинг на IOI',
                                'phys': 'Командный рейтинг на IPhO',
                                'bio': 'Командный рейтинг на IBO'}

        self.modeToTitle = {
            'score': 'Рейтинг по сумме баллов, набранных учениками',
            'medals': 'Рейтинг по медалям (по олимпийской системе)',
            'medals-stats': 'Два взгляда на рейтинг по медалям (олимпийской системе)',
            'position': 'Рейтинг по положению учеников в абсолютном рейтинге'
        }

    def plot(self, countries, colors, mode, suffix):
        # ---- тупой костыль (нужен чтобы на пдфках не было текста о непрогрузке mathjax)
        ran_fig = go.Figure(data = go.Scatter(x=[0,1,2,3], y=[0,1,4,9]))
        ran_fig.write_image('random.pdf')
        time.sleep(2) 
        # ---- конец тупого костыля
        subjToData = {}
        for subj, parser in self.parsers[mode].items():
            if mode == 'score': rating = parser.export_ratings_based_on_score(countries)
            elif mode == 'medals': rating = parser.export_ratings_based_on_medals(countries)
            elif mode == 'position': rating = parser.export_ratings_based_on_position(countries)
            subjToData[subj] = rating

        subjToTraces = {}
        subplot_titles = []
        for i, (subj, data) in enumerate(subjToData.items()):
            if i == 0: showlegend=True
            else: showlegend=False
            subplot_titles.append(self.subplotTitles[subj])
            traces = []
            for i, country in enumerate(countries):
                xVals, yVals = [], []
                for year, data in subjToData[subj].items():
                    if country in data:
                        xVals.append(int(year))
                        yVals.append(data[country])
                trace = self._create_trace(xVals, yVals, country, colors[i], showlegend)
                traces.append(trace)
            subjToTraces[subj] = traces


        if (numsubj:=len(subjToData)) % 2 == 0:
            rows = numsubj // 2
        else:
            rows = numsubj // 2 + 1

        # fig = go.Figure()
        fig = make_subplots(rows=rows, cols=2, subplot_titles=subplot_titles)

        for i, (subj, traces) in enumerate(subjToTraces.items()):
            for trace in traces:
                fig.append_trace(trace, i // 2 + 1, i % 2 + 1)
            xpos = 0.23*(2.4* (i % 2) +1)
            # print(xpos)
            fig.layout.annotations[i].update(x=xpos)
            # fig.update_layout(title_pad=dict(b=109))
            fig.update_annotations(borderpad=20)
        for i in range(numsubj):
            self._update_fig(fig, self.modeToTitle[mode], 'Год', 'Место в рейтинге', row=i//2+1, col=i%2+1)
        
        for i, (subj, data) in enumerate(subjToData.items()):
            total = max([data[year]['total'] for year in data.keys()])
            # print(i//2+1, i%2+1)
            fig.update_yaxes(range=[total+10, 0], row=i//2+1, col=i%2+1)

        factor = (len(self.parsers[mode]))//2+(len(self.parsers[mode]))%2
        fig.update_layout(height=360*factor)
        fig.write_image(f'exports/svg/total-{mode}{suffix}.svg')
        fig.write_image(f'exports/pdf/total-{mode}{suffix}.pdf')
        fig.write_image(f'exports/jpg/total-{mode}{suffix}.jpg', scale=5.0)



    def main(self, countries, colors, showPlaces, suffix):
        self.showPlaces = showPlaces
        self.plot(countries, colors, 'score', suffix)
        self.plot(countries, colors, 'medals', suffix)
        self.plot(countries, colors, 'position', suffix)
    
    def medal_stats(self):
        # ---- тупой костыль (нужен чтобы на пдфках не было текста о непрогрузке mathjax)
        ran_fig = go.Figure(data = go.Scatter(x=[0,1,2,3], y=[0,1,4,9]))
        ran_fig.write_image('random.pdf')
        time.sleep(2) 
        # ---- конец тупого костыля

        subjToData = {}
        for subj, parser in self.parsers['medals'].items():
            rating = parser.export_medal_statistics()
            subjToData[subj] = rating


        subjToTraces = {}
        subplot_titles = []
        for i, (subj, data) in enumerate(subjToData.items()):
            if i == 0: showlegend=True
            else: showlegend=False
            subplot_titles.append(self.subplotTitles[subj])
            traces = []
            keyToData = {}
            for key in {'kz_place', 'max_place', 'above', 'total'}:
                xVals, yVals = [], []
                for year in sorted(data):
                    stats = data[year]
                    xVals.append(year)
                    yVals.append(stats[key])
                keyToData[key] = xVals, yVals
            
            # colors = ['#BBBDF6', '#6A4C93', '#DAFFED', '#63ADF2']
            colors = ['#BBBDF6', '#6A4C93', '#F72585', '#3993DD']
            traces.append(self._create_bar_trace(keyToData['total'][0], keyToData['total'][1], colors[0], 'Кол-во стран-участниц', showlegend))
            traces.append(self._create_bar_trace(keyToData['above'][0], keyToData['above'][1], colors[1], 'Кол-во стран, выше РК в рейтинге', showlegend))
            traces.append(self._create_scatter_trace(keyToData['kz_place'][0], keyToData['kz_place'][1], colors[2], 'Место РК в рейтинге', showlegend))
            traces.append(self._create_scatter_trace(keyToData['kz_place'][0], keyToData['max_place'][1], colors[3], 'Общее кол-во мест в рейтинге', showlegend))
            subjToTraces[subj] = traces


        if (numsubj:=len(subjToData)) % 2 == 0:
            rows = numsubj // 2
        else:
            rows = numsubj // 2 + 1

        # fig = go.Figure()
        fig = make_subplots(rows=rows, cols=2, subplot_titles=subplot_titles)

        for i, (subj, traces) in enumerate(subjToTraces.items()):
            for trace in traces:
                fig.append_trace(trace, i // 2 + 1, i % 2 + 1)
            xpos = 0.23*(2.4* (i % 2) +1)
            # print(xpos)
            fig.layout.annotations[i].update(x=xpos)
            # fig.update_layout(title_pad=dict(b=109))
            fig.update_annotations(borderpad=20)
        for i in range(numsubj):
            self._update_fig(fig, self.modeToTitle['medals-stats'], 'Год', 'Место в рейтинге', row=i//2+1, col=i%2+1)
        
        for i, (subj, data) in enumerate(subjToData.items()):
            total = max([data[year]['total'] for year in data.keys()])
            # print(i//2+1, i%2+1)
            fig.update_yaxes(range=[total+10,0], row=i//2+1, col=i%2+1)
        fig.update_layout(barmode='overlay')
        factor = (len(self.parsers['medals']))//2+(len(self.parsers['medals']))%2
        fig.update_layout(height=360*factor)
        fig.write_image(f'exports/svg/total-medal-stats.svg')
        fig.write_image(f'exports/pdf/total-medal-stats.pdf')
        fig.write_image(f'exports/jpg/total-medal-stats.jpg', scale=5.0)
    

combObj = CombinedPlot()
# combObj.main(('KZ', 'UZ', 'RU', 'total'), colors = ['#090C9B', '#09814A', '#EF3E36', '#242423'], showPlaces=False, suffix='-compare')
# combObj.main(('KZ', 'total'), colors = ['#090C9B', '#242423'], showPlaces=True, suffix='-absolute')
combObj.medal_stats()