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

CREATE TABLE event(
	event_id SERIAL PRIMARY KEY,
	trial_id INTEGER NOT NULL,
	--event_timestamp TIMESTAMP NOT NULL,
	press_xcoor INTEGER,
	press_ycoor INTEGER,
	delay NUMERIC,
	FOREIGN KEY (trial_id) REFERENCES trial(trial_id)
);
