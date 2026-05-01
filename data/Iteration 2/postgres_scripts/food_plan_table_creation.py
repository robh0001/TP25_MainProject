import psycopg2


connection = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pass,
        port=5432
    )

print("Connected successfully")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE nutrition_plan (
    id SERIAL PRIMARY KEY,
    week_number INT NOT NULL,
    day_number INT NOT NULL,
    meal_type VARCHAR(20) NOT NULL,
    meal_name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    calories INT NOT NULL,
    protein_g DECIMAL(5,1) NOT NULL,
    carbohydrates_g DECIMAL(5,1) NOT NULL,
    fat_g DECIMAL(5,1) NOT NULL,
    fibre_g DECIMAL(5,1) NOT NULL,
    sodium_mg DECIMAL(7,1) NOT NULL,
    calcium_mg DECIMAL(7,1) NOT NULL,
    iron_mg DECIMAL(5,1) NOT NULL
);
""")
connection.commit()


cursor.execute("""
               INSERT INTO nutrition_plan (week_number, day_number, meal_type, meal_name, description, calories, protein_g, carbohydrates_g, fat_g, fibre_g, sodium_mg, calcium_mg, iron_mg) 
               
               VALUES

(1, 1, 'Breakfast', 'French Toast with Fruit Cocktail',
 'Whole wheat bread dipped in an egg and milk mixture and cooked until golden, served with syrup and canned fruit cocktail alongside a glass of milk.',
 335, 14.6, 35.2, 15.5, 4.8, 552.0, 137.0, 2.9),

(1, 1, 'Lunch', 'Minestrone Soup with Crackers and Cheese',
 'A hearty vegetable and kidney bean soup served with whole wheat crackers, a piece of cheese, fresh apple, and milk.',
 274, 18.9, 46.2, 2.5, 12.4, 775.0, 119.0, 5.9),

(1, 1, 'Dinner', 'Baked Pork Chop with Brown Rice and Vegetables',
 'A pork chop baked with onion, brown sugar, and ketchup, served alongside brown rice and stir-fried vegetables, finished with canned peaches and yogurt.',
 290, 21.4, 19.5, 14.1, 0.7, 693.0, 43.0, 1.1),

(1, 1, 'Snack', 'Whole Wheat Toast with Orange and Milk',
 'A light snack of toasted whole wheat bread served with a fresh orange and a glass of milk.',
 198, 9.2, 34.9, 1.5, 5.0, 221.0, 229.0, 1.4),

(1, 2, 'Breakfast', 'Whole Grain Cereal with Canned Peaches',
 'A bowl of whole grain cereal served with canned peach slices and a small glass of milk.',
 250, 9.0, 46.8, 2.0, 5.6, 244.0, 252.0, 7.6),

(1, 2, 'Lunch', 'Leftover Pork with Stir-Fried Vegetables and Brown Rice',
 'Leftover baked pork served alongside stir-fried mixed vegetables and brown rice, with a fresh orange and yogurt.',
 45, 1.2, 7.9, 1.3, 1.4, 233.0, 26.0, 0.3),

(1, 2, 'Dinner', 'Hamburger Patty on Whole Wheat Bun with Salad and Homemade Fries',
 'A grilled hamburger patty served on a whole wheat bun with tomato, lettuce, and onion, accompanied by a tossed salad and oven-baked potato fries with milk.',
 284, 6.4, 55.4, 4.8, 5.1, 604.0, 39.0, 2.5),

(1, 2, 'Snack', 'Bran Muffin with Milk',
 'A fibre-rich bran muffin served with a glass of milk.',
 155, 4.4, 31.1, 3.5, 5.2, 229.0, 132.0, 3.4),

(1, 3, 'Breakfast', 'Poached Egg on Whole Wheat Toast with Bran Muffin',
 'A gently poached egg served on whole wheat toast alongside a bran muffin, a fresh apple, and a glass of milk.',
 74, 6.3, 0.4, 4.9, 0.0, 147.0, 27.0, 0.9),

(1, 3, 'Lunch', 'Mixed Bean Salad with Scone and Carrot Sticks',
 'A chilled salad of mixed legumes dressed with vinegar and oil, served with a freshly baked scone, carrot sticks, a banana, and milk.',
 337, 14.5, 50.7, 9.6, 12.0, 11.6, 84.0, 4.4),

(1, 3, 'Dinner', 'Baked Fish Fillet with Homemade Fries and Steamed Broccoli',
 'A baked fish fillet served with oven-baked potato fries, steamed broccoli, and a whole wheat dinner roll.',
 550, 35.1, 80.4, 11.0, 10.9, 1106.0, 138.0, 4.8),

