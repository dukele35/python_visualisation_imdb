import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 



##### MENU OPTION 1 #####
# 1.1. Data processing
# 1.1.1. cleaning the data
df = pd.read_csv('movie_metadata.csv')
df = df.drop(['movie_imdb_link', 'plot_keywords'], axis=1)
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['movie_title'] = df['movie_title'].str.replace('\xa0','')

# 1.1.2. creating 'director' Series
director = (df.groupby('director_name').sum()['gross']/1e9).sort_values(ascending = False)


# 1.1.3. creating 'actor' Series
# unique actors' names for the column actor_1_name
actor1 = df['actor_1_name'].unique() 

# unique actors' names for the column actor_2_name
actor2 = df['actor_2_name'].unique() 

# unique actors' names for the column actor_3_name
actor3 = df['actor_3_name'].unique() 

# all unique actors' names 
unique_actors = np.unique(np.concatenate((actor1, actor2, actor3)));

# sorting A-Z all unique actors' names
unique_actors_sorted = np.sort(unique_actors)

# total gross earnings of the movies associated with 'actor_1_name'
actor1_gross = df.groupby('actor_1_name').sum()['gross']/1e9

# tota2 gross earnings of the movies associated with 'actor_2_name'
actor2_gross = df.groupby('actor_2_name').sum()['gross']/1e9

# tota3 gross earnings of the movies associated with 'actor_3_name'
actor3_gross = df.groupby('actor_3_name').sum()['gross']/1e9

# calculate total gross earnings for each of the actor in all of 
# his/her positions, i.e. 'actor_1_name', 'actor_2_name' & 'actor_3 name'
temp = dict()
for i in unique_actors_sorted:
    if i in actor1_gross and i in actor2_gross and i in actor3_gross:
        temp[i] = actor1_gross[i] + actor2_gross[i] + actor3_gross[i]
    elif i in actor1_gross and i in actor2_gross:
        temp[i] = actor1_gross[i] + actor2_gross[i]
    elif i in actor1_gross and i in actor3_gross:
        temp[i] = actor1_gross[i] + actor3_gross[i]
    elif i in actor2_gross and i in actor3_gross:
        temp[i] = actor2_gross[i] + actor3_gross[i]
    elif i in actor1_gross:
        temp[i] = actor1_gross[i]
    elif i in actor2_gross:
        temp[i] = actor2_gross[i]
    else:
        temp[i] = actor3_gross[i]
        
actor = pd.Series(temp).sort_values(ascending = False)

# 1.2. Building plotting option for the most successful directors
def checking_value_type(n):
    try:
        n = int(n)
    except:
        return False
    return True    

def taking_n_director():
    n_director = input('Please enter number of the top most successful directors: ')
    return n_director

def input_n_director():
    n = taking_n_director()
    while checking_value_type(n) == False or (checking_value_type(n) == True and (int(n) < 1 or int(n) > len(director))):
        print('Please enter the correct input which must be', 
              '\n- A whole number', 
              '\n- In range of 1 -',
              len(director),
              '(Number of directors) inclusively')
        n = taking_n_director()
    return int(n)       

def plotting_director():
    n_director = input_n_director()
    plot1 = director[:n_director].plot.bar(rot=90, title='Top ' + str(n_director)+ ' most successful directors with respect to gross earnings of the movies', figsize = (16, 5))
    plot1.set_xlabel("Director's Name")
    plot1.set_ylabel("Gross earnings of the movies (Billion Dollars)")
    plt.show();


# 1.3. Building plotting option for the most successful actors
def taking_n_actor():
    n_actor = input('Please enter number of the top most successful actors: ')
    return n_actor

def input_n_actor():
    n = taking_n_actor()
    while checking_value_type(n) == False or (checking_value_type(n) == True and (int(n) < 1 or int(n) > len(actor))):
        print('Please enter the correct input which must be', 
              '\n- A whole number', 
              '\n- In range of 1 -',
              len(actor),
              '(Number of actors) inclusively')
        n = taking_n_actor()
    return int(n) 

