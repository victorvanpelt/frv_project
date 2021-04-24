clear all
set more off



/* please set directory first! */
cd "C:\Users\victo\Dropbox\Research\Projects\Rainer, Victor, and Farah\ACCDIN_CoordinatedDishonestyinReporting\04analyses"



/* Import data and file management */
import excel using "1_input\all_sessions.xlsx", firstrow

/* Variable naming */

// Generate base variables and identifiers
gen id = _n
rename coll_dishonest1playerid_in_gr id_in_group
gen prize_spread = (sessionconfigincentives == 1)
gen rpi = (sessionconfigrpi == 1)
gen payoff = sessionconfigparticipation_fee + coll_dishonest1playerpayoff
rename coll_dishonest1groupreport_on report_one
rename coll_dishonest1groupreport_tw report_two
gen dish_coll = (report_one==report_two)
gen treatment=(rpi==0 & prize_spread==0)
replace treatment=2 if rpi==1 & prize_spread==0
replace treatment=3 if rpi==0 & prize_spread==1
replace treatment=4 if rpi==1 & prize_spread==1
rename coll_dishonest1playerincentiv prize_spread_check
rename coll_dishonest1playerrpi_chec rpi_check
rename coll_dishonest1groupid_in_sub group_id_old

//rename demographics
rename coll_dishonest1playergender gender
rename coll_dishonest1playerage age
rename coll_dishonest1playerenglish english
rename coll_dishonest1playerrisk risk
rename coll_dishonest1playertrustwor trustworthy
rename coll_dishonest1playertrusting trusting
rename coll_dishonest1playercorona corona_fear



/* Sample Selection Criteria */

// Identify people to drop formally
gen exclude = 0

//People who did not find a partner
replace exclude = 1 if coll_dishonest1playerno_partn==1 

//People that dropped or whose partner dropped
replace exclude = 1 if coll_dishonest1playerdrop_out==1
replace exclude = 1 if FV==1

//drop if they fail the attention check
replace exclude = 1 if coll_dishonest1playerattentio!=2

//Create unique group ids and session ids
sort sessioncode group_id_old id_in_group
egen group_id = group(sessioncode group_id_old) if exclude==0
egen session_id = group(sessioncode)

//Create group selector (This code creates an indicator for full groups)
sort sessioncode group_id_old id_in_group group_id
gen group_full = (exclude==0)
by sessioncode group_id_old: replace group_full = 0 if id_in_group==1 & exclude[_n+1]==1 
by sessioncode group_id_old: replace group_full = 0 if id_in_group==2 & exclude[_n-1]==1 

// 272 obs total (100%) - 69 obs excluded (56%) = 154 obs usable sample (44%)
sum id if exclude==0
sum id if exclude==1
drop if exclude==1

// No duplicates
duplicates examples

//drop if timed_out
histogram time
sum time, d
list sessioncode if time>1000
list session_id


/* Manipulation Checks and Randomization */

//Check whether interventions worked
ttest rpi_check, by(rpi)
ttest prize_spread_check, by(prize_spread)

//Check randomization
regress gender i.treatment
regress age i.treatment
regress english i.treatment
regress risk i.treatment
regress trustworthy i.treatment
regress trusting i.treatment
regress corona_fear i.treatment

//SAVE all Data
save "2_process\all_session_total_clean.dta", replace



/* Analyses */

// Descriptive Statistics per Treatment
estpost tabstat report_one report_two dish_coll if id_in_group==1, statistics(mean sd min max n) by(treatment)
esttab using "3_output\Table 1.rtf", replace cells("report_one report_two dish_coll") noobs nomtitle nonumber eqlabels("No RPI / No Prize Spread" "RPI / No Prize Spread" "No RPI / Prize Spread" "RPI / Prize Spread") varwidth(20)

// ttests against 3.5 average per treatment
ttest report_one==3.5 if rpi==0 & prize_spread==0 & group_full==1 & id_in_group==1
ttest report_one==3.5 if rpi==1 & prize_spread==0 & group_full==1 & id_in_group==1
ttest report_one==3.5 if rpi==0 & prize_spread==1 & group_full==1 & id_in_group==1
ttest report_one==3.5 if rpi==1 & prize_spread==1 & group_full==1 & id_in_group==1

ttest report_two==3.5 if rpi==0 & prize_spread==0 & group_full==1 & id_in_group==1
ttest report_two==3.5 if rpi==1 & prize_spread==0 & group_full==1 & id_in_group==1
ttest report_two==3.5 if rpi==0 & prize_spread==1 & group_full==1 & id_in_group==1
ttest report_two==3.5 if rpi==1 & prize_spread==1 & group_full==1 & id_in_group==1

// logit regression of corrup collaboration on treatments
sum dish_coll if group_full==1 & rpi==0 & prize_spread==0 & id_in_group==1
sum dish_coll if group_full==1 & rpi==1 & prize_spread==0 & id_in_group==1
sum dish_coll if group_full==1 & rpi==0 & prize_spread==1 & id_in_group==1
sum dish_coll if group_full==1 & rpi==1 & prize_spread==1 & id_in_group==1

sum session_id
//anova dish_coll rpi##prize_spread if group_full==1 & id_in_group==1
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1, r
eststo: logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1, r
esttab using "3_output\Table 2.rtf", ///
replace stats(r2_p chi2 p df_m N) b(3) aux(se 3) star(* 0.10 ** 0.05 *** 0.01) obslast onecell nogaps ///
compress title(Table 5 - Logistic Regression) addnotes(p-levels are two-tailed, * p < 0.10, ** p < 0.05, *** p < 0.01; the numbers within the round parentheses are robust standard errors.) nonotes
eststo clear

exit, STATA clear