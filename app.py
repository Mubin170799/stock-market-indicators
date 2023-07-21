from flask import Flask, render_template, request, session
import json
import plotly
import pandas as pd
import os
import pickle
import plotly.graph_objects as go
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = "123"

DATA_PATH = os.path.join(os.path.dirname(__file__), "static", "data");
MODELS_PATH = os.path.join(os.path.dirname(__file__), "static", "models");

users = [
    {"username" : "user1" , "password" : "user1"},
    {"username" : "user2" , "password" : "user2"},
    {"username" : "user3" , "password" : "user3"},
    {"username" : "user4" , "password" : "user4"},
    {"username" : "user5" , "password" : "user5"},
]


@app.route("/", methods=['GET' , 'POST'])
def landingpage():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # if(username == "admin" and password == "admin123"):
        for user in users:
            if(username == user['username'] and password == user['password']):
                session['username'] = username
                return render_template("index.html", username=session['username'])
        else:
            return render_template("login.html", msg="Invalid Credentials!")
    else:
        return render_template("login.html")

@app.route("/logout", methods=['GET' , 'POST'])
def logout():
    session.pop('username', None)
    return render_template("login.html")


@app.route("/home", methods=['GET' , 'POST'])
def home():
    if request.method == 'POST' and session['username'] != None:
        # getting selected stock name
        stock = request.form['stockname']

        # reading data
        data = pd.read_csv(DATA_PATH + "\\"+ stock+".csv")
      
        data=data.rename(columns={"Date": "ds", "Close": "y"})

        # splitting 80 : 20 into train_data and test_data
        split = int(len(data)*80/100)
        train_data=data[0:split]
        test_data=data[split:]

        # loading prophet model
        model = pickle.load(open( MODELS_PATH +'\\'+ stock+"_model.pkl", 'rb'))

        # forecasting data
        forecast = model.predict(test_data)

        # saving plot
        # fig2 =model.plot(forecast)
        # fig2.savefig('prophetplot.png')

        # Creating interactive plot
        
       
        fig = go.Figure(data=[go.Candlestick(x=data['ds'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['y'])])
        fig.update_yaxes(rangemode='tozero')

        fig1 = go.Figure([
            go.Scatter(
                name='Close Price',
                x=train_data['ds'],
                y=round(train_data['y'], 2),
                mode='lines',
                line=dict(color='rgb(31, 119, 180)'),
                showlegend=False
            ),
            go.Scatter(
                name='Actual Price',
                x=test_data['ds'],
                y=round(test_data['y'], 2),
                mode='lines',
                line=dict(color='rgb(255, 0, 0)'),
            ),
            go.Scatter(
                name='Predicted Price',
                x=forecast['ds'],
                y=round(forecast['yhat'], 2),
                mode='lines',
                line=dict(color='rgb(46, 184, 46)'),
            ),
            go.Scatter(
                name='95% CI Upper',
                x=forecast['ds'],
                y=round(forecast['yhat_upper'], 2),
                mode='lines',
                marker=dict(color='#444'),
                line=dict(width=0),
                showlegend=False
            ),
            go.Scatter(
                name='95% CI Lower',
                x=forecast['ds'],
                y=round(forecast['yhat_lower'], 2),
                marker=dict(color='#444'),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False
            )
        ])
        fig1.update_layout(
            xaxis_title='Date',
            yaxis_title= 'Close Price',
            title= stock +' Stock Price Prediction for 3 Months',
            template='plotly_dark',
            hovermode='x'
        )
        fig1.update_yaxes(rangemode='tozero')

 
        # Jsonify the plot and send it to the UI
        graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        
        return render_template("index.html", stock=stock, graphJSON1=graphJSON1 ,graphJSON2=graphJSON2, username=session['username'] )
    else:
        return render_template("index.html", username=session['username'])



        # save the company name in a variable
        #company_name = input("Please provide the name of the Company or a Ticker: ")
        #As long as the company name is valid, not empty...
        def full_detail(comapny_n):
            

            if company_name != '':
                print(f'Searching for and analyzing {company_name}, Please be patient, it might take a while...')

                #Extract News with Google News
                googlenews = GoogleNews(start=yesterday,end=now)
                googlenews.search(company_name)
                result = googlenews.result()
                #store the results
                df = pd.DataFrame(result)
                # print(df)


        try:
            list =[] #creating an empty list 
            for i in df.index:
                dict = {} #creating an empty dictionary to append an article in every single iteration
                article = Article(df['link'][i],config=config) #providing the link
                try:
                    article.download() #downloading the article 
                    article.parse() #parsing the article
                    article.nlp() #performing natural language processing (nlp)
                except:
                    pass 
                #storing results in our empty dictionary
                dict['Date']=df['date'][i] 
                dict['Media']=df['media'][i]
                dict['Title']=article.title
                dict['Article']=article.text
                dict['Summary']=article.summary
                dict['Key_words']=article.keywords
                list.append(dict)
            check_empty = not any(list)
            # print(check_empty)
            if check_empty == False:
                news_df=pd.DataFrame(list) #creating dataframe
                #print(news_df)

        except Exception as e:
            #exception handling
            print("exception occurred:" + str(e))
            print('Looks like, there is some error in retrieving the data, Please try again or try with a different ticker.' )


        #Sentiment Analysis
        def percentage(part,whole):
            return 100 * float(part)/float(whole)

        #Assigning Initial Values
        positive = 0
        negative = 0
        neutral = 0
        #Creating empty lists
        news_list = []
        neutral_list = []
        negative_list = []
        positive_list = []

        #Iterating over the tweets in the dataframe
        for news in news_df['Summary']:
            news_list.append(news)
            analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
            neg = analyzer['neg']
            neu = analyzer['neu']
            pos = analyzer['pos']
            comp = analyzer['compound']

            if neg > pos:
                negative_list.append(news) #appending the news that satisfies this condition
                negative += 1 #increasing the count by 1
            elif pos > neg:
                positive_list.append(news) #appending the news that satisfies this condition
                positive += 1 #increasing the count by 1
            elif pos == neg:
                neutral_list.append(news) #appending the news that satisfies this condition
                neutral += 1 #increasing the count by 1 

        positive = percentage(positive, len(news_df)) #percentage is the function defined above
        negative = percentage(negative, len(news_df))
        neutral = percentage(neutral, len(news_df))

        #Converting lists to pandas dataframe
        news_list = pd.DataFrame(news_list)
        neutral_list = pd.DataFrame(neutral_list)
        negative_list = pd.DataFrame(negative_list)
        positive_list = pd.DataFrame(positive_list)
        #using len(length) function for counting
        print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n')
        print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n')
        print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n')

        #Creating PieCart
        labels = ['Positive ['+str(round(positive))+'%]' , 'Neutral ['+str(round(neutral))+'%]','Negative ['+str(round(negative))+'%]']
        sizes = [positive, neutral, negative]
        colors = ['yellowgreen', 'blue','red']
        patches, texts = plt.pie(sizes,colors=colors, startangle=90)
        plt.style.use('default')
        plt.legend(labels)
        plt.title("Sentiment Analysis Result for stock= "+company_name+"" )
        plt.axis('equal')
        plt.show()

        if positive>negative:
            print(f"It has more probability to store in the stock {company_name} with percentage {positive}")
        elif negative< positive:
            print(f"It has less probability to store in the stock {company_name} with percentage {negative}")
        else: 
            print(f"It has equal probability to store in the stock {company_name}")



    full_detail(stock)




if __name__ == '__main__':
    app.run(debug=True)