def plotting_actor():
    n_actor = input_n_actor()
    plot1 = actor[:n_actor].plot.bar(rot=90, title='Top ' + str(n_actor)+ ' most successful actors with respect to gross earnings of the movies', figsize = (16, 5))
    plot1.set_xlabel("Actor's Name")
    plot1.set_ylabel("Gross earnings of the movies (Billion Dollars)")
    plt.show();

# 1.4. Putting all together
def question1():
    print('\nYou chose Menu Option 1 – Most successful directors or actors', 
          '\nPlease choose your option:',
          '\n1. Successful directors',
          '\n2. Successful actors')
    choice = input('Please enter your option (1 or 2): ')
    while choice not in ['1', '2']:
        print('\nInvalid input', 
              '\nRemember:', 
              '\n1. Successful directors',
              '\n2. Successful actors')
        choice = input('Please enter your option (1 or 2): ')
    if choice == '1':
        print('\nNow you chose the option of the successful directors')
        plotting_director()
    else:
        print('\nNow you chose the option of the successful actors')
        plotting_actor()


##### MENU OPTION 2 #####

# comparing imdb scores between 2 selected movies
def comp_imdb_scores():
    print('\na. IBMD scores')
    global movie1
    global movie2
    global movie1_color
    global movie2_color
    comp_IMDB = df[['movie_title', 'imdb_score']][(df['movie_title'] == movie1) | (df['movie_title'] == movie2)]
    bin_size = 35
    df['imdb_score'].hist(bins = bin_size, figsize = (16,6),  color = 'slategrey').grid(False)
    plt.axvline(x = df['imdb_score'].median(), color = 'r', linestyle='dashed', linewidth=2)
    plt.axvline(x = comp_IMDB.iloc[0,1], color = movie1_color, linestyle='dashed', linewidth=2)
    plt.axvline(x = comp_IMDB.iloc[1,1], color = movie2_color, linestyle='dashed', linewidth=2)
    plt.legend(['Median Score = ' + str(df['imdb_score'].median()), 
                movie1 + ' = ' + str(comp_IMDB.iloc[0,1]), 
                movie2 + ' = ' + str(comp_IMDB.iloc[1,1]),
                'Distribution of IMDB scores'],
               loc="upper left",
               prop={"size":13})
    plt.title('IMDB SCORE DISTRIBUTION (Histogram)')
    plt.xlabel('IBMD score')
    plt.ylabel('Count')
    plt.show()

    ax = sns.barplot(x = 'movie_title', y = 'imdb_score', data = comp_IMDB, palette = (movie1_color, movie2_color))
    ax.figure.set_size_inches(16,6)
    plt.title('IMDB score comparison between ' + movie1 + ' and ' + movie2)
    plt.show();

# comparing gross earnings between 2 selected movies
def comp_gross_earnings():
    print('\nb. Gross Earnings')
    global movie1
    global movie2
    global movie1_color
    global movie2_color
    comp_gross = df[['movie_title', 'gross']][(df['movie_title'] == movie1) | (df['movie_title'] == movie2)]
    comp_gross['gross'] = comp_gross['gross']/1e6
    bin_size = 50
    (df['gross']/1e6).hist(bins = bin_size, figsize = (16,6), color = 'slategrey').grid(False)
    plt.axvline(x = df['gross'].median()/1e6, color = 'r', linestyle='dashed', linewidth=2)
    plt.axvline(x = comp_gross.iloc[0,1], color = movie1_color, linestyle='dashed', linewidth=2)
    plt.axvline(x = comp_gross.iloc[1,1], color = movie2_color, linestyle='dashed', linewidth=2)
    plt.legend(['Median Gross = ' + str(df['gross'].median()/1e6), 
                movie1 + ' = ' + str(comp_gross.iloc[0,1]), 
                movie2 + ' = ' + str(comp_gross.iloc[1,1]),
                'Distribution of Gross Earnings'],
               loc="upper right", 
               prop={"size":13})
    plt.title('GROSS EARNING DISTRIBUTION (Histogram)')
    plt.xlabel('Gross Earnings (Million US Dollars)')
    plt.ylabel('Count')
    plt.xlim((0,800))
    plt.show()

    ax = sns.barplot(x = 'movie_title', y = 'gross', data = comp_gross, palette = (movie1_color, movie2_color))
    ax.figure.set_size_inches(16,6)
    plt.title('IMDB score comparison between ' + movie1 + ' and ' + movie2)
    plt.ylabel('gross earnings (million US dollars)')
    plt.show();


