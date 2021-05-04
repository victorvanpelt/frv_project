clear all
set more off



/* please set directory first! */
cd "C:\Users\victo\Dropbox\Research\Projects\Rainer, Victor, and Farah\ACCDIN_CoordinatedDishonestyinReporting\frv_project"



/* Import data and file management */
import excel using "1_input\all_sessions.xlsx", firstrow






/* Variable naming and cleaning */

//rename demographics
rename coll_dishonest1playergender gender
rename coll_dishonest1playerage age
rename coll_dishonest1playerenglish english
rename coll_dishonest1playerrisk risk
rename coll_dishonest1playertrustwor trustworthy
rename coll_dishonest1playertrusting trusting
rename coll_dishonest1playercorona corona_fear

// Generate base variables and rename variables
gen id = _n
rename coll_dishonest1playerid_in_gr id_in_group
gen prize_spread = (sessionconfigincentives == 1)
gen rpi = (sessionconfigrpi == 1)
gen payoff = sessionconfigparticipation_fee + coll_dishonest1playerpayoff
drop sessionconfigparticipation_fee coll_dishonest1playerpayoff
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
gen male=(gender==1)
gen female=(gender==2)
rename coll_dishonest1groupwinner_pa one_won
rename HC two_won
rename GX number_correct_two
rename coll_dishonest1groupnumber_co number_correct_one
rename GY time_left_two
rename coll_dishonest1grouptime_left time_left_one
rename coll_dishonest1grouppayoff_pa payoff_part1_one
rename HA payoff_part1_two
rename coll_dishonest1groupcheck_rep check_report_one
rename HE check_report_two
rename HH payoff_part2_one
rename HI payoff_part2_two
rename FV drop_out_mate
rename coll_dishonest1playerno_partn no_partner
drop coll_dishonest1playerInstr1 coll_dishonest1playerInstr2 coll_dishonest1playerInstr3
rename coll_dishonest1playerInstr1_w cd_instr1_wrong
rename coll_dishonest1playerInstr2_w cd_instr2_wrong
rename coll_dishonest1playerInstr3_w cd_instr3_wrong
rename raven1playerInstr1_wrong raven_instr1_wrong
rename raven1playerInstr2_wrong raven_instr2_wrong
rename coll_dishonest1playerdrop_out drop_out
rename coll_dishonest1playerattentio attention_check

// Remove variables we won't use
drop coll_dishonest1groupincentive coll_dishonest1grouprpi participant_is_bot participant_index_in_pages participant_index_in_pages participant_max_page_index participant_current_app_name participant_current_page_name participanttime_started participantvisited participantmturk_worker_id participantmturk_assignment_id participantpayoff sessionmturk_HITId sessionmturk_HITGroupId sessionis_demo coll_dishonest1subsessionroun payment_info1playerid_in_grou payment_info1playerpayoff payment_info1playerincentives payment_info1playerrpi payment_info1playermturk_feed payment_info1groupid_in_subse payment_info1subsessionround_ participantid_in_session sessionconfigrpi sessionconfigincentives sessionconfigreal_world_curren raven1playerid_in_group raven1playerpayoff raven1playerincentives raven1playerrpi raven1playerInstr1 raven1playerInstr2 raven_instr1_wrong raven_instr2_wrong raven1playertask raven1playercheck_task raven1playernumber_correct raven1playertime_left raven1groupid_in_subsession raven1subsessionround_number raven2playerid_in_group raven2playerpayoff raven2playerincentives raven2playerrpi raven2playertask raven2playercheck_task raven2playernumber_correct raven2playertime_left raven2groupid_in_subsession raven2subsessionround_number raven3playerid_in_group raven3playerpayoff raven3playerincentives raven3playerrpi raven3playertask raven3playercheck_task raven3playernumber_correct raven3playertime_left raven3groupid_in_subsession raven3subsessionround_number raven4playerid_in_group raven4playerpayoff raven4playerincentives raven4playerrpi raven4playertask raven4playercheck_task raven4playernumber_correct raven4playertime_left raven4groupid_in_subsession raven4subsessionround_number raven5playerid_in_group raven5playerpayoff raven5playerincentives raven5playerrpi raven5playertask raven5playercheck_task raven5playernumber_correct raven5playertime_left raven5groupid_in_subsession raven5subsessionround_number raven6playerid_in_group raven6playerpayoff raven6playerincentives raven6playerrpi raven6playertask raven6playercheck_task raven6playernumber_correct raven6playertime_left raven6groupid_in_subsession raven6subsessionround_number raven7playerid_in_group raven7playerpayoff raven7playerincentives raven7playerrpi raven7playertask raven7playercheck_task raven7playernumber_correct raven7playertime_left raven7groupid_in_subsession raven7subsessionround_number raven8playerid_in_group raven8playerpayoff raven8playerincentives raven8playerrpi raven8playertask raven8playercheck_task raven8playernumber_correct raven8playertime_left raven8groupid_in_subsession raven8subsessionround_number raven9playerid_in_group raven9playerpayoff raven9playerincentives raven9playerrpi raven9playertask raven9playercheck_task raven9playernumber_correct raven9playertime_left raven9groupid_in_subsession raven9subsessionround_number raven10playerid_in_group raven10playerpayoff raven10playerincentives raven10playerrpi raven10playertask raven10playercheck_task raven10playernumber_correct raven10playertime_left raven10groupid_in_subsession raven10subsessionround_number







