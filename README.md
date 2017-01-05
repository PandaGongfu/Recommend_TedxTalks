# Recommend_TedxTalks
Recommend Similar Tedx Talks and Ted blogs using topic modeling  

This goal of this project is to recommend Tedx talks and Ted blog posts that are similar to a given Ted Talk.  
The motivation is that there are more than 80k+ Tedx videos and it's difficult for people to navigate and   
find exactly what they need.   

Use topic modeling (NMF), we create an app that allowers users to quickly locate the most similar Tedx talks   
based on contents. The workflow is as follows:  
1. Scrape transcripts of Ted and Tedx talks from youtube and Ted idea blogs from Ted.com.   
2. Use NMF to assign topic socres.   
3. Calculate similarity and make recommendations.    

Code for step 1 - scraping is included in scripts.  
Code for step 2 is included in jupyter_notebooks.       
Code for step 3 is included in app.  

![screenshot](images/ted_app.png)
