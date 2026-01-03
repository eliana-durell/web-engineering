DROP TABLE if EXISTS category_items CASCADE;
DROP table if EXISTS nutrition CASCADE;
DROP TABLE if EXISTS categories CASCADE;


CREATE TABLE nutrition (
    id SERIAL PRIMARY KEY NOT NULL,
    item VARCHAR(30) NOT NULL,
    calories REAL NOT NULL,
    totalFat REAL NOT NULL,
    saturatedFat REAL NOT NULL,
    transFat REAL NOT NULL,
    protein REAL NOT NULL,
    carbohydrate REAL NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(30) NOT NULL
);

CREATE TABLE category_items (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL,
    nutrition_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (nutrition_id) REFERENCES nutrition(id)
);

INSERT INTO nutrition(item, calories, totalFat, saturatedFat, transFat, protein, carbohydrate) VALUES 
                    ('steak', 300, 5.73, 2.183, 0.182, 29.44, 0.0),
                    ('ground beef', 200, 13.1, 5.3, 0.6, 15.18, 0.0),
                    ('chicken' , 100, 9.3, 2.5, 0.1, 27.14, 0.0),
                    ('fish', 80,  6.34, 1.0, 0.0, 19.84, 0.0),
                    ('soy', 50, 19.94, 2.884, 0.0, 36.49, 30.16),

                    ('orange', 300, 0.12, 0.0, 0.0, 0.94, 11.75),
                    ('banana', 200, 0.33, 0.0, 0.0, 1.09, 22.84),
                    ('pineapple', 100, 0.12, 0.0, 0.0, 0.54, 13.12),
                    ('grapes', 80, 0.16, 0.0, 0.0, 0.72, 18.1 ),
                    ('blueberries', 50, 0.33, 0.0, 0.0, 0.74, 14.49),

                    ('romaine', 30, 0.3, 0.0, 0.0, 1.2, 3.3),
                    ('green beans', 40, 0.22, 0.0, 0.0, 1.83, 6.97),
                    ('squash', 100, 0.2, 0.0, 0.0, 1.2, 3.4),
                    ('spinach', 50, 0.4, 0.0, 0.0, 2.9, 3.6),
                    ('kale', 10, 0.9, 0.0, 0.0, 4.3, 8.8  ),

                    ('milk', 300, 3.9, 2.4, 0.0, 3.2, 4.8  ),
                    ('yoghurt', 200, 5.0, 0.0, 0.0, 9.0, 3.98),
                    ('cheddar cheese', 200, 9.0, 6.0, 0.0, 7.0, 0.0),
                    ('skim milk', 100, 0.2, 0.1, 0.0, 8.3, 12.5),
                    ('cottage cheese', 80, 4.3, 0.0, 0.0, 11.12, 3.38),

                    ('bread', 200, 1.1, 0.0, 0.0, 4.0, 13.8),
                    ('bagel', 300, 1.7, 0.1, 0.0, 13.8, 68),
                    ('pita', 250, 1.7, 0.3, 0.0, 6.3, 35.2),
                    ('naan', 210, 3.3, 0.1, 0.0, 2.7, 16.9),
                    ('tortilla', 120, 0.5, 0.1, 0.0, 1.1, 8.5);

INSERT INTO categories (category_name) VALUES 
                        ('Proteins'),
                        ('Fruits'),
                        ('Vegetables'),
                        ('Dairy'),
                        ('Grain');

insert into category_items (category_id, nutrition_id) VALUES 
                            (1, 1), --steak
                            (1, 2), --ground beef
                            (1, 3), --chicken
                            (1, 4), --fish
                            (1, 5), --soy

                            (2, 6), --orange
                            (2, 7), --banana
                            (2, 8), --pineapple
                            (2, 9), --grapes
                            (2, 10), --blueberries

                            (3, 11), --romaine
                            (3, 12), --green beans
                            (3, 13), --squash
                            (3, 14), --spinach
                            (3, 15), --kale

                            (4, 16), --milk
                            (4, 17), --yoghurt
                            (4, 18), --cheddar cheese
                            (4, 19), --skim milk
                            (4, 20), --cottage cheese

                            (5, 21), --bread
                            (5, 22), --bagel
                            (5, 23), --pita
                            (5, 24), --naan
                            (5, 25) --tortilla 

--    The API and how you use it could still be improved. 
--  What you are doing now is basically pulling the entire dataset all at once. 
--  That's not going break things in this small dataset, but practically (in real-world apps) you wouldn't want to do that.
--   If you just pull categories first, and then as someone selects a category you do a GET on the items for that category,
--  it's much more efficient.  (Real world: What if you had 10,000 food items per category?)
-- So -- good enough for now (for class work), but always think how a real-world app would be designed