# comparing facebook likes between 2 selected movies
def comp_facebook_likes():
    print('\nc. Movie Facebook Likes')
    global movie1
    global movie2
    global movie1_color
    global movie2_color
    comp_movie_FB_likes = df[['movie_title', 'movie_facebook_likes']][(df['movie_title'] == movie1) | (df['movie_title'] == movie2)]
    bin_size = 30
    df['movie_facebook_likes'].hist(bins = bin_size, figsize = (16,6), color = 'slategrey').grid(False)
    plt.axvline(x = df['movie_facebook_likes'].median(), color = 'r', linestyle='dashed', linewidth=2)
    plt.axvline(x = comp_movie_FB_likes.iloc[0,1], color = movie1_color, linestyle='dashed', linewidth=2)
    plt.axvline(x = comp_movie_FB_likes.iloc[1,1], color = movie2_color, linestyle='dashed', linewidth=2)
    plt.legend(['Median Facebook Likes = ' + str(df['movie_facebook_likes'].median()), 
                movie1 + ' = ' + str(comp_movie_FB_likes.iloc[0,1]), 
                movie2 + ' = ' + str(comp_movie_FB_likes.iloc[1,1]),
                'Distribution of Movie Facebook Likes'],
               loc="upper right", prop={"size":13})
    plt.title('MOVIE FACEBOOK LIKES DISTRIBUTION (Histogram)')
    plt.xlabel('No. of Movie Facebook Likes')
    plt.ylabel('Count')
    plt.xlim((0,350000))
    plt.show()

    ax = sns.barplot(x = 'movie_title', y = 'movie_facebook_likes', data = comp_movie_FB_likes, palette = (movie1_color, movie2_color))
    ax.figure.set_size_inches(8, 6)
    plt.title('Movie Facebook Likes comparison between ' + movie1 + ' and ' + movie2)
    plt.ylabel('No. of Movie Facebook Likes')
    plt.show();

# putting together
def question2():
    global movie1
    global movie2
    global movie1_color
    global movie2_color
    print('\nYou chose Menu Option 2 - Film Comparison')
    movie1 = input('Please enter your first movie: ')
    while movie1 not in sorted(df['movie_title']):
        print('\nInvalid input', 'Please try again')
        movie1 = input('Please enter again your first movie: ')
    movie2 = input('Please enter your second movie: ')
    while movie2 not in sorted(df['movie_title']):
        print('\nInvalid input', 'Please try again')
        movie2 = input('Please enter again your second movie: ')
    # print('Now choose the comparison option:',
    #       '\n1. IBMD scores',
    #       '\n2. Gross Earnings',
    #       '\n3. Movie Facebook Likes')
    movie1_color = 'orange'
    movie2_color = 'deepskyblue'
    print('\nComparison between your first movie ' + movie1 + ' and your second movie ' + movie2 + ' :')
    comp_imdb_scores()
    comp_gross_earnings()
    comp_facebook_likes()

    # choice = input('Please enter your option (1,2 or 3): ')
    # while choice not in ['1','2','3']:
    #     print('Please enter the valid option', '\nRemember:', 
    #           '\n1. IBMD scores',
    #           '\n2, Gross Earnings',
    #           '\n3.Movie Facebook Likes')
    #     choice = input('Please enter again your option (1,2 or 3): ')
    # if choice == '1':
    #     comp_imdb_scores()
    # elif choice == '2':
    #     comp_gross_earnings()
    # else:
    #     comp_facebook_likes()


##### MENU OPTION 3 #####

