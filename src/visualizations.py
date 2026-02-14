import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_missions_by_country_map(df: pd.DataFrame) -> px.choropleth:
    """Create a choropleth map showing space missions by country."""
    df['Country'] = df['Location'].str.split(', ').str[-1]
    missions_by_country = df['Country'].value_counts().reset_index()
    missions_by_country.columns = ['Country', 'Missions']

    fig = px.choropleth(
        missions_by_country,
        locations='Country',
        locationmode='country names',
        color='Missions',
        title='Space Missions by Country',
        color_continuous_scale='YlOrRd'
    )

    fig.update_layout(
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type='natural earth',
            landcolor='rgb(240, 240, 245)',
            oceancolor='rgb(220, 235, 250)',
            showocean=True,
            showcountries=True,
            countrycolor='rgba(100, 100, 100, 0.5)',
            countrywidth=0.5
        ),
        title=dict(
            text='Space Missions by Country',
            x=0.45,
            xanchor='center',
            font=dict(size=24, color='#333', family='Arial Black')
        ),
        coloraxis_colorbar=dict(
            title=dict(text='Missions', font=dict(size=14)),
            thickness=20,
            len=0.8,
            bgcolor='rgba(255,255,255,0.8)',
            borderwidth=1
        ),
        margin=dict(l=10, r=10, t=60, b=10),
        height=550,
        width=1100
    )

    fig.update_traces(
        hovertemplate='<b>%{location}</b><br>Missions: %{z}<extra></extra>',
        marker_line_color='white',
        marker_line_width=0.5
    )

    return fig


def create_company_activity_heatmap(df: pd.DataFrame, top_n: int = 20) -> go.Figure:
    """Create a heatmap showing which companies were active in which years."""
    df = df.copy()
    df['Year'] = df['Date'].apply(lambda x: x.year)

    # Get top N companies by total missions
    top_companies = df['Company'].value_counts().head(top_n).index.tolist()
    df_filtered = df[df['Company'].isin(top_companies)]

    # Create pivot table: companies vs years
    pivot = df_filtered.pivot_table(
        index='Company',
        columns='Year',
        values='Mission',
        aggfunc='count',
        fill_value=0
    )

    pivot['Total'] = pivot.sum(axis=1)
    pivot = pivot.sort_values('Total', ascending=True).drop('Total', axis=1)

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='YlOrRd',
        hovertemplate='<b>%{y}</b><br>Year: %{x}<br>Missions: %{z}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='Company Activity Timeline',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#333')
        ),
        xaxis=dict(
            title='Year',
            tickfont=dict(size=15),
            dtick=5
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=15)
        ),
        height=600,
        margin=dict(l=150, r=20, t=60, b=60)
    )

    return fig

def create_histogram(df, column):
    fig = px.histogram(df, x=column, nbins=20)
    return fig