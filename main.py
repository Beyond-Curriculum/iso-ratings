import parsers.chemistry
import parsers.mathematics
import parsers.informatics
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

class SubjectRating:

    def __init__(self, parser, subject):
        self.parser = parser.export_ratings_based_on_score
        self.subject = subject
        self.subjToOl = {'chemistry': 'IChO', 'mathematics': 'IMO', 'informatics': 'IOI'}

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
            figure.update_layout(height=720)
            # figure.update_annotations(font=dict(size=16, color='#333333'),
            #     x=0.5, y=0.99, yanchor='top')


    def _create_trace(self, xVals, yVals, country, color):
        if country in {'KZ', 'total'}:
            return go.Scatter(x=xVals, y=yVals, mode='markers+lines+text', name=country, text=yVals, marker_color=color, textposition="top center")
        else:
            return go.Scatter(x=xVals, y=yVals, mode='markers+lines', name=country, text=yVals, marker_color=color)

    def plot(self, countries):
        # ---- тупой костыль (нужен чтобы на пдфках не было текста о непрогрузке mathjax)
        ran_fig = go.Figure(data = go.Scatter(x=[0,1,2,3], y=[0,1,4,9]))
        ran_fig.write_image('random.pdf')
        time.sleep(2) 
        # ---- конец тупого костыля

        yearToPlace = self.parser(countries)
        fig = go.Figure()
        traces = []
        for country in countries:
            xVals, yVals = [], []
            for year, data in yearToPlace.items():
                if country in data:
                    xVals.append(int(year))
                    yVals.append(data[country])
            trace = self._create_trace(xVals, yVals, country)
            traces.append(trace)
        
        for trace in traces: fig.add_trace(trace)
        self._update_fig(fig, f'Командный рейтинг на {self.subjToOl[self.subject]}', 'Год', 'Место в рейтинге')
        with open(f'exports/html/{self.subject}.html', 'w') as f:
            f.write(fig.to_html(include_plotlyjs='cdn'))
        fig.write_image(f'exports/svg/{self.subject}.svg')
        fig.write_image(f'exports/pdf/{self.subject}.pdf')
        fig.write_image(f'exports/jpg/{self.subject}.jpg', scale=5.0)



# chemObj = SubjectRating(parsers.chemistry, 'chemistry')
# chemObj.plot(('KZ', 'UZ', 'RU', 'total'))

# mathObj = SubjectRating(parsers.mathematics, 'mathematics')
# mathObj.plot(('KZ', 'UZ', 'RU', 'total'))

# csObj = SubjectRating(parsers.informatics, 'informatics')
# csObj.plot(('KZ', 'UZ', 'RU', 'total'))


class CombinedPlot(SubjectRating):

    def __init__(self):
        self.parsers = {'score' : {'chem': parsers.chemistry, 'math': parsers.mathematics, 'cs': parsers.informatics}}
        # self.subjToData = {}
        self.subplotTitles = {'chem': 'Командный рейтинг на IChO',
                                'math': 'Командный рейтинг на IMO',
                                'cs': 'Командный рейтинг на IOI'}

    def plot_on_score(self, countries, colors):
        subjToData = {}
        for subj, parser in self.parsers['score'].items():
            subjToData[subj] = parser.export_ratings_based_on_score(countries)

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
            print(xpos)
            fig.layout.annotations[i].update(x=xpos)
            # fig.update_layout(title_pad=dict(b=109))
            fig.update_annotations(borderpad=20)
        for i in range(numsubj):
            self._update_fig(fig, '', 'Год', 'Место в рейтинге', row=i//2+1, col=i%2+1)
        
        for i, (subj, data) in enumerate(subjToData.items()):
            total = max([data[year]['total'] for year in data.keys()])
            print(i//2+1, i%2+1)
            fig.update_yaxes(range=[total+10,-15], row=i//2+1, col=i%2+1)

        fig.write_image(f'exports/svg/total.svg')
        fig.write_image(f'exports/pdf/total.pdf')



    def main(self, countries, colors):
        self.plot_on_score(countries, colors)
    

combObj = CombinedPlot()
combObj.main(('KZ', 'UZ', 'RU', 'total'), colors = ['#090C9B', '#09814A', '#EF3E36', '#242423'])
combObj.main(('KZ', 'RU', 'total'), colors = ['#090C9B', '#EF3E36', '#242423'])