(1, 3, 'Snack', 'Bran Flakes with Canned Peaches and Milk',
 'A bowl of bran flake cereal served with canned peach slices and milk.',
 239, 8.7, 47.6, 1.0, 7.6, 373.0, 176.0, 8.3),

(1, 4, 'Breakfast', 'Whole Grain Bagel with Peanut Butter and Grapefruit',
 'A toasted whole grain bagel spread with peanut butter, served with a fresh grapefruit and a glass of milk.',
 545, 25.0, 81.0, 12.3, 7.5, 631.0, 392.0, 3.5),

(1, 4, 'Lunch', 'Salmon Salad in Pita with Tomato Soup',
 'Canned salmon mixed with light mayonnaise and green onion, served in a whole wheat pita with lettuce and tomato, alongside tomato soup made with milk and carrot sticks.',
 175, 13.5, 3.1, 11.8, 0.3, 444.0, 188.0, 0.9),

(1, 4, 'Dinner', 'Whole Wheat Spaghetti with Homestyle Tomato Sauce',
 'Whole wheat spaghetti topped with a herb-seasoned homemade tomato sauce and grated cheddar cheese, served with a tossed green salad and a fresh apple.',
 82, 1.8, 12.3, 3.7, 2.2, 459.0, 53.0, 2.1),

(1, 4, 'Snack', 'Mixed Bean Salad with Whole Wheat Toast',
 'A serving of mixed bean salad paired with a slice of whole wheat toast.',
 337, 14.5, 50.7, 9.6, 12.0, 11.6, 84.0, 4.4),

(1, 5, 'Breakfast', 'Whole Grain Cereal with Toast and Banana',
 'A bowl of whole grain cereal with a slice of whole wheat toast, a fresh banana, and a small glass of milk.',
 392, 13.6, 73.8, 3.4, 9.0, 404.0, 281.0, 8.7),

(1, 5, 'Lunch', 'Minestrone Soup with Toast and Cheese',
 'A bowl of minestrone soup served with whole wheat toast, a slice of cheddar cheese, tomato slices, canned fruit cocktail, and a glass of milk.',
 274, 18.9, 46.2, 2.5, 12.4, 775.0, 119.0, 5.9),

(1, 5, 'Dinner', 'Meatloaf with Steamed Vegetables and Coleslaw',
 'A baked beef meatloaf served with steamed carrots, broccoli, and yellow wax beans, alongside coleslaw and a whole wheat dinner roll with milk.',
 300, 29.5, 19.2, 11.1, 1.9, 498.0, 68.0, 3.6),

(1, 5, 'Snack', 'Banana with Orange and Cheese on Crackers',
 'A light snack of a fresh banana, orange, and cheddar cheese served with whole wheat crackers.',
 379, 11.6, 54.8, 12.2, 7.6, 396.0, 277.0, 1.6),

(1, 6, 'Breakfast', 'Whole Wheat English Muffin with Peanut Butter and Grapefruit',
 'A toasted whole wheat English muffin spread with peanut butter, accompanied by a fresh grapefruit and a small glass of milk.',
 383, 16.1, 51.5, 11.6, 7.1, 397.0, 311.0, 2.5),

(1, 6, 'Lunch', 'Whole Grain Bagel with Salmon Salad and Coleslaw',
 'A toasted whole grain bagel filled with salmon salad, lettuce, and tomato, served with coleslaw, a banana, and a glass of milk.',
 175, 13.5, 3.1, 11.8, 0.3, 444.0, 188.0, 0.9),

(1, 6, 'Dinner', 'Bean Burritos with Mixed Vegetables',
 'Kidney bean burritos baked in whole wheat tortillas with cheese, green onion, salsa, and sour cream, served alongside steamed mixed vegetables and canned fruit cocktail.',
 417, 21.6, 59.3, 11.4, 12.3, 682.0, 227.0, 6.0),

(1, 6, 'Snack', 'Nuts with Oatmeal Cookies and Orange',
 'A small handful of unsalted nuts with two oatmeal cookies and a fresh orange.',
 320, 6.5, 33.6, 17.4, 5.3, 99.0, 80.0, 1.5),

(1, 7, 'Breakfast', 'Scrambled Egg on Toast with Orange',
 'A lightly scrambled egg served on whole wheat toast with a fresh orange and a small glass of milk.',
 110, 6.5, 1.0, 8.8, 0.1, 590.0, 38.0, 0.7),

