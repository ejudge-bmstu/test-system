--
-- PostgreSQL database dump
--

-- Dumped from database version 10.7 (Ubuntu 10.7-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.7

-- Started on 2019-04-05 10:49:13 MSK

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE ejudge;
--
-- TOC entry 3018 (class 1262 OID 16384)
-- Name: ejudge; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE ejudge WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


\connect ejudge

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 13041)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 3021 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 517 (class 1247 OID 16386)
-- Name: progr_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.progr_type AS ENUM (
    'python',
    'c',
    'cpp'
);


--
-- TOC entry 520 (class 1247 OID 16394)
-- Name: role_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.role_type AS ENUM (
    'user',
    'admin'
);


--
-- TOC entry 602 (class 1247 OID 16400)
-- Name: sex_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.sex_type AS ENUM (
    'male',
    'female'
);


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 196 (class 1259 OID 16405)
-- Name: answers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.answers (
    id uuid NOT NULL,
    program_text text NOT NULL,
    programming_language public.progr_type NOT NULL
);


--
-- TOC entry 197 (class 1259 OID 16411)
-- Name: categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.categories (
    id uuid NOT NULL,
    name text NOT NULL
);


--
-- TOC entry 198 (class 1259 OID 16417)
-- Name: email_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_tokens (
    id uuid NOT NULL,
    token text NOT NULL,
    creation_date bigint NOT NULL,
    user_id uuid NOT NULL
);


--
-- TOC entry 207 (class 1259 OID 16549)
-- Name: example_tests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.example_tests (
    id uuid NOT NULL,
    input_data text,
    output_data text,
    task_id uuid
);


--
-- TOC entry 199 (class 1259 OID 16423)
-- Name: profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.profiles (
    id uuid NOT NULL,
    name text,
    surname text,
    sex public.sex_type,
    birthday bigint
);


--
-- TOC entry 208 (class 1259 OID 16557)
-- Name: queue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.queue (
    id uuid NOT NULL,
    solution_id uuid,
    unixtime bigint
);


--
-- TOC entry 200 (class 1259 OID 16429)
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.refresh_tokens (
    id uuid NOT NULL,
    token text NOT NULL,
    user_id uuid NOT NULL
);


--
-- TOC entry 201 (class 1259 OID 16435)
-- Name: status; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.status (
    id uuid NOT NULL,
    result text NOT NULL,
    passed integer,
    error_test_id uuid,
    extended_information text
);


--
-- TOC entry 202 (class 1259 OID 16441)
-- Name: task_limits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task_limits (
    id uuid NOT NULL,
    memory_limit integer,
    time_limit integer,
    task_id uuid NOT NULL,
    programming_language public.progr_type NOT NULL
);


--
-- TOC entry 203 (class 1259 OID 16444)
-- Name: tasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tasks (
    id uuid NOT NULL,
    name text NOT NULL,
    description text,
    report_permission text NOT NULL,
    category_id uuid,
    owner_id uuid NOT NULL
);


--
-- TOC entry 204 (class 1259 OID 16450)
-- Name: tests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tests (
    id uuid NOT NULL,
    input_data text NOT NULL,
    output_data text NOT NULL,
    task_id uuid NOT NULL
);


--
-- TOC entry 205 (class 1259 OID 16456)
-- Name: user_solutions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_solutions (
    id uuid NOT NULL,
    solution_date bigint NOT NULL,
    user_id uuid NOT NULL,
    task_id uuid NOT NULL,
    answer_id uuid NOT NULL,
    status_id uuid NOT NULL
);


--
-- TOC entry 206 (class 1259 OID 16459)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    username text NOT NULL,
    password_hash text NOT NULL,
    email text NOT NULL,
    profile_id uuid NOT NULL,
    role public.role_type NOT NULL,
    enabled boolean NOT NULL
);


--
-- TOC entry 2854 (class 2606 OID 16466)
-- Name: answers answers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_pkey PRIMARY KEY (id);


--
-- TOC entry 2852 (class 2606 OID 16467)
-- Name: profiles birthday_check; Type: CHECK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE public.profiles
    ADD CONSTRAINT birthday_check CHECK ((birthday > 0)) NOT VALID;


--
-- TOC entry 2856 (class 2606 OID 16469)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 2851 (class 2606 OID 16470)
-- Name: email_tokens creation_date_check; Type: CHECK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE public.email_tokens
    ADD CONSTRAINT creation_date_check CHECK ((creation_date > 0)) NOT VALID;


--
-- TOC entry 2858 (class 2606 OID 16472)
-- Name: email_tokens email_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_tokens
    ADD CONSTRAINT email_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 2876 (class 2606 OID 16556)
-- Name: example_tests example_tests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.example_tests
    ADD CONSTRAINT example_tests_pkey PRIMARY KEY (id);


--
-- TOC entry 2860 (class 2606 OID 16474)
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (id);


--
-- TOC entry 2878 (class 2606 OID 16561)
-- Name: queue queue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_pkey PRIMARY KEY (id);


--
-- TOC entry 2862 (class 2606 OID 16476)
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 2864 (class 2606 OID 16478)
-- Name: status status_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.status
    ADD CONSTRAINT status_pkey PRIMARY KEY (id);


--
-- TOC entry 2866 (class 2606 OID 16480)
-- Name: task_limits task_limits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_limits
    ADD CONSTRAINT task_limits_pkey PRIMARY KEY (id);


--
-- TOC entry 2868 (class 2606 OID 16482)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 2870 (class 2606 OID 16484)
-- Name: tests tests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tests
    ADD CONSTRAINT tests_pkey PRIMARY KEY (id);


--
-- TOC entry 2872 (class 2606 OID 16486)
-- Name: user_solutions user_solutions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_solutions
    ADD CONSTRAINT user_solutions_pkey PRIMARY KEY (id);


--
-- TOC entry 2874 (class 2606 OID 16488)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 2886 (class 2606 OID 16489)
-- Name: user_solutions answer_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2883 (class 2606 OID 16494)
-- Name: tasks category_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2881 (class 2606 OID 16499)
-- Name: status error_test_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2884 (class 2606 OID 16504)
-- Name: tasks owner_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2890 (class 2606 OID 16509)
-- Name: users profile_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2887 (class 2606 OID 16514)
-- Name: user_solutions status_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2885 (class 2606 OID 16519)
-- Name: tests task_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2888 (class 2606 OID 16524)
-- Name: user_solutions task_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2882 (class 2606 OID 16529)
-- Name: task_limits task_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2891 (class 2606 OID 16562)
-- Name: example_tests task_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2889 (class 2606 OID 16534)
-- Name: user_solutions user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2880 (class 2606 OID 16539)
-- Name: refresh_tokens user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 2879 (class 2606 OID 16544)
-- Name: email_tokens user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--



--
-- TOC entry 3020 (class 0 OID 0)
-- Dependencies: 6
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2019-04-05 10:49:13 MSK

--
-- PostgreSQL database dump complete
--

