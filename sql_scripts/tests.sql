set serveroutput on;

-- Tests with some complex querries
-- Fetch spaces with events and average participant count
DECLARE
    CURSOR space_event_cursor IS
        SELECT s.name AS space_name, e.title AS event_title, COUNT(ep.user_id) AS participant_count
        FROM Spaces s
        JOIN Events e ON s.space_id = e.space_id
        LEFT JOIN Event_Participants ep ON e.event_id = ep.event_id
        GROUP BY s.name, e.title;
    v_space_name VARCHAR2(100);
    v_event_title VARCHAR2(100);
    v_participant_count NUMBER;
BEGIN
    OPEN space_event_cursor;
    LOOP
        FETCH space_event_cursor INTO v_space_name, v_event_title, v_participant_count;
        EXIT WHEN space_event_cursor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('Space: ' || v_space_name || ', Event: ' || v_event_title || ', Participants: ' || v_participant_count);
    END LOOP;
    CLOSE space_event_cursor;
END;
/
-- Spaces with average congestion and highest-rated events
DECLARE
    CURSOR space_congestion_rating_cursor IS
        SELECT s.name AS space_name, AVG(CASE WHEN r.rating IS NOT NULL THEN r.rating ELSE 0 END) AS avg_rating,
               COUNT(CASE WHEN cr.congestion_level = 'High' THEN 1 END) AS high_congestion_reports
        FROM Spaces s
        LEFT JOIN Reviews r ON s.space_id = r.space_id
        LEFT JOIN Congestion_Reports cr ON s.space_id = cr.space_id
        GROUP BY s.name;
    v_space_name VARCHAR2(100);
    v_avg_rating NUMBER;
    v_high_congestion_reports NUMBER;
BEGIN
    OPEN space_congestion_rating_cursor;
    LOOP
        FETCH space_congestion_rating_cursor INTO v_space_name, v_avg_rating, v_high_congestion_reports;
        EXIT WHEN space_congestion_rating_cursor%NOTFOUND;
        DBMS_OUTPUT.PUT_LINE('Space: ' || v_space_name || ', Avg Rating: ' || v_avg_rating || ', High Congestion Reports: ' || v_high_congestion_reports);
    END LOOP;
    CLOSE space_congestion_rating_cursor;
END;
/

-- Test for the 'update_avg_congestion' trigger
BEGIN
    -- Insert a new congestion report
    INSERT INTO Congestion_Reports (space_id, user_id, congestion_level, congestion_comment)
    VALUES (1, 2, 'High', 'Very crowded');

    -- Check if the average congestion in the Spaces table is updated
    DECLARE
        v_avg_congestion VARCHAR2(10);
        v_last_reported_at TIMESTAMP;
    BEGIN
        SELECT avg_congestion, last_reported_at
        INTO v_avg_congestion, v_last_reported_at
        FROM Spaces
        WHERE space_id = 1;

        DBMS_OUTPUT.PUT_LINE('Average Congestion: ' || v_avg_congestion);
        DBMS_OUTPUT.PUT_LINE('Last Reported At: ' || v_last_reported_at);
    END;
END;
/

-- Test for the 'update_event_participants' trigger
BEGIN
    -- Add a new participant to an event
    INSERT INTO Event_Participants (event_id, user_id, joined_at)
    VALUES (1, 3, CURRENT_TIMESTAMP);

    -- Verify if the current_participants field in Events is updated
    DECLARE
        v_current_participants NUMBER;
    BEGIN
        SELECT current_participants
        INTO v_current_participants
        FROM Events
        WHERE event_id = 1;

        DBMS_OUTPUT.PUT_LINE('Current Participants: ' || v_current_participants);
    END;
END;
/

-- Test for the 'get_event_participants_count' function
DECLARE
    v_count NUMBER;
BEGIN
    -- Get the number of participants for an event
    v_count := get_event_participants_count(1);
    DBMS_OUTPUT.PUT_LINE('Total participants in event 1: ' || v_count);
END;
/

-- Test for the 'update_space_description' procedure
BEGIN
    -- Update the description of a space
    update_space_description(1, 'Updated description for testing.');

    -- Verify the description has been updated
    DECLARE
        v_description CLOB;
    BEGIN
        SELECT description
        INTO v_description
        FROM Spaces
        WHERE space_id = 1;

        DBMS_OUTPUT.PUT_LINE('Updated Description: ' || v_description);
    END;
END;
/

-- Test for the 'get_average_space_rating' function
DECLARE
    v_avg_rating NUMBER;
BEGIN
    -- Get the average rating of a space
    v_avg_rating := get_average_space_rating(1);
    DBMS_OUTPUT.PUT_LINE('Average rating for space 1: ' || v_avg_rating);
END;
/

-- Test: Create a new event
BEGIN
    INSERT INTO Events (space_id, organizer_id, title, description, start_time, end_time, max_participants)
    VALUES (1, 1, 'Evening Basketball', 'Casual game with friends.',
            TO_TIMESTAMP('2025-01-20 18:00:00', 'YYYY-MM-DD HH24:MI:SS'),
            TO_TIMESTAMP('2025-01-20 20:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10);

    DECLARE
        v_title VARCHAR2(100);
        v_description CLOB;
        v_start_time TIMESTAMP;
        v_end_time TIMESTAMP;
    BEGIN
        SELECT title, description, start_time, end_time
        INTO v_title, v_description, v_start_time, v_end_time
        FROM Events
        WHERE title = 'Evening Basketball';

        DBMS_OUTPUT.PUT_LINE('Event Created: ' || v_title);
        DBMS_OUTPUT.PUT_LINE('Description: ' || v_description);
        DBMS_OUTPUT.PUT_LINE('Starts At: ' || v_start_time);
        DBMS_OUTPUT.PUT_LINE('Ends At: ' || v_end_time);
    END;
END;
/

-- Test: Add participants to an event
BEGIN
    INSERT INTO Event_Participants (event_id, user_id, joined_at)
    VALUES (2, 2, CURRENT_TIMESTAMP);
    INSERT INTO Event_Participants (event_id, user_id, joined_at)
    VALUES (2, 3, CURRENT_TIMESTAMP);

    DECLARE
        v_participant_count NUMBER;
    BEGIN
        v_participant_count := get_event_participants_count(2);
        DBMS_OUTPUT.PUT_LINE('Total participants in Evening Basketball: ' || v_participant_count);
    END;
END;
/

-- Test: Add and retrieve a congestion report
BEGIN
    INSERT INTO Congestion_Reports (space_id, user_id, congestion_level, congestion_comment)
    VALUES (1, 3, 'Medium', 'Getting busier as the evening progresses.');

    DECLARE
        v_avg_congestion VARCHAR2(10);
    BEGIN
        SELECT avg_congestion
        INTO v_avg_congestion
        FROM Spaces
        WHERE space_id = 1;

        DBMS_OUTPUT.PUT_LINE('Updated Average Congestion for Space 1: ' || v_avg_congestion);
    END;
END;
/

-- Test: Add a review for a space
BEGIN
    INSERT INTO Reviews (space_id, user_id, rating, review_comment)
    VALUES (1, 2, 4, 'Great place to play, but parking is a bit tricky.');

    DECLARE
        v_new_avg_rating NUMBER;
    BEGIN
        v_new_avg_rating := get_average_space_rating(1);
        DBMS_OUTPUT.PUT_LINE('New Average Rating for Space 1: ' || v_new_avg_rating);
    END;
END;
/