# defining plotting function
def gross_plotting():
    global year_start
    global year_end
    
    # creating a dataframe having the chosen period of years
    selected_gross_by_year = df[['title_year','gross']][(df['title_year'] >= year_start) & (df['title_year'] <= year_end)]
    selected_gross_by_year['gross'] = selected_gross_by_year['gross']/1e6
    
    # change 'title_year' to integer value
    selected_gross_by_year['title_year'] = selected_gross_by_year['title_year']
    
    # calculating gross's maximun, minimum, mean and median
    max_gross_by_year = selected_gross_by_year.groupby('title_year').max()['gross']
    min_gross_by_year = selected_gross_by_year.groupby('title_year').min()['gross']
    mean_gross_by_year = selected_gross_by_year.groupby('title_year').mean()['gross']
    median_gross_by_year = selected_gross_by_year.groupby('title_year').median()['gross']
    
    # plotting1: Distribution of Gross Earning in the Chosen Year Range (line)
    max_gross_by_year.plot(figsize = (16,6))
    min_gross_by_year.plot()
    median_gross_by_year.plot()
    mean_gross_by_year.plot()
    plt.xticks(np.arange(year_start, year_end + 1, 1), rotation = 90)
    plt.grid(color = 'gainsboro', linestyle='dashed')
    plt.ylim((selected_gross_by_year['gross'].min() - 20, selected_gross_by_year['gross'].max() + 20))
    plt.title('THE DISTRIBUTION OF GROSS EARNINGS DURING THE CHOSEN RANGE OF YEARS (' + str(year_start) +' - ' + str(year_end) +')')
    plt.xlabel('Years')
    plt.ylabel('Gross Earnings (Million US Dollars)')
    plt.legend(['Max Gross Earning', 
                'Min Gross Earning', 
                'Median Gross Earning',
                'Mean Gross Earning'],
               loc="upper left", 
               prop={"size":13})
    plt.show()

    # plotting2: Number of Movies in Each Year in the Chosen Year Range
    ax = sns.countplot(data=selected_gross_by_year, x = 'title_year',color = 'slategrey')
    ax.figure.set_size_inches(16, 6)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_axisbelow(True)
    plt.title('Number of movies in individual years')
    plt.xlabel('Year')
    plt.grid(color = 'gainsboro', linestyle='dashed')
    plt.show()
    
    # plotting3: Distribution of Gross Earning in the Chosen Year Range (boxplot)
    ax = sns.boxplot(x='title_year', y='gross', data=selected_gross_by_year)
    ax.figure.set_size_inches(16,6)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_axisbelow(True)
    plt.title('THE DISTRIBUTION OF GROSS EARNINGS DURING THE CHOSEN RANGE OF YEARS (' + str(year_start) +' - ' + str(year_end) +')')
    plt.xlabel('Year')
    plt.grid(color = 'gainsboro', linestyle='dashed')
    plt.ylabel('Gross Earnings (Million US Dollars)')
    plt.show();

