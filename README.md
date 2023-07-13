# world-bank-economic-indicators-db

The world bank indicators are an amazing data source for any one interested in social/economic research. The World Bank Indicators API provides access to nearly 16,000 time series indicators across a range of topics, listed below:

1. Agriculture & Rural Development
2. Aid Effectiveness
3. Economy & Growth
4. Education
5. Energy & Mining
6. Environment
7. Financial Sector
8. Health
9. Infrastructure
10. Social Protection & Labor
11. Poverty
12. Private Sector
13. Public Sector
14. Science & Technology
15. Social Development
16. Urban Development
17. Gender
18. Millenium Development Goals
19. Climate Change
20. External Debt
21. Trade

Despite the multitude of topics, only economy and growth statistics have been pulled for the time being due to some upcoming time-series analysis of financial data at work. As a result, I wanted a robust, accessible dataset to trial some of the more obscure r packages on. 

Consequently, I decided to build a simple data model using the economy and growth metrics. Following the API calls, the data was then  normalised to tables in SQLite with a values fact table, alongside country, income level, an indicators info and also a source table for all the different government sources to provide context. 

Lunar modeller was used to visualise the data model. Pytest has been utilised and I tried to introduce dbt but the sqlite package is sub-optimal due to it being a third-party community project.
