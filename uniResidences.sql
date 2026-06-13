--
-- PostgreSQL database dump
--

\restrict C8lYEsRmoh6902G7OtP0JoEk7Ag249rB9ktLN1Rkz2StMnek4LaJwMgzNbgL5B5

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: applicationstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.applicationstatus AS ENUM (
    'ACCEPTED',
    'REJECTED',
    'PENDING'
);


ALTER TYPE public.applicationstatus OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    "admin_Id" integer NOT NULL,
    password_hash character varying(120) NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.applications (
    "application_Id" integer NOT NULL,
    status public.applicationstatus NOT NULL,
    reason_for_refusal character varying(300),
    application_message character varying(500) NOT NULL,
    submission_date timestamp without time zone NOT NULL,
    "student_Id" integer NOT NULL,
    "room_Id" integer NOT NULL,
    "admin_Id" integer
);


ALTER TABLE public.applications OWNER TO postgres;

--
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    "room_Id" integer NOT NULL,
    available boolean NOT NULL,
    rent integer NOT NULL,
    description character varying(300) NOT NULL
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    "student_Id" integer NOT NULL,
    student_name character varying(100) NOT NULL,
    password_hash character varying(120) NOT NULL
);


ALTER TABLE public.students OWNER TO postgres;

--
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins ("admin_Id", password_hash) FROM stdin;
753	34f52e1b0414e2a56bce77f435131d5ae2cd7b55c728f55fc24d4a78b5f9e3024ab86f5211fb9e5ea5d0e375b86e74de988c
5542	1dcf01119e17a7d65e8e2454d1e722cb1a219474c77ad650e76c754a0730079d17f8f83510aad57575c1e463a26d9fc80b65
3264	79bfb727a7b2c61ca7b926796f7441a8488c98b5bfe1b26f1f8ef366424a68b1aa552614910c09ce8d3344efc707bad297f9
7219	7661158caa6e0a803cde934012b6419a0d976326f1d64c26bbb85041e8d03e59e099d3a431ba58e30942f2d34ca60dd9841b
6067	6da13687abd2906c0fdc8f3e0993ec34ac1a4e1c039cd60d092a92643ecb562276f8a887103061c86b8033b0c50d2d95d80f
2951	feb3780a2bb16c2fbb60d70a3051bb96cded226d84502c7a1df902cf813c8b07edc05480160e8c001e78fbc3018a184c4a4e
4749	5af402f06914e7ab5fb9d0ac2bea3499a38e102e91a3b05b94a79f3fe334815f80d585ddff3877ec2267e1c3bc85a57ffbc3
6391	1067b05e421f9d3812114efc280725a8f6f6a4ea945cabe370327321b5e4e1e5f0662ca73abfa5613af2cdc9c6e7eda1c003
7712	c4da0f983eb57317ae2e88c47e0772f6f1c5c2ff8bc709cc2199fba86d246cbc300c88b2f98cf73b9067d24f80081844a1e3
8640	02c619f92954f172c77c5cee6df10d3b937d57a1363cf2da7d97c22b6960e5aa1a7d32f16231697f129dd9549419aa488c7c
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.applications ("application_Id", status, reason_for_refusal, application_message, submission_date, "student_Id", "room_Id", "admin_Id") FROM stdin;
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms ("room_Id", available, rent, description) FROM stdin;
509	t	464	Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2. Located at : Kayl\nRent: 464
2386	t	578	Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Mersch\nRent: 578
9774	t	439	Type 4: Studio apartment. Private bathroom and kitchen. Double (only for couples), average size, 35 m2. Located at : Esch-sur-Alzette\nRent: 439
1635	t	380	Type 2: Single room. Private bathroom, shared kitchen, average surface: 19 m2. Located at : Kayl\nRent: 380
9963	t	867	Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Mersch\nRent: 867
9028	t	553	Type 4: Studio apartment. Private bathroom and kitchen. Double (only for couples), average size, 35 m2. Located at : Kayl\nRent: 553
9754	t	809	Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2. Located at : Esch-sur-Alzette\nRent: 809
7024	t	513	Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2. Located at : Dudelange\nRent: 513
3627	t	509	Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2. Located at : Niederkorn\nRent: 509
6324	t	444	Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Differdange\nRent: 444
9991	t	702	Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2. Located at : Esch-sur-Alzette\nRent: 702
8885	t	820	Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Clervaux\nRent: 820
9144	t	430	Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2. Located at : Differdange\nRent: 430
3250	t	941	Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Esch-sur-Alzette\nRent: 941
4841	t	583	Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Kayl\nRent: 583
6327	t	453	Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2. Located at : Ettelbruck\nRent: 453
2764	t	723	Type 3: Studio apartment. Private bathroom and kitchen. Single, average size, 24 m2. Located at : Differdange\nRent: 723
4474	t	564	Type 1: Single room. Shared bathroom and kitchen, average size: 15 m2. Located at : Luxembourg City\nRent: 564
4110	t	896	Type 2: Single room. Private bathroom, shared kitchen, average surface: 19 m2. Located at : Ettelbruck\nRent: 896
4522	t	738	Type 5: Two-room apartment. Private kitchen/living room, bathroom and one bedroom. (Only for couples): average size, 44 m2. Located at : Kayl\nRent: 738
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students ("student_Id", student_name, password_hash) FROM stdin;
7617	Hmideh Karl	48eca1ecf94b3e1595a8bc648328a44d3a627f36c54fc272b6e0a5ef28c6af604c96ef26ac0f0378ba698fc2f71d1503be61
2366	Jones Ivan	bf38987e96f61c981cb526ee517dfd535b2aaab1162d756cf762c2f5329058a83f46333eab41a43345491849c76c26e2ff77
6404	Taylor Peggy	f95d2c488c1df0faf26ebdb3512a29efbee28311eed187b2f367b3971ffb08a2f4a1c8a6370a795e7a2f8393e0811f409640
1927	Gonzalez Ingrid	c9ed3fdae3219a7509ec7456ad6ed6aca7101e12b5a5cbb37bac87f40670598b40dd7380a213f27110dbc975c87f15f6d1dd
4989	Martinez Nina	c69175f9c4ae8b2e6d8795653e70863f1a143a0e751d592b183661c549b407f0cb3a595e407cb5cb2d267c1d72ea5107e92b
5138	Chekam Quentin	16ebe46c661e26128273709b52ccf0c0171d905882840457e47a9e9c313e31cbeed76b5e1239c56d1697c6451964010ff9e9
2203	Davis Bob	83007a9eb6b6a2b5cce94da5980907d93c3206354bf3379da528bd1ba70d4081175e3508885229b40f89437bf2fb7f19c049
6218	Hmideh Peggy	6411e2ce4fc8e0eb99ee8558af9fe5d63b8d54adc4288e6a826885c76caa63a85488f49f7a67ad20ffe776689fcf3ded009f
614	Anderson Quentin	64947e683f8925685aa16a0d3973f39a2f763abbcd46eb23ce9e4071b9a2ba4298d054cdb3064e8703978f9c07c3605c4226
1688	Hernandez Charlie	6e1ca4d878630c102ab23786d922f5778f590538e516827beeb51f116b44ead9e83d24496685cff742405a4655aa0c0ff134
1890	Hmideh Nina	37f0d32b42d8e7e8ea5b22a140056e759e792fb50d89dcc7fafe053c7541879c872d176c3fcf7387d60ab738df451819251c
9116	Davis Grace	2c6001114945665f431c4abff26cf1ec0886bda0e658de24c818678dd765ac8e6ceb22be7039d593897a99902c2d8774e4ef
6496	Brown Bob	e2ee547a72cdd5374dbca2b1cb4de604bb47670ae3bd39bfee4744171c309dcb564ff1fc7bac9c4da30318aea929f2dd0594
9589	Rodriguez Oscar	e762c1bd286a9bc557d6eacc2904a903521c3de9c391477888794102ae20ea00e47c10a5c46e0ab16f6e3db7115d302836c0
6715	Moore Bob	5103793eaf77b2819b8df1ea199ac8cd07c009a22f83dd8ce88847a287583af7d71e2ff1ff74fcefef1c0cae3bc99a008114
5247	Brown Trent	8ddafbfccca61d783228d100f1b2b177d487e206c58df2ee839eccdedafd97023bd537e393efdbd8f3e35ec15414b2e0e7f7
8908	Davis Ivan	0c2c5569a2f5358878b5fabe0b8508758561611f0e1bf44f32892867970d40c2f1a42823cc7f4cb01dbfbe23db1a8b226cbf
8766	Miller Quentin	0654fcd13765cf7ccd9700a74ba99f11e97a80d76c45e2d4240dd8f793f45ac8c4b4da0d4f777f17335ebe95a9a832d0ca89
3550	Smith Rupert	d7c254fb657672ad406947e134f7ac13cde66cbad2feff5f791bc74131627659fb6fa3f4d7b01aa0bf879ceeb255914f7606
4391	Hernandez Grace	8deadc84ec55a44014a09b09a211e71057c6c94c1ee2a85ccc3b93b3a167778801450c185a19613afc6d2ecf8b8f52f5ae25
\.


--
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY ("admin_Id");


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY ("application_Id");


--
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY ("room_Id");


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY ("student_Id");


--
-- Name: applications applications_admin_Id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT "applications_admin_Id_fkey" FOREIGN KEY ("admin_Id") REFERENCES public.admins("admin_Id");


--
-- Name: applications applications_room_Id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT "applications_room_Id_fkey" FOREIGN KEY ("room_Id") REFERENCES public.rooms("room_Id");


--
-- Name: applications applications_student_Id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.applications
    ADD CONSTRAINT "applications_student_Id_fkey" FOREIGN KEY ("student_Id") REFERENCES public.students("student_Id");


--
-- PostgreSQL database dump complete
--

\unrestrict C8lYEsRmoh6902G7OtP0JoEk7Ag249rB9ktLN1Rkz2StMnek4LaJwMgzNbgL5B5

