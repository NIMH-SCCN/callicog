CREATE VIEW search AS
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
)
select * from ttable tt;