(1, 7, 'Lunch', 'Bean Burrito with Tomato Soup and Carrot Sticks',
 'A kidney bean burrito with sour cream and salsa, served alongside tomato soup made with milk, carrot sticks, and a fresh apple.',
 417, 21.6, 59.3, 11.4, 12.3, 682.0, 227.0, 6.0),

(1, 7, 'Dinner', 'Mini Whole Wheat Pizza with Tossed Salad',
 'Whole wheat English muffin mini pizzas topped with homemade tomato sauce, green onion, mushrooms, and mozzarella cheese, served with a large tossed salad, a banana, and a bran muffin with milk.',
 253, 13.4, 33.9, 8.6, 5.9, 879.0, 354.0, 2.6),

(1, 7, 'Snack', 'Banana Bread with Canned Peaches and Nuts',
 'A slice of homemade banana bread served with canned peach slices and a small portion of unsalted nuts.',
 237, 3.2, 32.1, 10.7, 1.5, 165.0, 9.0, 0.9);


-- Week 2

INSERT INTO nutrition_plan (week_number, day_number, meal_type, meal_name, description, calories, protein_g, carbohydrates_g, fat_g, fibre_g, sodium_mg, calcium_mg, iron_mg) VALUES

(2, 1, 'Breakfast', 'Pancakes with Banana and Milk',
 'Fluffy pancakes served with syrup, a fresh banana, and a small glass of milk.',
 476, 12.1, 94.2, 5.2, 3.9, 584.0, 281.0, 2.3),

(2, 1, 'Lunch', 'Split Pea Soup with Bannock and Tossed Salad',
 'A thick split pea soup served with a piece of freshly baked bannock, a tossed green salad with dressing, a fresh apple, and milk.',
 101, 7.4, 15.9, 1.0, 2.5, 476.0, 28.5, 1.1),

(2, 1, 'Dinner', 'Baked Chicken Thighs with Brown Rice and Coleslaw',
 'Oven-baked chicken thighs served with brown rice, steamed carrots, coleslaw, grapefruit, and a small glass of milk.',
 125, 0.5, 0.3, 13.8, 0.1, 475.0, 2.0, 0.1),

(2, 1, 'Snack', 'Banana Bread with Canned Pears and Milk',
 'A slice of banana bread served with canned pear slices and a glass of milk.',
 237, 3.2, 32.1, 10.7, 1.5, 165.0, 9.0, 0.9),

(2, 2, 'Breakfast', 'Bran Flakes with Banana Bread and Grapefruit',
 'A bowl of bran flake cereal served with a slice of banana bread, a fresh grapefruit, and a glass of milk.',
 237, 3.2, 32.1, 10.7, 1.5, 165.0, 9.0, 0.9),

(2, 2, 'Lunch', 'Chicken Salad Pita with Cream of Mushroom Soup',
 'Chopped cooked chicken mixed with light mayonnaise and served in a whole wheat pita with lettuce and tomato, alongside cream of mushroom soup made with milk and whole wheat crackers.',
 137, 18.5, 3.6, 4.9, 0.5, 632.0, 16.0, 0.7),

(2, 2, 'Dinner', 'Meatloaf with Baked Potato and Mixed Bean Salad',
 'A slice of baked meatloaf served with a baked potato, mixed bean salad, steamed broccoli, a banana, and milk.',
 300, 29.5, 19.2, 11.1, 1.9, 498.0, 68.0, 3.6),

(2, 2, 'Snack', 'Bran Muffin with Dried Apricots and Milk',
 'A bran muffin served with a few dried apricots and a glass of milk.',
 155, 4.4, 31.1, 3.5, 5.2, 229.0, 132.0, 3.4),

(2, 3, 'Breakfast', 'Oatmeal with Bannock and Banana',
 'A warm bowl of oatmeal served alongside a piece of bannock, a fresh banana, and a glass of milk.',
 129, 2.6, 16.6, 6.0, 1.6, 276.0, 52.0, 1.0),

(2, 3, 'Lunch', 'Ham and Cheese Bagel with Carrot Sticks',
 'A whole grain bagel filled with shaved deli ham and cheddar cheese with lettuce and tomato, served with carrot sticks, a fresh orange, and milk.',
 631, 39.6, 80.3, 15.4, 8.0, 1574.0, 632.0, 4.1),

(2, 3, 'Dinner', 'Grilled Chicken Breast with Baked Potato and Stir-Fried Vegetables',
 'A grilled chicken breast served with a baked potato, stir-fried mixed vegetables, a whole wheat dinner roll, and milk.',
 161, 4.3, 36.6, 0.2, 3.8, 17.0, 26.0, 1.9),

(2, 3, 'Snack', 'Banana Bread with Canned Pears',
 'A slice of banana bread paired with canned pear slices.',
 237, 3.2, 32.1, 10.7, 1.5, 165.0, 9.0, 0.9),

