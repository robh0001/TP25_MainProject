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

cursor.execute("DROP TABLE IF EXISTS exercise_plan")

connection.commit()


cursor.execute("""
CREATE TABLE exercise_plan (
    id SERIAL PRIMARY KEY,
    week_number INT NOT NULL,
    letter CHAR(1) NOT NULL,
    exercise_name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL
);
""")
connection.commit()


cursor.execute("""
-- Week 1

INSERT INTO exercise_plan (week_number, letter, exercise_name, description) VALUES
(1, 'A', 'Animal Walk',       'Move across the floor by crawling on all fours in a bear-like position, keeping the body low and the limbs engaged.'),
(1, 'C', 'Crab Walk',         'Position the body face-up with hands and feet on the ground, then move sideways by coordinating the arms and legs together.'),
(1, 'E', 'Elephant Stomp',    'Walk with deliberate, heavy steps while lifting the knees high with each stride to mimic the movement of an elephant.'),
(1, 'G', 'Gorilla Shuffle',   'Lower the body into a crouched position and move from side to side while keeping the posture low throughout the movement.'),
(1, 'I', 'Inchworm',          'Begin in a standing position, walk the hands forward along the ground until the body is extended, then walk the feet back in towards the hands.'),
(1, 'K', 'Kangaroo Hops',     'Perform small jumps on the spot while holding both hands out in front of the body, mimicking the movement of a kangaroo.'),
(1, 'M', 'Mountain Climbers', 'Start in a plank position and alternate driving each knee towards the chest in a controlled and continuous motion.'),
(1, 'O', 'Obstacle Course',   'Set up a series of simple physical challenges either indoors or outdoors and move through each one in sequence.'),
(1, 'Q', 'Quick Feet',        'Run on the spot as rapidly as possible, focusing on fast and light foot movements close to the ground.'),
(1, 'S', 'Star Jumps',        'Jump upward while simultaneously extending the arms and legs outward into a star shape, then return to a standing position on landing.'),
(1, 'U', 'Underwater Swim',   'Remain standing and simulate swimming strokes with both arms as though moving through water.'),
(1, 'W', 'Windmill',          'Stand with the feet apart and reach each hand down toward the opposite foot in an alternating and continuous windmill motion.'),
(1, 'Y', 'Yoji Pose',         'Hold a simple yoga-inspired balancing pose such as a tree pose, focusing on stillness and controlled breathing.');


-- Week 2

INSERT INTO exercise_plan (week_number, letter, exercise_name, description) VALUES
(2, 'B', 'Balloon Bounce',    'Keep a balloon in the air by tapping it upward repeatedly using the hands, ensuring it does not touch the ground.'),
(2, 'D', 'Duck Walk',         'Lower into a squat position and walk forward while maintaining the crouched posture, waddling from side to side with each step.'),
(2, 'F', 'Frog Jumps',        'Squat down low and then leap forward as far as possible, landing softly before returning to the squat position to repeat.'),
(2, 'H', 'High Knees',        'Run or walk on the spot while lifting each knee as high as possible with every step to increase effort and engagement.'),
(2, 'J', 'Jumping Jacks',     'Begin with feet together and arms at the sides, then jump to separate the feet while raising the arms overhead, before returning to the starting position.'),
(2, 'L', 'Lizard Crawls',     'Crawl forward across the floor in a low position, keeping the body close to the ground throughout the movement in a lizard-like manner.'),
(2, 'N', 'Ninja Kicks',       'Stand in place and perform quick, controlled front kicks with alternating legs, maintaining balance and a stable upright posture.'),
(2, 'P', 'Penguin Waddle',    'Walk with the heels together and the toes pointed outward, taking small waddling steps to imitate the movement of a penguin.'),
(2, 'R', 'Rocket Jumps',      'Crouch down low to the ground and then jump upward with full force, reaching both arms toward the sky at the peak of the jump.'),
(2, 'T', 'Tummy Twists',      'Stand or sit upright and rotate the torso from side to side in a controlled twisting motion, engaging the core throughout.'),
(2, 'V', 'Volcano Jump',      'Start in a low squat and then explode upward into a jump, mimicking the burst of a volcanic eruption before landing and resetting.'),
(2, 'X', 'X-Jumps',           'Jump upward while crossing the arms and legs in front of the body at the peak of the jump, then open them back out on landing.'),
(2, 'Z', 'Zig Zag',           'Run or move forward in a zig zag pattern, changing direction at each point to improve agility and coordination.');


-- Week 3

INSERT INTO exercise_plan (week_number, letter, exercise_name, description) VALUES
(3, 'A', 'Animal Walk',       'Revisit the bear crawl movement, this time focusing on keeping a steady and controlled pace across a longer distance.'),
(3, 'D', 'Duck Walk',         'Perform the duck walk again but challenge yourself to cover a greater distance or add a turn at each end of the space.'),
(3, 'F', 'Frog Jumps',        'Return to frog jumps with an added focus on jumping as far forward as possible with each leap before resetting into the squat.'),
(3, 'H', 'High Knees',        'Increase the pace of the high knees exercise this week, aiming for a faster rhythm while still lifting each knee to hip height.'),
(3, 'J', 'Jumping Jacks',     'Perform jumping jacks again with increased repetitions, maintaining steady breathing and a consistent rhythm throughout the set.'),
(3, 'K', 'Kangaroo Hops',     'Revisit kangaroo hops and try to cover more ground with each jump, focusing on soft and controlled landings.'),
(3, 'N', 'Ninja Kicks',       'Return to ninja kicks and increase the speed of each alternating kick while maintaining balance and a firm standing position.'),
(3, 'P', 'Penguin Waddle',    'Revisit the penguin waddle and try to complete a longer path or add a slight obstacle to navigate around while waddling.'),
(3, 'R', 'Rocket Jumps',      'Perform rocket jumps again with a focus on achieving greater height and landing as softly and steadily as possible.'),
(3, 'T', 'Tummy Twists',      'Return to tummy twists and slow the movement down this time, focusing on a deeper and more controlled rotation with each twist.'),
(3, 'V', 'Volcano Jump',      'Revisit the volcano jump and try to hold the low squat position for a brief moment before exploding upward into the jump.'),
(3, 'X', 'X-Jumps',           'Return to X-jumps and focus on achieving a clear and full arm and leg extension at the peak of each jump.'),
(3, 'Z', 'Zig Zag',           'Revisit the zig zag run and tighten the turning points to make each direction change sharper and more challenging.');


-- Week 4

INSERT INTO exercise_plan (week_number, letter, exercise_name, description) VALUES
(4, 'B', 'Balloon Bounce',    'Return to the balloon bounce and challenge yourself to use only one hand, or try keeping two balloons in the air at the same time.'),
(4, 'C', 'Crab Walk',         'Revisit the crab walk and try to cover a longer distance or incorporate a simple obstacle to navigate around while in the crab position.'),
(4, 'E', 'Elephant Stomp',    'Perform elephant stomps again with a focus on exaggerating each high knee lift and making the stomps as deliberate and powerful as possible.'),
(4, 'G', 'Gorilla Shuffle',   'Return to the gorilla shuffle and increase the distance covered side to side, keeping the body low and controlled throughout.'),
(4, 'I', 'Inchworm',          'Revisit the inchworm and try to extend the hands as far forward as possible before walking the feet back in to maximise the stretch.'),
(4, 'L', 'Lizard Crawls',     'Return to lizard crawls and focus on keeping the body as low to the ground as possible while moving at a steady and consistent pace.'),
(4, 'M', 'Mountain Climbers', 'Revisit mountain climbers and increase the pace of the alternating knee drives, focusing on maintaining a stable and level plank position.'),
(4, 'O', 'Obstacle Course',   'Set up a more challenging obstacle course than in Week 1, incorporating more stations or more complex physical challenges to complete.'),
(4, 'Q', 'Quick Feet',        'Return to quick feet and push for a faster pace than previous weeks, focusing on maintaining light and rapid foot contact with the ground.'),
(4, 'S', 'Star Jumps',        'Revisit star jumps and aim for a higher jump with a fuller arm and leg extension at the peak before landing in a controlled manner.'),
(4, 'U', 'Underwater Swim',   'Return to underwater swim and slow the arm strokes down this time, focusing on a full and deliberate range of motion with each stroke.'),
(4, 'W', 'Windmill',          'Revisit the windmill and increase the pace of the alternating reaches, keeping the legs straight and the movement fluid throughout.'),
(4, 'Y', 'Yoji Pose',         'Return to the yoga balance pose and attempt to hold it for a longer duration than in Week 1, focusing on stillness and steady breathing.'); """)

connection.commit()
           
cursor.execute("SELECT * FROM exercise_plan;")
rows = cursor.fetchall()

for row in rows:
    print(row)


cursor.close()
connection.close()
