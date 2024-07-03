--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Homebrew)
-- Dumped by pg_dump version 16.3 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: get_experiment_data(integer); Type: FUNCTION; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE FUNCTION public.get_experiment_data(param_id integer) RETURNS TABLE(experiment_id integer, animal character varying, template character varying, task character varying, progression character varying, trials integer, sessions integer, success_rate numeric, rolling_size integer, task_complete character varying, session_id integer, trial_id integer, trial_status character varying, window_id integer, window_type character varying, delay numeric, is_outcome character varying, timeout numeric, out_fail character varying, out_fail_pos_x integer, out_fail_pos_y integer, eeg_label character varying, stimulus_id integer, shape character varying, size_x integer, size_y integer, pos_x integer, pos_y integer, on_touch character varying, color_rgb character varying, timeout_gain numeric, touched character varying, flip timestamp without time zone, touch timestamp without time zone, release timestamp without time zone, touch_x integer, touch_y integer)
    LANGUAGE sql
    AS $$

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
,(case when wo.window_transition is null then wo.flip_timestamp else so.stimulus_flip_timestamp end) as flip
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

$$;


ALTER FUNCTION public.get_experiment_data(param_id integer) OWNER TO $CALLICOG_DB_USER;

--
-- Name: query_trials(integer, integer, integer, character varying, character varying, character varying, timestamp without time zone, timestamp without time zone, numeric, integer, integer, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE FUNCTION public.query_trials(param_trial_id integer, param_session_id integer, param_experiment_id integer, param_template_name character varying, param_task_name character varying, param_animal_code character varying, param_trial_start timestamp without time zone, param_trial_end timestamp without time zone, param_timeout numeric, param_ntargets integer, param_ndistractors integer, param_trial_outcome character varying, param_target character varying, param_color character varying, param_delay character varying) RETURNS TABLE(animal character varying, template character varying, task character varying, experiment integer, session integer, trial integer, start timestamp without time zone, duration double precision, outcome character varying, flip timestamp without time zone, out_x integer, out_y integer, target character varying, color_r numeric, color_g numeric, color_b numeric, pos_x integer, pos_y integer, size_x integer, size_y integer, touch_x integer, touch_y integer, touch_response double precision, release_response double precision, ntargets bigint, ndistractors bigint, delay character varying, timeout numeric)
    LANGUAGE sql
    AS $$

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
$$;


ALTER FUNCTION public.query_trials(param_trial_id integer, param_session_id integer, param_experiment_id integer, param_template_name character varying, param_task_name character varying, param_animal_code character varying, param_trial_start timestamp without time zone, param_trial_end timestamp without time zone, param_timeout numeric, param_ntargets integer, param_ndistractors integer, param_trial_outcome character varying, param_target character varying, param_color character varying, param_delay character varying) OWNER TO $CALLICOG_DB_USER;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: animal; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.animal (
    animal_id integer NOT NULL,
    animal_code character varying(50) NOT NULL
);


ALTER TABLE public.animal OWNER TO $CALLICOG_DB_USER;

--
-- Name: animal_animal_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.animal_animal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animal_animal_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: animal_animal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.animal_animal_id_seq OWNED BY public.animal.animal_id;


--
-- Name: experiment; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.experiment (
    experiment_id integer NOT NULL,
    animal_id integer NOT NULL,
    template_id integer NOT NULL,
    experiment_start timestamp without time zone NOT NULL,
    experiment_end timestamp without time zone
);


ALTER TABLE public.experiment OWNER TO $CALLICOG_DB_USER;

--
-- Name: experiment_experiment_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.experiment_experiment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.experiment_experiment_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: experiment_experiment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.experiment_experiment_id_seq OWNED BY public.experiment.experiment_id;


--
-- Name: protocol; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.protocol (
    protocol_id integer NOT NULL,
    protocol_name character varying(50) NOT NULL
);


ALTER TABLE public.protocol OWNER TO $CALLICOG_DB_USER;

--
-- Name: protocol_parameter; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.protocol_parameter (
    protocol_parameter_id integer NOT NULL,
    parameter_name character varying(50) NOT NULL,
    protocol_id integer NOT NULL
);


ALTER TABLE public.protocol_parameter OWNER TO $CALLICOG_DB_USER;

--
-- Name: protocol_parameter_protocol_parameter_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.protocol_parameter_protocol_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.protocol_parameter_protocol_parameter_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: protocol_parameter_protocol_parameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.protocol_parameter_protocol_parameter_id_seq OWNED BY public.protocol_parameter.protocol_parameter_id;


--
-- Name: protocol_protocol_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.protocol_protocol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.protocol_protocol_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: protocol_protocol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.protocol_protocol_id_seq OWNED BY public.protocol.protocol_id;


--
-- Name: session; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.session (
    session_id integer NOT NULL,
    task_id integer NOT NULL,
    session_start timestamp without time zone,
    session_end timestamp without time zone,
    session_status character varying(50) DEFAULT 'new'::character varying
);


ALTER TABLE public.session OWNER TO $CALLICOG_DB_USER;

--
-- Name: stimulus_object; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.stimulus_object (
    stimulus_object_id integer NOT NULL,
    stimulus_shape character varying(50),
    stimulus_size_x integer,
    stimulus_size_y integer,
    stimulus_position_x integer,
    stimulus_position_y integer,
    stimulus_outcome character varying(50),
    stimulus_color_r numeric,
    stimulus_color_g numeric,
    stimulus_color_b numeric,
    stimulus_image_file character varying(100),
    stimulus_timeout_gain numeric,
    stimulus_touched boolean DEFAULT false,
    stimulus_touch_x integer,
    stimulus_touch_y integer,
    stimulus_flip_timestamp timestamp without time zone,
    stimulus_touch_timestamp timestamp without time zone,
    stimulus_release_timestamp timestamp without time zone,
    window_object_id integer
);


ALTER TABLE public.stimulus_object OWNER TO $CALLICOG_DB_USER;

--
-- Name: task; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.task (
    task_id integer NOT NULL,
    experiment_id integer NOT NULL,
    template_protocol_id integer NOT NULL,
    complete boolean DEFAULT false
);


ALTER TABLE public.task OWNER TO $CALLICOG_DB_USER;

--
-- Name: template; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.template (
    template_id integer NOT NULL,
    template_name character varying(50) NOT NULL
);


ALTER TABLE public.template OWNER TO $CALLICOG_DB_USER;

--
-- Name: template_protocol; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.template_protocol (
    template_protocol_id integer NOT NULL,
    template_id integer NOT NULL,
    protocol_id integer NOT NULL,
    task_order integer NOT NULL,
    progression character varying(50) NOT NULL,
    target_trials integer,
    target_sessions integer,
    success_rate numeric,
    rolling_window_size integer
);


ALTER TABLE public.template_protocol OWNER TO $CALLICOG_DB_USER;

--
-- Name: trial; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.trial (
    trial_id integer NOT NULL,
    session_id integer NOT NULL,
    trial_start timestamp without time zone,
    trial_end timestamp without time zone,
    trial_status character varying(50) DEFAULT 'new'::character varying
);


ALTER TABLE public.trial OWNER TO $CALLICOG_DB_USER;

--
-- Name: trial_parameter; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.trial_parameter (
    trial_parameter_id integer NOT NULL,
    protocol_parameter_id integer NOT NULL,
    parameter_value character varying(200),
    stimulus_object_id integer,
    trial_id integer NOT NULL
);


ALTER TABLE public.trial_parameter OWNER TO $CALLICOG_DB_USER;

--
-- Name: window_object; Type: TABLE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE TABLE public.window_object (
    window_object_id integer NOT NULL,
    is_outcome boolean DEFAULT false,
    window_delay numeric NOT NULL,
    window_label character varying(100) NOT NULL,
    window_transition character varying(50),
    window_timeout numeric NOT NULL,
    is_outside_fail boolean NOT NULL,
    flip_timestamp timestamp without time zone NOT NULL,
    trial_id integer NOT NULL,
    outside_fail_position_x integer,
    outside_fail_position_y integer
);


ALTER TABLE public.window_object OWNER TO $CALLICOG_DB_USER;

--
-- Name: search; Type: VIEW; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE VIEW public.search AS
 WITH ttable AS (
         SELECT an.animal_code AS animal,
            te.template_name AS template,
            pr.protocol_name AS task,
            ex.experiment_id AS experiment,
            se.session_id AS session,
            tr.trial_id AS trial,
            tr.trial_start AS start,
                CASE
                    WHEN (tr.trial_end IS NOT NULL) THEN EXTRACT(epoch FROM (tr.trial_end - tr.trial_start))
                    ELSE NULL::numeric
                END AS duration,
            tr.trial_status AS outcome,
            wo.flip_timestamp AS flip,
            wo.outside_fail_position_x AS out_x,
            wo.outside_fail_position_y AS out_y,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_shape
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::character varying
                END AS target,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_color_r
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::numeric
                END AS color_r,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_color_g
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::numeric
                END AS color_g,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_color_b
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::numeric
                END AS color_b,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_position_x
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::integer
                END AS pos_x,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_position_y
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::integer
                END AS pos_y,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_size_x
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::integer
                END AS size_x,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_size_y
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::integer
                END AS size_y,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_touch_x
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::integer
                END AS touch_x,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT so.stimulus_touch_y
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::integer
                END AS touch_y,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT EXTRACT(epoch FROM (so.stimulus_touch_timestamp - so.stimulus_flip_timestamp)) AS "extract"
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::numeric
                END AS touch_response,
                CASE
                    WHEN (( SELECT count(*) AS count
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) = 1) THEN ( SELECT EXTRACT(epoch FROM (so.stimulus_release_timestamp - so.stimulus_touch_timestamp)) AS "extract"
                       FROM public.stimulus_object so
                      WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text)))
                    ELSE NULL::numeric
                END AS release_response,
            ( SELECT count(*) AS count
                   FROM public.stimulus_object so
                  WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'success'::text))) AS ntargets,
            ( SELECT count(*) AS count
                   FROM public.stimulus_object so
                  WHERE ((so.window_object_id = wo.window_object_id) AND ((so.stimulus_outcome)::text = 'fail'::text))) AS ndistractors,
            ( SELECT trp.parameter_value
                   FROM (public.trial_parameter trp
                     JOIN public.protocol_parameter pp ON ((pp.protocol_parameter_id = trp.protocol_parameter_id)))
                  WHERE (((pp.parameter_name)::text = 'delay'::text) AND (trp.trial_id = tr.trial_id))) AS delay,
            wo.window_timeout AS timeout
           FROM ((((((((public.trial tr
             JOIN public.window_object wo ON ((wo.trial_id = tr.trial_id)))
             JOIN public.session se ON ((se.session_id = tr.session_id)))
             JOIN public.task ta ON ((ta.task_id = se.task_id)))
             JOIN public.template_protocol tp ON ((tp.template_protocol_id = ta.template_protocol_id)))
             JOIN public.protocol pr ON ((pr.protocol_id = tp.protocol_id)))
             JOIN public.template te ON ((te.template_id = tp.template_id)))
             JOIN public.experiment ex ON ((ex.experiment_id = ta.experiment_id)))
             JOIN public.animal an ON ((an.animal_id = ex.animal_id)))
          WHERE (wo.is_outcome = true)
        )
 SELECT animal,
    template,
    task,
    experiment,
    session,
    trial,
    start,
    duration,
    outcome,
    flip,
    out_x,
    out_y,
    target,
    color_r,
    color_g,
    color_b,
    pos_x,
    pos_y,
    size_x,
    size_y,
    touch_x,
    touch_y,
    touch_response,
    release_response,
    ntargets,
    ndistractors,
    delay,
    timeout
   FROM ttable tt;


