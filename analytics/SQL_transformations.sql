create or replace view rider_match_history as
select * from if_heat;

select * from if_match order by date desc;

select * from rider_match_history where match_hash = 'e82428b345ade1948ed38a8d6fcfc09c0039509a68f19d5a63bae851b95bb221';
select * from if_match where match_hash = 'e82428b345ade1948ed38a8d6fcfc09c0039509a68f19d5a63bae851b95bb221';

-- remove repeated heats
create view max_heat_id_per_heat as 
select max(heat_id) as max_heat_id from if_heat group by match_hash, heat_number;

create or replace view rider_score_heat as 
select * from
(select heat_id, match_hash, heat_number, a_rider as rider, a_score as score from if_heat
union all
select heat_id, match_hash, heat_number, b_rider as rider, b_score as score from if_heat
union all
select heat_id, match_hash, heat_number, c_rider as rider, c_score as score from if_heat
union all
select heat_id, match_hash, heat_number, d_rider as rider, d_score as score from if_heat) uni
where
	exists (select 1 from max_heat_id_per_heat mhiph where uni.heat_id = mhiph.max_heat_id);
	
	
select
	rsh.*,
		(select count(score) from rider_score_heat rsh2 where rsh2.heat_number < rsh.heat_number group by match_hash, rider) as sum_points
from rider_score_heat rsh

select count(score) from rider_score_heat rsh2 where rsh2.heat_number > 1 group by match_hash, rider


order by match_hash, heat_number;

select distinct score from rider_score_heat;

delete from if_heat;

delete from if_match;