import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import time

from sqlalchemy import create_engine
engine = create_engine("mysql+mysqlconnector://root:@localhost/airbnbdb")

#setupp streamlit page
icon = 'https://avatars.githubusercontent.com/u/698437?s=280&v=4'
st.set_page_config(page_title='AIRBNB',page_icon=icon, initial_sidebar_state='expanded',
                   layout='wide',menu_items={'about':'Developed by Kathiravan'})

title_text = '''<h1 style = 'font-size: 36px;color:#ff5a5f; text-align:center;'>AIRBNB</h1>
            <h2 style = 'font-size: 24px;color:#008891;text-align:center;'>Explore Your Dream Stays</h2> '''
st.markdown(title_text,unsafe_allow_html=True)

#set up home page and optionmenu
selected = option_menu("MainMenu",
                       options=["OVERVIEW","HOME","DISCOVER","INSIGHTS","ABOUT"],
                       icons=["list icon","house","globe","lightbulb","info-circle"],
                       default_index=1,
                       orientation="horizontal",
                       styles={"container":{"width": "100%","border": "1px ridge","background-color":"#EFC3CA",
                                            "primaryColor":"#E4080A"},
                                            "icon":{"color": "#060270", "font-size": "20px"}})
#SelectionMenu
if selected == "OVERVIEW":

    st.subheader(':red[Project Title :]')
    st.markdown('<h5> AIRBNB ANALYSIS',unsafe_allow_html=True)

    st.subheader(':red[Domain :]')
    st.markdown('<h5> Travel Industry, Property Management and Tourism',unsafe_allow_html=True)

    st.subheader(':red[Technologies :]')
    st.markdown('<h5> Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.',unsafe_allow_html=True)

    st.subheader(':red[Overview :]')
    bullet_points = [
    " Accessed and processed a JSON dataset containing Airbnb data from 2019",
    " Utilized Python for data transformation, ensuring it fit into a structured DataFrame",
    " Applied data preprocessing techniques, including cleaning and organizing, to enhance data quality and usability",
    " Leveraged the MySQL Python connector to establish a relational database",
    " Inserted the preprocessed data into appropriate tables within the database",
    " Developed an interactive dashboard using Streamlit, providing users with a platform to explore insights from the dataset",
    " Incorporated dynamic visualizations with Plotly to enrich the dashboard's analytical capabilities"
    ]

    for point in bullet_points:
        st.markdown(f'**> {point}**')
    
    # st.subheader(':blue[PowerBI :]')
    # st.markdown("**I demonstrated this project in PowerBI. Click the button below to get a glimpse of my dashboard.**")

    # image_path='airbnb (1).png'
    
    # if 'show_image' not in st.session_state:
    #     st.session_state = False

    # if st.button('View Dashboard'):
    #     st.session_state.show_image = not st.session_state.show_image

    # if st.session_state.show_image:
    #     st.image(image_path, caption='Power BI Dashboard', use_column_width=True)

    # st.subheader(':red[Request :]')
    # st.markdown('''**Please go through all the options with in this app**''')

#Home details