ALTER VIEW public.search OWNER TO $CALLICOG_DB_USER;

--
-- Name: session_session_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.session_session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.session_session_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: session_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.session_session_id_seq OWNED BY public.session.session_id;


--
-- Name: stimulus_object_stimulus_object_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.stimulus_object_stimulus_object_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stimulus_object_stimulus_object_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: stimulus_object_stimulus_object_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.stimulus_object_stimulus_object_id_seq OWNED BY public.stimulus_object.stimulus_object_id;


--
-- Name: task_task_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.task_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_task_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: task_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.task_task_id_seq OWNED BY public.task.task_id;


--
-- Name: template_protocol_template_protocol_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.template_protocol_template_protocol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.template_protocol_template_protocol_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: template_protocol_template_protocol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.template_protocol_template_protocol_id_seq OWNED BY public.template_protocol.template_protocol_id;


--
-- Name: template_template_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.template_template_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.template_template_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: template_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.template_template_id_seq OWNED BY public.template.template_id;


--
-- Name: trial_parameter_trial_parameter_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.trial_parameter_trial_parameter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trial_parameter_trial_parameter_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: trial_parameter_trial_parameter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.trial_parameter_trial_parameter_id_seq OWNED BY public.trial_parameter.trial_parameter_id;


--
-- Name: trial_trial_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.trial_trial_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trial_trial_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: trial_trial_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.trial_trial_id_seq OWNED BY public.trial.trial_id;


