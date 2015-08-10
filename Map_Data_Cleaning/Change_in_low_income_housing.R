
data_cleaner = function(filename){
	aff = read.csv(filename)
	mi_aff = aff[aff$states == "MI Michigan",]
	mi_final = data.frame(matrix(NA, nrow = length(unique(mi_aff$code)), ncol = 8))
	names(mi_final) = c("FIPS", "Public Housing", "Housing Choice Vouchers", "Mod Rehab", "Section 8", "Section 236", "Multi-Family Other", "Total")
	for(i in c(1:length(unique(mi_aff$code)))){
		one_tract = mi_aff[mi_aff$code == unique(mi_aff$code)[i],]
		sum_tract = sum(one_tract$total_units, na.rm = TRUE)
		ph = one_tract[one_tract$program == 2,]$total_units
		hcv = one_tract[one_tract$program == 3,]$total_units
		mr = one_tract[one_tract$program == 4,]$total_units
		s8 = one_tract[one_tract$program == 5,]$total_units
		s236 = one_tract[one_tract$program == 6,]$total_units
		mfo = one_tract[one_tract$program == 7,]$total_units
		mi_final[i,] = c(unique(mi_aff$code)[i], ph, hcv, mr, s8, s236, mfo, sum_tract)
	}
	return(mi_final)
}

####CLEANING 2014 HUD AFFORDABILITY DATA

mi_final = data_cleaner("TRACT_AK_MN.csv")
write.csv(mi_final, "detroit_aff.csv")

####CLEANING 2009 HUD AFFORDABILITY DATA

mi_final_09 = data_cleaner("TRACT_AK_MN_2009.csv")
write.csv(mi_final_09, "detroit_aff_09.csv")

####OPENING KIRWAN OPPORTUNITY INDEX FILE AND CONVERTING IT TO NUMERIC FACTOR FOR MAPPING

d_opp = read.csv("Detroit_opp.csv")
library(plyr)
d_opp$ALLCOMPLEV = revalue(d_opp$ALLCOMPLEV, c("Very Low" = "1", "Low" = "2", "Moderate" = "3", "High" = "4", "Very High" = "5"))
d_final = merge(d_aff_change, d_opp)
write.csv(d_final, "det_opp_aff_change.csv")

###crosswalk from 2000 census tracts (used in 2009 files) to 2010 census tracts (used in 2014 files)

cross = read.csv("crosswalk_2000_2010.csv")
cross = cross[,1:3]
names(cross) = c("FIPS", "new_FIPS", "weight")
post_cross_det = merge(cross, d_aff_2009)
post_cross_det$weighted_total = post_cross_det$weight * post_cross_det$Total_09
det_final_2009 = data.frame(unique(post_cross_det$new_FIPS), rep(0, length(unique(post_cross_det$new_FIPS))))
names(det_final_2009) = c("FIPS_2010" , "aff_count")
for(i in c(1:length(post_cross_det$FIPS))){
	tract_2010 = post_cross_det[i,]$new_FIPS
	det_final_2009[det_final_2009$FIPS_2010 == tract_2010,]$aff_count = det_final_2009[det_final_2009$FIPS_2010 == tract_2010,]$aff_count + post_cross_det[i,]$weighted_total
}
names(det_final_2009) = c("FIPS", "Total_09")

###getting change from 2009 to 20014

d_aff_change = merge(d_aff_2014, det_final_2009)
d_aff_change$change = d_aff_change$Total - d_aff_change$Total_09
write.csv(d_aff_change, "det_opp_aff_change.csv")

