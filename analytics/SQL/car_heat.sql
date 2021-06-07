drop materialized view car_heat;
create materialized view car_heat as
select distinct tr_heat.heat_id,
	tr_heat.match_hash,
	tr_heat.heat_number,
	tr_heat.a_rider,
	tr_heat.a_score,
	ph_a.sum_points as a_previous_points,
	ph_a.no_heats as a_previous_heats_no,
	tr_heat.b_rider,
	tr_heat.b_score,
	ph_b.sum_points as b_previous_points,
	ph_b.no_heats as b_previous_heats_no,
	tr_heat.c_rider,
	tr_heat.c_score,
	ph_c.sum_points as c_previous_points,
	ph_c.no_heats as c_previous_heats_no,
	tr_heat.d_rider,
	tr_heat.d_score,
	ph_d.sum_points as d_previous_points,
	ph_d.no_heats as d_previous_heats_no,
	tr_match.stadium,
	tr_match.round,
	tr_match.date,
	tr_match.year,
	tr_match.time,
	tr_match.name_team_home,
	tr_match.name_team_away
from tr_heat 
left join tr_previous_heats ph_a
on
	tr_heat.heat_id = ph_a.heat_id
	and tr_heat.a_rider = ph_a.rider
left join tr_previous_heats ph_b
on
	tr_heat.heat_id = ph_b.heat_id
	and tr_heat.b_rider = ph_b.rider
left join tr_previous_heats ph_c
on
	tr_heat.heat_id = ph_c.heat_id
	and tr_heat.c_rider = ph_c.rider
left join tr_previous_heats ph_d
on
	tr_heat.heat_id = ph_d.heat_id
	and tr_heat.d_rider = ph_d.rider
left join tr_match
	on tr_heat.match_hash = tr_match.match_hash
	
;