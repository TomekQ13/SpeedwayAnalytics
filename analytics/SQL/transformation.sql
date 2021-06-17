drop  materialized view tr_heat cascade;
create materialized view tr_heat as 
WITH max_heat_id_per_heat as (
	select max(heat_id) as max_heat_id
	from if_heat
	group by match_hash, heat_number
), scores_casted as (
	select
	heat_id,
	match_hash,
	heat_number,
	a_rider,
	cast(case when a_score in ('0','1','2','3') then a_score else '0' end as integer) as a_score,
	b_rider,
	cast(case when b_score in ('0','1','2','3') then b_score else '0' end as integer) as b_score,
	c_rider,
	cast(case when c_score in ('0','1','2','3') then c_score else '0' end as integer) as c_score,
	d_rider,
	cast(case when d_score in ('0','1','2','3') then d_score else '0' end as integer) as d_score,
	added_dttm
	from if_heat t1
	inner join max_heat_id_per_heat t2
		on t1.heat_id = t2.max_heat_id
	where
		match_hash is not null
		and a_rider <> '-'
		and b_rider <> '-'
		and c_rider <> '-'
		and d_rider <> '-'
), sum_6_heats as (
	select heat_id, sum(a_score + b_score + c_score + d_score) as score_sum
	from scores_casted
	group by heat_id
)
select scores_casted.*
from scores_casted
inner join sum_6_heats 
	on sum_6_heats.heat_id = scores_casted.heat_id
where
	sum_6_heats.score_sum = 6

;
		

create materialized view tr_match as
	select 	if_match.*
	from if_match
	inner join tr_heat
	on if_match.match_hash = tr_heat.match_hash;

create materialized view tr_rider_score_heat as 
	select * from
	(select heat_id, match_hash, heat_number, a_rider as rider, a_score as score from tr_heat
	union all
	select heat_id, match_hash, heat_number, b_rider as rider, b_score as score from tr_heat
	union all
	select heat_id, match_hash, heat_number, c_rider as rider, c_score as score from tr_heat
	union all
	select heat_id, match_hash, heat_number, d_rider as rider, d_score as score from tr_heat) uni
	where
		exists (select 1 from tr_heat mhiph where uni.heat_id = mhiph.heat_id)
;

--drop index for_previous_heats;
create index for_previous_heats on tr_rider_score_heat(heat_number, rider, match_hash) include (score);


create materialized view tr_previous_heats as
select
	rsh.*,
	coalesce((select sum(score) from tr_rider_score_heat rsh2 where rsh2.heat_number < rsh.heat_number and rsh.rider = rsh2.rider and rsh.match_hash = rsh2.match_hash group by match_hash, rider),0) as sum_points,
	coalesce((select count(score) from tr_rider_score_heat rsh2 where rsh2.heat_number < rsh.heat_number and rsh.rider = rsh2.rider and rsh.match_hash = rsh2.match_hash group by match_hash, rider),0) as no_heats
from tr_rider_score_heat rsh;