if selected == "HOME":
    col1,col2 =st.columns(2)

    with col2:
        st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExN292YXdvdjhnZ3djYXhhenhlMXkyem0xcDdwYjZzcWYxNTdoYmlyaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AErExHJVxRbkm5hPkB/giphy.gif",use_column_width=True)

    with col1:
        #st.write(' ')
        st.subheader(':red[Embark on your journey]')
        st.markdown('''**Start Your Adventure with Airbnb! Dive into detailed hotel listings and find the perfect accommodation for your next journey.**''')

        df_country = pd.read_sql_query('''SELECT DISTINCT country FROM hotels_info''',con=engine)
        selected_country = st.selectbox('Search Destinations',options=df_country['country'].tolist(),index=None)
        
        df_street = pd.read_sql_query('''SELECT DISTINCT street from hotels_info WHERE country = %s''',con=engine,
                                      params=[(selected_country,)])
        selected_street = st.selectbox('Search Street',options=df_street['street'].tolist(),index=None)

        df_hotels = pd.read_sql_query('''SELECT DISTINCT name FROM hotels_info WHERE street = %s''',con=engine,
                                      params=[(selected_street,)])
        selected_hname = st.selectbox('Search Hotel',options=df_hotels['name'].tolist(),index = None)

        st.write("Selected Accommodation:", f"<span style='color:#F8CD47'>{selected_hname}</span>", unsafe_allow_html=True)

    if selected_hname:
        more = st.button('click for details')

        if more:
            st.write(':red[Note: The information provided below is from the year 2019]')

            df = pd.read_sql_query('''SELECT name,listing_url,description,country,price,images,property_type,room_type,amenities,
                                        host_picture_url,host_name,host_url,host_about,host_location,overall_score,rating,number_of_reviews
                                        from hotels_info
                                        JOIN rooms_info ON hotels_info.id = rooms_info.id
                                        JOIN host_info ON hotels_info.id = host_info.id
                                    JOIN reviews_info ON hotels_info.id = reviews_info.id
                                    WHERE name = %s''',con=engine,params=[(selected_hname,)])
            extract_detail = df.to_dict(orient='records')[0]
            c1,c2 = st.columns(2)

            with c1:
                
                st.write('**:green[Hotel Details]**')
                st.write("**:violet[Name :]**", f'**{extract_detail['name']}**')
                st.write("**:violet[Website Url :]**",extract_detail['listing_url'])
                st.write("**:violet[Country :]**",f'**{extract_detail['country']}**')
                st.write("**:violet[Description :]**",extract_detail['description'])
                st.write("**:violet[Price in $ :]**",f'**{extract_detail['price']}**')
                st.write("**:violet[Total Reviews :]**",f'**{extract_detail['number_of_reviews']}**')
                st.write("**:violet[Overall Score:]**", f"**{extract_detail['overall_score']} &nbsp;&nbsp; **:violet[Rating:]** {extract_detail['rating']}**")
                st.write("**:violet[Room Picture :]**")
                st.image(extract_detail['images'],width=300)

            with c2:

                st.write(':green[Room Details]')
                st.write('**:violet[Property_type:]**',f'**{extract_detail['property_type']}**')
                st.write("**:violet[Room Type :]**",f'**{extract_detail['room_type']}**')
                st.write("**:violet[Amenities :]**",f'**{extract_detail['amenities']}**')
                st.write('**:green[Host Details]**')
                st.write("**:violet[Host Name :]**",f'**{extract_detail['host_name']}**')
                st.write("**:violet[Host Url :]**",extract_detail['host_url'])
                st.write("**:violet[Host location :]**",f'**{extract_detail['host_location']}**')
                st.write("**:violet[Host About :]**",f'**{extract_detail['host_about']}**')
                st.write("**:violet[Host Picture :]**")
                st.image(extract_detail['host_picture_url'],width=300)

            df = pd.read_sql_query('''SELECT reviewer_name,comments FROM comments_info JOIN
                                hotels_info ON comments_info.id = hotels_info.id
                                WHERE name = %s LIMIT 10''',con=engine,params=[(selected_hname,)])
            
            st.write('**:green[Top Comments]**')
            st.dataframe(df,hide_index=True,use_container_width=True)

#DISCOVER page

