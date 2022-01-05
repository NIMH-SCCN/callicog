CREATE TABLE animal (
	animal_id SERIAL PRIMARY KEY,
	animal_code VARCHAR(50) NOT NULL
);

CREATE TABLE protocol (
	protocol_id SERIAL PRIMARY KEY,
	protocol_name VARCHAR(50) NOT NULL
);

CREATE TABLE template (
	template_id SERIAL PRIMARY KEY,
	template_name VARCHAR(50) NOT NULL
);

CREATE TABLE template_protocol(
	template_protocol_id SERIAL PRIMARY KEY,
	template_id INTEGER NOT NULL,
	protocol_id INTEGER NOT NULL,
	task_order INTEGER NOT NULL,
	progression VARCHAR(50) NOT NULL,
	target_trials INTEGER,
	target_sessions INTEGER,
	success_rate NUMERIC,
	rolling_window_size INTEGER,
	FOREIGN KEY (template_id) REFERENCES template(template_id),
	FOREIGN KEY (protocol_id) REFERENCES protocol(protocol_id)
);

CREATE TABLE experiment (
	experiment_id SERIAL PRIMARY KEY,
	animal_id INTEGER NOT NULL,
	template_id INTEGER NOT NULL,
	experiment_start TIMESTAMP NOT NULL,
	experiment_end TIMESTAMP,
	FOREIGN KEY (animal_id) REFERENCES animal(animal_id),
	FOREIGN KEY (template_id) REFERENCES template(template_id)
);

CREATE TABLE task (
	task_id SERIAL PRIMARY KEY,
	experiment_id INTEGER NOT NULL,
	template_protocol_id INTEGER NOT NULL,
	complete BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (experiment_id) REFERENCES experiment(experiment_id),
	FOREIGN KEY (template_protocol_id) REFERENCES template_protocol(template_protocol_id)
);

CREATE TABLE session (
	session_id SERIAL PRIMARY KEY,
	task_id INTEGER NOT NULL,
	session_start TIMESTAMP,
	session_end TIMESTAMP,
	session_status VARCHAR(50) DEFAULT 'new',
	FOREIGN KEY (task_id) REFERENCES task(task_id)
);

CREATE TABLE trial(
	trial_id SERIAL PRIMARY KEY,
	session_id INTEGER NOT NULL,
	trial_start TIMESTAMP,
	trial_end TIMESTAMP,
	trial_status VARCHAR(50) DEFAULT 'new',
	FOREIGN KEY (session_id) REFERENCES session(session_id)
);

CREATE TABLE window_object(
	window_object_id SERIAL PRIMARY KEY,
	is_outcome BOOLEAN DEFAULT FALSE,
	window_delay NUMERIC NOT NULL,
	window_label VARCHAR(100) NOT NULL,
	window_transition VARCHAR(50),
	window_timeout NUMERIC NOT NULL,
	is_outside_fail BOOLEAN NOT NULL,
	flip_timestamp TIMESTAMP NOT NULL,
	trial_id INTEGER NOT NULL,
	FOREIGN KEY (trial_id) REFERENCES trial(trial_id)
);

CREATE TABLE stimulus_object(
	stimulus_object_id SERIAL PRIMARY KEY,
	stimulus_shape VARCHAR(50),
	stimulus_size_x INTEGER,
	stimulus_size_y INTEGER,
	stimulus_position_x INTEGER,
	stimulus_position_y INTEGER,
	stimulus_outcome VARCHAR(50),
	stimulus_color_r NUMERIC,
	stimulus_color_g NUMERIC,
	stimulus_color_b NUMERIC,
	stimulus_image_file VARCHAR(100),
	stimulus_timeout_gain NUMERIC,
	stimulus_touched BOOLEAN DEFAULT FALSE,
	stimulus_touch_x INTEGER,
	stimulus_touch_y INTEGER,
	stimulus_flip_timestamp TIMESTAMP,
	stimulus_touch_timestamp TIMESTAMP,
	stimulus_release_timestamp TIMESTAMP,
	window_object_id INTEGER NOT NULL,
	FOREIGN KEY (window_object_id) REFERENCES window_object(window_object_id)
);

--CREATE TABLE event(
--	event_id SERIAL PRIMARY KEY,
--	trial_id INTEGER NOT NULL,
--	flip_timestamp TIMESTAMP,
--	touch_timestamp TIMESTAMP,
--	release_timestamp TIMESTAMP,
--	input_xcoor INTEGER,
--	input_ycoor INTEGER,
--	stimulus_object_id INTEGER,
--	window_object_id INTEGER,
--	FOREIGN KEY (stimulus_object_id) REFERENCES stimulus_object(stimulus_object_id),
--	FOREIGN KEY (window_object_id) REFERENCES window_object(window_object_id),
--	FOREIGN KEY (trial_id) REFERENCES trial(trial_id)
--);
