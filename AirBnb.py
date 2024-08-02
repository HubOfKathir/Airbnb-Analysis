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

            df = pd.read_sql_query('''SELECT name as 'Hotel Name',reviewer_name,comments FROM comments_info JOIN
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
    select_insights = option_menu('',options=['TOP INSIGHTS'],
                                  icons=['bar-chart'],
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

        def stream1():
                for i in t_1:
                    yield i + ''
                    time.sleep(0.02)
        def stream2():
                for i in t_2:
                        yield i + '' 
                        time.sleep(0.02)
        def stream3():
                for i in t_3:
                        yield i + ''
                        time.sleep(0.02)
        def stream4():
                for i in t_4:
                        yield i + ''
                        time.sleep(0.02)

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

                t_1='''🟡 Istanbul, Turkey: "Center of Istanbul Sisli" stands out as the most expensive accommodation with a price of 48,842 Turkish Lira,
                reflecting its prime location in the heart of Istanbul's vibrant Sisli district.'''                                   
                
                t_2='''🟡 Hong Kong: The city boasts several high-priced accommodations, including "HS1-2人大床房+丰泽､苏宁､百脑汇+女人街+美食中心" and 
                "良德街3号温馨住宅" priced at 11,681 Hong Kong Dollars each, suggesting a strong demand for upscale lodging options in this bustling metropolis.'''               
                
                t_3='''🟡 Brazil: Not to be outdone, Brazil features luxurious accommodations like "Apartamento de luxo em Copacabana - 4 quartos" and "Deslumbrante apartamento na AV.Atlantica"
                with prices exceeding 6,000 Brazilian Reais, catering to travelers seeking premium experiences along the country's picturesque coastlines'''
                

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())

        if query == opt[1]:
            col1,col2 = st.columns(2)

            with col1:
                df = pd.read_sql_query('''SELECT name,country,MIN(price) AS 'price' FROM hotels_info
                                       GROUP BY name ORDER BY MIN(price) LIMIT 10''',con=engine)
                
                fig = px.bar(df, y='name',x='price',color = 'name',
                             hover_data = ['name','country'],title='Top 10 Accommodation with Lowest price',
                             color_continuous_midpoint=px.colors.carto.Aggrnyl_r)
                fig.update_layout(showlegend = False)

                st.plotly_chart(fig,use_container_width=True)
                st.dataframe(df,hide_index=True)

            with col2:
                fig=px.pie(df,names='name',values='price',color='name',
                        title='Percentage of Top 10 Accommodation with Lowest price',
                        color_discrete_sequence=px.colors.cmocean.balance_r)
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                t_1='''🟡 Among the top 10 accommodations listed, the most budget-friendly options are found in Portugal and Spain.'''
                
                t_2='''🟡 Portugal offers the most affordable accommodations, with prices ranging from  9 to 13 dollers.'''
                
                t_3='''🟡 Spain also provides reasonably priced options, with room rates starting at 10 and 12 dollers.'''
                
                t_4='''🟡 Notably, Canada appears in the top 10 list with a "Good room" priced at $13, reflecting a competitive pricing compared to European destinations.'''

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())

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

                t_1='''🟡 The United States dominates the Airbnb market with 1,222 listings, indicating a significant presence of accommodations in the country.'''
                
                t_2='''🟡 Turkey, Canada, and Spain follow closely behind, with 661, 649, and 633 listings respectively, showcasing a strong presence of Airbnb properties in these regions.'''
                
                t_3='''🟡 Australia, Brazil, and Hong Kong also demonstrate substantial Airbnb activity, with 610, 606, and 600 listings respectively, 
                            suggesting a diverse range of accommodation options available to travelers.'''
                
                t_4='''🟡 Portugal and China round out the list with 555 and 19 listings respectively, highlighting varying levels of Airbnb adoption in different regions.'''
                
                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())

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

            
                st.subheader('Get the details in table view')
                st.dataframe(df,hide_index=True)

            with col2:

                st.markdown('<br>', unsafe_allow_html=True)

                t_1='''🟡 Entire homes and apartments are the most popular Airbnb listings in the US, 
                        Canada, Portugal, Australia, Hong Kong, and Spain. This suggests travelers in these areas prefer private spaces.'''
                    
                t_2='''🟡 Some countries, like Canada, Portugal, Australia, Hong Kong, and Spain, also have private rooms for travelers
                    seeking a budget-friendly option with some privacy. Interestingly, Turkey has more private rooms than entire listings'''
                
                t_3='''🟡 Shared rooms, where guests share space with the host or others, are the least common option across all countries.
                        This could be due to travelers wanting more privacy or cultural norms.'''
                
                t_4='''🟡 China has fewer listings overall, and most are entire homes/apartments.
                This could be due to regulations or travel patterns specific to China.'''
                
                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())

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

                st.subheader('Get the details in table view')
                st.dataframe(df,hide_index=True)

            with col2:
                st.markdown('<br>', unsafe_allow_html=True)

                t_1='''🟡 Jov leads the pack with an impressive tally of 18 listings, showcasing a significant presence in the accommodation landscape.'''

                t_2='''🟡 Sonder follows closely with 11 listings, indicating a substantial contribution to the Airbnb platform.'''

                t_3='''🟡 Alejandro and Eva&Jacques each boast 9 listings, further diversifying the options available to Airbnb guests.'''

                t_4='''🟡 Feels Like Home, Liiiving, Mark, Marina, Captain Cook Resorts, and Debe round out the top hosts, each offering between 6 to 7 listings,
                        reflecting the rich variety of accommodations available worldwide.'''

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())
        
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

                st.subheader('Get the details in table view')
                st.dataframe(df,hide_index=True)

                
                with col2:

                    t_1='''🟡 Diverse Accommodation Options: This collection of top-reviewed Airbnb stays showcases a diverse range of accommodation options, 
                    from private studios to spacious apartments, each offering unique experiences and amenities.'''

                    t_2='''🟡 Popular Destinations: Situated in sought-after locations like Waikiki and close to landmarks such as La Sagrada Familia,
                        these accommodations provide convenient access to attractions and transportation.'''

                    t_3='''🟡 Consistent Guest Satisfaction: With numerous positive reviews, these stays consistently deliver exceptional service,
                    cleanliness, and overall guest satisfaction.'''

                    t_4='''🟡 Trusted Choices for Travelers: These Airbnb listings are trusted by travelers for their reliability and positive feedback,
                        making them dependable options for a comfortable and enjoyable stay.'''

                    st.markdown('<br>', unsafe_allow_html=True)

                    st.write_stream(stream1())
                    st.write_stream(stream2())
                    st.write_stream(stream3())
                    st.write_stream(stream4())

                    

        if query == opt[6]:
            col1,col2 = st.columns(2)
            
            with col1:
                df = pd.read_sql_query('''SELECT rating,COUNT(id) as 'total stays' FROM reviews_info
                                       GROUP BY rating ORDER BY count(id) DESC''',con=engine)
                
                fig=px.line(df,x='rating',y='total stays',markers=True,
                        title='Hotels Count by Rating')
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,use_container_width=True)

                st.subheader('Get the details in table view')
                st.dataframe(df,hide_index=True)

            with col2:

                t_1='''🟡 Distribution of Ratings: The majority of Airbnb listings have ratings ranging from 90 to 100, with the highest concentration around the 100 rating mark.'''
                    
                t_2='''🟡 Highly Rated Listings: A significant number of listings receive ratings of 95 and above, indicating a high level of satisfaction among guests.'''
                
                t_3='''🟡 Variety of Ratings: While most listings have high ratings, there is also diversity in ratings across the platform, with some listings receiving ratings below 80.'''
                
                t_4='''🟡 Room for Improvement: Despite the overall positive trend, there are opportunities for improvement in some listings, 
                        as reflected in the lower ratings received by a small percentage of accommodations.'''
                
                st.markdown('<br>', unsafe_allow_html=True)

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())


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

                st.subheader('Get the details in table view')
                st.dataframe(df,hide_index=True)

            with col2:
                

                t_1=''' 🟡 For shorter-term stays (30 days), Australia, Canada, Spain, and the United States offer durations ranging from 8 to 10 days on average.'''
                    
                t_2='''🟡 Brazil, Hong Kong, and Portugal provide moderate availability for stays of 60 days, averaging between 20 and 25 days.'''
                
                t_3='''🟡 China leads in availability for longer-term stays (365 days), offering approximately 235 days on average.'''
                
                t_4='''🟡 Turkey stands out with the longest availability for both 60 and 365 days, providing around 45 and 256 days, respectively, on average.'''

                st.markdown('<br>', unsafe_allow_html=True)

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())

        if query == opt[8]:
            col1,col2 = st.columns(2)

            with col1:
                df=pd.read_sql_query('''SELECT country ,AVG(price) as 'Average Price' from hotels_info 
                                    group by country order by AVG(price) desc ''',con=engine)

                fig=px.bar(df,x='country',y='Average Price',color='country',
                        hover_name='country',title='Average Accommodation Prices by Country')

                st.plotly_chart(fig,use_container_width=True)

                st.subheader('Get the details in table view')
                st.dataframe(df,hide_index=True,use_container_width=True)
            
            with col2:
                t_1='''🟡 Varied Pricing: Accommodation prices span a wide range, from luxurious in Hong Kong to budget-friendly in Portugal. 
                        This diversity allows travelers to choose options that align with their budget and preferences. '''

                t_2='''🟡 Value for Money: Turkey and Spain offer affordable stays without compromising quality, making them ideal choices for
                    budget-conscious travelers seeking comfortable accommodations.'''
                
                t_3='''🟡 Budget Flexibility: Options cater to every budget, ensuring there's something for everyone across these countries.
                        Whether travelers are looking for upscale experiences or budget-friendly stays, they can find suitable options.'''
                
                t_4='''🟡 Tailored Choices: With diverse options available, travelers can easily find accommodations that fit their budget and preferences,
                    guaranteeing a pleasant stay. From cozy guesthouses to modern apartments, there's something for every type of traveler. '''

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())

                

        if query == opt[9]:
            col1,col2 = st.columns(2)

            with col1:
                df = pd.read_sql_query('''SELECT country,property_type,count(room_type)as 'Property Count' FROM rooms_info
                                       JOIN hotels_info ON rooms_info.id = hotels_info.id
                                       GROUP BY country,property_type''',con=engine)
                
                fig = px.sunburst(df, path=['country','property_type'], values='Property Count',
                        title='Property type Distribution by country', color_continuous_scale='RdBu')
                st.plotly_chart(fig,use_container_width=True)

                st.subheader('Get the details in table view')
                st.dataframe(df,hide_index=True)

            with col2:
                t_1='''🟡 The most common property types across these countries are Apartments, reflecting the popularity 
                            of urban living spaces and providing comfortable accommodation options for travelers.'''
                    
                t_2='''🟡 Other prevalent property types include Houses, Townhouses, and Condominiums, offering diverse choices 
                        for different preferences and travel styles.'''
                
                t_3='''🟡 Additionally, unique accommodations such as Lofts, Serviced Apartments, and Boutique Hotels cater to travelers 
                        seeking distinctive and memorable lodging experiences.'''
                
                t_4='''🟡 Overall, the availability of a wide range of property types highlights the diversity and richness of accommodation 
                            options in these countries, accommodating various traveler needs and preferences.'''
                
                st.markdown('<br>', unsafe_allow_html=True)

                st.write_stream(stream1())
                st.write_stream(stream2())
                st.write_stream(stream3())
                st.write_stream(stream4())


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