# putting together
def question3():
    global year_start
    global year_end
    print('\nYou chose Menu Option 3 - Analyse the distribution of gross earnings')
    year_start = input('Please enter the starting year: ')
    while checking_value_type(year_start) == False or (
        checking_value_type(year_start) == True and ((int(year_start) < df['title_year'].min()) or 
                                                     (int(year_start) > df['title_year'].max()) )):
        print('Please enter a correct starting year which must be', 
              '\n- A whole number', 
              '\n- In range of ',
              df['title_year'].min(), ' - ',
              df['title_year'].max(), ' inclusively')
        year_start = input('Please enter again the starting year: ')
    year_start = int(year_start)
    # dealing with non-consecutive years
    if year_start not in set(df['title_year']):
        if year_start == 1928:
            year_start = 1929
        elif year_start in [1930,1931,1932]:
            year_start = 1933
        elif year_start == 1934:
            year_start = 1935
        elif year_start == 1938:
            year_start = 1939
        elif year_start in [1941,1942,1943,1944,1945]:
            year_start = 1946
        elif year_start == 1949:
            year_start = 1950
        elif year_start == 1951:
            year_start = 1952
        elif year_start in [1955,1956]:
            year_start = 1957
        elif year_start == 1958:
            year_start = 1959
            
    year_end = input('Please enter the ending year: ')
    while checking_value_type(year_end) == False or (
        checking_value_type(year_end) == True and ((int(year_end) < df['title_year'].min()) or 
                                                   (int(year_end) > df['title_year'].max()) or 
                                                   (int(year_end) <= year_start ) )):
        print('Please enter a correct ending year which must be', 
              '\n- A whole number', 
              '\n- In range of ',
              df['title_year'].min(), ' - ',
              df['title_year'].max(), ' inclusively',
              '\n- Must be greater than ', year_start)
        year_end = input('Please enter again the ending year: ')
    year_end = int(year_end)
    # dealing with non-consecutive years
    if year_end not in set(df['title_year']):
        if year_end == 1928:
            year_end = 1929
        elif year_end in [1930,1931,1932]:
            year_end = 1933
        elif year_end == 1934:
            year_end = 1935
        elif year_end == 1938:
            year_end = 1939
        elif year_end in [1941,1942,1943,1944,1945]:
            year_end = 1946
        elif year_end == 1949:
            year_end = 1950
        elif year_end == 1951:
            year_end = 1952
        elif year_end in [1955,1956]:
            year_end = 1957
        elif year_end == 1958:
            year_end = 1959
            
    gross_plotting()   


##### MENU OPTION 4 #####

