import streamlit as st
import pandas as pd
import plotly.graph_objects as pgo

st.set_page_config(page_title="Artists by Country", page_icon="🌐")

st.markdown("# Artists by Country")
st.sidebar.header("Artists by Country")
st.write(
        """
        A map of the number of artists I like by country!
        """
)

conn = st.connection('favouritemusic_db', type='sql')

artists_by_country = conn.query("""
                                SELECT c.country_code
                                     , c.country_name
                                     , COUNT(DISTINCT a.artist_name) AS num_artists
                                FROM countries c
                                INNER JOIN artists a
                                        ON c.country_code = a.artist_country
                                GROUP BY c.country_code, c.country_name
                                ORDER BY num_artists DESC
                                """)

country_choropleth = pgo.Figure(data=pgo.Choropleth(
        locations = artists_by_country['country_code'],
        z = artists_by_country['num_artists'],
        text = artists_by_country['country_name'],
        colorscale=[[0,'rgb(249, 255, 230)'],[1,'rgb(195, 255, 0)']],
        autocolorscale=False,
        reversescale=False,
        colorbar_title='Number of Artists',
        colorbar_title_font_weight=700,
        colorbar_bgcolor="#1b081b",
        colorbar_title_font_color="#dfff80",
        colorbar_tickcolor="#dfff80",
        colorbar_tickfont_color="#dfff80",
        colorbar_tickfont_weight=700,
        colorbar_bordercolor="#dfff80",
        colorbar_outlinecolor="#dfff80",
        hoverlabel_font_color="#1b081b",
        hoverlabel_bordercolor="#1b081b",
        marker_line_color="#dfff80",
        ))

country_choropleth.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgb(27, 8, 27)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=250
        )

st.plotly_chart(country_choropleth)

all_artists = ((conn.query("""
                         SELECT a.artist_name
                              , c.country_name
                         FROM artists a
                         LEFT JOIN countries c
                                ON a.artist_country = c.country_code
                         ORDER BY a.artist_name
                         """))
               .fillna(value='N/A')
               .rename(columns={'artist_name': 'Artist', 'country_name': 'Country'})
               )

st.dataframe(all_artists, use_container_width=True, hide_index=True)
