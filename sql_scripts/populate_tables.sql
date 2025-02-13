-- Populate Users table
INSERT INTO Users (name, email, password_hash, profile_picture_url, bio) VALUES
('Janusz Manusz', 'janusz@example.com', 'hashed_password_0', 'https://example.com/janusz.jpg', 'Gram w gale.'),
('Alice Johnson', 'alice@example.com', 'hashed_password_1', 'https://example.com/alice.jpg', 'Sports enthusiast and nature lover.'),
('Bob Smith', 'bob@example.com', 'hashed_password_2', 'https://example.com/bob.jpg', 'Basketball player and coach.'),
('Cathy Brown', 'cathy@example.com', 'hashed_password_3', NULL, 'Fitness freak and marathon runner.');

-- Populate Spaces table
INSERT INTO Spaces (name, address, latitude, longitude, description, opening_hours, sport_types, avg_congestion, last_reported_at) VALUES
('Baltasis Tiltas Courts', 'Vilnius', 53.785091, -73.968285, 'Skate park, basketball courts, voleyball sandboxes.', '6 AM - 11 PM', 'Basketball', 'Medium', CURRENT_TIMESTAMP),
('Central Park Basketball Court', 'Central Park, NYC', 40.785091, -73.968285, 'Outdoor basketball court surrounded by trees.', '6 AM - 10 PM', 'Basketball', 'Medium', CURRENT_TIMESTAMP),
('Riverside Soccer Field', 'Riverside Park, NYC', 40.800676, -73.972554, 'Well-maintained soccer field near the river.', '6 AM - 9 PM', 'Soccer', 'Low', CURRENT_TIMESTAMP),
('Downtown Gym', '123 Main St, NYC', 40.712776, -74.005974, 'Fully equipped indoor gym with modern facilities.', '5 AM - 11 PM', 'General Fitness', 'High', CURRENT_TIMESTAMP);

-- Populate Events table
INSERT INTO Events (space_id, organizer_id, title, description, start_time, end_time, max_participants, current_participants) VALUES
(1, 1, 'Saturday Basketball Game', 'Join us for a friendly game of basketball.', TO_TIMESTAMP('2024-12-30 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-12-30 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 10, 5),
(2, 2, 'Weekend Soccer Match', 'Casual soccer game open to all skill levels.', TO_TIMESTAMP('2024-12-31 15:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-12-31 17:00:00', 'YYYY-MM-DD HH24:MI:SS'), 22, 12),
(3, 3, 'Morning Yoga Session', 'Start your day with a refreshing yoga session.', TO_TIMESTAMP('2024-12-29 07:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2024-12-29 08:00:00', 'YYYY-MM-DD HH24:MI:SS'), 20, 15);

-- Populate Congestion_Reports table
INSERT INTO Congestion_Reports (space_id, user_id, congestion_level, congestion_comment, reported_at) VALUES
(21, 1, 'Medium', 'Duzo narodu.', CURRENT_TIMESTAMP),
(1, 1, 'Medium', 'Pretty crowded but manageable.', CURRENT_TIMESTAMP),
(2, 2, 'Low', 'Almost empty and very peaceful.', CURRENT_TIMESTAMP),
(3, 3, 'High', 'Overcrowded and noisy.', CURRENT_TIMESTAMP);

-- Populate Event_Participants table
INSERT INTO Event_Participants (event_id, user_id, joined_at) VALUES
(1, 2, CURRENT_TIMESTAMP),
(1, 3, CURRENT_TIMESTAMP),
(2, 1, CURRENT_TIMESTAMP),
(2, 3, CURRENT_TIMESTAMP),
(3, 2, CURRENT_TIMESTAMP);

-- Populate Chats table
INSERT INTO Chats (event_id, created_at) VALUES
(1, CURRENT_TIMESTAMP),
(2, CURRENT_TIMESTAMP),
(3, CURRENT_TIMESTAMP);

-- Populate Messages table
INSERT INTO Messages (chat_id, sender_id, content, sent_at) VALUES
(1, 2, 'Looking forward to the game!', CURRENT_TIMESTAMP),
(1, 3, 'Me too! It will be fun.', CURRENT_TIMESTAMP),
(2, 1, 'Who else is joining the soccer match?', CURRENT_TIMESTAMP),
(3, 3, 'Great yoga session today!', CURRENT_TIMESTAMP);

-- Populate Reviews table
INSERT INTO Reviews (space_id, user_id, rating, review_comment, created_at) VALUES
(1, 1, 4, 'Great court, but a bit crowded.', CURRENT_TIMESTAMP),
(2, 2, 5, 'Perfect field, well-maintained.', CURRENT_TIMESTAMP),
(3, 3, 3, 'Good gym, but too many people.', CURRENT_TIMESTAMP);
