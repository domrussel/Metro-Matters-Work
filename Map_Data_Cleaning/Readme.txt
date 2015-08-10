README

This folder includes two R scripts used for data cleaning. We convert raw data from the census bureau's American Fact Finder, HUD's Picture of Subsidized Households, and the Kirwan Institute's Child Opportunity Index.  

CHANGE_IN_LOW_INCOME_HOUSING.R

-Opens HUD's Subsidized Households by Tract Information from 2014 and 2009
-Converts information listed by program to total units by tract and by program
-Merges the data with Kirwan Opportunity Index factorized opportunity level by census tract
-Uses Brown University's Longitudinal Tract Based Data to Convert 2000 Census Tracts to 2010 Census Tracts
-Creates a varible estimating change in total subsidized housing for 10 years



RCAP_and_aff_housing.R

-Creates a list of census tracts that qualify as Racialy Concentrated Areas of Poverty Using the Definition: Either 40 percent of residents live below the poverty line or 3 times the mean poverty rate AND more than fifty percent of residents are non_white
-Converts data listed by program in HUD's Subsidizied Household infomration to total units by tract and by program
-Merge affordable housing data with total housing units data from the census
-Calculate four final varibles: percent of housing subsidized for low-income persons in all Detroit-metro Census Tracts, percent of housing subsidized for low-income persons in Detroit-metro RCAPs, percent of housing that is low-income subsidized in the CBSA in RCAPs, percent of housing that in the CBSA that is in RCAPs