import parsers.chemistry
import parsers.mathematics
import parsers.informatics
import plotly.graph_objects as go
import time

class SubjectRating:

    def __init__(self, parser, subject):
        self.parser = parser.export_ratings_based_on_score
        self.subject = subject
        self.subjToOl = {'chemistry': 'IChO', 'mathematics': 'IMO', 'informatics': 'IOI'}

    def _update_fig(self, figure, title, xAxis, yAxis):
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
            autosize=False,
            width = 1080,
            height = 480,
            margin=dict(
                # autoexpand=True,
                l=100,
                r=20,
                t=110,
            ),
            # showlegend=False,
            plot_bgcolor='white'
        )

        figure.update_layout(
            barmode='stack',
            title={
                'text': title,
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(color='#333333'), })



    def _create_trace(self, xVals, yVals, country):
        return go.Scatter(x=xVals, y=yVals, mode='markers+lines+text', name=country, text=yVals, textposition="top center")

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



chemObj = SubjectRating(parsers.chemistry, 'chemistry')
chemObj.plot(('KZ', 'UZ', 'RU', 'total'))

mathObj = SubjectRating(parsers.mathematics, 'mathematics')
mathObj.plot(('KZ', 'UZ', 'RU', 'total'))

csObj = SubjectRating(parsers.informatics, 'informatics')
csObj.plot(('KZ', 'UZ', 'RU', 'total'))