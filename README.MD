# <h1 align = "center"> **US Births Data 2016-2021** </h1>

# <h2 align = "left"> **Link to Dashboard App** </h2>
https://us-birth-data-map-2016-2023.onrender.com

# <h2 align = "left"> **Project Description** </h2>
The following dashboard was developed to showcase my skills and knowledge in building a dashboard using Dash. This dashboard will visually present an overview of data collected on US Births between 2016 and 2021. Dash is an open-source framework for building data visualization interfaces in Python.
This dashboard utilizes a dataset that contains the following information:
- State
- State Abbreviation
- Year
- Education Level of Mother - The highest education level the mother posseses.
- Number of Births 
- Total Births in State   
- Average Age of Mother
- Political Party Governing the State.

# <h2 align = "left"> **Dashboard Layout** </h2>
The dashboard layout consists of two main parts: 
- Sidebar - This container includes interactive widgets to control the behavior and parameters of the dashboard.
- Main Window - The main window is where the US Map and a bar chart will be displayed based on the user's inputs through the sidebar.

# <h2 align = "left"> **Sidebar Widgets** </h2>
The sidebar of the dashboard consists of the following widgets:
- Dropdown Menu for Map Data Display Options: This widget allows users to select the type of data they want to visualize on the map. The available options are:
    - Percentage of Education Level
    - Average Age of Mother by Education level
- Dropdown Menu for Highest Education Level: This widget enables users to choose the highest education level attained by individuals who became mothers. The available options for this dropdown menu are: 
    - 8th Grade
    - Between 9th and 12th Grade
    - High School Graduate
    - Some College Credits
    - Associate Degree
    - Bachelor's Degree
    - Master's Degree
    - Doctorate
    - Unknown
- Slider for Year Selection: This widget allows users to filter the data based on a specific year or a range of years. Users can slide the slider to select a single year or drag the slider handles to specify a range of years. This feature provides flexibility in analyzing data for a particular time frame.

Based on the user's input, the dashboard allows users to visualize data on a US map based on different parameters. The first dropdown menu enables the selection of a specific data parameter, such as "Percentage of Education Level" or "Average Age of Mother by Education Level".

The second dropdown menu allows users to choose a specific category within the selected parameter, such as "High School Graduate" or any other education level.

Additionally, the slider widget allows users to filter the data based on a specified range of years, such as 2016-2018.

Based on the chosen options, the dashboard will display the corresponding data on the US map. For example, if "Percentage of Education Level" is selected, and "High School Graduate" is chosen as the category, the map will show the percentage of births in each state where the mother's highest level of education is a high school diploma during the specified years.

Alternatively, if "Average Age of Mother by Education Level" is selected, and "High School Graduate" is chosen as the category, the map will display the average age at which individuals with a high school education level become mothers.

By providing these interactive features and data visualizations, the dashboard enables users to explore and gain insights into various aspects of education levels and maternal age across different states in the United States.

# <h2 align = "left"> **Main Window** </h2>
The main window of the dashboard consists of two visualizations:
- Interactive Choropleth Map: This visualization displays the United States map, where each state is color-coded based on the selected data parameter. Users can interact with the map by clicking on any state to view additional information or specific data related to that state.
- Bar Chart: This visualization complements the choropleth map by displaying a bar chart that shows the percentage of births by education level for the state selected through the choropleth map. The bar chart provides a detailed breakdown of the educational attainment of mothers in the selected state. Each education level category is represented by a bar, and the height of each bar represents the corresponding percentage of births for that education level category.

Together, these visualizations offer a comprehensive view of the data. The choropleth map provides a spatial representation of the data across different states, allowing users to identify regional patterns or variations. The bar chart offers a more detailed and specific analysis of the educational levels of mothers within the selected state, providing insights into the distribution of births by education level.