(2, 4, 'Breakfast', 'Whole Wheat English Muffin with Hard Cooked Egg',
 'A toasted whole wheat English muffin served alongside a hard cooked egg, a fresh apple, and a glass of milk.',
 78, 6.3, 0.6, 5.3, 0.0, 62.0, 25.0, 0.6),

(2, 4, 'Lunch', 'Split Pea Soup with Dinner Roll and Carrot Sticks',
 'A bowl of split pea soup served with a whole wheat dinner roll, carrot sticks, a banana, and a glass of milk.',
 101, 7.4, 15.9, 1.0, 2.5, 476.0, 28.5, 1.1),

(2, 4, 'Dinner', 'Tuna Casserole with Steamed Broccoli and Carrots',
 'A baked tuna and whole wheat noodle casserole with peas and cream of mushroom sauce, served alongside steamed broccoli and carrots, whole wheat bread, and a fresh orange with milk.',
 312, 25.2, 27.5, 11.4, 5.0, 820.0, 144.0, 3.3),

(2, 4, 'Snack', 'Bran Flakes with Dried Apricots and Milk',
 'A bowl of bran flake cereal with a few dried apricots and a glass of milk.',
 277, 13.3, 52.1, 1.1, 8.0, 429.0, 335.0, 8.6),

(2, 5, 'Breakfast', 'Bannock with Peanut Butter and Orange',
 'Two pieces of freshly baked bannock spread with peanut butter, served with a fresh orange and a glass of milk.',
 129, 2.6, 16.6, 6.0, 1.6, 276.0, 52.0, 1.0),

(2, 5, 'Lunch', 'Grilled Cheese Sandwich with Coleslaw and Canned Pears',
 'A grilled cheese sandwich on whole wheat bread served with coleslaw and canned pear slices.',
 80, 0.8, 4.7, 6.9, 1.3, 21.0, 27.0, 0.4),

(2, 5, 'Dinner', 'Baked Pork Chop with Baked Potato and Green Peas',
 'A baked pork chop served with a baked potato, steamed green peas, a whole wheat dinner roll, canned pineapple, and yogurt.',
 290, 21.4, 19.5, 14.1, 0.7, 693.0, 43.0, 1.1),

(2, 5, 'Snack', 'Nuts with Whole Wheat Toast and Banana',
 'A small handful of unsalted nuts served with a slice of whole wheat toast and a fresh banana with milk.',
 504, 19.3, 57.2, 21.7, 7.2, 283.0, 382.0, 2.5),

(2, 6, 'Breakfast', 'Poached Egg on Toast with Canned Pineapple',
 'A poached egg served on two slices of whole wheat toast with canned pineapple and a glass of milk.',
 74, 6.3, 0.4, 4.9, 0.0, 147.0, 27.0, 0.9),

(2, 6, 'Lunch', 'Tuna Casserole with Apple',
 'A serving of baked tuna and noodle casserole with steamed broccoli and carrots, accompanied by a fresh apple.',
 312, 25.2, 27.5, 11.4, 5.0, 820.0, 144.0, 3.3),

(2, 6, 'Dinner', 'Stir-Fried Vegetables with Leftover Pork and Brown Rice',
 'Stir-fried mixed vegetables tossed with leftover pork served over brown rice with a glass of milk.',
 45, 1.2, 7.9, 1.3, 1.4, 233.0, 26.0, 0.3),

(2, 6, 'Snack', 'Apple with Nuts',
 'A fresh apple served alongside a small portion of unsalted nuts.',
 294, 6.0, 22.6, 20.3, 5.7, 6.0, 45.0, 1.2),

(2, 7, 'Breakfast', 'Whole Grain Cereal with Banana Bread and Orange',
 'A bowl of whole grain cereal served with a slice of banana bread, a fresh orange, and a glass of milk.',
 237, 3.2, 32.1, 10.7, 1.5, 165.0, 9.0, 0.9),

(2, 7, 'Lunch', 'Split Pea Soup with Crackers and Tossed Salad',
 'A bowl of split pea soup served with whole wheat crackers, a tossed green salad, canned pineapple, and yogurt.',
 101, 7.4, 15.9, 1.0, 2.5, 476.0, 28.5, 1.1),

(2, 7, 'Dinner', 'Hamburger Patty on Whole Wheat Bun with Apple Crisp',
 'A grilled hamburger patty on a whole wheat bun served alongside homemade oven-baked potato fries, apple crisp with oat topping, and frozen yogurt.',
 394, 4.5, 67.9, 13.7, 6.2, 176.0, 57.0, 2.1),

