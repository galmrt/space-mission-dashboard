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
    """Create a heatmap showing which companies were active in which years.
    Shows top_n companies by total missions in descending order."""
    df = df.copy()
    df['Year'] = df['Date'].apply(lambda x: x.year)

    top_companies = df['Company'].value_counts().head(top_n).index.tolist()
    df_filtered = df[df['Company'].isin(top_companies)]

    pivot = df_filtered.pivot_table(
        index='Company',
        columns='Year',
        values='Mission',
        aggfunc='count',
        fill_value=0
    )

    pivot['Total'] = pivot.sum(axis=1)
    pivot = pivot.sort_values('Total', ascending=True)
    totals = pivot['Total'].values
    pivot = pivot.drop('Total', axis=1)

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='YlOrRd',
        hovertemplate='<b>%{y}</b><br>Year: %{x}<br>Missions: %{z}<extra></extra>',
        colorbar=dict(
            title=dict(text='Missions', font=dict(size=14)),
            bgcolor='rgba(255,255,255,0.8)',
            borderwidth=1, 
        )
    ))

    max_year = pivot.columns.max()
    for company, total in zip(pivot.index, totals):
        fig.add_annotation(
            x=max_year + 2,
            y=company,
            text=f"{int(total)}",
            showarrow=False,
            font=dict(size=15, color='#333'),
            xanchor='left'
        )

    fig.add_annotation(
        x=max_year + 2,
        y=1.06,
        yref='paper',
        text="Total",
        showarrow=False,
        font=dict(size=15, color='#333'),
        xanchor='left'
    )

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
            dtick=5,
            range=[pivot.columns.min() - 0.5, max_year + 6]
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=15)
        ),
        height=600,
        margin=dict(l=150, r=80, t=60, b=60)
    )

    return fig

def create_histogram(df, column):
    """Create a styled histogram for the given column."""
    df = df.copy()

    # Special handling for Time column
    if column == 'Time':
        df['Hour'] = df['Time'].apply(lambda x: int(str(x).split(':')[0]) if pd.notna(x) else None)
        df = df.dropna(subset=['Hour'])

        fig = px.histogram(
            df,
            x='Hour',
            nbins=24,
            color_discrete_sequence=['#4C78A8'],
            range_x=[-0.5, 23.5]
        )

        fig.update_layout(
            xaxis=dict(
                title='Hour of Day',
                tickmode='array',
                tickvals=list(range(0, 24)),
                ticktext=[f'{h:02d}:00' for h in range(0, 24)],
                range=[-0.5, 23.5]
            )
        )
        title_text = 'Distribution of Launch Times (by Hour)'
    elif column == 'Company':
        company_counts = df['Company'].value_counts()
        companies_over_100 = company_counts[company_counts > 50].index.tolist()
        df = df[df['Company'].isin(companies_over_100)]

        fig = px.histogram(
            df,
            x=column,
            color_discrete_sequence=['#4C78A8']
        )
        title_text = f'Distribution of {column} (50+ launches)'
    elif column == 'Rocket':
        rocket_counts = df['Rocket'].value_counts()
        rockets_over_50 = rocket_counts[rocket_counts > 50].index.tolist()
        df = df[df['Rocket'].isin(rockets_over_50)]

        fig = px.histogram(
            df,
            x=column,
            color_discrete_sequence=['#4C78A8']
        )
        title_text = f'Distribution of {column} (50+ launches)'
    else:
        fig = px.histogram(
            df,
            x=column,
            nbins=25,
            color_discrete_sequence=['#4C78A8']
        )
        title_text = f'Distribution of {column}'

    fig.update_traces(
        marker_line_color='white',
        marker_line_width=1,
        opacity=0.85,
        hovertemplate=f'<b>{column}</b>: %{{x}}<br>Count: %{{y}}<extra></extra>'
    )

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#333')
        ),
        xaxis=dict(
            tickfont=dict(size=12),
            gridcolor='rgba(200, 200, 200, 0.3)'
        ),
        yaxis=dict(
            title='Count',
            tickfont=dict(size=12),
            gridcolor='rgba(200, 200, 200, 0.3)'
        ),
        bargap=0.05,
        plot_bgcolor='rgba(250, 250, 250, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        margin=dict(l=60, r=30, t=60, b=60)
    )

    return fig