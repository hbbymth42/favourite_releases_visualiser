import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt
import plotly.graph_objects as go

st.set_page_config(page_title="Releases by Year", page_icon="📅")

st.markdown("# 📅 Releases by Year")
st.write(
        """
        Various Charts for my favourite music releases!
        """
)

graph_type = st.sidebar.radio(
        "Select a relevant decade:",
        ["All", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
)

conn = st.connection('favouritemusic_db', type='sql')

releases = ((conn.query("""
                        SELECT DISTINCT r.release_title
                                      , a.artist_name
                                      , r.release_type
                                      , r.release_date
                        FROM releases r
                        INNER JOIN releases_artists ra
                                ON r.release_mbid = ra.release_mbid
                        INNER JOIN artists a
                                ON ra.artist_mbid = a.artist_mbid
                        ORDER BY r.release_date, r.release_title, a.artist_name
                        """))
            .assign(release_date = lambda x: pd.to_datetime(x['release_date'], format='%Y-%m-%d'),
                    release_year = lambda x: x['release_date'].dt.year,
                    release_decade = lambda x: (np.floor(x['release_year']/10).astype(int) * 10).astype(str) + 's')
            )

releases_decade = (releases
                   [['release_title', 'release_year', 'release_decade']]
                   .drop_duplicates()
                   .value_counts(['release_decade', 'release_year'])
                   .reset_index()
                   .sort_values(by=['release_decade', 'release_year'], ignore_index=True, ascending=True)
                   )



if graph_type != "All": 
    filtered_releases = releases.query(f"release_decade == '{graph_type}'")
    if filtered_releases.shape[0] == 0:
        st.write("No Releases from this Decade! Please select another Decade.")
    else:
        filtered_releases_yearly_count = (releases_decade
                                          .query(f"release_decade == '{graph_type}'")
                                          [['release_year','count']]
                                          .drop_duplicates()
                                          .sort_values(by='release_year', ignore_index=True, ascending=True)
                                          )
        bar_chart = go.Figure(go.Bar(
                                x=filtered_releases_yearly_count['count'],
                                y=filtered_releases_yearly_count['release_year'],
                                orientation='h',
                                marker_color="#d2ff4d",
                                hoverlabel=dict(
                                    font=dict(
                                        color="#1b081b"
                                        ),
                                    bordercolor="#1b081b"
                                    ),
                                )
                              )
        bar_chart.update_layout(
                plot_bgcolor="#1b081b",
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(
                    showgrid=True,
                    gridcolor="#dfff80",
                    tickfont_color="#1b081b",
                    zeroline=True,
                    zerolinecolor="#dfff80",
                    dtick=1,
                    ),
                yaxis=dict(
                    tickfont_color="#1b081b",
                    type='category',
                    )
            )
        st.plotly_chart(bar_chart, use_container_width=True)

        st.data_editor(
                filtered_releases[['release_title', 'artist_name', 'release_type', 'release_date']],
                column_config={
                    "release_title": st.column_config.TextColumn(
                        "Release",
                        help="Name of Music Release",
                        ),
                    "artist_name": st.column_config.TextColumn(
                        "Artist",
                        help="Name of Music Artist",
                        ),
                    "release_type": st.column_config.TextColumn(
                        "Release Type",
                        help="Type of Release (typically, Format of Release)",
                        ),
                    "release_date": st.column_config.DateColumn(
                        "Release Date",
                        help="Date of Release",
                        format="YYYY-MM-DD",
                        )
                    },
                hide_index=True,
                use_container_width=True,
                disabled=True,
                )
else:
    decades_count = (releases_decade
                     [['release_decade', 'count']]
                     .groupby(by='release_decade')
                     .sum()
                     .reset_index()
                     .sort_values(by=['release_decade'], ascending=True)
                     )
    bar_chart = go.Figure(go.Bar(
                            y=decades_count['count'],
                            x=decades_count['release_decade'],
                            orientation='v',
                            marker_color="#d2ff4d",
                            hoverlabel=dict(
                                font=dict(
                                    color="#1b081b"
                                    ),
                                bordercolor="#1b081b"
                                )
                            )
                          )
    bar_chart.update_layout(
            plot_bgcolor="#1b081b",
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis=dict(
                showline=False,
                gridcolor="#dfff80",
                tickfont_color="#1b081b",
                zerolinecolor="#dfff80",
                ),
            xaxis=dict(
                tickfont_color="#1b081b",
                )
        )
    st.plotly_chart(bar_chart, use_container_width=True)

    st.data_editor(
            releases[['release_title', 'artist_name', 'release_type', 'release_date']],
            column_config={
                "release_title": st.column_config.TextColumn(
                    "Release",
                    help="Name of Music Release",
                    ),
                "artist_name": st.column_config.TextColumn(
                    "Artist",
                    help="Name of Music Artist",
                    ),
                "release_type": st.column_config.TextColumn(
                    "Release Type",
                    help="Type of Release (typically, Format of Release)",
                    ),
                "release_date": st.column_config.DateColumn(
                    "Release Date",
                    help="Date of Release",
                    format="YYYY-MM-DD",
                    )
                },
            hide_index=True,
            use_container_width=True,
            disabled=True,
            )