/* Sample Selection Criteria */

// Identify people to drop formally
gen exclude = 0

//People who did not find a partner
replace exclude = 1 if no_partner==1 

//People that dropped or whose partner dropped
replace exclude = 1 if drop_out==1
replace exclude = 1 if drop_out_mate==1

//drop if they fail the attention check
replace exclude = 1 if attention_check!=2

//Create unique group ids and session ids
sort sessioncode group_id_old id_in_group
egen group_id = group(sessioncode group_id_old)
egen session_id = group(sessioncode)

//Create group selector (This code creates an indicator for full groups)
//sort sessioncode group_id_old id_in_group group_id
sort sessioncode group_id id_in_group
gen group_full = 1
by sessioncode group_id: replace group_full = 0 if id_in_group==1 & exclude[_n+1]==1 
by sessioncode group_id: replace group_full = 0 if id_in_group==2 & exclude[_n-1]==1 
by sessioncode group_id: egen single_member = count(group_id)
replace group_full = 0 if single_member==1

//Drop if not a full group
replace exclude = 1 if group_full==0

// 1042 obs total (100%) - 272 obs excluded = 770 obs usable sample
sum id if exclude==0
sum id if exclude==1
drop if exclude==1

// No duplicates
duplicates examples





/* Manipulation Checks and Randomization */
sort sessioncode group_id id_in_group

//How long did they take? Few outliers, but leaving them in.
histogram time
sum time, d

//Check whether interventions worked
ttest rpi_check, by(rpi)
ttest prize_spread_check, by(prize_spread)

//Check randomization
regress male i.treatment
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

ttest report_two==3.5 if rpi==0 & prize_spread==0 & group_full==1 & id_in_group==2
ttest report_two==3.5 if rpi==1 & prize_spread==0 & group_full==1 & id_in_group==2
ttest report_two==3.5 if rpi==0 & prize_spread==1 & group_full==1 & id_in_group==2
ttest report_two==3.5 if rpi==1 & prize_spread==1 & group_full==1 & id_in_group==2

// Descriptive statistics for collective dishonesty
sum dish_coll if group_full==1 & rpi==0 & prize_spread==0 & id_in_group==2
sum dish_coll if group_full==1 & rpi==1 & prize_spread==0 & id_in_group==2
sum dish_coll if group_full==1 & rpi==0 & prize_spread==1 & id_in_group==2
sum dish_coll if group_full==1 & rpi==1 & prize_spread==1 & id_in_group==2

//Not really any simple effects
tabulate dish_coll prize_spread if group_full==1 & rpi==0 & id_in_group==2, chi2
tabulate dish_coll rpi if group_full==1 & prize_spread==0 & id_in_group==2, chi2
tabulate dish_coll rpi if group_full==1 & prize_spread==1 & id_in_group==2, chi2
tabulate dish_coll prize_spread if group_full==1 & rpi==1 & id_in_group==2, chi2

//Also no difference between absent/absent and present/present
tabulate dish_coll treatment if group_full==1 & treatment!=2 & treatment!=3 & id_in_group==2, chi2

// (logit) regression of player 2 collaborating on treatments
regress dish_coll report_one rpi##prize_spread if group_full==1 & id_in_group==2, r
eststo: logistic dish_coll report_one rpi##prize_spread if group_full==1 & id_in_group==2, r

