CREATE TABLE animal (
	animal_id SERIAL PRIMARY KEY,
	animal_code VARCHAR(50) NOT NULL
);

CREATE TABLE protocol (
	protocol_id SERIAL PRIMARY KEY,
	protocol_name VARCHAR(50) NOT NULL
);

CREATE TABLE experiment (
	experiment_id SERIAL PRIMARY KEY,
	animal_id INTEGER NOT NULL,
	experiment_start TIMESTAMP NOT NULL,
	experiment_end TIMESTAMP,
	FOREIGN KEY (animal_id) REFERENCES animal(animal_id)
);

CREATE TABLE task (
	task_id SERIAL PRIMARY KEY,
	experiment_id INTEGER NOT NULL,
	protocol_id INTEGER NOT NULL,
	task_order INTEGER NOT NULL,
	progression VARCHAR(50) NOT NULL,
	complete BOOLEAN DEFAULT FALSE,
	FOREIGN KEY (protocol_id) REFERENCES protocol(protocol_id),
	FOREIGN KEY (experiment_id) REFERENCES experiment(experiment_id)
);

CREATE TABLE session (
	session_id SERIAL PRIMARY KEY,
	task_id INTEGER NOT NULL,
	session_start TIMESTAMP,
	session_end TIMESTAMP,
<<<<<<< HEAD
	session_status VARCHAR(50) DEFAULT 'new',
=======
>>>>>>> 3cd8763e591d8cc8aa9042a08f61369de3994ce3
	FOREIGN KEY (task_id) REFERENCES task(task_id)
);

CREATE TABLE trial(
	trial_id SERIAL PRIMARY KEY,
	session_id INTEGER NOT NULL,
	trial_start TIMESTAMP,
	trial_end TIMESTAMP,
<<<<<<< HEAD
	trial_status VARCHAR(50) DEFAULT 'new',
=======
	trial_status VARCHAR(50) DEFAULT 'NEW',
>>>>>>> 3cd8763e591d8cc8aa9042a08f61369de3994ce3
	FOREIGN KEY (session_id) REFERENCES session(session_id)
);

CREATE TABLE event(
	event_id SERIAL PRIMARY KEY,
	trial_id INTEGER NOT NULL,
<<<<<<< HEAD
	event_description VARCHAR(100) NOT NULL,
=======
>>>>>>> 3cd8763e591d8cc8aa9042a08f61369de3994ce3
	event_timestamp TIMESTAMP NOT NULL,
	press_xcoor INTEGER,
	press_ycoor INTEGER,
	delay NUMERIC,
	FOREIGN KEY (trial_id) REFERENCES trial(trial_id)
);
