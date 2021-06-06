


create materialized view rider_score_heat as 
WITH max_heat_id_per_heat as (
	select max(heat_id) as max_heat_id
	from if_heat
	group by match_hash, heat_number
), no_match_without_heats as (
	select 	*
	from if_match
	inner join if_heat
	on if_match.match_hash = if_heat.match_hash
), no_heats_without_match_hash as (
	select t1.*
	from if_heat t1
	inner join max_heat_id_per_heat t2
	on t1.heat_id = t2.max_heat_id
	where
		match_hash is not null
), rider_score_heat as (
	select * from
	(select heat_id, match_hash, heat_number, a_rider as rider, a_score as score from no_heats_without_match_hash
	union all
	select heat_id, match_hash, heat_number, b_rider as rider, b_score as score from no_heats_without_match_hash
	union all
	select heat_id, match_hash, heat_number, c_rider as rider, c_score as score from no_heats_without_match_hash
	union all
	select heat_id, match_hash, heat_number, d_rider as rider, d_score as score from no_heats_without_match_hash) uni
	where
		exists (select 1 from max_heat_id_per_heat mhiph where uni.heat_id = mhiph.max_heat_id)
)

select heat_id, match_hash, heat_number, rider, cast(case when score in ('0','1','2','3') then score else '0' end as integer) as score
from rider_score_heat
where rider <> '-'
order by match_hash
;


create materialized view tr_previous_heats as
select
	rsh.*,
	coalesce((select sum(score) from tr_rider_score_heat rsh2 where rsh2.heat_number < rsh.heat_number and rsh.rider = rsh2.rider and rsh.match_hash = rsh2.match_hash group by match_hash, rider),0) as sum_points,
	coalesce((select count(score) from tr_rider_score_heat rsh2 where rsh2.heat_number < rsh.heat_number and rsh.rider = rsh2.rider and rsh.match_hash = rsh2.match_hash group by match_hash, rider),0) as no_heats
from tr_rider_score_heat rsh;


