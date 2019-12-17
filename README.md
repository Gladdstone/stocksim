
# Stock Simulator Proposal
## Summary
A simulated stock trading application implementing the multiple realtime and historical stock APIs to execute simulated user trades versus the NYSE and NASDAQ in real time. Users are able to set a starting amount of virtual money and execute simulated trades.

## Input
We will be pulling from various finance and stock APIs to get the realtime and historical price of the stocks, the index, the stock symbol, and the time bought.

* User data from database
* Generated report data pulled from database
* Dynamic interaction with API

## Data Sources
1. Alpha Vantage - An API that allows users to pull real-time and historical stock data (5 API requests per minute and 500 requests per day)

2. Investor Exchange Trading API - unlimited real time stock API to enable automated trading (over 100 requests per second.)

3. Tradier API (60 request per minute.)

## Technology Stack
#### Front End
* Vanilla JavaScript
  * Our focus is mainly on the Database and Backend portion of the application since the project is for Database Application Development. We decided to stick with Vanilla JS in order to keep it simple as well as make sure any member can easily contribute.
* SASS
 * SASS is relatively  easy to learn and most members are comfortable with SASS 
* D3.js 
	* D3 is being used to help with data visualization on the front end

#### Back End
* Python
  * Developers on the team are comfortable programming in Python. Python provides a range of libraries that allow the team to meet the needs of the project.
  
#### Database
* PostgreSQL
  * PostgreSQL is a great open source option that provides features to protect data integrity, extensible, and a chance to explore a new type of relational database for most team members.

-------
Please refer to the project's Wiki in the upcoming weeks for up to date documentation. The Wiki will contain in-depth details of design patterns, architecture, roles, expectations, and more.
