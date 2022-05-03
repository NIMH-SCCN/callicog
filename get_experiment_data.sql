CREATE OR REPLACE FUNCTION get_experiment_data(param_id INTEGER)
RETURNS TABLE(experiment_id INTEGER
	,animal VARCHAR(50)
	,template VARCHAR(50)
	,task VARCHAR(50)
	,progression VARCHAR(50)
	,trials INTEGER
	,sessions INTEGER
	,success_rate NUMERIC
	,rolling_size INTEGER
	,task_complete VARCHAR(50)
	,session_id INTEGER
	,trial_id INTEGER
	,trial_status VARCHAR(50)
	,window_id INTEGER
	,window_type VARCHAR(50)
	,delay NUMERIC
	,is_outcome VARCHAR(50)
	,timeout NUMERIC
	,out_fail VARCHAR(50)
	,out_fail_pos_x INTEGER
	,out_fail_pos_y INTEGER
	,eeg_label VARCHAR(50)
	,stimulus_id INTEGER
	,shape VARCHAR(50)
	,size_x INTEGER
	,size_y INTEGER
	,pos_x INTEGER
	,pos_y INTEGER
	,on_touch VARCHAR(50)
	,color_rgb VARCHAR(50)
	,timeout_gain NUMERIC
	,touched VARCHAR(50)
	,flip TIMESTAMP
	,touch TIMESTAMP
	,release TIMESTAMP
	,touch_x INTEGER
	,touch_y INTEGER
) AS $$

select ex.experiment_id as experiment_id
,an.animal_code as animal
,te.template_name as template
,pr.protocol_name as task
,tp.progression as progression
,tp.target_trials as trials
,tp.target_sessions as sessions
,tp.success_rate as success_rate
,tp.rolling_window_size as rolling_size
,(case when ta.complete then 'yes' else 'no' end) as task_complete
,se.session_id as session_id
,tr.trial_id as trial_id
,tr.trial_status as trial_status
,wo.window_object_id as window_id
,(case when wo.window_transition is null then 'delay' else wo.window_transition end) as window_type
,nullif(wo.window_delay, 0) as delay
,(case when wo.is_outcome then 'yes' else 'no' end) as is_outcome
,nullif(wo.window_timeout, 0) as timeout
,(case when wo.is_outside_fail then 'yes' else 'no' end) as out_fail
,wo.outside_fail_position_x as out_fail_pos_x
,wo.outside_fail_position_y as out_fail_pos_y
,wo.window_label as eeg_label
,so.stimulus_object_id as stimulus_id
,so.stimulus_shape as shape
,so.stimulus_size_x as size_x
,so.stimulus_size_y as size_y
--,'(' || so.stimulus_size_x || ',' || so.stimulus_size_y || ')' as size
,so.stimulus_position_x as pos_x
,so.stimulus_position_y as pos_y
--,'(' || so.stimulus_position_x || ',' || so.stimulus_position_y || ')' as pos
,so.stimulus_outcome as on_touch
,'(' || so.stimulus_color_r || ',' || so.stimulus_color_g || ',' || so.stimulus_color_b || ')' as color_rgb
,so.stimulus_timeout_gain as timeout_gain
,(case when so.stimulus_touched is not null then (case when so.stimulus_touched then 'yes' else 'no' end) else null end) as touched
,(case when so.stimulus_flip_timestamp is not null then so.stimulus_flip_timestamp else wo.window_flip_timestamp end) as flip
,so.stimulus_touch_timestamp as touch
,so.stimulus_release_timestamp as release
,so.stimulus_touch_x as touch_x
,so.stimulus_touch_y as touch_y
from window_object as wo
--from stimulus_object so
--left join window_object wo on wo.window_object_id = so.window_object_id
left join stimulus_object so on wo.window_object_id = so.window_object_id
inner join trial tr on tr.trial_id = wo.trial_id
inner join session se on se.session_id = tr.session_id
inner join task ta on ta.task_id = se.task_id
inner join template_protocol tp on tp.template_protocol_id = ta.template_protocol_id
inner join template te on te.template_id = tp.template_id
inner join protocol pr on pr.protocol_id = tp.protocol_id
inner join experiment ex on ex.experiment_id = ta.experiment_id
inner join animal an on an.animal_id = ex.animal_id
where ex.experiment_id = param_id
order by ta.task_id, se.session_id, tr.trial_id, wo.flip_timestamp, so.stimulus_flip_timestamp;

$$ LANGUAGE 'sql';