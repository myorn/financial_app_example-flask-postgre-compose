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

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';

CREATE TABLE public.api_users
    (
        usr_id uuid DEFAULT public.uuid_generate_v4(),
	    username VARCHAR(40) NOT NULL,
	    money NUMERIC DEFAULT 0,
	    PRIMARY KEY (usr_id)
	);

CREATE TABLE public.bank
    (
        bank_id uuid DEFAULT public.uuid_generate_v4(),
        bank_name VARCHAR(40) NOT NULL,
        charged_overall NUMERIC DEFAULT 0,
        comission_percent NUMERIC DEFAULT 0,
        PRIMARY KEY (bank_id)
	);

CREATE TABLE public.transaction_list
    (
        tra_id uuid DEFAULT public.uuid_generate_v4(),
        sender_id uuid NOT NULL,
	    receiver_id uuid NOT NULL,
	    money_amount NUMERIC NOT NULL,
	    bank_comission NUMERIC NOT NULL,
	    bank_id uuid NOT NULL,
	    dt timestamp with time zone DEFAULT now(),
        PRIMARY KEY (tra_id),
        CONSTRAINT fk_sender
            FOREIGN KEY(sender_id)
	            REFERENCES public.api_users(usr_id),
	    CONSTRAINT fk_recv
            FOREIGN KEY(receiver_id)
	            REFERENCES public.api_users(usr_id),
	    CONSTRAINT fk_bank
            FOREIGN KEY(bank_id)
	            REFERENCES public.bank(bank_id)
	);

create or replace function public.make_transaction(sender uuid,
                                                   receiver uuid,
                                                   amount NUMERIC,
                                                   bank_id_ uuid DEFAULT '00000000-0000-0000-0000-000000000001')
returns json
language plpgsql
as
$$
declare
    comission NUMERIC;
begin
    if bank_id_ not in (SELECT bank_id FROM bank) then
        return '{"error":"Wrong bank id"}';
    end if;

    if sender not in (SELECT usr_id FROM api_users) then
        return '{"error":"Sender is not our client"}';
    end if;

    if receiver not in (SELECT usr_id FROM api_users) then
        return '{"error":"Receiver is not our client"}';
    end if;

    SELECT comission_percent * amount FROM bank WHERE bank_id = bank_id_ INTO comission;

    if (SELECT money FROM api_users WHERE usr_id = sender) < amount + comission then
        return '{"error":"Insufficient funds"}';
    end if;

    UPDATE api_users SET money = money - (amount + comission) WHERE usr_id = sender;

    UPDATE api_users SET money = money + amount WHERE usr_id = receiver;

    INSERT INTO transaction_list(sender_id,receiver_id,money_amount,bank_comission,bank_id)
         VALUES(sender,receiver,amount,comission,bank_id_);

    UPDATE bank SET charged_overall = charged_overall + comission WHERE bank_id = bank_id_;

    return '{"message":"Done successfully"}';
end;
$$;

INSERT INTO public.api_users
VALUES
('40e6215d-b5c6-4896-987c-f30f3678f608','Alice',300),
('6ecd8c99-4036-403d-bf84-cf8400f67836','Bob',1000);

INSERT INTO public.bank(bank_id,bank_name,comission_percent)
VALUES('00000000-0000-0000-0000-000000000001','bank101',0.015);