For this project, we designed a dashboard that could reflect the different kinds of data associated with the rise of energy drink consumption.
As energy drinks have seemed to grow in popularity, escpecially on campuses such as ours, it could be interesting to evaluate the negative
health consequences, while also looking at the regional differences in sales and popularity over the past several years.

The web app has the most recent build deployed through Render at (https://dashproject-k4l6.onrender.com/).

Data sources: 
MIT Licensed Sales Data: (https://www.kaggle.com/datasets/prasadahirekar/soft-drink-sales) <br>
Google Trends Data: __ <br>
Health Data: API Openfda.gov ("https://api.fda.gov/food/event.json?search=products.name_brand:%22RED+BULL%22+OR+products.name_brand:%22MONSTER+ENERGY%22+OR+products.name_brand:%225+HOUR%22+OR+products.name_brand:%22BANG%22+OR+products.name_brand:%22C4%22+OR+products.name_brand:%22CELSIUS%22&limit=1000") <br>

Authors: Conner Small, Tai Chirasittikorn, Julia Levy

Data Dictionary: 

| Data Item          | Data Type  |       Example      | 
| ------------------ | ---------- | ------------------ |
| reaction           | dictionary | {"Chest pain"}     |
| name_brand         | dictionary | {"MONSTER ENERGY"} |
| Period             | string     |      "2021Q1"      |
| Customer State     | string     |     "Virginia      |
| Region Code        | string     |        "VA"        |
| Interest over time | int        |        100         |
| year               | date       |        2024        |