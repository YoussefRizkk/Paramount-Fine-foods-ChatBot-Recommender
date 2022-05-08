SELECT * 
FROM [dbo].['Covid Deaths']
order by 3,4

--SELECT * 
--FROM [dbo].['Covid Vaccinations']
--order by 3,4



/* Select the data that we are going to be using */ 

SELECT  DE.location,DE.date,DE.total_cases,DE.new_cases,DE.total_deaths,DE.population
FROM [dbo].['Covid Deaths'] DE
order by 1,2



/* Total Cases Vs Total Death: show the % of deaths */ 

SELECT  DE.location,DE.date,DE.total_cases,DE.total_deaths, (total_deaths/total_cases)*100 Percentage_Of_Death
FROM [dbo].['Covid Deaths'] DE
order by 1,2            
/* Analyse Results: for example: from row number 29, you have a 2.5% to die if you got Covid and lives in Afghanistan */ 



/* Total Cases Vs Total Death in any location that has the word state in it */ 

SELECT  DE.location,DE.date,DE.total_cases,DE.total_deaths, (total_deaths/total_cases)*100 Percentage_Of_Death
FROM [dbo].['Covid Deaths'] DE
WHERE location like '%states%' 
order by 1,2  

/* Total Cases Vs Total Death in any location that has the word canada in it */ 

SELECT  DE.location,DE.date,DE.total_cases,DE.total_deaths, (total_deaths/total_cases)*100 Percentage_Of_Death
FROM [dbo].['Covid Deaths'] DE
WHERE location like '%canada%' 
order by 1,2  



/* Total Cases Vs Population: show the % of cases in Canada */ 

SELECT  DE.location,DE.date,DE.total_cases,DE.population, (total_cases/population)*100 Percentage_of_Cases 
FROM [dbo].['Covid Deaths'] DE
WHERE location like '%canada%'
order by 1,2

/* All the coming quires are related to Canada: */

/* Min and max number of new cases, total cases , new deaths, total deaths. Min and max percentage of cases and deaths that Canada has reached: */

SELECT Min(DE.total_cases) Min_total_cases,Min(DE.new_cases) Min_new_cases,Min(DE.new_deaths)Min_new_deaths,Min(DE.total_deaths)Min_total_deaths,
Max(DE.total_cases) Max_total_cases,Max(DE.new_cases) Max_new_cases,Max(DE.new_deaths)Max_new_deaths,Max(DE.total_deaths)Max_total_deaths,
Min(DE.total_cases/DE.population)*100 Min_percent_Of_cases,Min(DE.total_deaths/DE.total_cases)*100 Min_Percent_Of_deaths,
Max(DE.total_cases/DE.population)*100 Max_percent_Of_cases,Max(DE.total_deaths/DE.total_cases)*100 Max_Percent_Of_deaths
FROM [dbo].['Covid Deaths'] DE
WHERE location like '%canada%'


/* Date of the max number of new cases */ 
/* The easy method */ 
SELECT DE.date,new_cases Max_new_cases 
FROM [dbo].['Covid Deaths'] DE
WHERE new_cases = (SELECT Max(new_cases) FROM [dbo].['Covid Deaths'])

/* Second method contains creating and saving a variable, we are applying this method here just to show how to create and save a variable then use it in a query */

DECLARE @max_new_cases INT
SET @max_new_cases = (SELECT Max(new_cases) FROM [dbo].['Covid Deaths'])
SELECT date,new_cases FROM [dbo].['Covid Deaths']
WHERE new_cases=@max_new_cases  



/*  Which continent has the largest total number of cases  */

SELECT DE.continent, sum(total_cases) Total_Cases 
FROM [dbo].['Covid Deaths'] DE
WHERE continent <> 'Null'
group by DE.continent
order by Total_Cases DESC


/* What Country has the highest infection rate with respect to its population */ 

SELECT location,population, max((total_cases)/population)*100 Max_infection_rate
FROM [dbo].['Covid Deaths']
group by location,population
order by Max_infection_rate desc  


/* What Continent has the highest infection rate with respect to its population */ 

SELECT DE.continent, max((total_cases/ population)*100) Max_infection_rate
FROM [dbo].['Covid Deaths'] DE
group by continent
order by Max_infection_rate desc 


/* Which countries has highest death rate with respect to population */ 

SELECT location, max((total_deaths/population)*100) max_death_rate 
FROM [dbo].['Covid Deaths']
group by location
order by max_death_rate desc 

/* Which countries has the highest death count  */ 


Select location, max(total_deaths) max_total_deaths
FROM [dbo].['Covid Deaths']
group by location 
order by max_total_deaths desc    /* When we look at the resukts, they doesn't make sense, most of them are 90s so we cast the max total deaths as integer */ 
/* This happens alot of times */ 