# defining plotting function
def genre_plotting():
    global genre_set
    global genre
    
    # creating a pandas Series containing all IMDB scores belonging to the selected genre, i.e. 'genre'
    result = df['genres'].str.contains(genre)
    imdb_of_selected_genre = df[result]['imdb_score']
    
    # describe information
    print('\n\na. Descriptive Statistics of the ' + genre + " movies' IMDB scores:\n")
    print(imdb_of_selected_genre.describe().drop('count').to_string())
     
    # plotting1: Distribution of IMDB scores of the selected movie genre
    # creating a list of imdb scores for each of movie genre, i.e. 'imdb_of_all_genres'
    imdb_of_all_genres = []
    for i in genre_set:
        r = df['genres'].str.contains(i)
        imdb_for_single_genre = df[r]['imdb_score']
        imdb_of_all_genres.append(imdb_for_single_genre)
    # plotting
    imdb_of_selected_genre.hist(figsize = (16,6), color = 'slategrey').grid(False)
    plt.axvline(x = imdb_of_selected_genre.mean(), color = 'red', linestyle='dashed', linewidth=2)
    plt.axvline(x = imdb_of_selected_genre.median(), color = 'limegreen', linestyle='dashed', linewidth=2)
    plt.legend(['Mean Score = ' + str(round(imdb_of_selected_genre.mean(), 2)), 
                'Median Score = ' + str(round(imdb_of_selected_genre.median(), 2))],
               loc="upper left",
              prop={"size":13})
    plt.title('IMDB SCORE DISTRIBUTION OF ' + genre.upper() + ' MOVIES')
    plt.xlabel('IBMD score')
    plt.ylabel('Count')
    plt.xticks(np.arange(0,10.5, 0.5), rotation = 0)
    plt.show()
    
    # plotting2:  Distribution of IMDB scores of the selected movie genre with other genres
    plt.figure(figsize=(16,6))
    box = plt.boxplot(imdb_of_all_genres, patch_artist = True)
    plt.xticks(np.arange(1,len(genre_set)+1, 1), genre_set, rotation = 90)
    plt.yticks(np.arange(1,10.5, 0.5))
    plt.xlabel('Movie Gerne')
    plt.ylabel('IDBD score')
    plt.title('BOXPLOTS OF IMDB SCORES WITH ' + genre.upper()+ ' MOVIES (RED) AND OTHER MOVIE GENRES')
    plt.grid(color = 'gainsboro',linestyle='dashed')
    colors = ['silver'] * len(genre_set)
    colors[genre_set.index(genre)] = 'red'
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()
    
    # plotting3a: Other comparisons
    temp = dict()
    for i in genre_set:
        r = df['genres'].str.contains(i)
        temp[i] = df[r].count()[0]
    k = pd.Series(temp)
    print('\nb. Number of ' + genre + ' movies: ' + str(k[genre]) + ' movies')
    # plotting
    plot4 = k.plot.bar(rot=90, title='BARPLOT OF NUMBER OF MOVIES FOR EACH MOVIE GENRE - ' + genre.upper() + ' (RED)', 
                       figsize = (16, 6), color = colors)
    plot4.set_xlabel("Movie Genre")
    plot4.set_ylabel("Number of Movies")
    plot4.grid(linestyle='dashed', linewidth='0.5', color='grey')
    plot4.set_axisbelow(True)
    plt.show()
    
    
    # plotting3b: Other comparisons
    # creating a list of gross earnings for each of movie genre, i.e. 'gross_of_all_genres'
    gross_of_all_genres = []
    for i in genre_set:
        r = df['genres'].str.contains(i)
        gross_for_single_genre = df[r]['gross']/1e8
        gross_of_all_genres.append(gross_for_single_genre)
    # descriptive statistics: 
    print("\nc. Descriptive Statistics of the " + genre + " movies' gross earnings: \n")
    print(gross_of_all_genres[genre_set.index(genre)].describe().drop('count').to_string())
    # plotting
    plt.figure(figsize=(16,6))
    box = plt.boxplot(gross_of_all_genres, patch_artist = True, showfliers = False)
    plt.xticks(np.arange(1,len(genre_set)+1, 1), genre_set, rotation = 90)
    #plt.yticks(np.arange(1,10.5, 0.5))
    plt.xlabel('Movie Gerne')
    plt.ylabel('Gross Earnings (Million US Dollars)')
    plt.title('BOXPLOTS OF GROSS EARNINGS WITH DIFFERENT MOVIE GENRES (WITHOUT OUTLIERS) - ' + genre.upper() + ' (RED)')
    plt.grid(color = 'gainsboro', linestyle='dashed')
    colors = ['silver'] * len(genre_set)
    colors[genre_set.index(genre)] = 'red'
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show()
    
    
    # plotting3c: Other comparisons
    # creating a list of movie facebook likes for each of movie genre, i.e. 'movie_FB_likes_of_all_genres'
    movie_FB_likes_of_all_genres = []
    for i in genre_set:
        r = df['genres'].str.contains(i)
        movie_FB_likes_for_single_genre = df[r]['movie_facebook_likes']
        movie_FB_likes_of_all_genres.append(movie_FB_likes_for_single_genre)
    # descriptive statistics:
    print("\nd. Descriptive Statistics of the " + genre + " movies' Facebook likes:\n")
    print(movie_FB_likes_of_all_genres[genre_set.index(genre)].describe().drop('count').to_string())
    # plotting
    plt.figure(figsize=(16,6))
    box = plt.boxplot(movie_FB_likes_of_all_genres, patch_artist = True, showfliers = False)
    plt.xticks(np.arange(1,len(genre_set)+1, 1), genre_set, rotation = 90)
    plt.xlabel('Movie Gerne')
    plt.ylabel('Number of Movie Facebook Likes')
    plt.title('BOXPLOTS OF MOVIE FACEBOOK LIKES WITH DIFFERENT MOVIE GENRES (WITHOUT OUTLIERS) - ' + genre.upper() + ' (RED)')
    plt.grid(color = 'gainsboro', linestyle='dashed')
    colors = ['silver'] * len(genre_set)
    colors[genre_set.index(genre)] = 'red'
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.show();

# putting together
def question4():
    global genre_set
    global genre
    
    print('\nYou chose Menu Option 4 - Genre Analysis')
    test = df['genres'].str.split('|')
    genre_set = set()
    for i in test:
        for j in i:
            genre_set.add(j)
    genre_set = sorted(genre_set)
    print('LIST OF GENRES:')
    for i in genre_set: 
        print(i)
        
    genre = input('Please enter a movie genre for analysis: ')
    while genre not in genre_set:
        print('\nInvalid input', '\nPlease try again')
        genre = input('Please enter again a movie genre for analysis: ')
    genre_plotting()


