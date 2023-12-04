DROP TABLE user_accounts;
DROP SEQUENCE user_accounts_seq;

CREATE SEQUENCE user_accounts_seq --lack permissions on temple server to auto generate an incremented unique ID, these changes solve that
    START WITH 1
    INCREMENT BY 1
    NOCACHE;

CREATE TABLE user_accounts (
    user_id NUMBER,
    username VARCHAR2(50) NOT NULL,
    password_hash VARCHAR2(64) NOT NULL,
    CONSTRAINT pk_user_id PRIMARY KEY (user_id)
);

CREATE OR REPLACE TRIGGER user_accounts_trigger
BEFORE INSERT ON user_accounts
FOR EACH ROW
BEGIN
    SELECT user_accounts_seq.NEXTVAL
    INTO :new.user_id
    FROM dual;
END;

COMMIT;

SELECT * FROM user_accounts;

