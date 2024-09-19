import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def services_piechart():
    #plotly.express pie chart
    # Calculate the count of each unique value in the column
    value_counts = df['Primary streaming service'].value_counts()

    # Create a Pie chart using Plotly Express
    fig = px.pie(names=value_counts.index, values=value_counts.values, title='Primary Streaming Services')
    fig.update_layout(
    title=dict( font=dict(size=24)), autosize=True)
    st.plotly_chart(fig, use_container_width=True)

def music_effects_piechart():
    # Calculate the count of each unique value in the column
    value_counts = df['Music effects'].value_counts()

    # Create a Pie chart using Plotly Express
    fig = px.pie(names=value_counts.index, values=value_counts.values, title='Outcome of listening to music')
    fig.update_layout(
    title=dict( font=dict(size=24)), autosize=True)
    st.plotly_chart(fig, use_container_width=True)

def mh_issues_boxplot():
    df_long = pd.melt(df, id_vars=['Age'], value_vars=['Anxiety', 'Depression', 'Insomnia', 'OCD'],
            var_name='Condition', value_name='Level')
    fig = px.box(df_long, x='Condition', y='Level', title='Distribution of Conditions by Level')
    fig.update_layout(autosize=True, title=dict(font=dict(size=28)) )
    st.plotly_chart(fig)

def effects_by_issue():
    fig = make_subplots(rows=2, cols=2, start_cell="bottom-left", shared_xaxes=True, 
                    subplot_titles=['Depression', 'Anxiety','Insomnia',  'OCD'])

    filtered_df = df[(df['Depression'] > 7)]
    # Count the occurrences of each level of improvement for the filtered data
    improvement_counts = filtered_df['Music effects'].value_counts()

    # Create a bar chart
    fig.add_trace(go.Bar(x=improvement_counts.index,y=improvement_counts.values), 
                row=1, col=1)

    filtered_df = df[(df['Anxiety'] > 7)]
    # Count the occurrences of each level of improvement for the filtered data
    improvement_counts = filtered_df['Music effects'].value_counts()
    fig.add_trace(go.Bar( x=improvement_counts.index,y=improvement_counts.values),  
                row=1, col=2)

    filtered_df = df[(df['Insomnia'] > 7)]
    # Count the occurrences of each level of improvement for the filtered data
    improvement_counts = filtered_df['Music effects'].value_counts()
    fig.add_trace(go.Bar( x=improvement_counts.index,y=improvement_counts.values), 
                row=2, col=1)

    filtered_df = df[(df['OCD'] > 7)]
    # Count the occurrences of each level of improvement for the filtered data
    improvement_counts = filtered_df['Music effects'].value_counts()
    fig.add_trace(go.Bar( x=improvement_counts.index,y=improvement_counts.values),  
                row=2, col=2)
    fig.update_traces(showlegend=False)
    fig.update_layout(height=600, width=800,
                    title_text="Music Effects for different Mental Health Issues", title=dict(font=dict(size=28)))

  # Update y-axis range for both rows
    for row in [1, 2]:
        for col in [1, 2]:
            fig.update_yaxes(range=[0, 200], row=row, col=col)
    
    st.plotly_chart(fig) 

def services_piechart_by_age(age_filter):
    if age_filter == '10-20':
        age_data = df[(df['Age'] >= 10) & (df['Age'] <= 20)]
    if age_filter == '21-30':
        age_data = df[(df['Age'] >= 21) & (df['Age'] <= 30)]
    if age_filter == '31-40':
        age_data = df[(df['Age'] >= 31) & (df['Age'] <= 40)]
    if age_filter == '41-50':
        age_data = df[(df['Age'] >= 41) & (df['Age'] <= 50)]   
    value_counts = age_data['Primary streaming service'].value_counts()
    fig = px.pie(names=value_counts.index, values=value_counts.values, title='Primary Streaming Services')
    fig.update_layout(title=dict( font=dict(size=28)))
    st.plotly_chart(fig) 

def age_cond_barchart(cond_filter):
    avg_condition = df.groupby('Age')[cond_filter].mean().reset_index()
    fig = px.bar(avg_condition, x='Age', y=cond_filter, labels={'Age': 'Age', cond_filter: 'Average ' + cond_filter},
                 title="Mental Health Issue by Age")
    fig.update_layout(autosize=True, title=dict(font=dict(size=28)) )
    st.plotly_chart(fig)

def music_info():
    st.subheader("Music Information")
    col1, col2 = st.columns(2)
    with col1:
        music_effects_piechart()
    with col2: 
        services_piechart()
        

def mh_info():
    st.subheader("Mental Health Information")
    mh_issues_boxplot()
    effects_by_issue()


def interactive_info():
    st.subheader("Interactive Information")
    age_filter = st.selectbox(label='Choose an age group to view preferences',
        options=('10-20', '21-30', '31-40', '41-50'), label_visibility='collapsed')
    services_piechart_by_age(age_filter)
    cond_filter = st.radio(label='Choose which mental health issue you want to view',
        options=('Depression', 'Anxiety', 'Insomnia', 'OCD'), label_visibility='collapsed')
    age_cond_barchart(cond_filter)
    

@st.cache_data
def get_data():
    df = pd.read_csv('data/mxmh_survey_results.csv')
    df = df[df['Age'] <= 50]
    return df

# start of main page layout 
st.set_page_config(page_title = 'Music and Mental Health Dashboard',
                    layout='wide',
                    initial_sidebar_state="expanded"
)


st.title("Music and Mental Health Dashboard")
df = get_data()

with st.sidebar:
    st.subheader("Menu")
    selected = st.selectbox('  ',
        ['Home',
        'Music Information',
        'Mental Health Information',
        'Interactive Information']
    )

if selected == 'Home':
    st.subheader('Data file')
    st.write(df)
elif selected == 'Music Information':
    music_info()
elif selected == 'Mental Health Information':
    mh_info()
elif selected == 'Interactive Information':
    interactive_info()
