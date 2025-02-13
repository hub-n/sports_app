-- Procedure to register a new user
CREATE OR REPLACE PROCEDURE register_user (
    p_name IN VARCHAR2,
    p_email IN VARCHAR2,
    p_password_hash IN VARCHAR2,
    p_profile_picture_url IN VARCHAR2,
    p_bio IN CLOB
)
AS
BEGIN
    INSERT INTO Users (name, email, password_hash, profile_picture_url, bio, created_at)
    VALUES (p_name, p_email, p_password_hash, p_profile_picture_url, p_bio, CURRENT_TIMESTAMP);
END;
/

-- Function to get the total number of participants in an event
CREATE OR REPLACE FUNCTION get_event_participants_count (
    p_event_id IN NUMBER
) RETURN NUMBER
AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM Event_Participants
    WHERE event_id = p_event_id;

    RETURN v_count;
END;
/

-- Procedure to update a space's description
CREATE OR REPLACE PROCEDURE update_space_description (
    p_space_id IN NUMBER,
    p_new_description IN CLOB
)
AS
BEGIN
    UPDATE Spaces
    SET description = p_new_description
    WHERE space_id = p_space_id;
END;
/

-- Function to calculate the average rating for a space
CREATE OR REPLACE FUNCTION get_average_space_rating (
    p_space_id IN NUMBER
) RETURN NUMBER
AS
    v_avg_rating NUMBER;
BEGIN
    SELECT AVG(rating) INTO v_avg_rating
    FROM Reviews
    WHERE space_id = p_space_id;

    RETURN NVL(v_avg_rating, 0); -- Return 0 if no reviews exist
END;
/

-- Trigger to update the average congestion level in the Spaces table after a new congestion report is added
CREATE OR REPLACE TRIGGER update_avg_congestion
FOR INSERT OR DELETE OR UPDATE ON Congestion_Reports
COMPOUND TRIGGER
    -- Variables to store intermediate results
    TYPE space_id_list IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
    space_ids space_id_list;
    idx PLS_INTEGER := 0;

    -- Before each row: Collect affected `space_id` values
    BEFORE EACH ROW IS
    BEGIN
        idx := idx + 1;
        space_ids(idx) := :NEW.space_id;
    END BEFORE EACH ROW;

    -- After statement: Process the affected spaces
    AFTER STATEMENT IS
        v_low_count NUMBER;
        v_medium_count NUMBER;
        v_high_count NUMBER;
        v_total_count NUMBER;
        v_new_avg VARCHAR2(10);
    BEGIN
        -- Remove duplicate space_ids
        FOR i IN 1 .. space_ids.COUNT LOOP
            IF i = 1 OR space_ids(i) != space_ids(i - 1) THEN
                -- Calculate the new congestion levels
                SELECT SUM(CASE WHEN congestion_level = 'Low' THEN 1 ELSE 0 END),
                       SUM(CASE WHEN congestion_level = 'Medium' THEN 1 ELSE 0 END),
                       SUM(CASE WHEN congestion_level = 'High' THEN 1 ELSE 0 END),
                       COUNT(*)
                INTO v_low_count, v_medium_count, v_high_count, v_total_count
                FROM Congestion_Reports
                WHERE space_id = space_ids(i);

                -- Determine the new average congestion level
                IF v_low_count >= v_medium_count AND v_low_count >= v_high_count THEN
                    v_new_avg := 'Low';
                ELSIF v_medium_count >= v_low_count AND v_medium_count >= v_high_count THEN
                    v_new_avg := 'Medium';
                ELSE
                    v_new_avg := 'High';
                END IF;

                -- Update the Spaces table
                UPDATE Spaces
                SET avg_congestion = v_new_avg, last_reported_at = CURRENT_TIMESTAMP
                WHERE space_id = space_ids(i);
            END IF;
        END LOOP;
    END AFTER STATEMENT;
END;
/

-- Trigger to auto-update the current_participants in Events table when a new participant joins
CREATE OR REPLACE TRIGGER update_event_participants
FOR INSERT OR DELETE ON Event_Participants
COMPOUND TRIGGER
    TYPE event_id_list IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
    event_ids event_id_list;
    idx PLS_INTEGER := 0;

    BEFORE EACH ROW IS
    BEGIN
        idx := idx + 1;
        event_ids(idx) := :NEW.event_id;
    END BEFORE EACH ROW;

    AFTER STATEMENT IS
        v_current_participants NUMBER;
    BEGIN
        -- Remove duplicate event_ids
        FOR i IN 1 .. event_ids.COUNT LOOP
            IF i = 1 OR event_ids(i) != event_ids(i - 1) THEN
                -- Calculate the number of participants for each event
                SELECT COUNT(*)
                INTO v_current_participants
                FROM Event_Participants
                WHERE event_id = event_ids(i);

                -- Update the current_participants field in Events
                UPDATE Events
                SET current_participants = v_current_participants
                WHERE event_id = event_ids(i);
            END IF;
        END LOOP;
    END AFTER STATEMENT;
END;
/
