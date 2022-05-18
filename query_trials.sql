CREATE OR REPLACE FUNCTION query_trials(
	param_trial_id INTEGER
	,param_session_id INTEGER
	,param_experiment_id INTEGER
	,param_template_name VARCHAR(50)
	,param_task_name VARCHAR(50)
	,param_animal_code VARCHAR(50)
	,param_trial_start TIMESTAMP
	,param_trial_end TIMESTAMP
	,param_timeout NUMERIC
	,param_ntargets INTEGER
	,param_ndistractors INTEGER
	,param_trial_outcome VARCHAR(50)
	,param_target VARCHAR(50)
	,param_color VARCHAR(50)
	,param_delay VARCHAR(50))
RETURNS TABLE(
	animal VARCHAR(50)
	,template VARCHAR(50)
	,task VARCHAR(50)
	,experiment INTEGER
	,session INTEGER
	,trial INTEGER
	,start TIMESTAMP
	,duration double precision
	,outcome VARCHAR(50)
	,flip TIMESTAMP
	,out_x INTEGER
	,out_y INTEGER
	,target VARCHAR(50)
	,color_r NUMERIC
	,color_g NUMERIC
	,color_b NUMERIC
	,pos_x INTEGER
	,pos_y INTEGER
	,size_x INTEGER
	,size_y INTEGER
	,touch_x INTEGER
	,touch_y INTEGER
	,touch_response double precision
	,release_response double precision
	,ntargets bigint
	,ndistractors bigint
	,delay VARCHAR(50)
	,timeout NUMERIC
) AS $$

with ttable as
(
	select
	an.animal_code as animal
	,te.template_name as template
	,pr.protocol_name as task
	,ex.experiment_id as experiment
	,se.session_id as session
	,tr.trial_id as trial
	,tr.trial_start as start
	,case when (tr.trial_end is not null) then extract(epoch from (tr.trial_end - tr.trial_start)) else null end as duration
	,tr.trial_status as outcome
	,wo.flip_timestamp as flip
	,wo.outside_fail_position_x as out_x
	,wo.outside_fail_position_y as out_y
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_shape from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as target
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_color_r from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as color_r
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_color_g from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as color_g
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_color_b from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as color_b
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_position_x from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as pos_x
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_position_y from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as pos_y
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_size_x from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as size_x
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_size_y from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as size_y
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_touch_x from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as touch_x
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select so.stimulus_touch_y from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as touch_y
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select extract(epoch from (so.stimulus_touch_timestamp - so.stimulus_flip_timestamp)) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as touch_response
	,case when (select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') = 1 then (select extract(epoch from (so.stimulus_release_timestamp - so.stimulus_touch_timestamp)) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') else null end as release_response
	,(select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'success') as ntargets
	,(select count(*) from stimulus_object so where so.window_object_id = wo.window_object_id and so.stimulus_outcome = 'fail') as ndistractors
	,(select trp.parameter_value from trial_parameter trp inner join protocol_parameter pp on pp.protocol_parameter_id = trp.protocol_parameter_id where pp.parameter_name = 'delay' and trp.trial_id = tr.trial_id) as delay
	,wo.window_timeout as timeout
	from trial tr
	inner join window_object wo on wo.trial_id = tr.trial_id
	inner join session se on se.session_id = tr.session_id
	inner join task ta on ta.task_id = se.task_id
	inner join template_protocol tp on tp.template_protocol_id = ta.template_protocol_id
	inner join protocol pr on pr.protocol_id = tp.protocol_id
	inner join template te on te.template_id = tp.template_id
	inner join experiment ex on ex.experiment_id = ta.experiment_id
	inner join animal an on an.animal_id = ex.animal_id
	where wo.is_outcome = True
	and (param_timeout is null or wo.window_timeout = param_timeout)
	and (param_trial_outcome is null or tr.trial_status = param_trial_outcome)
	and (param_trial_id is null or tr.trial_id = param_trial_id)
	and (param_session_id is null or se.session_id = param_session_id)
	and (param_task_name is null or pr.protocol_name = param_task_name)
	and (param_experiment_id is null or ex.experiment_id = param_experiment_id)
	and (param_template_name is null or te.template_name = param_template_name)
	and (param_animal_code is null or an.animal_code = param_animal_code)
	and ((param_trial_start is null and param_trial_end is null) or (tr.trial_start >= param_trial_start and tr.trial_start <= param_trial_end))
)
select * from ttable tt
where (param_ntargets is null or tt.ntargets = param_ntargets)
and (param_ndistractors is null or tt.ndistractors = param_ndistractors)
and (param_target is null or tt.target = param_target)
and (param_color is null or concat('(', tt.color_r, ',', tt.color_g, ',', tt.color_b, ')') = param_color)
and (param_delay is null or tt.delay = param_delay);
$$ LANGUAGE 'sql';
