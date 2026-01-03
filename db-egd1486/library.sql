DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS libraries;

CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category VARCHAR(30) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    publish_date DATE,
    summary VARCHAR(300) NOT NULL,
    CONSTRAINT check_category CHECK (category='Fiction' OR category='Non-Fiction')
);

CREATE TABLE libraries (
    id SERIAL PRIMARY KEY, 
    lib_name VARCHAR(50) NOT NULL
);

CREATE TABLE inventory (
    book_id INTEGER NOT NULL, 
    available_count INTEGER NOT NULL,
    checkout_count INTEGER NOT NULL,
    library_id INTEGER NOT NULL,
    PRIMARY KEY (library_id, book_id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY(library_id) REFERENCES libraries(id)
);

CREATE TABLE history (
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    library_id INTEGER NOT NULL,
    status_tag VARCHAR(30) NOT NULL,
    checkout_date DATE,
    due_date DATE, 
    return_date DATE,
    PRIMARY KEY(user_id, book_id, library_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (library_id) REFERENCES libraries(id),
    CONSTRAINT check_status_tag CHECK (status_tag='checked_out' OR 
        status_tag='reserved' OR status_tag='returned' OR status_tag='overdue' OR status_tag='late_return')
);

INSERT INTO users (first_name, last_name, email, active) VALUES 
                    ('Ada', 'Lovelace', 'adalovelace@gmail.com', DEFAULT),
                    ('Mary', 'Shelley', 'mshelly@hotmail.com', DEFAULT),
                    ('Jackie', 'Gleason', 'jg@bookies.com', DEFAULT),
                    ('Art', 'Garfunkel', 'artgarfunkel@go.com', DEFAULT),
                    ('Frank', 'Wonder', 'frankywonder@mail.com', FALSE), 
                    ('Stevie', 'Wonder', 'steviewonder@gmail.com', FALSE);

INSERT INTO books (title, author, category, genre, publish_date, summary) VALUES 
                    ('The Echoes of Glass', 'Maren Elwood', 'Fiction', 'Mystery', '2021-2-12', 
                        'A woman uncovers generations of secrets within a shattered mansion, where the past whispers through every pane of glass.'),
                    ('Beneath Hollow Skies', 'K.J. Harrow', 'Fiction', 'Post-Apocalyptic', '2019-9-3',
                        'In a world where the sky has mysteriously collapsed, a group of survivors must navigate shifting loyalties and unseen dangers to find hope.'),
                    ('The Lantern Keeper’s Promise', 'Eira Monroe', 'Fiction', 'Drama', '2023-6-17',
                        'A solitary lighthouse keeper is forced to confront his past and fulfill a long-forgotten vow when a storm brings an unexpected visitor.'),
                    ('Wired for Wonder: The Neuroscience of Curiosity', 'Dr. Alicia Renn', 'Non-Fiction', 'Science', '2020-4-9',
                        'Explores how curiosity shapes the brain, fuels innovation, and drives human learning from childhood to adulthood.'),
                    ('The Hidden Cost of Convenience', 'Marcus Leung', 'Non-Fiction', 'Social Studies', '2022-11-14',
                        'Investigates the environmental, social, and psychological consequences of our modern obsession with ease and instant gratification.'),
                    ('Voices from the Edge: Climate Stories from the Front Lines', 'Sarita Javed', 'Non-Fiction', 'Environmental', '2021-8-28',
                        'A powerful collection of personal accounts from communities directly impacted by climate change, offering insight, urgency, and resilience.'),
                    ('Frankenstein', 'Mary Shelley', 'Fiction', 'Gothic Horror', '1818-1-1',
                        'A haunting tale of scientific ambition and moral consequence, exploring the boundaries of creation and the depths of human isolation.');


INSERT INTO libraries (lib_name) VALUES ('Towns of Penfield'), ('Fairport'), ('Henrietta'), ('Pittsford');


INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 0, 1, l.id
    FROM books b
    JOIN libraries  l ON l.lib_name='Towns of Penfield'
    WHERE title='The Echoes of Glass' AND author='Maren Elwood';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 3, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Fairport'
    WHERE title='The Echoes of Glass' AND author='Maren Elwood';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 1, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Henrietta'
    WHERE title='The Echoes of Glass' AND author='Maren Elwood';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 0, 1, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Pittsford'
    WHERE title='Beneath Hollow Skies' AND author='K.J. Harrow';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 3, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Towns of Penfield'
    WHERE title='Beneath Hollow Skies' AND author='K.J. Harrow';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 0, 1, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Henrietta'
    WHERE title='Beneath Hollow Skies' AND author='K.J. Harrow';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 3, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Fairport'
    WHERE title='The Lantern Keeper’s Promise' AND author='Eira Monroe';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 1, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Pittsford'
    WHERE title='The Lantern Keeper’s Promise' AND author='Eira Monroe';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 1, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Towns of Penfield'
    WHERE title='The Lantern Keeper’s Promise' AND author='Eira Monroe';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 3, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Towns of Penfield'
    WHERE title='Wired for Wonder: The Neuroscience of Curiosity' AND author='Dr. Alicia Renn';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 2, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Henrietta'
    WHERE title='Wired for Wonder: The Neuroscience of Curiosity' AND author='Dr. Alicia Renn';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 2, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Henrietta'
    WHERE title='The Hidden Cost of Convenience' AND author='Marcus Leung';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 2, 1, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Fairport'
    WHERE title='The Hidden Cost of Convenience' AND author='Marcus Leung';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 0, 1, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Towns of Penfield'
    WHERE title='Voices from the Edge: Climate Stories from the Front Lines' AND author='Sarita Javed';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 4, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Pittsford'
    WHERE title='Voices from the Edge: Climate Stories from the Front Lines' AND author='Sarita Javed';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 2, 1, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Fairport'
    WHERE title='Frankenstein' AND author='Mary Shelley';

INSERT INTO inventory (book_id, available_count, checkout_count, library_id) 
    SELECT b.id, 2, 0, l.id
    FROM books b
    JOIN libraries l ON l.lib_name='Henrietta'
    WHERE title='Frankenstein' AND author='Mary Shelley';


INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'returned', '2022-9-30', '2022-10-14', '2022-10-1'
    FROM users u 
    JOIN books b ON b.title='The Echoes of Glass' AND b.author='Maren Elwood'
    JOIN libraries l ON lib_name='Towns of Penfield'
    WHERE first_name='Ada' AND last_name='Lovelace';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'returned', '2020-1-5', '2020-1-19', '2020-1-15'
    FROM users u 
    JOIN books b ON b.title='Beneath Hollow Skies' AND b.author='K.J. Harrow'
    JOIN libraries l ON lib_name='Pittsford'
    WHERE first_name='Mary' AND last_name='Shelley';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'returned', '2020-3-2', '2020-3-16', '2020-3-8'
    FROM users u 
    JOIN books b ON b.title='Beneath Hollow Skies' AND b.author='K.J. Harrow'
    JOIN libraries l ON lib_name='Henrietta'
    WHERE first_name='Ada' AND last_name='Lovelace';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'checked_out', '2023-5-21', '2023-6-5', NULL
    FROM users u 
    JOIN books b ON b.title='Voices from the Edge: Climate Stories from the Front Lines' AND b.author='Sarita Javed'
    JOIN libraries l ON lib_name='Towns of Penfield'
    WHERE first_name='Jackie' AND last_name='Gleason';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'returned', '2019-10-19', '2019-11-3', '2019-10-21'
    FROM users u 
    JOIN books b ON b.title='Beneath Hollow Skies' AND b.author='K.J. Harrow'
    JOIN libraries l ON lib_name='Pittsford'
    WHERE first_name='Jackie' AND last_name='Gleason';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'checked_out', '2019-10-2', '2019-10-16', NULL
    FROM users u 
    JOIN books b ON b.title='Frankenstein' AND b.author='Mary Shelley'
    JOIN libraries l ON lib_name='Fairport'
    WHERE first_name='Jackie' AND last_name='Gleason';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'checked_out', '2022-9-30', '2022-10-14', NULL
    FROM users u 
    JOIN books b ON b.title='The Echoes of Glass' AND b.author='Maren Elwood'
    JOIN libraries l ON lib_name='Towns of Penfield'
    WHERE first_name='Art' AND last_name='Garfunkel';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'late_return', '2012-8-2', '2012-8-16', '2012-8-30'
    FROM users u 
    JOIN books b ON b.title='Frankenstein' AND b.author='Mary Shelley'
    JOIN libraries l ON lib_name='Fairport'
    WHERE first_name='Frank' AND last_name='Wonder';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'checked_out', '2014-4-5', '2014-4-19', NULL
    FROM users u 
    JOIN books b ON b.title='The Hidden Cost of Convenience' AND b.author='Marcus Leung'
    JOIN libraries l ON lib_name='Fairport'
    WHERE first_name='Frank' AND last_name='Wonder';