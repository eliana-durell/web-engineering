DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS libraries;

CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL, --1
    full_name VARCHAR(50) NOT NULL, --John Doe (called username)
    username VARCHAR(30) NOT NULL UNIQUE, --jd500 (called userID)
    email VARCHAR(50) NOT NULL UNIQUE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    hashed_password VARCHAR(200) NOT NULL,
    session_key DECIMAL(39) UNIQUE
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
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (library_id) REFERENCES libraries(id),
    CONSTRAINT check_status_tag CHECK (status_tag='checked_out' OR 
        status_tag='reserved' OR status_tag='returned' OR status_tag='overdue' OR status_tag='late_return')
);

INSERT INTO users (full_name, username, email, active, hashed_password, session_key) VALUES 
                    ('Ada Lovelace', 'ada_love', 'adalovelace@gmail.com', DEFAULT, 
                        '6f0653b3772153182365664d03796bee0f2b33eddea02fe5b4d54e9d3ffbc9a5e10207cb45eba60555dfffa0d11c95fc30dea60f36e3e67d9f19abd370af0283', NULL), --math!science?
                    ('Mary Shelley', 'franks_mom', 'mshelly@hotmail.com', DEFAULT, 
                        'acc0a6ecce34da822415285bb8bb2cf68c498c5e3648fbdc555a7b3138dfa5966bd2fdde43278e1bbddf071dea268741e2c6f9b1f931a1e5938b954ad7373f91', NULL), --thebookist
                    ('Jackie Gleason', 'jackie_G', 'jg@bookies.com', DEFAULT, 
                        '61c72f7d44c3b8d3ecb9bf84b0013f34f10874bfb01633b72f0b48bb4c0feb11d982bd6aaffe6bfa75043baa2e8036f8ff119065f231328f3cb29f7fb9730d9e', NULL), --baseball
                    ('Art Garfunkel', 'art', 'artgarfunkel@go.com', DEFAULT, 
                        'e9a92ebc35c55423633fb7ea989c5e06429436dbaacde9821334f0116ae3145b234a2695e997173f5b491393530151e696adb6ea9677fabbf6c14bf0f8b09d9c', NULL), --vangogh
                    ('Frank Wonder', 'Frank_Wonder', 'frankywonder@mail.com', FALSE, 
                        '1995b6cd67849ea3c0a0829bbb1842e1d3110bae566903475cc23ae12fcada56babc31a8c3efc6d4db77666ae1c3bab1213f501226fe1d1af415ea8ed1b15ffe', NULL), --5wonders 
                    ('Stevie Wonder', 'Stevie_Wonder', 'steviewonder@gmail.com', FALSE, 
                        'b12bb0f6b92d49a00ec4fdd14faa724717036e088b93b35ec6650f6f2f24bda9a3f577ada64c65c892fc5aacebd491402ac1a859955918cf5f7c741af89a0f2d', NULL); --3blindmice

INSERT INTO books (title, author, category, genre, publish_date, summary) VALUES 
                    ('The Echoes of Glass', 'Maren Elwood', 'Fiction', 'Mystery', '2021-02-12', 
                        'A woman uncovers generations of secrets within a shattered mansion, where the past whispers through every pane of glass.'),
                    ('Beneath Hollow Skies', 'K.J. Harrow', 'Fiction', 'Post-Apocalyptic', '2019-09-03',
                        'In a world where the sky has mysteriously collapsed, a group of survivors must navigate shifting loyalties and unseen dangers to find hope.'),
                    ('The Lantern Keeper’s Promise', 'Eira Monroe', 'Fiction', 'Drama', '2023-06-17',
                        'A solitary lighthouse keeper is forced to confront his past and fulfill a long-forgotten vow when a storm brings an unexpected visitor.'),
                    ('Wired for Wonder: The Neuroscience of Curiosity', 'Dr. Alicia Renn', 'Non-Fiction', 'Science', '2020-04-09',
                        'Explores how curiosity shapes the brain, fuels innovation, and drives human learning from childhood to adulthood.'),
                    ('The Hidden Cost of Convenience', 'Marcus Leung', 'Non-Fiction', 'Social Studies', '2022-11-14',
                        'Investigates the environmental, social, and psychological consequences of our modern obsession with ease and instant gratification.'),
                    ('Voices from the Edge: Climate Stories from the Front Lines', 'Sarita Javed', 'Non-Fiction', 'Environmental', '2021-08-28',
                        'A powerful collection of personal accounts from communities directly impacted by climate change, offering insight, urgency, and resilience.'),
                    ('Frankenstein', 'Mary Shelley', 'Fiction', 'Gothic Horror', '1818-01-01',
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
    SELECT u.id, b.id, l.id, 'returned', '2022-09-30', '2022-10-14', '2022-10-01'
    FROM users u 
    JOIN books b ON b.title='The Echoes of Glass' AND b.author='Maren Elwood'
    JOIN libraries l ON lib_name='Towns of Penfield'
    WHERE username='ada_love';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'returned', '2020-01-5', '2020-01-19', '2020-01-15'
    FROM users u 
    JOIN books b ON b.title='Beneath Hollow Skies' AND b.author='K.J. Harrow'
    JOIN libraries l ON lib_name='Pittsford'
    WHERE username='franks_mom';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'returned', '2020-03-02', '2020-03-16', '2020-03-08'
    FROM users u 
    JOIN books b ON b.title='Beneath Hollow Skies' AND b.author='K.J. Harrow'
    JOIN libraries l ON lib_name='Henrietta'
    WHERE username='ada_love';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'checked_out', '2023-05-21', '2023-06-05', NULL
    FROM users u 
    JOIN books b ON b.title='Voices from the Edge: Climate Stories from the Front Lines' AND b.author='Sarita Javed'
    JOIN libraries l ON lib_name='Towns of Penfield'
    WHERE username='jackie_G';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'returned', '2019-10-19', '2019-11-03', '2019-10-21'
    FROM users u 
    JOIN books b ON b.title='Beneath Hollow Skies' AND b.author='K.J. Harrow'
    JOIN libraries l ON lib_name='Pittsford'
    WHERE username='jackie_G';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'checked_out', '2019-10-02', '2019-10-16', NULL
    FROM users u 
    JOIN books b ON b.title='Frankenstein' AND b.author='Mary Shelley'
    JOIN libraries l ON lib_name='Fairport'
    WHERE username='jackie_G';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'checked_out', '2022-09-30', '2022-10-14', NULL
    FROM users u 
    JOIN books b ON b.title='The Echoes of Glass' AND b.author='Maren Elwood'
    JOIN libraries l ON lib_name='Towns of Penfield'
    WHERE username='art';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'late_return', '2012-08-02', '2012-08-16', '2012-08-30'
    FROM users u 
    JOIN books b ON b.title='Frankenstein' AND b.author='Mary Shelley'
    JOIN libraries l ON lib_name='Fairport'
    WHERE username='Frank_Wonder';

INSERT INTO history (user_id, book_id, library_id, status_tag, checkout_date, due_date, return_date) 
    SELECT u.id, b.id, l.id, 'checked_out', '2014-04-05', '2014-04-19', NULL
    FROM users u 
    JOIN books b ON b.title='The Hidden Cost of Convenience' AND b.author='Marcus Leung'
    JOIN libraries l ON lib_name='Fairport'
    WHERE username='Frank_Wonder';