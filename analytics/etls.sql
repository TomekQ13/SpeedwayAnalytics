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

create materialized view previous_heats as
select
	rsh.*,
	coalesce((select sum(score) from rider_score_heat rsh2 where rsh2.heat_number < rsh.heat_number and rsh.rider = rsh2.rider and rsh.match_hash = rsh2.match_hash group by match_hash, rider),0) as sum_points,
	coalesce((select count(score) from rider_score_heat rsh2 where rsh2.heat_number < rsh.heat_number and rsh.rider = rsh2.rider and rsh.match_hash = rsh2.match_hash group by match_hash, rider),0) as no_heats
from rider_score_heat rsh;


select * from previous_heats where match_hash = '012bd5536e3c39bca7c4a5399368385a65273076668873d4431f07a1e1391909' and rider = 'Nicki Pedersen' order by heat_number;


--create extraction + data quality layer
select * from if_heat where match_hash is null;
select * from if_match where match_hash is null;

select m.match_hash, count(*) as cnt from if_match m
inner join if_heat h
on m.match_hash = h.match_hash
group by m.match_hash;



select * from if_heat where match_hash = '442a7575ae5e6e8b562c09b349ac902b3c0938c9b58235a44818fc4154277066';