(2, 7, 'Snack', 'Milk with Apple and Nuts',
 'A glass of milk served with a fresh apple and a small portion of unsalted nuts.',
 382, 14.6, 34.8, 20.5, 5.7, 120.0, 355.0, 1.3);


-- Week 3

INSERT INTO nutrition_plan (week_number, day_number, meal_type, meal_name, description, calories, protein_g, carbohydrates_g, fat_g, fibre_g, sodium_mg, calcium_mg, iron_mg) VALUES

(3, 1, 'Breakfast', 'Whole Grain Bagel with Cheese and Apple',
 'A toasted whole grain bagel served with a slice of cheddar cheese, a fresh apple, and a small glass of milk.',
 490, 21.3, 74.7, 11.1, 6.8, 669.0, 412.0, 3.3),

(3, 1, 'Lunch', 'Lentil Soup with Bannock and Orange',
 'A thick lentil soup seasoned with garlic and cumin, served with a piece of bannock, oatmeal cookies, and a fresh orange with milk.',
 384, 28.3, 46.4, 10.0, 8.1, 1126.0, 69.2, 7.4),

(3, 1, 'Dinner', 'Baked Chicken Thigh with Baked Potato and Green Peas',
 'An oven-baked chicken thigh served with a baked potato, steamed green peas, and whole wheat bread, followed by canned peach slices.',
 125, 0.5, 0.3, 13.8, 0.1, 475.0, 2.0, 0.1),

(3, 1, 'Snack', 'Whole Grain Cereal with Banana and Milk',
 'A bowl of whole grain cereal served with a fresh banana and a glass of milk.',
 340, 14.1, 62.7, 2.3, 6.9, 298.0, 408.0, 7.6),

(3, 2, 'Breakfast', 'Bannock with Scrambled Eggs and Orange',
 'A piece of freshly baked bannock served alongside two scrambled eggs, a fresh orange, and a glass of milk.',
 110, 6.5, 1.0, 8.8, 0.1, 590.0, 38.0, 0.7),

(3, 2, 'Lunch', 'Chicken Sandwich on Whole Wheat Bread with Carrot and Celery Sticks',
 'Leftover chicken served in a sandwich on whole wheat bread with lettuce and tomato, alongside carrot and celery sticks and a fresh banana.',
 137, 18.5, 3.6, 4.9, 0.5, 632.0, 16.0, 0.7),

(3, 2, 'Dinner', 'Whole Wheat Spaghetti with Homestyle Tomato Sauce and Apple Crisp',
 'Whole wheat spaghetti topped with herb-seasoned homemade tomato sauce and a tossed salad, followed by apple crisp with a glass of milk.',
 82, 1.8, 12.3, 3.7, 2.2, 459.0, 53.0, 2.1),

(3, 2, 'Snack', 'Bran Muffin with Apple and Yogurt',
 'A bran muffin served with a fresh apple and a serving of yogurt.',
 155, 4.4, 31.1, 3.5, 5.2, 229.0, 132.0, 3.4),

(3, 3, 'Breakfast', 'Oatmeal with Banana Bread and Grapefruit',
 'A warm bowl of oatmeal served with a slice of banana bread, a fresh grapefruit, and a glass of milk.',
 237, 3.2, 32.1, 10.7, 1.5, 165.0, 9.0, 0.9),

(3, 3, 'Lunch', 'Chicken and Vegetable Soup with Crackers and Bran Muffin',
 'A wholesome chicken and vegetable soup served with whole wheat crackers, a slice of cheddar cheese, a bran muffin, apple crisp, and milk.',
 143, 7.2, 26.5, 1.2, 3.8, 355.0, 32.0, 1.9),

(3, 3, 'Dinner', 'Baked Fish Fillet with Brown Rice and Mixed Vegetables',
 'A baked fish fillet served over brown rice with steamed mixed vegetables and a fresh orange.',
 456, 31.0, 66.2, 6.1, 11.5, 339.0, 120.0, 2.7),

(3, 3, 'Snack', 'Cantaloupe with Nuts and Milk',
 'A serving of fresh cantaloupe alongside a small portion of unsalted nuts and a glass of milk.',
 329, 14.8, 22.0, 20.4, 3.2, 130.0, 356.0, 1.3),

(3, 4, 'Breakfast', 'Scone with Peanut Butter and Cantaloupe',
 'A freshly baked scone spread with peanut butter, served with a portion of fresh cantaloupe and a small glass of milk.',
 129, 3.7, 18.4, 4.8, 1.6, 390.0, 63.0, 1.0),