//With controls
regress dish_coll report_one rpi##prize_spread male age english risk trustworthy trusting corona_fear if group_full==1 & id_in_group==1, r
logistic dish_coll report_one rpi##prize_spread male age english risk trustworthy trusting corona_fear if group_full==1 & id_in_group==1, r

// Split Second mover analysis by winner/loser
// Descriptive statistics
sum dish_coll if group_full==1 & rpi==0 & prize_spread==0 & id_in_group==2 & two_won==0
sum dish_coll if group_full==1 & rpi==1 & prize_spread==0 & id_in_group==2 & two_won==0
sum dish_coll if group_full==1 & rpi==0 & prize_spread==1 & id_in_group==2 & two_won==0
sum dish_coll if group_full==1 & rpi==1 & prize_spread==1 & id_in_group==2 & two_won==0

//
sum dish_coll if group_full==1 & rpi==0 & prize_spread==0 & id_in_group==2 & two_won==1
sum dish_coll if group_full==1 & rpi==1 & prize_spread==0 & id_in_group==2 & two_won==1
sum dish_coll if group_full==1 & rpi==0 & prize_spread==1 & id_in_group==2 & two_won==1
sum dish_coll if group_full==1 & rpi==1 & prize_spread==1 & id_in_group==2 & two_won==1
// (Logit) regressions
regress dish_coll report_one rpi##prize_spread if group_full==1 & two_won==1 & id_in_group==2, r
eststo: logistic dish_coll report_one rpi##prize_spread if group_full==1 & two_won==1 & id_in_group==2, r

regress dish_coll report_one rpi##prize_spread if group_full==1 & two_won==0 & id_in_group==2, r
eststo: logistic dish_coll report_one rpi##prize_spread if group_full==1 & two_won==0 & id_in_group==2, r

// Export the three logistic regressions (all, second mover won, second mover lost)
esttab using "3_output\Table 2.rtf", replace stats(r2_p chi2 p df_m N) b(3) aux(se 3) star(* 0.10 ** 0.05 *** 0.01) obslast onecell nogaps ///
compress title(Table 5 - Logistic Regressions of Second Mover Collaboration) addnotes(p-levels are two-tailed, * p < 0.10, ** p < 0.05, *** p < 0.01; the numbers within the round parentheses are robust standard errors.) nonotes
eststo clear

// First mover analysis
eststo: regress report_one rpi##prize_spread if group_full==1 & id_in_group==1, r
eststo: regress report_one rpi##prize_spread if group_full==1 & one_won==1 & id_in_group==1, r
eststo: regress report_one rpi##prize_spread if group_full==1 & one_won==0 & id_in_group==1, r

// Export the three regressions (all, second mover won, second mover lost)
esttab using "3_output\Table 3.rtf", replace stats(r2_a F p df_m N) b(3) aux(se 3) star(* 0.10 ** 0.05 *** 0.01) obslast onecell nogaps ///
compress title(Table 5 - OLS Regressions of First Mover Report) addnotes(p-levels are two-tailed, * p < 0.10, ** p < 0.05, *** p < 0.01; the numbers within the round parentheses are robust standard errors.) nonotes
eststo clear

/*
// JUST SAVED NOTES FOR VICTOR (CAN BE REMOVED)

//Additional splits
//Gender
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & male==1, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & male==1, r
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & female==1, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & female==1, r

//Trusting people
////---> Tournament negative effect with trusting people ONLY
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & trusting==1, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & trusting==1, r
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & trusting==0, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & trusting==0, r

//Trustworthy people
sum trustworthy, d
gen d_trustworthy = (trustworthy>=r(p50))
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & d_trustworthy==1, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & d_trustworthy==1, r
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & d_trustworthy==0, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & d_trustworthy==0, r

//Risk people
sum risk, d
gen d_risk = (risk>=r(p50))
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & d_risk==1, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & d_risk==1, r
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & d_risk==0, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & d_risk==0, r

regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & male==1 & male_two==1, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & male==1 & male_two==1, r
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & female==1 & female_two==1, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & female==1 & female_two==1, r
regress dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & male!=male_two, r
logistic dish_coll rpi##prize_spread if group_full==1 & id_in_group==1 & male!=male_two, r
*/
exit, STATA clear