--
-- Name: window_object_window_object_id_seq; Type: SEQUENCE; Schema: public; Owner: $CALLICOG_DB_USER
--

CREATE SEQUENCE public.window_object_window_object_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.window_object_window_object_id_seq OWNER TO $CALLICOG_DB_USER;

--
-- Name: window_object_window_object_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER SEQUENCE public.window_object_window_object_id_seq OWNED BY public.window_object.window_object_id;


--
-- Name: animal animal_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.animal ALTER COLUMN animal_id SET DEFAULT nextval('public.animal_animal_id_seq'::regclass);


--
-- Name: experiment experiment_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.experiment ALTER COLUMN experiment_id SET DEFAULT nextval('public.experiment_experiment_id_seq'::regclass);


--
-- Name: protocol protocol_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.protocol ALTER COLUMN protocol_id SET DEFAULT nextval('public.protocol_protocol_id_seq'::regclass);


--
-- Name: protocol_parameter protocol_parameter_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.protocol_parameter ALTER COLUMN protocol_parameter_id SET DEFAULT nextval('public.protocol_parameter_protocol_parameter_id_seq'::regclass);


--
-- Name: session session_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.session ALTER COLUMN session_id SET DEFAULT nextval('public.session_session_id_seq'::regclass);


--
-- Name: stimulus_object stimulus_object_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.stimulus_object ALTER COLUMN stimulus_object_id SET DEFAULT nextval('public.stimulus_object_stimulus_object_id_seq'::regclass);