if selected == 'DISCOVER':
    st.subheader(':red[Explore Accommodation by country]')

    df_country = pd.read_sql_query('''SELECT DISTINCT country FROM hotels_info''',con=engine)
    selected_country = st.selectbox('Search Country',options=df_country['country'].tolist(),index=None)

    if selected_country:

        check = st.checkbox(f'Click to view accommodation by property wise and room type in {selected_country}')

        if not check:
            df = pd.read_sql_query('''SELECT name as 'HotelName',price, SUBSTRING_INDEX(coordinates, ',',1) AS longitude,
                                   SUBSTRING_INDEX(coordinates, ',',-1) AS latitude FROM hotels_info
                                   WHERE country = %s ''',con=engine,params=[(selected_country,)])
            
            df[['longitude','latitude']] = df[['longitude','latitude']].astype('float')

            fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                                        hover_name='HotelName',zoom=10,
                                        hover_data={'longitude':False,'latitude':False, 'price': True},
                                        color_discrete_sequence=px.colors.colorbrewer.Dark2)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

            st.plotly_chart(fig,use_container_width=True)

        if check:
            st.subheader(f":red[Explore Accommodation by Property wise and room type in {selected_country}]")
            df_prop  = pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info 
                                        join hotels_info on rooms_info.id = hotels_info.id where country=%s''',con=engine,
                                        params = [(selected_country,)])
            selected_property = st.selectbox('Select the property',options=df_prop['property_type'].tolist(),index = None)

            df_room=pd.read_sql_query('''SELECT DISTINCT room_type from rooms_info join hotels_info on rooms_info.id=hotels_info.id
                                where property_type=%s and country =%s  ''',con=engine,params=[(selected_property,selected_country)])
            selected_room=st.radio('select a Room type',options=df_room['room_type'].tolist(),index=None)

            if selected_room:

                df = pd.read_sql_query('''SELECT name as 'HotelName',property_type,room_type,price,
                                       SUBSTRING_INDEX(coordinates, ',',1) AS longitude,
                                       SUBSTRING_INDEX(coordinates, ',',-1) AS latitude
                                       FROM hotels_info JOIN rooms_info ON hotels_info.id = rooms_info.id
                                       WHERE country = %s AND property_type = %s AND room_type = %s
                                       GROUP BY name, property_type,room_type;''',
                                       con=engine,params=[(selected_country,selected_property,selected_room)])
                
                df[['longitude','latitude']] = df[['longitude','latitude']].astype('float')

                fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                                            hover_name='HotelName',zoom=10,
                                            hover_data={'longitude':False,'latitude':False, 'price': True,'property_type':True,'room_type':True},
                                            color_discrete_sequence=px.colors.colorbrewer.Blues_r)
                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

                st.plotly_chart(fig,use_container_width=True)

if selected == 'INSIGHTS':
    select_insights = option_menu('',options=['TOP INSIGHTS','FILTER INSIGHTS'],
                                  icons=['bar-chart','toggles'],
                                  orientation = 'horizontal',
                                  styles = {'container':{'border':'2px ridge'},
                                            'icon':{'color':'#F8CD47','font-size':'20px'}})
    
    if select_insights == 'TOP INSIGHTS':
        opt=['Top 10 Accommodation with Highest price',
            'Top 10 Accommodation with Lowest price ',
            'Number of Hotels Count by Country',
            'Room Type Distribution by Country',
            'Host with Highest Listing',
            'Top 10 Accommodation with Highest Reviews',
            'Hotels Count by Rating',
            'Average Availability of Stays by Country',
            'Average Accommodation Prices by Country',
            'Property type Distribution by country',]
        
        query=st.selectbox(':red[Select a Query]',options=opt,index=None)

        if query == opt[0]:
            col1,col2 = st.columns(2)

            with col1:
                df = pd.read_sql_query('''SELECT name,country,MAX(price) AS 'price' FROM hotels_info
                                       GROUP BY name ORDER BY MAX(price) DESC LIMIT 10''',con=engine)
                
                fig = px.bar(df, y='name',x='price',color = 'name',
                             hover_data = ['name','country'],title='Top 10 Accommodation with Highest price',
                             color_continuous_midpoint=px.colors.carto.Aggrnyl_r)
                fig.update_layout(showlegend = False)

                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True)

            with col2:
                fig=px.pie(df,names='name',values='price',color='name',
                        title='Percentage of Top 10 Accommodation with Highest price',
                        color_discrete_sequence=px.colors.cmocean.balance_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

        if query == opt[1]:
            col1,col2 = st.columns(2)

            with col1:
                df = pd.read_sql_query('''SELECT name,country,MIN(price) AS 'price' FROM hotels_info
                                       GROUP BY name ORDER BY MIN(price) DESC LIMIT 10''',con=engine)
                
                fig = px.bar(df, y='name',x='price',color = 'name',
                             hover_data = ['name','country'],title='Top 10 Accommodation with Lowest price',
                             color_continuous_midpoint=px.colors.carto.Aggrnyl_r)
                fig.update_layout(showlegend = False)

                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True)

            with col2:
                fig=px.pie(df,names='name',values='price',color='name',
                        title='Percentage of Top 10 Accommodation with Lowset price',
                        color_discrete_sequence=px.colors.cmocean.balance_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

        if query == opt[2]:
            col1,col2 = st.columns(2)

            with col1:
                df=pd.read_sql_query('''SELECT country,COUNT(name) as 'Hotel Count' FROM hotels_info GROUP BY country
                                    order by COUNT(name) Desc  ''',con=engine)

                fig=px.bar(df,x='country',y='Hotel Count',color='country',
                        hover_name='country',title="Number of Hotels Count by Country",
                        color_discrete_sequence=px.colors.qualitative.Plotly_r)
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True)

            with col2:
                fig=px.pie(df,names='country',values='Hotel Count',color='country',
                        title="Number of Hotels by Country in percentage",
                        color_discrete_sequence=px.colors.carto.Purpor_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

        if query == opt[3]:
            col1,col2 = st.columns(2)
            #'Room Type Distribution by Country'
            with col1:
                df = pd.read_sql_query('''SELECT country,room_type, count(room_type) as 'count of room type' 
                                       FROM rooms_info JOIN hotels_info ON rooms_info.id = hotels_info.id
                                       GROUP BY country,room_type''',con=engine)
                fig = px.sunburst(df,path=['country','room_type'],values='count of room type',
                                  title = 'Rooms types by country',color_continuous_scale='RdBu')
                st.plotly_chart(fig,use_container_width=True)

            with col2:
                st.dataframe(df,hide_index=True)

        if query == opt[4]:
            col1,col2 = st.columns(2)
            with col1:
                df = pd.read_sql_query('''SELECT host_id,host_name,count(host_id) as 'total listing' FROM host_info
                                       GROUP BY host_id,host_name ORDER BY COUNT(host_id) DESC LIMIT 10''',con=engine
                                       )
                fig=px.bar(df,x='host_name',y='total listing',color='host_name',
                        hover_name='host_name',title="Host with Highest Listing",
                        color_discrete_sequence=px.colors.diverging.Temps_r)
                fig.update_layout(showlegend = False)
                st.plotly_chart(fig,use_container_width=True)

            with col2:
                st.dataframe(df,hide_index=True)
        
        if query == opt[5]:
            col1,col2 = st.columns(2)

            with col1:
                df = pd.read_sql_query('''SELECT name,max(number_of_reviews) as 'Total Reviews' FROM reviews_info
                                       JOIN hotels_info ON reviews_info.id = hotels_info.id GROUP BY hotels_info.id
                                       ORDER BY max(number_of_reviews) DESC LIMIT 10''',con=engine)
                
                fig=px.bar(df,y='name',x='Total Reviews',color='name',
                        hover_name='name',title='Top 10 Accommodation with Highest Reviews',
                        color_discrete_sequence=px.colors.qualitative.Bold_r)
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                
                with col2:
                    st.dataframe(df,hide_index=True)

        if query == opt[6]:
            col1,col2 = st.columns(2)
            
            with col1:
                df = pd.read_sql_query('''SELECT rating,COUNT(id) as 'total stays' FROM reviews_info
                                       GROUP BY rating ORDER BY count(id) DESC''',con=engine)
                
                fig=px.line(df,x='rating',y='total stays',markers=True,
                        title='Hotels Count by Rating')
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)
            with col2:
                st.dataframe(df,hide_index=True)


        if query == opt[7]:
            col1,col2 = st.columns(2)

            with col1:
                df = pd.read_sql_query('''SELECT country,AVG(availability_30) as 'avg_availability_30',AVG(availability_60)  as 'avg_availability_60',
                                    AVG(availability_365) as 'avg_availability_365' from rooms_info
                                    join hotels_info on rooms_info.id=hotels_info.id GROUP by country ''',con=engine)
                
                fig = px.bar(df, x='country', y=['avg_availability_30', 'avg_availability_60', 'avg_availability_365'],
                            title='Average Availability of Stays by Country',
                            labels={'value': 'Average Availability', 'variable': 'Availability Period', 'country': 'Country'},
                            barmode='group')
                st.plotly_chart(fig,use_container_width=True)
            with col2:
                st.dataframe(df,hide_index=True)

        if query == opt[8]:
            col1,col2 = st.columns(2)

            with col1:
                df=pd.read_sql_query('''SELECT country ,AVG(price) as 'Average Price' from hotels_info 
                                    group by country order by AVG(price) desc ''',con=engine)

                fig=px.bar(df,x='country',y='Average Price',color='country',
                        hover_name='country',title='Average Accommodation Prices by Country')

                st.plotly_chart(fig,use_container_width=True)
            with col2:
                st.dataframe(df,hide_index=True,use_container_width=True)

        if query == opt[9]:
            col1,col2 = st.columns(2)

            with col1:
                df = pd.read_sql_query('''SELECT country,property_type,count(room_type)as 'Property Count' FROM rooms_info
                                       JOIN hotels_info ON rooms_info.id = hotels_info.id
                                       GROUP BY country,property_type''',con=engine)
                
                fig = px.sunburst(df, path=['country','property_type'], values='Property Count',
                        title='Property type Distribution by country', color_continuous_scale='RdBu')
                st.plotly_chart(fig,use_container_width=True)

            with col2:
                st.dataframe(df,hide_index=True)

    if select_insights == 'FILTER INSIGHTS':

        Ques = ['Property wise Accommodation count and Average price for specific country',
                'Room type wise Accommodation count and Average price for specific country',
                'Average Availability days for specific property and country',
                'Country wise Average price of stays for specific Property and Room type',
                'Average pricing and fees for a speciific country',
                'Cancellation Policy-wise Stays Count for a Specific Country',]
        
        query = st.selectbox(':red[Select a Query]',options=Ques,index=None)

        if query==Ques[0]:

            df_country = pd.read_sql_query('''SELECT DISTINCT country FROM hotels_info''',con = engine)
            selected_country = st.selectbox('Select a Country',options=df_country['country'].tolist(),index=None)

            if selected_country:
                df = pd.read_sql_query('''SELECT property_type,avg(price)  as 'Average price',COUNT(property_type) as 'Total Stays' from rooms_info 
                                        join hotels_info on rooms_info.id=hotels_info.id   where country= %s
                                        GROUP by property_type''',con=engine,params=[(selected_country,)])
                
                fig = px.scatter(df,x='property_type',y='Total Stays',color='property_type',
                        labels={'property_type': 'Property Type', 'Total Stays': 'Total Stays'},
                        title=f'Property wise Accommodation count for {selected_country}')
                
                st.plotly_chart(fig,use_container_width=True)

                col1,col2=st.columns(2)
                with col1:
                    fig=px.pie(df,names='property_type',values='Average price',color='property_type',
                            title=f'Property wise Average price for {selected_country}',
                            color_discrete_sequence=px.colors.qualitative.Safe)
                    
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig,use_container_width=True)

                with col2:
                    st.write('**Dataframe**')
                    st.dataframe(df,hide_index=True,use_container_width=True)

        if query == Ques[1]:

            df_country = pd.read_sql_query('''SELECT DISTINCT country FROM hotels_info''',con = engine)
            selected_country = st.selectbox('Select a Country',options=df_country['country'].tolist(),index=None)

            if selected_country:
                df = pd.read_sql_query('''SELECT room_type,avg(price)  as 'Average price',COUNT(room_type) as 'Total Stays' from rooms_info 
                                        join hotels_info on rooms_info.id=hotels_info.id   where country= %s
                                        GROUP by room_type''',con=engine,params=[(selected_country,)])
                
                fig = px.scatter(df,x='room_type',y='Total Stays',color='room_type',
                        labels={'room_type': 'Room Type', 'Total Stays': 'Total Stays'},
                        title=f'Room wise Accommodation count for {selected_country}')
                
                st.plotly_chart(fig,use_container_width=True)

                col1,col2=st.columns(2)
                with col1:
                    fig=px.pie(df,names='room_type',values='Average price',color='room_type',
                            title=f'Property wise Average price for {selected_country}',
                            color_discrete_sequence=px.colors.qualitative.Safe)
                    
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig,use_container_width=True)

                with col2:
                    st.write('**Dataframe**')
                    st.dataframe(df,hide_index=True,use_container_width=True)

        if query == Ques[2]:

            df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
            selected_country= st.selectbox("Select a country",options=df_Country['country'].tolist(),index=None)

            df_property=pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info 
                                        join hotels_info on rooms_info.id = hotels_info.id where country=%s''',engine,params=[(selected_country,)])
            selected_prop=st.selectbox('select a property',options=df_property['property_type'].tolist(),index=None)

            if selected_prop:

                df=pd.read_sql_query('''SELECT country,AVG(availability_30) as 'avg_availability_30',AVG(availability_60)  as 'avg_availability_60',
                                        AVG(availability_365) as 'avg_availability_365' from rooms_info
                                        join hotels_info on rooms_info.id=hotels_info.id 
                                        where country =%s AND property_type=%s ''',con=engine,params=[(selected_country,selected_prop)])
                    
                fig = px.bar(df, x='country', y=['avg_availability_30', 'avg_availability_60', 'avg_availability_365'],
                                title=f'Average Availability days for {selected_prop} in {selected_country}',
                                labels={'value': 'Average Availability', 'variable': 'Period'},
                                barmode='group')
                st.plotly_chart(fig,use_container_width=True)

                st.write('**Dataframe**')
                st.dataframe(df,hide_index=True,use_container_width=True)
        if query==Ques[3]:
            st.markdown('<br>', unsafe_allow_html=True)

            df_property=pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info ''',con=engine)
            selected_prop=st.selectbox('select a property',options=df_property['property_type'].tolist(),index=None)

            df_room=pd.read_sql_query('''SELECT DISTINCT room_type from rooms_info 
                                        where property_type=%s ''',engine,params=[(selected_prop,)])
            selected_room=st.radio('select a Room type',options=df_room['room_type'].tolist(),index=None)

            if selected_room:

                df=pd.read_sql_query('''SELECT country, AVG(price) as 'average price' FROM hotels_info 
                                        JOIN rooms_info ON hotels_info.id = rooms_info.id 
                                        WHERE rooms_info.property_type =%s and rooms_info.room_type=%s
                                        GROUP BY country;''',con=engine,params=[(selected_prop,selected_room)])
                
                fig = px.bar(df, x='country', y='average price',color='country',
                                title=f'country wise Average price of stay for {selected_prop} and {selected_room}',
                                labels={'country': 'country', 'average price': 'average price'},
                                color_discrete_sequence=px.colors.qualitative.Bold_r)
                
                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True,use_container_width=True)


        if query == Ques[4]:

            df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
            selected_country= st.selectbox("Select a country",options=df_Country['country'].tolist(),index=None)

            if selected_country:
                    check=st.checkbox(f"Click to view pricing details by property type in {selected_country}.")

                    if not check:

                        df=pd.read_sql_query('''SELECT country,AVG(weekly_price) as 'avg Weekly price',AVG(monthly_price)  as 'avg Monthly price',
                                            AVG(security_deposit) as 'avg security deposit', AVG(cleaning_fee) as 'avg cleaning price'
                                            from hotels_info  where country=%s GROUP by country ''',con=engine,params=[(selected_country,)])
                        
                        fig = px.bar(df, x='country', y=['avg Weekly price', 'avg Monthly price', 'avg security deposit','avg cleaning price'],
                                    title=f'Average Pricing and Fees of stays in {selected_country} ',
                                    labels={'value':'Average pricing', 'variable':'cataogory' },
                                    barmode='group')
                        
                        st.plotly_chart(fig,use_container_width=True)

                    if check:

                        df_property = pd.read_sql_query('''SELECT DISTINCT property_type FROM rooms_info
                                               JOIN hotels_info ON rooms_info.id = hotels_info.id WHERE country = %s''',engine,
                                               params = [(selected_country,)])
                        selected_property = st.selectbox('Select a Property',options=df_property['property_type'].tolist(),index=None )

                        if selected_property:

                            df=pd.read_sql_query('''SELECT country,AVG(weekly_price) as 'avg Weekly price',AVG(monthly_price)  as 'avg Monthly price',
                                                    AVG(security_deposit) as 'avg security deposit', AVG(cleaning_fee) as 'avg cleaning price'
                                                    from hotels_info  join rooms_info on hotels_info.id=rooms_info.id
                                                    where country=%s and property_type=%s GROUP by country''',con=engine,params=[(selected_country,selected_prop)])
                            
                            fig = px.bar(df, x='country', y=['avg Weekly price', 'avg Monthly price', 'avg security deposit', 'avg cleaning price'], 
                                        title=f'Average Price & Fees in {selected_country} - property type : {selected_prop}',
                                        labels={'value':'Average pricing', 'variable':'cataogory' },
                                        color_discrete_sequence=px.colors.qualitative.D3_r,
                                        barmode='group')
                            
                            st.plotly_chart(fig,use_container_width=True)

        if query==Ques[5]:
            st.markdown('<br>', unsafe_allow_html=True)
                
            df_Country=pd.read_sql_query('''SELECT DISTINCT country from hotels_info''',con=engine)
            selected_country= st.selectbox("Select a country",options=df_Country['country'].tolist(),index=None)

            if selected_country:
                    chek=st.checkbox(f"Click to view property wise count of stays for {selected_country} ")

                    if not chek:

                        df=pd.read_sql_query('''SELECT cancellation_policy, COUNT(*) AS 'Stays Count' FROM hotels_info
                                JOIN rooms_info ON hotels_info.id = rooms_info.id
                                WHERE country = %s GROUP BY cancellation_policy''',con=engine,params=[(selected_country,)])
                        
                        fig = px.bar(df, x='cancellation_policy', y='Stays Count', color='cancellation_policy',
                                    title=f'Cancellation Policy-wise Stays Count for {selected_country}',
                                    labels={'cancellation_policy': 'Cancellation Policy', 'Stays Count': 'Stays Count'})
                        
                        st.plotly_chart(fig,use_container_width=True)

                    if chek:

                        df_property=pd.read_sql_query('''SELECT DISTINCT property_type from rooms_info 
                                        join hotels_info on rooms_info.id = hotels_info.id where country=%s''',engine,params=[(selected_country,)])
                        selected_prop=st.selectbox('select a property',options=df_property['property_type'].tolist(),index=None)

                        if selected_prop:

                            df=pd.read_sql_query('''SELECT country, cancellation_policy, COUNT(*) AS 'Stays Count' FROM hotels_info
                                JOIN rooms_info ON hotels_info.id = rooms_info.id
                                WHERE country =%s and  property_type=%s
                                GROUP BY country, cancellation_policy''',con=engine,params=[(selected_country,selected_prop)])
                            
                            fig = px.pie(df, values='Stays Count', names='cancellation_policy',hole=0.3,
                                    title=f'Cancellation Policy-wise Stays Count for {selected_prop} in {selected_country}',
                                    labels={'Stays Count': 'Stays Count', 'cancellation_policy': 'Cancellation Policy'})
                            
                            st.plotly_chart(fig,use_container_width=True)


#set up the details for option 'About'
if selected=="ABOUT":
        st.subheader(':red[What is Airbnb ?]')
        st.markdown('''Airbnb is a popular online marketplace that connects people who want to rent out their properties with travelers seeking accommodations.
                    It allows individuals to rent out their homes, apartments, rooms, or other lodging accommodations to guests. Airbnb offers a wide range of accommodation
                    options in various locations around the world, providing travelers with unique and personalized experiences while offering hosts an opportunity 
                    to earn income from their properties.''')
        st.subheader(':red[History :]')
        st.markdown('''History of Airbnb In 2008, Brian Chesky (the current CEO), Nathan Blecharczyk, and Joe Gebbia, established the company now known as Airbnb.
                    The idea blossomed after two of the founders started renting air mattresses in their San Francisco home to conference visitors. Hence, the original name of Airbed & Breakfast.         
                    In 2009, the name Airbnb was introduced and its offerings grew beyond air mattresses to include spare rooms, apartments, entire houses, and more. 
                    The locations in which it operated grew, as well. By 2011, Airbnb had opened an office in Germany and in 2013, it established a European headquarters in Dublin, Ireland. 
                    Its primary corporate location is still San Francisco.''')

        st.write(':black[Thank You.]')

        

            








    
     



                                       

            
                            
 



                



                                                                                                                                                               



                 






            
