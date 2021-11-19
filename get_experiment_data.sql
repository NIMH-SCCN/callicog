CREATE OR REPLACE FUNCTION get_experiment_data(param_id INTEGER)
RETURNS TABLE(experiment_id INTEGER
	,animal VARCHAR(50)
	,template VARCHAR(50)
	,task VARCHAR(50)
	,session_id INTEGER
	,trial_id INTEGER
	,status VARCHAR(50)
	,event_id INTEGER
	,transition VARCHAR(50)
	,out_fail BOOLEAN
	,delay NUMERIC
	,timeout NUMERIC
	,outcome_window BOOLEAN
	,flip TIMESTAMP
	,touch TIMESTAMP
	,release TIMESTAMP
	,at_x INTEGER
	,at_y INTEGER
	,shape VARCHAR(50)
	,color_r NUMERIC
	,color_g NUMERIC
	,color_b NUMERIC
	,size_x INTEGER
	,size_y INTEGER
	,pos_x INTEGER
	,pos_y INTEGER
	,value VARCHAR(50)
	,image VARCHAR(100)
	,timeout_gain NUMERIC
) AS $$

SELECT ex.experiment_id as experiment_id
	,an.animal_code as animal
	,te.template_name as template
	,pr.protocol_name as task
	,se.session_id as session_id
	,ev.trial_id as trial_id
	,tr.trial_status as status
	,ev.event_id as event_id
	,wo.window_transition as transition
	,wo.is_outside_fail as out_fail
	,nullif(wo.window_delay, 0) as delay
	,nullif(wo.window_timeout, 0) as timeout
	,wo.is_outcome as outcome_window
	,ev.flip_timestamp as flip
	,ev.touch_timestamp as touch
	,ev.release_timestamp as release
	,ev.input_xcoor as at_x
	,ev.input_ycoor as at_y
	,so.stimulus_shape as shape
	,so.stimulus_color_r as color_r
	,so.stimulus_color_g as color_g
	,so.stimulus_color_b as color_b
	,so.stimulus_size_x as size_x
	,so.stimulus_size_y as size_y
	,so.stimulus_position_x pos_x
	,so.stimulus_position_y pos_y
	,so.stimulus_outcome as value
	,so.stimulus_image_file as image
	,so.stimulus_timeout_gain as timeout_gain
FROM event as ev
INNER JOIN trial as tr ON tr.trial_id = ev.trial_id
INNER JOIN session as se ON se.session_id = tr.session_id
INNER JOIN task as ta ON ta.task_id = se.task_id
INNER JOIN template_protocol as tp ON tp.template_protocol_id = ta.template_protocol_id
INNER JOIN protocol as pr ON pr.protocol_id = tp.protocol_id
INNER JOIN experiment as ex ON ex.experiment_id = ta.experiment_id
INNER JOIN template as te ON te.template_id = ex.template_id
INNER JOIN animal as an ON an.animal_id = ex.animal_id
LEFT JOIN window_object as wo ON wo.window_object_id = ev.window_object_id
LEFT JOIN stimulus_object as so ON so.stimulus_object_id = ev.stimulus_object_id
WHERE ta.task_id = param_id
ORDER BY ta.task_id, se.session_id, tr.trial_id, ev.event_id;

$$ LANGUAGE 'sql';