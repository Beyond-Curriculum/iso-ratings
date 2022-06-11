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
        self.parser = parser.export_ratings_based_on_score
        self.subject = subject
        self.subjToOl = {'chemistry': 'IChO', 'mathematics': 'IMO', 'informatics': 'IOI', 'biology': 'IBO', 'physics': 'IPhO'}

    def _update_fig(self, figure, title, xAxis, yAxis, row=None, col=None):
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
                    autorange='reversed',
                    # range=[120,-15],
                    title=yAxis,
                    showgrid=False,
                    zeroline=False,
                    showline=True,
                    showticklabels=True,
                    mirror=True,
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


    def _create_trace(self, xVals, yVals, country, color):
        if country in {'KZ', 'total'}:
            return go.Scatter(x=xVals, y=yVals, mode='markers+lines+text', name=country, text=yVals, marker_color=color, textposition="top center")
        else:
            return go.Scatter(x=xVals, y=yVals, mode='markers+lines', name=country, text=yVals, marker_color=color)

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



# chemObj = SubjectRating(parsers.chemistry, 'chemistry')
# chemObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# chemObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# chemObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')

# mathObj = SubjectRating(parsers.mathematics, 'mathematics')
# mathObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# mathObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# mathObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')

# csObj = SubjectRating(parsers.informatics, 'informatics')
# csObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# csObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# csObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')

# physObj = SubjectRating(parsers.physics, 'physics')
# physObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# physObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# physObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')

# bioObj = SubjectRating(parsers.biology, 'biology')
# bioObj.plot(('KZ', 'UZ', 'RU', 'total'), 'score')
# bioObj.plot(('KZ', 'UZ', 'RU', 'total'), 'medals')
# bioObj.plot(('KZ', 'UZ', 'RU', 'total'), 'position')


class CombinedPlot(SubjectRating):

    def __init__(self):
        self.parsers = {'score' : {'chem': parsers.chemistry, 'cs': parsers.informatics, 'math': parsers.mathematics,  'bio': parsers.biology},
            'medals' : {'chem': parsers.chemistry, 'cs': parsers.informatics, 'math': parsers.mathematics, 'bio': parsers.biology, 'phys': parsers.physics},
            'position' : {'chem': parsers.chemistry, 'cs': parsers.informatics, 'math': parsers.mathematics, 'bio': parsers.biology, 'phys': parsers.physics}}
        # self.subjToData = {}
        self.subplotTitles = {'chem': 'Командный рейтинг на IChO',
                                'math': 'Командный рейтинг на IMO',
                                'cs': 'Командный рейтинг на IOI',
                                'phys': 'Командный рейтинг на IPhO',
                                'bio': 'Командный рейтинг на IBO'}

        self.modeToTitle = {
            'score': 'Рейтинг по сумме баллов, набранных учениками',
            'medals': 'Рейтинг по медалям (по олимпийской системе)',
            'position': 'Рейтинг по положению учеников в абсолютном рейтинге'
        }

    def plot(self, countries, colors, mode):
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
        for subj, data in subjToData.items():
            subplot_titles.append(self.subplotTitles[subj])
            traces = []
            for i, country in enumerate(countries):
                xVals, yVals = [], []
                for year, data in subjToData[subj].items():
                    if country in data:
                        xVals.append(int(year))
                        yVals.append(data[country])
                trace = self._create_trace(xVals, yVals, country, colors[i])
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
            fig.update_yaxes(range=[total+10,-15], row=i//2+1, col=i%2+1)

        factor = (len(self.parsers[mode]))//2+(len(self.parsers[mode]))%2
        fig.update_layout(height=360*factor)
        fig.write_image(f'exports/svg/total-{mode}.svg')
        fig.write_image(f'exports/pdf/total-{mode}.pdf')
        fig.write_image(f'exports/jpg/total-{mode}.jpg', scale=5.0)



    def main(self, countries, colors):
        self.plot(countries, colors, 'score')
        self.plot(countries, colors, 'medals')
        self.plot(countries, colors, 'position')
    

combObj = CombinedPlot()
# combObj.main(('KZ', 'UZ', 'RU', 'total'), colors = ['#090C9B', '#09814A', '#EF3E36', '#242423'])
combObj.main(('KZ', 'RU', 'total'), colors = ['#090C9B', '#EF3E36', '#242423'])