Select location, max(cast(total_deaths as int)) max_total_deaths
FROM [dbo].['Covid Deaths']
group by location 
order by max_total_deaths desc    /* This issue was solved but now we have another issue: we notice locations as world , north america, Asia...
but we are looking for countries not continents ..) one of the reasons we noticed is that when the continent is empty, the name of the continet is inserted in the 
location column so to solve that: ( 2mrar bdl ma ynzl 2sm l continent be l column lal continet 3m ynzl bl column lal location w 3m ynzl null bdel l2sm) */ 


Select location, max(cast(total_deaths as int)) max_total_deaths
FROM [dbo].['Covid Deaths']
WHERE continent is not null 
group by location 
order by max_total_deaths desc  


/* Showing the continent with highest Death count: */ 
SELECT continent, Max(cast(total_deaths as INT)) Max_total_deaths
FROM [dbo].['Covid Deaths']
WHERE continent is not null
Group by continent
order by Max_total_deaths desc 


-- GLOBAL NUMBERS : 

/* Global  cases , deaths every day and death rate every day : */ 

/* Since bddi 2st3ml group by so total death and total deaths lezm 23mlln aggregate function, so 27sa she bdl ma 2st3mln bst3ml new cases w b3mlln sum by3toni l 
total cases and same lal total deaths */

SELECT date, sum(new_cases) Total_cases ,sum(new_deaths) Total_deaths 
FROM [dbo].['Covid Deaths']
WHERE continent is not null 
Group by date 
order by 2   /* We notice that if we run this code , we will get an error: 3m y2lna 2nno fe data type nvchar w ana 3m 23mlla sum w
ma fena n3ml hek, ana 3m 23ml sum lal new cases and new deaths, bro7 bt2kkd mn ldata type t3oltn: 3l shmel 2sm ltable fe plus sign 7ddo, brj3 bkbs 3l 
columns w by3tini ltype la kl column, so bddi 2rj3 23ml cast to int: */ 

SELECT date, sum(new_cases) Total_cases ,sum(cast(new_deaths as INT)) Total_deaths 
FROM [dbo].['Covid Deaths']
WHERE continent is not null 
Group by date 
order by 1,2 

/* Add to the above code the death rate: */

SELECT date, sum(new_cases) Total_cases ,sum(cast(new_deaths as INT)) Total_deaths , (sum(cast(new_deaths as int))/sum(new_cases))*100 Death_rate 
FROM [dbo].['Covid Deaths']
WHERE continent is not null 
Group by date 
order by 1,2 


/* Total Global cases, deaths, death rate: */

Select sum(new_cases) Total_cases,sum(cast(new_deaths as INT)) Total_deaths,(sum(cast(new_deaths as int))/sum(new_cases))*100 Death_rate 
FROM [dbo].['Covid Deaths']
WHERE continent is not null 


 /* We separated in the first of the projet the data into two tables to be easier to read and extract quires , now we will start using the second table for quires: 

 Total Vaccinated people , for that we need the vaccinated people from covid_vaccinations table and population from covid_deaths tabl so we will join the two tables*/

SELECT DE.continent,DE.date,DE.population,CONVERT(INT,VAC.new_vaccinations) New_Vaccinations
FROM [dbo].['Covid Deaths'] DE
JOIN [dbo].['Covid_Vaccinations'] VAC
ON DE.date = VAC.date 
and DE.location = VAC.location 
WHERE DE.continent is not null
Order by 4 desc  


/*Compare new cases in each location with the total new cases in this location ( partition by method) */

SELECT DE.location,DE.date,DE.population, new_cases,
sum(new_cases) OVER (Partition by location) Total_new_cases
FROM [dbo].['Covid Deaths'] DE
WHERE DE.continent is not null 
order by 1,2 


/* Compare total cases in each continent with respect to the global total cases and show a rate: */

SELECT continent,date, new_cases,sum(new_cases) OVER (Partition by continent) Total_Continent_Cases
FROM [dbo].['Covid Deaths'] DE
WHERE DE.continent is not null 
order by 1,2

/* Show total continent cases, total global cases and infection rate */


DECLARE @Global_Cases float 
SET @Global_Cases = (SELECT sum(new_cases) FROM [dbo].['Covid Deaths'] WHERE continent is not null)
SELECT continent, sum(new_cases) Total_Continent_Cases, @Global_Cases Total_global_cases , (sum(new_cases)/@Global_Cases)*100 Infection_rate 
FROM [dbo].['Covid Deaths']
WHERE continent is not null
GROUP BY continent
ORDER BY 1 


/* To create a view */ 

CREATE VIEW First_VIEW as 
SELECT DE.continent,DE.date,DE.population,CONVERT(INT,VAC.new_vaccinations) New_Vaccinations
FROM [dbo].['Covid Deaths'] DE
JOIN [dbo].['Covid_Vaccinations'] VAC
ON DE.date = VAC.date 
and DE.location = VAC.location 
WHERE DE.continent is not null
--Order by 4 desc  