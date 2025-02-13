-- Create Users table
CREATE TABLE Users (
    user_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    email VARCHAR2(255) NOT NULL UNIQUE,
    password_hash VARCHAR2(255) NOT NULL,
    profile_picture_url VARCHAR2(255),
    bio VARCHAR2(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Spaces table
CREATE TABLE Spaces (
    space_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    address VARCHAR2(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    description VARCHAR2(255),
    opening_hours VARCHAR2(100),
    sport_types VARCHAR2(100),
    avg_congestion VARCHAR2(10) CHECK (avg_congestion IN ('Low', 'Medium', 'High')),
    last_reported_at TIMESTAMP
);

-- Create Events table
CREATE TABLE Events (
    event_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    space_id NUMBER NOT NULL,
    organizer_id NUMBER NOT NULL,
    title VARCHAR2(100) NOT NULL,
    description VARCHAR2(255),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    max_participants NUMBER,
    current_participants NUMBER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (space_id) REFERENCES Spaces(space_id) ON DELETE CASCADE,
    FOREIGN KEY (organizer_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Event_Participants table
CREATE TABLE Event_Participants (
    participant_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    event_id NUMBER NOT NULL,
    user_id NUMBER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Chats table
CREATE TABLE Chats (
    chat_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    event_id NUMBER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE
);

-- Create Messages table
CREATE TABLE Messages (
    message_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    chat_id NUMBER NOT NULL,
    sender_id NUMBER NOT NULL,
    content VARCHAR2(255) NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES Chats(chat_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Congestion_Reports table
CREATE TABLE Congestion_Reports (
    report_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    space_id NUMBER NOT NULL,
    user_id NUMBER NOT NULL,
    congestion_level VARCHAR2(10) CHECK (congestion_level IN ('Low', 'Medium', 'High')) NOT NULL,
    congestion_comment VARCHAR2(500),
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (space_id) REFERENCES Spaces(space_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Create Reviews table
CREATE TABLE Reviews (
    review_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    space_id NUMBER NOT NULL,
    user_id NUMBER NOT NULL,
    rating NUMBER CHECK (rating BETWEEN 1 AND 5),
    review_comment VARCHAR2(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (space_id) REFERENCES Spaces(space_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);