--
-- Name: task task_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.task ALTER COLUMN task_id SET DEFAULT nextval('public.task_task_id_seq'::regclass);


--
-- Name: template template_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.template ALTER COLUMN template_id SET DEFAULT nextval('public.template_template_id_seq'::regclass);


--
-- Name: template_protocol template_protocol_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.template_protocol ALTER COLUMN template_protocol_id SET DEFAULT nextval('public.template_protocol_template_protocol_id_seq'::regclass);


--
-- Name: trial trial_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.trial ALTER COLUMN trial_id SET DEFAULT nextval('public.trial_trial_id_seq'::regclass);


--
-- Name: trial_parameter trial_parameter_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.trial_parameter ALTER COLUMN trial_parameter_id SET DEFAULT nextval('public.trial_parameter_trial_parameter_id_seq'::regclass);


--
-- Name: window_object window_object_id; Type: DEFAULT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.window_object ALTER COLUMN window_object_id SET DEFAULT nextval('public.window_object_window_object_id_seq'::regclass);


--
-- Name: animal animal_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.animal
    ADD CONSTRAINT animal_pkey PRIMARY KEY (animal_id);


--
-- Name: experiment experiment_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.experiment
    ADD CONSTRAINT experiment_pkey PRIMARY KEY (experiment_id);