(3, 4, 'Lunch', 'Tuna Salad Pita with Cucumber and Banana',
 'Canned tuna mixed with light mayonnaise and green onion, served in a whole wheat pita with lettuce, tomato, and cucumber slices, alongside a banana and milk.',
 150, 19.0, 3.6, 6.1, 0.5, 414.0, 24.0, 1.1),

(3, 4, 'Dinner', 'Baked Beans on Whole Wheat Toast with Carrot and Cucumber Sticks',
 'Homemade baked white beans in a molasses and ketchup sauce served on toasted whole wheat bread, with carrot and cucumber sticks and oatmeal cookies.',
 363, 20.0, 62.1, 4.8, 10.7, 730.0, 425.0, 12.8),

(3, 4, 'Snack', 'Canned Pears with Milk',
 'A serving of canned pear slices with a glass of milk.',
 150, 9.0, 26.6, 0.3, 2.2, 119.0, 316.0, 0.3),

(3, 5, 'Breakfast', 'Bannock with Peanut Butter and Grapefruit',
 'Two pieces of bannock spread with peanut butter, served with a fresh grapefruit and a small glass of milk.',
 129, 2.6, 16.6, 6.0, 1.6, 276.0, 52.0, 1.0),

(3, 5, 'Lunch', 'Lentil Soup with Scones and Tossed Salad',
 'A bowl of lentil soup served with two freshly baked scones, a tossed green salad with dressing, cantaloupe, and milk.',
 384, 28.3, 46.4, 10.0, 8.1, 1126.0, 69.2, 7.4),

(3, 5, 'Dinner', 'Beef Stroganoff with Mixed Vegetables and Whole Wheat Bread',
 'A baked beef and whole wheat noodle stroganoff with peas, cream of mushroom sauce, and a breadcrumb topping, served with steamed mixed vegetables, whole wheat bread, and canned pear slices with milk.',
 440, 23.8, 55.0, 13.5, 3.6, 558.0, 91.0, 5.0),

(3, 5, 'Snack', 'Whole Wheat Toast with Cottage Cheese and Fruit Cocktail',
 'A slice of whole wheat toast served with cottage cheese and canned fruit cocktail.',
 266, 18.9, 33.2, 6.1, 3.1, 541.0, 128.0, 1.6),

(3, 6, 'Breakfast', 'Whole Wheat English Muffin with Poached Egg and Cantaloupe',
 'A toasted whole wheat English muffin served with a poached egg, a portion of fresh cantaloupe, and yogurt.',
 74, 6.3, 0.4, 4.9, 0.0, 147.0, 27.0, 0.9),

(3, 6, 'Lunch', 'Toasted Whole Grain Bagel with Cottage Cheese and Carrot Sticks',
 'A toasted whole grain bagel served with cottage cheese, carrot and celery sticks, and canned pear slices.',
 594, 40.7, 78.3, 12.0, 8.1, 1276.0, 273.0, 3.7),

(3, 6, 'Dinner', 'Bean Burrito with Brown Rice and Tossed Salad',
 'A kidney bean burrito with sour cream and salsa served alongside brown rice, a tossed green salad, and canned fruit cocktail with milk.',
 417, 21.6, 59.3, 11.4, 12.3, 682.0, 227.0, 6.0),

(3, 6, 'Snack', 'Cheddar Cheese with Apple and Nuts',
 'A small portion of cheddar cheese served with a fresh apple and a handful of unsalted nuts.',
 304, 10.1, 20.8, 20.3, 4.7, 174.0, 237.0, 1.0),

(3, 7, 'Breakfast', 'Whole Wheat Toast with Scrambled Eggs and Banana',
 'Two scrambled eggs served on whole wheat toast alongside a fresh banana and a glass of milk.',
 110, 6.5, 1.0, 8.8, 0.1, 590.0, 38.0, 0.7),

(3, 7, 'Lunch', 'Tuna Salad Sandwich with Cucumber and Orange',
 'Canned tuna salad served in a sandwich on two slices of whole wheat bread with lettuce, tomato, and cucumber, alongside a fresh orange and yogurt.',
 150, 19.0, 3.6, 6.1, 0.5, 414.0, 24.0, 1.1),

(3, 7, 'Dinner', 'Vegetable Lasagna with Tossed Salad and Garlic Toast',
 'A baked vegetable lasagna with cottage cheese, spinach, mushrooms, and mozzarella cheese, served with a tossed green salad, garlic toast, and milk.',
 423, 22.7, 54.4, 14.0, 5.9, 971.0, 317.0, 5.8),