##### MENU OPTION 5 #####

def question5():
    temp = df[['duration', 
           'director_facebook_likes',
           'num_user_for_reviews',
           'num_critic_for_reviews',
           'num_voted_users',
           'cast_total_facebook_likes',
           'movie_facebook_likes',
           'facenumber_in_poster',
           'title_year',
           'aspect_ratio',
           'gross',
           'budget',
           'imdb_score']]
    
    print('\nDescriptive Statistics of All movies :')
    print(temp['imdb_score'].describe())
    print('\nPlease wait a moment, this takes sometime to run')
    
    sns.set(style="ticks")
    ax = sns.pairplot(temp)
    plt.show()
    
    ax = sns.heatmap(round(temp.corr(),2),
                     cmap="YlGnBu", 
                     cbar_kws={'ticks': [-1.0, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0]}, 
                     vmin=-1, 
                     vmax=1,
                     linewidths=.5,
                     annot=True)
    ax.set_title('HEATMAP PLOT - PEARSON CORRELATION COEFFICIENTS BETWEEN VARIABLES')
    ax.figure.set_size_inches(13,10)
    plt.show()
    
    sns.set_style("whitegrid")
    sns.pairplot(temp, 
                 x_vars=["duration", "director_facebook_likes", "num_user_for_reviews", "num_critic_for_reviews"],
                 y_vars=["imdb_score"], 
                 plot_kws={'line_kws':{'color':'red'}, 'scatter_kws':{"s": 10, 'alpha':0.3, 'color': 'navy'}},
                 height=4, aspect=1, kind="reg")
    plt.suptitle('PAIRPLOTS OF IMDB SCORES WITH OTHER VARIABLES', size = 20)
    sns.pairplot(temp, 
                 x_vars=["num_voted_users", "cast_total_facebook_likes", "movie_facebook_likes", "facenumber_in_poster"],
                 y_vars=["imdb_score"],
                 plot_kws={'line_kws':{'color':'red'}, 'scatter_kws':{"s": 10, 'alpha':0.3, 'color': 'navy'}},
                 height=4, aspect=1, kind="reg")
    sns.pairplot(temp, 
                 x_vars=["title_year", "aspect_ratio", "gross", "budget"],
                 y_vars=["imdb_score"],
                 plot_kws={'line_kws':{'color':'red'}, 'scatter_kws':{"s": 10, 'alpha':0.3, 'color': 'navy'}},
                 height=4, aspect=1, kind="reg")
    plt.show()


##### FINAL - PUTTING ALL TOGETHER #####
def main():
    print('MOVIE ANALYSIS',
          '\nPlease select your option below:',
          '\n1. Menu Option 1 – Most successful directors or actors', 
          '\n2. Menu Option 2 – Movie Comparison',
          '\n3. Menu Option 3 – Analyse the distribution of gross earnings',
          '\n4. Menu Option 4 – Genre Analysis',
          '\n5. Menu Option 5 - IMDB scores vs. Other numeric variables',
          '\n6. Menu Option 6 – Exit')
    menus = ['1','2','3','4','5','6']
    menu = input('Please enter an option for analysis (1,2,3,4,5 or 6): ')
    while menu != '6':
        if menu == '1':
            question1()
        elif menu == '2':
            question2()
        elif menu == '3':
            question3()
        elif menu == '4':
            question4()
        elif menu == '5':
            question5()
        print('Now you could choose AGAIN one of the following options',           
              '\n1. Menu Option 1 – Most successful directors or actors', 
              '\n2. Menu Option 2 – Movie Comparison',
              '\n3. Menu Option 3 – Analyse the distribution of gross earnings',
              '\n4. Menu Option 4 – Genre Analysis', 
              '\n5. Menu Option 5 - IMDB scores vs. Other numeric variables', 
              '\n6. Menu Option 6 – Exit')
        menu = input('Please enter an option for analysis (1,2,3,4,5 or 6): ')
    if menu == '6':
        print ('\nThank you!')
        return None
        