--
-- Name: protocol_parameter protocol_parameter_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.protocol_parameter
    ADD CONSTRAINT protocol_parameter_pkey PRIMARY KEY (protocol_parameter_id);


--
-- Name: protocol protocol_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.protocol
    ADD CONSTRAINT protocol_pkey PRIMARY KEY (protocol_id);


--
-- Name: session session_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_pkey PRIMARY KEY (session_id);


--
-- Name: stimulus_object stimulus_object_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.stimulus_object
    ADD CONSTRAINT stimulus_object_pkey PRIMARY KEY (stimulus_object_id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (task_id);


--
-- Name: template template_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.template
    ADD CONSTRAINT template_pkey PRIMARY KEY (template_id);


--
-- Name: template_protocol template_protocol_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.template_protocol
    ADD CONSTRAINT template_protocol_pkey PRIMARY KEY (template_protocol_id);


--
-- Name: trial_parameter trial_parameter_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.trial_parameter
    ADD CONSTRAINT trial_parameter_pkey PRIMARY KEY (trial_parameter_id);


--
-- Name: trial trial_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.trial
    ADD CONSTRAINT trial_pkey PRIMARY KEY (trial_id);


--
-- Name: window_object window_object_pkey; Type: CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.window_object
    ADD CONSTRAINT window_object_pkey PRIMARY KEY (window_object_id);


--
-- Name: experiment experiment_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.experiment
    ADD CONSTRAINT experiment_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animal(animal_id);


--
-- Name: experiment experiment_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.experiment
    ADD CONSTRAINT experiment_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.template(template_id);


--
-- Name: protocol_parameter protocol_parameter_protocol_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.protocol_parameter
    ADD CONSTRAINT protocol_parameter_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocol(protocol_id);


--
-- Name: session session_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.task(task_id);


--
-- Name: stimulus_object stimulus_object_window_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.stimulus_object
    ADD CONSTRAINT stimulus_object_window_object_id_fkey FOREIGN KEY (window_object_id) REFERENCES public.window_object(window_object_id);


--
-- Name: task task_experiment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_experiment_id_fkey FOREIGN KEY (experiment_id) REFERENCES public.experiment(experiment_id);


--
-- Name: task task_template_protocol_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_template_protocol_id_fkey FOREIGN KEY (template_protocol_id) REFERENCES public.template_protocol(template_protocol_id);


--
-- Name: template_protocol template_protocol_protocol_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.template_protocol
    ADD CONSTRAINT template_protocol_protocol_id_fkey FOREIGN KEY (protocol_id) REFERENCES public.protocol(protocol_id);


--
-- Name: template_protocol template_protocol_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.template_protocol
    ADD CONSTRAINT template_protocol_template_id_fkey FOREIGN KEY (template_id) REFERENCES public.template(template_id);


--
-- Name: trial_parameter trial_parameter_protocol_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.trial_parameter
    ADD CONSTRAINT trial_parameter_protocol_parameter_id_fkey FOREIGN KEY (protocol_parameter_id) REFERENCES public.protocol_parameter(protocol_parameter_id);


--
-- Name: trial_parameter trial_parameter_stimulus_object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.trial_parameter
    ADD CONSTRAINT trial_parameter_stimulus_object_id_fkey FOREIGN KEY (stimulus_object_id) REFERENCES public.stimulus_object(stimulus_object_id);


--
-- Name: trial_parameter trial_parameter_trial_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.trial_parameter
    ADD CONSTRAINT trial_parameter_trial_id_fkey FOREIGN KEY (trial_id) REFERENCES public.trial(trial_id);


--
-- Name: trial trial_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.trial
    ADD CONSTRAINT trial_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.session(session_id);


--
-- Name: window_object window_object_trial_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: $CALLICOG_DB_USER
--

ALTER TABLE ONLY public.window_object
    ADD CONSTRAINT window_object_trial_id_fkey FOREIGN KEY (trial_id) REFERENCES public.trial(trial_id);


--
-- PostgreSQL database dump complete
--