(3, 7, 'Snack', 'Bran Muffin with Dried Apricots',
 'A bran muffin served alongside a few dried apricots.',
 155, 4.4, 31.1, 3.5, 5.2, 229.0, 132.0, 3.4);


-- Week 4

INSERT INTO nutrition_plan (week_number, day_number, meal_type, meal_name, description, calories, protein_g, carbohydrates_g, fat_g, fibre_g, sodium_mg, calcium_mg, iron_mg) VALUES

(4, 1, 'Breakfast', 'French Toast with Grapefruit and Milk',
 'Whole wheat French toast served with syrup, a fresh grapefruit, and a glass of milk.',
 335, 14.6, 35.2, 15.5, 4.8, 552.0, 137.0, 2.9),

(4, 1, 'Lunch', 'Chunky Vegetable Soup with Bean Burrito and Banana Bread',
 'A hearty chunky vegetable and kidney bean soup served alongside a bean burrito and a slice of banana bread.',
 333, 20.4, 54.5, 4.9, 13.7, 827.0, 142.0, 7.1),

(4, 1, 'Dinner', 'Baked Pork Chop with Baked Potato and Roast Carrots',
 'A baked pork chop served with a baked potato, roasted carrots, a slice of whole wheat bread, a tossed green salad, and canned peach slices.',
 290, 21.4, 19.5, 14.1, 0.7, 693.0, 43.0, 1.1),

(4, 1, 'Snack', 'Cantaloupe with Yogurt',
 'A portion of fresh cantaloupe served with a serving of yogurt.',
 141, 10.0, 19.6, 3.2, 0.8, 129.0, 324.0, 0.3),

(4, 2, 'Breakfast', 'Whole Grain Bagel with Cheese and Tomato',
 'A toasted whole grain bagel served with a slice of cheddar cheese, diced tomato, and a small glass of milk.',
 426, 21.6, 59.1, 11.0, 4.5, 672.0, 413.0, 3.3),

(4, 2, 'Lunch', 'Pork Sandwich on Whole Wheat Bread with Coleslaw',
 'Leftover pork served in a sandwich on two slices of whole wheat bread, alongside coleslaw and canned pineapple.',
 80, 0.8, 4.7, 6.9, 1.3, 21.0, 27.0, 0.4),

(4, 2, 'Dinner', 'Vegetable Lasagna with Garlic Toast and Mixed Vegetables',
 'A baked vegetable lasagna served with garlic toast, steamed mixed vegetables, a fresh orange, and yogurt.',
 423, 22.7, 54.4, 14.0, 5.9, 971.0, 317.0, 5.8),

(4, 2, 'Snack', 'Apple with Nuts',
 'A fresh apple served with a small portion of unsalted nuts.',
 294, 6.0, 22.6, 20.3, 5.7, 6.0, 45.0, 1.2),

(4, 3, 'Breakfast', 'Whole Grain Cereal with Bannock and Orange',
 'A bowl of whole grain cereal served with a piece of bannock, a fresh orange, and a small glass of milk.',
 129, 2.6, 16.6, 6.0, 1.6, 276.0, 52.0, 1.0),

(4, 3, 'Lunch', 'Chunky Vegetable Soup with Bran Muffins and Cottage Cheese',
 'A bowl of chunky vegetable soup served with two bran muffins, cottage cheese, carrot sticks, and canned pineapple.',
 333, 20.4, 54.5, 4.9, 13.7, 827.0, 142.0, 7.1),

(4, 3, 'Dinner', 'Baked Fish Fillet with Brown Rice and Stir-Fried Vegetables',
 'A baked fish fillet served with brown rice and stir-fried mixed vegetables, followed by frozen yogurt and milk.',
 45, 1.2, 7.9, 1.3, 1.4, 233.0, 26.0, 0.3),

(4, 3, 'Snack', 'Bran Flakes with Banana and Milk',
 'A bowl of bran flake cereal served with a fresh banana and a glass of milk.',
 329, 13.8, 63.5, 1.3, 8.9, 427.0, 332.0, 8.3),

(4, 4, 'Breakfast', 'Whole Wheat English Muffin with Peanut Butter and Yogurt',
 'A toasted whole wheat English muffin spread with peanut butter, served with a fresh grapefruit and yogurt.',
 455, 21.2, 59.8, 14.5, 7.1, 458.0, 472.0, 2.5),

(4, 4, 'Lunch', 'Egg Salad Sandwich on Whole Wheat Bread with Coleslaw',
 'A sandwich of hard cooked egg salad on two slices of whole wheat bread, served with coleslaw and a glass of milk alongside unsalted nuts.',
 201, 12.8, 4.2, 14.4, 0.3, 713.0, 58.0, 1.4),

(4, 4, 'Dinner', 'Baked Chicken Thigh with Baked Potato and Steamed Broccoli and Carrots',
 'An oven-baked chicken thigh served with a baked potato, steamed broccoli, steamed carrots, and a fresh orange.',
 125, 0.5, 0.3, 13.8, 0.1, 475.0, 2.0, 0.1),

(4, 4, 'Snack', 'Nuts with Bran Muffin and Banana',
 'A small portion of unsalted nuts served with a bran muffin and a fresh banana.',
 155, 4.4, 31.1, 3.5, 5.2, 229.0, 132.0, 3.4),

(4, 5, 'Breakfast', 'Bran Flakes with Cheese and Apple',
 'A bowl of bran flake cereal served with a slice of cheddar cheese, a fresh apple, and a glass of milk.',
 405, 19.3, 58.5, 9.9, 9.5, 597.0, 541.0, 8.4),

(4, 5, 'Lunch', 'Chunky Vegetable Soup with Chicken Salad Sandwich and Canned Peaches',
 'A bowl of chunky vegetable and kidney bean soup served with a chicken salad sandwich on whole wheat bread, canned peach slices, and oatmeal cookies.',
 333, 20.4, 54.5, 4.9, 13.7, 827.0, 142.0, 7.1),

(4, 5, 'Dinner', 'Beef and Macaroni Casserole with Tossed Salad and Garlic Toast',
 'A baked beef and whole wheat macaroni casserole in a tomato and herb sauce, served with a tossed green salad, garlic toast, steamed green peas, and frozen yogurt.',
 309, 23.1, 43.4, 6.1, 5.4, 715.0, 79.0, 4.8),

(4, 5, 'Snack', 'Dried Apricots with Yogurt and Orange',
 'A few dried apricots served with a portion of yogurt and a fresh orange.',
 226, 11.3, 37.8, 3.3, 4.7, 122.0, 371.0, 0.9),

(4, 6, 'Breakfast', 'Oatmeal with Bran Muffin and Orange',
 'A warm bowl of oatmeal served with a bran muffin, a fresh orange, and a glass of milk.',
 155, 4.4, 31.1, 3.5, 5.2, 229.0, 132.0, 3.4),

(4, 6, 'Lunch', 'Tossed Salad with Canned Salmon and Whole Wheat Bread',
 'A large tossed green salad served with canned salmon and two slices of whole wheat bread, alongside a fresh banana.',
 34, 2.3, 7.0, 0.4, 2.8, 12.0, 41.0, 1.1),

(4, 6, 'Dinner', 'Baked Beans with Garlic Toast and Carrot and Cucumber Sticks',
 'Homemade baked beans served on garlic toast alongside carrot and cucumber sticks, canned peach slices, and a glass of milk.',
 363, 20.0, 62.1, 4.8, 10.7, 730.0, 425.0, 12.8),

(4, 6, 'Snack', 'Apple with Oatmeal Cookies and Milk',
 'A fresh apple served with two oatmeal cookies and a glass of milk.',
 304, 11.1, 49.6, 6.3, 4.3, 210.0, 329.0, 1.0),

(4, 7, 'Breakfast', 'Whole Wheat English Muffin with Peanut Butter and Canned Pineapple',
 'A toasted whole wheat English muffin spread with peanut butter, served with canned pineapple and a glass of milk.',
 429, 19.5, 60.2, 11.6, 5.7, 455.0, 452.0, 2.6),

(4, 7, 'Lunch', 'Salmon Salad Sandwich on Whole Wheat Bread with Coleslaw',
 'Canned salmon mixed with light mayonnaise served in a sandwich on whole wheat bread, alongside coleslaw and a fresh apple.',
 175, 13.5, 3.1, 11.8, 0.3, 444.0, 188.0, 0.9),

(4, 7, 'Dinner', 'Beef and Macaroni Casserole with Tossed Salad and Mixed Vegetables',
 'A baked beef and whole wheat macaroni casserole served with a tossed green salad, steamed mixed vegetables, and a small glass of milk.',
 309, 23.1, 43.4, 6.1, 5.4, 715.0, 79.0, 4.8),

(4, 7, 'Snack', 'Whole Grain Cereal with Banana and Milk',
 'A bowl of whole grain cereal served with a fresh banana and a glass of milk.',
 340, 14.1, 62.7, 2.3, 6.9, 298.0, 408.0, 7.6);""")
               
               
cursor.execute("SELECT * FROM nutrition_plan;")
rows = cursor.fetchall()

for row in rows:
    print(row)


cursor.close()
connection.close()
