CREATE TABLE workout_plan (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    week_number     TINYINT UNSIGNED NOT NULL COMMENT 'Week number (1 to 4)',
    day_number      TINYINT UNSIGNED NOT NULL COMMENT 'Day of the week (1 to 7). Days 1 to 4 are active workout days. Days 5, 6, and 7 are scheduled rest days.',
    workout_number  TINYINT UNSIGNED NOT NULL COMMENT 'Workout number (1 to 4)',
    exercise_name   VARCHAR(100)     NOT NULL COMMENT 'Name of the exercise',
    description     TEXT             NOT NULL COMMENT 'Paraphrased description of how to perform the exercise'
);


-- Week 1


INSERT INTO workout_plan (week_number, day_number, workout_number, exercise_name, description) VALUES

-- Day 1 | Workout 1
(1, 1, 1, 'Squats',
 'Stand with feet shoulder-width apart, lower the body by bending the knees until the thighs are parallel to the floor, then return to a standing position. This exercise can be performed with added weight such as dumbbells or a kettlebell to increase resistance.'),

(1, 1, 1, 'Jumping Jacks',
 'Begin in a standing position with feet together and arms at the sides, then jump the feet outward while raising both arms overhead simultaneously, before returning to the starting position in a continuous rhythmic motion.'),

(1, 1, 1, 'Wall Half and Full Press Ups',
 'Place the hands flat against a wall at shoulder height and perform a pressing movement by bending and extending the arms. Beginners may use a closer wall position, while more advanced participants can progress to a full floor press up.'),

(1, 1, 1, 'Butt Kicks',
 'Jog or run on the spot while driving each heel upward toward the glutes in an alternating motion, keeping the core engaged and maintaining an upright posture throughout.'),

(1, 1, 1, 'Alternate Lunges',
 'Step one foot forward into a lunge position so that both knees form approximately right angles, then return to standing and repeat on the opposite side. This exercise can be performed with added weight to increase the level of difficulty.'),

(1, 1, 1, 'High Knees',
 'Run or march on the spot while driving each knee upward toward the chest in an alternating and continuous motion, engaging the core and maintaining an upright posture throughout the exercise.'),

-- Day 2 | Workout 2
(1, 2, 2, 'Stiff Leg Deadlift',
 'Stand upright holding weights at the front of the thighs, then hinge forward at the hips with a slight bend in the knees, lowering the weights toward the floor while keeping the back flat, before returning to the starting position. Added weight such as dumbbells or a kettlebell can be used.'),

(1, 2, 2, 'Ski Jumps',
 'Stand with feet together and perform small lateral jumps from side to side in a continuous motion, keeping the knees soft on landing and swinging the arms to assist momentum, mimicking the movement of a downhill skier.'),

(1, 2, 2, 'Sit Ups',
 'Lie on the back with knees bent and feet flat on the floor, then engage the core and raise the upper body toward the knees before lowering back down in a controlled manner. Added weight held at the chest can be used to increase resistance.'),

(1, 2, 2, 'Mountain Climbers',
 'Begin in a plank position with the arms fully extended, then alternate driving each knee toward the chest in a rapid and continuous motion while keeping the hips level and the core engaged throughout.'),

(1, 2, 2, 'Tricep Dips off a Chair',
 'Sit on the edge of a sturdy chair with both hands gripping the seat beside the hips, then lower the body by bending the elbows to approximately ninety degrees before pushing back up to the starting position, keeping the back close to the chair throughout.'),

(1, 2, 2, 'Skips',
 'Skip on the spot or along a short distance using a skipping rope if one is available, or perform the same jumping and arm rotation motion without a rope. Maintain a light landing on the balls of the feet throughout.'),

-- Day 3 | Workout 3
(1, 3, 3, 'Squat Jumps',
 'Perform a standard squat and at the lowest point explode upward into a jump, landing softly with bent knees before immediately descending into the next repetition. Added weight can be used by more advanced participants to increase intensity.'),

(1, 3, 3, 'Reverse Lunge and Hammer Curl',
 'Step one foot backward into a reverse lunge while simultaneously performing a bicep curl with the arms in a hammer grip, then return to standing and repeat on the opposite side, combining lower and upper body movement in one fluid action.'),

(1, 3, 3, 'Skater Jumps',
 'Leap laterally from one foot to the other in a skating motion, landing softly on the outside foot while swinging the opposite leg behind and reaching the opposite arm toward the landing foot to mimic the movement of a speed skater.'),

(1, 3, 3, 'Glute Bridge Raises',
 'Lie on the back with knees bent and feet flat on the floor, then press through the heels to raise the hips toward the ceiling, squeezing the glutes at the top before lowering back down in a controlled manner. Added weight placed across the hips can be used to increase resistance.'),

(1, 3, 3, 'Burpees',
 'Begin standing, then drop the hands to the floor and jump or step the feet back into a plank position, perform a press up if desired, then jump or step the feet back toward the hands before explosively jumping upward with arms raised overhead.'),

(1, 3, 3, 'Sit Ups',
 'Lie on the back with knees bent and feet flat on the floor, engage the core and raise the upper body toward the knees before lowering back in a controlled manner. This exercise can be performed with added weight held at the chest for increased difficulty.'),

-- Day 4 | Workout 4
(1, 4, 4, 'Jumping Jacks',
 'Begin standing with feet together and arms at the sides, then jump the feet outward while simultaneously raising both arms overhead before returning to the starting position in a continuous and rhythmic motion.'),

(1, 4, 4, 'Stiff Leg Deadlift',
 'Stand upright holding weights at the front of the thighs, hinge forward at the hips with a slight knee bend and lower the weights toward the floor while maintaining a flat back, then return to standing. Added weight can be used to increase resistance.'),

(1, 4, 4, 'High Knees',
 'Run or march on the spot while driving each knee upward toward the chest in an alternating continuous motion, keeping the core tight and maintaining an upright posture throughout the exercise.'),

(1, 4, 4, 'Plank Hold',
 'Hold a forearm or full plank position with the body in a straight line from head to heels, engaging the core, glutes, and legs to maintain the position for the duration of the work interval without allowing the hips to sag or rise.'),

(1, 4, 4, 'Skips',
 'Skip on the spot or along a short distance using a skipping rope if available, or replicate the jumping and arm rotation motion without a rope, landing lightly on the balls of the feet throughout the exercise.'),

(1, 4, 4, 'Curtsy Squats',
 'Stand with feet hip-width apart, then step one foot diagonally behind the opposite leg and lower into a squat position before returning to standing and repeating on the other side. Added weight can be used to increase the level of challenge.');

-- Days 5, 6, 7 | Rest Days
INSERT INTO workout_plan (week_number, day_number, workout_number, exercise_name, description) VALUES
(1, 5, 0, 'Rest Day',
 'This is a scheduled rest day. No structured exercise is required. Allow the body to recover and repair from the preceding four days of training. Light walking or gentle stretching is encouraged if desired.'),
(1, 6, 0, 'Rest Day',
 'This is a scheduled rest day. Focus on rest, adequate hydration, and nutritious food to support recovery. Avoid high intensity activity and allow the muscles time to adapt and strengthen.'),
(1, 7, 0, 'Rest Day',
 'This is the final rest day of the week. Use this day to prepare mentally and physically for the following week of training. Light mobility work or a gentle walk is acceptable if the body feels ready.');


-- Week 2


INSERT INTO workout_plan (week_number, day_number, workout_number, exercise_name, description) VALUES

-- Day 1 | Workout 1
(2, 1, 1, 'Squats',
 'Stand with feet shoulder-width apart and lower the body by bending the knees until the thighs are parallel to the floor, then drive through the heels to return to standing. Focus on maintaining an upright chest and engaged core throughout. Added weight may be used.'),

(2, 1, 1, 'Jumping Jacks',
 'Start standing with feet together and arms at the sides. Jump the feet outward while raising both arms overhead, then return to the starting position in a fluid and continuous motion, maintaining a light landing throughout.'),

(2, 1, 1, 'Wall Half and Full Press Ups',
 'Position the hands against a wall at shoulder height and perform a controlled pressing movement by bending and extending the arms. Progress to a lower surface or full floor press up as fitness improves.'),

(2, 1, 1, 'Butt Kicks',
 'Jog on the spot while kicking each heel upward toward the glutes in an alternating motion. Keep the torso upright and the core engaged, increasing pace as fitness allows.'),

(2, 1, 1, 'Alternate Lunges',
 'Step forward with one foot into a lunge so that both knees reach approximately ninety degrees, then return to standing before repeating on the opposite side. Aim to increase depth and control compared to Week 1. Added weight may be used.'),

(2, 1, 1, 'High Knees',
 'Drive each knee upward toward the chest in an alternating running motion on the spot. Focus on increasing pace and height of the knee drive compared to the previous week while maintaining upright posture.'),

-- Day 2 | Workout 2
(2, 2, 2, 'Stiff Leg Deadlift',
 'Hinge at the hips with a slight bend in the knees and lower weights toward the floor while keeping the back flat and the core tight. Focus on feeling the stretch through the hamstrings before driving the hips forward to return to standing. Added weight may be used.'),

(2, 2, 2, 'Ski Jumps',
 'Perform continuous lateral jumps from side to side with feet together, keeping the knees soft on landing and using the arms to assist momentum. Aim to increase the speed and range of each jump compared to the previous week.'),

(2, 2, 2, 'Sit Ups',
 'Lie on the back with knees bent, engage the core and raise the upper body toward the knees before lowering in a controlled manner. Aim to increase the number of repetitions completed within the work interval this week. Added weight may be used.'),

(2, 2, 2, 'Mountain Climbers',
 'Hold a plank position and alternate driving each knee toward the chest in a rapid motion. Focus on increasing pace while keeping the hips level and the core engaged throughout each repetition.'),

(2, 2, 2, 'Tricep Dips off a Chair',
 'Grip the edge of a sturdy chair and lower the body by bending the elbows to approximately ninety degrees before pushing back up. Aim to increase the range of motion and control compared to Week 1.'),

(2, 2, 2, 'Skips',
 'Skip continuously on the spot or along a short distance with or without a rope. Focus on maintaining a consistent rhythm and increasing duration within the work interval compared to the previous week.'),

-- Day 3 | Workout 3
(2, 3, 3, 'Squat Jumps',
 'Lower into a squat and explode upward into a jump, landing softly with bent knees before immediately moving into the next repetition. Focus on increasing the height of the jump and the depth of the squat compared to Week 1. Added weight may be used.'),

(2, 3, 3, 'Reverse Lunge and Hammer Curl',
 'Step backward into a reverse lunge while performing a hammer curl simultaneously, then return to standing and repeat on the other side. Aim to increase the weight used or the number of repetitions compared to the previous week.'),

(2, 3, 3, 'Skater Jumps',
 'Leap laterally from foot to foot in a skating motion, reaching the opposite arm toward the landing foot on each side. Focus on increasing the distance of each lateral jump compared to Week 1.'),

(2, 3, 3, 'Glute Bridge Raises',
 'Lie on the back with knees bent and feet flat on the floor, then raise the hips toward the ceiling by pressing through the heels and squeezing the glutes at the top. Hold the raised position briefly before lowering. Added weight placed across the hips may be used.'),

(2, 3, 3, 'Burpees',
 'Perform the full burpee sequence from standing to plank, adding a press up at the bottom if desired, then returning to standing with an explosive jump overhead. Aim to increase pace or add a press up if not included in Week 1.'),

(2, 3, 3, 'Sit Ups',
 'Perform sit ups with a focus on controlled movement and full range of motion. Aim to increase the number of repetitions within the work interval compared to Week 1. Added weight may be used for additional challenge.'),

-- Day 4 | Workout 4
(2, 4, 4, 'Jumping Jacks',
 'Perform continuous jumping jacks with feet jumping outward and arms raising overhead on each repetition. Focus on increasing speed and maintaining consistent form throughout the work interval.'),

(2, 4, 4, 'Stiff Leg Deadlift',
 'Hinge at the hips with a slight knee bend and lower weights toward the floor while keeping the back flat. Focus on increasing the weight used or improving control and hamstring engagement compared to Week 1. Added weight may be used.'),

(2, 4, 4, 'High Knees',
 'Drive the knees upward toward the chest in a running motion on the spot, focusing on increasing pace and height of the knee drive compared to the previous week while maintaining an upright and stable torso.'),

(2, 4, 4, 'Plank Hold',
 'Hold a forearm or full plank with the body in a straight line and the core fully engaged. Aim to increase the duration of the hold compared to Week 1 while maintaining correct alignment.'),

(2, 4, 4, 'Skips',
 'Skip with or without a rope at a consistent and controlled pace. Focus on increasing the duration or speed of skipping within the work interval compared to the previous week.'),

(2, 4, 4, 'Curtsy Squats',
 'Step one foot diagonally behind the opposite leg and lower into a curtsy squat before returning to standing and repeating on the other side. Focus on increasing depth and control compared to Week 1. Added weight may be used.');

-- Days 5, 6, 7 | Rest Days
INSERT INTO workout_plan (week_number, day_number, workout_number, exercise_name, description) VALUES
(2, 5, 0, 'Rest Day',
 'This is a scheduled rest day. No structured exercise is required. Allow the body to recover and repair from the preceding four days of training. Light walking or gentle stretching is encouraged if desired.'),
(2, 6, 0, 'Rest Day',
 'This is a scheduled rest day. Focus on rest, adequate hydration, and nutritious food to support recovery. Avoid high intensity activity and allow the muscles time to adapt and strengthen.'),
(2, 7, 0, 'Rest Day',
 'This is the final rest day of the week. Use this day to prepare mentally and physically for the following week of training. Light mobility work or a gentle walk is acceptable if the body feels ready.');


-- Week 3


INSERT INTO workout_plan (week_number, day_number, workout_number, exercise_name, description) VALUES

-- Day 1 | Workout 1
(3, 1, 1, 'Squats',
 'Perform squats with a focus on depth and control, aiming to reach below parallel if possible. Increase the weight used compared to previous weeks or add a pause at the bottom of the movement to increase time under tension.'),

(3, 1, 1, 'Jumping Jacks',
 'Perform jumping jacks at an increased pace compared to previous weeks, focusing on explosive arm and leg movements while maintaining a soft and controlled landing throughout the work interval.'),

(3, 1, 1, 'Wall Half and Full Press Ups',
 'Progress to a lower surface such as a bench or step, or perform full floor press ups if not already doing so. Focus on achieving a full range of motion with the chest reaching close to the surface on each repetition.'),

(3, 1, 1, 'Butt Kicks',
 'Increase the pace of the butt kick movement, driving the heels higher toward the glutes with each repetition. Focus on maintaining an upright posture and keeping the core engaged throughout.'),

(3, 1, 1, 'Alternate Lunges',
 'Perform alternate lunges with an increased weight or a more challenging tempo, such as pausing at the bottom of each lunge to increase time under tension and muscular engagement. Focus on maintaining knee alignment over the toes.'),

(3, 1, 1, 'High Knees',
 'Increase the pace and height of the knee drive, focusing on driving the knees as high as possible toward the chest on each repetition. Use the arms actively to assist momentum and maintain a strong upright posture.'),

-- Day 2 | Workout 2
(3, 2, 2, 'Stiff Leg Deadlift',
 'Increase the weight used or slow the tempo of the movement to increase time under tension through the hamstrings and glutes. Focus on maintaining a flat back and controlled movement throughout each repetition.'),

(3, 2, 2, 'Ski Jumps',
 'Increase the speed and distance of the lateral jumps, focusing on explosive push-off from each foot and a soft controlled landing. Aim to maintain consistent form throughout the entire work interval.'),

(3, 2, 2, 'Sit Ups',
 'Increase the number of repetitions or add weight held at the chest to progress this exercise in Week 3. Focus on initiating the movement from the core rather than using momentum from the arms or neck.'),

(3, 2, 2, 'Mountain Climbers',
 'Increase the pace of the knee drives while maintaining a stable and level plank position. Focus on keeping the hips from rising or dropping and ensuring the core remains fully engaged throughout.'),

(3, 2, 2, 'Tricep Dips off a Chair',
 'Increase the range of motion by lowering further toward the floor, or extend one leg out straight to increase the load placed through the arms. Focus on controlled movement and full elbow extension at the top.'),

(3, 2, 2, 'Skips',
 'Increase the pace or introduce double unders if using a skipping rope, aiming for a faster and more explosive skipping action compared to previous weeks. Focus on landing lightly on the balls of the feet.'),

-- Day 3 | Workout 3
(3, 3, 3, 'Squat Jumps',
 'Increase the depth of the squat before each jump and focus on maximum height on the upward phase. Add light weights if not already doing so, or increase the weight used compared to previous weeks.'),

(3, 3, 3, 'Reverse Lunge and Hammer Curl',
 'Increase the weight used for the hammer curl component or slow the tempo of the lunge to increase muscular engagement. Focus on maintaining balance and upright posture throughout each repetition.'),

(3, 3, 3, 'Skater Jumps',
 'Increase the distance of each lateral leap and focus on a controlled and balanced landing on each side. Add a brief pause on the landing foot before pushing off to increase stability challenge.'),

(3, 3, 3, 'Glute Bridge Raises',
 'Add weight across the hips if not already doing so, or increase the weight used. Focus on holding the raised position for a count of two to three seconds before lowering to increase glute activation.'),

(3, 3, 3, 'Burpees',
 'Perform burpees at an increased pace or add a tuck jump at the top of the movement in place of a standard jump to increase the cardiovascular and muscular demand of the exercise.'),

(3, 3, 3, 'Sit Ups',
 'Increase the weight used or perform the exercise on a slight decline to increase the range of motion and difficulty. Focus on slow and controlled lowering to maximise core engagement on each repetition.'),

-- Day 4 | Workout 4
(3, 4, 4, 'Jumping Jacks',
 'Perform jumping jacks at maximum effort and pace, focusing on full arm extension overhead and a wide foot landing on each repetition. Aim to maintain this intensity for the full duration of the work interval.'),

(3, 4, 4, 'Stiff Leg Deadlift',
 'Increase the weight used compared to previous weeks, focusing on a slow and controlled lowering phase to maximise hamstring and glute engagement. Maintain a flat back and neutral spine throughout.'),

(3, 4, 4, 'High Knees',
 'Perform high knees at maximum pace, driving the knees as high as possible and pumping the arms to assist speed. Focus on maintaining this intensity consistently throughout the work interval.'),

(3, 4, 4, 'Plank Hold',
 'Aim to hold the plank for a longer duration than in previous weeks. Focus on preventing any movement in the hips or lower back and maintaining full tension through the core, glutes, and legs.'),

(3, 4, 4, 'Skips',
 'Increase the intensity of the skipping by increasing pace or attempting double unders with a rope. Focus on maintaining a light and consistent landing on the balls of the feet throughout the work interval.'),

(3, 4, 4, 'Curtsy Squats',
 'Increase the weight used or slow the tempo to add time under tension. Focus on achieving a deeper range of motion on each repetition and maintaining knee alignment throughout the movement.');

-- Days 5, 6, 7 | Rest Days
INSERT INTO workout_plan (week_number, day_number, workout_number, exercise_name, description) VALUES
(3, 5, 0, 'Rest Day',
 'This is a scheduled rest day. No structured exercise is required. Allow the body to recover and repair from the preceding four days of training. Light walking or gentle stretching is encouraged if desired.'),
(3, 6, 0, 'Rest Day',
 'This is a scheduled rest day. Focus on rest, adequate hydration, and nutritious food to support recovery. Avoid high intensity activity and allow the muscles time to adapt and strengthen.'),
(3, 7, 0, 'Rest Day',
 'This is the final rest day of the week. Use this day to prepare mentally and physically for the following week of training. Light mobility work or a gentle walk is acceptable if the body feels ready.');


-- Week 4


INSERT INTO workout_plan (week_number, day_number, workout_number, exercise_name, description) VALUES

-- Day 1 | Workout 1
(4, 1, 1, 'Squats',
 'Perform squats at maximum effort, using the heaviest weight manageable with correct form or increasing the number of rounds compared to Week 3. Focus on achieving full depth and driving powerfully through the heels on the upward phase.'),

(4, 1, 1, 'Jumping Jacks',
 'Perform jumping jacks at maximum speed and with full range of motion throughout the work interval. Focus on explosive arm and leg movements and maintaining a light, controlled landing on each repetition.'),

(4, 1, 1, 'Wall Half and Full Press Ups',
 'Perform full floor press ups if not already doing so, or increase the number of rounds completed. Focus on achieving a full range of motion on every repetition with the chest reaching close to the floor at the bottom of the movement.'),

(4, 1, 1, 'Butt Kicks',
 'Perform butt kicks at maximum pace, driving the heels as high as possible toward the glutes on each repetition. Maintain an upright posture and engaged core throughout the entire work interval.'),

(4, 1, 1, 'Alternate Lunges',
 'Use the highest weight manageable with correct form or increase the number of rounds completed. Focus on achieving maximum depth on each lunge while maintaining knee alignment and an upright torso throughout.'),

(4, 1, 1, 'High Knees',
 'Perform high knees at maximum effort and pace for the full duration of the work interval. Focus on driving the knees as high as possible and using the arms actively to maintain speed and rhythm.'),

-- Day 2 | Workout 2
(4, 2, 2, 'Stiff Leg Deadlift',
 'Use the heaviest weight manageable with correct form or increase the number of rounds completed. Focus on a slow and controlled lowering phase to maximise the stretch through the hamstrings and glutes on each repetition.'),

(4, 2, 2, 'Ski Jumps',
 'Perform ski jumps at maximum speed and with the greatest lateral distance achievable. Focus on explosive push-off from each foot and a soft, balanced landing throughout the work interval.'),

(4, 2, 2, 'Sit Ups',
 'Use the maximum weight manageable or perform the greatest number of repetitions within the work interval. Focus on controlled movement and full range of motion throughout each repetition without using momentum.'),

(4, 2, 2, 'Mountain Climbers',
 'Perform mountain climbers at maximum pace while maintaining a stable and level plank position. Focus on keeping the core fully engaged and the hips level throughout the entire duration of the work interval.'),

(4, 2, 2, 'Tricep Dips off a Chair',
 'Extend both legs out straight to increase the load through the arms, or add a weight plate across the thighs if available. Focus on achieving a full range of motion with complete elbow extension at the top of each repetition.'),

(4, 2, 2, 'Skips',
 'Skip at maximum pace or perform double unders continuously if using a rope. Focus on maintaining a light and consistent landing and sustaining the highest intensity achievable throughout the work interval.'),

-- Day 3 | Workout 3
(4, 3, 3, 'Squat Jumps',
 'Perform squat jumps with maximum effort, using the heaviest weight manageable or increasing the number of rounds. Focus on maximum explosive height on the jump and full squat depth before each upward phase.'),

(4, 3, 3, 'Reverse Lunge and Hammer Curl',
 'Use the heaviest weight manageable for the hammer curl component while maintaining correct lunge form. Focus on a controlled and balanced movement throughout each repetition and increase rounds if able.'),

(4, 3, 3, 'Skater Jumps',
 'Perform skater jumps with maximum lateral distance and a controlled landing on each side. Focus on a brief balance hold on each landing foot before pushing off explosively to the other side.'),

(4, 3, 3, 'Glute Bridge Raises',
 'Use the maximum weight manageable across the hips, or increase the number of rounds completed. Focus on a strong glute squeeze and a hold of two to three seconds at the top of each repetition before lowering.'),

(4, 3, 3, 'Burpees',
 'Perform burpees at maximum pace with a full press up and explosive tuck jump on each repetition. Focus on maintaining correct form throughout even as fatigue increases and aim to complete the greatest number possible within the work interval.'),

(4, 3, 3, 'Sit Ups',
 'Perform sit ups with maximum weight or on a decline surface to achieve the greatest difficulty. Focus on slow and controlled movement throughout each repetition and aim to beat the number achieved in Week 3.'),

-- Day 4 | Workout 4
(4, 4, 4, 'Jumping Jacks',
 'Perform jumping jacks at maximum speed and full range of motion for the entire work interval. Focus on explosive movement and maintaining consistent form even as fatigue sets in toward the end of the set.'),

(4, 4, 4, 'Stiff Leg Deadlift',
 'Use the maximum weight manageable with correct form, focusing on the slowest controlled lowering phase achieved across all four weeks. Drive powerfully through the hips to return to standing on each repetition.'),

(4, 4, 4, 'High Knees',
 'Perform high knees at maximum effort for the entire work interval, focusing on the highest knee drive and fastest pace achieved across all four weeks. Maintain an upright and stable torso throughout.'),

(4, 4, 4, 'Plank Hold',
 'Aim to hold the plank for the longest duration achieved across all four weeks. Focus on maintaining full tension through the core, glutes, and legs without any movement in the hips or lower back.'),

(4, 4, 4, 'Skips',
 'Skip at the highest intensity achieved across all four weeks, maintaining a light and consistent landing throughout. Focus on sustaining maximum pace or double unders for the full duration of the work interval.'),

(4, 4, 4, 'Curtsy Squats',
 'Use the maximum weight manageable or perform the greatest number of rounds. Focus on achieving the deepest range of motion across all four weeks while maintaining knee alignment and an upright torso throughout.');

-- Days 5, 6, 7 | Rest Days
INSERT INTO workout_plan (week_number, day_number, workout_number, exercise_name, description) VALUES
(4, 5, 0, 'Rest Day',
 'This is a scheduled rest day. No structured exercise is required. Allow the body to recover and repair from the preceding four days of training. Light walking or gentle stretching is encouraged if desired.'),
(4, 6, 0, 'Rest Day',
 'This is a scheduled rest day. Focus on rest, adequate hydration, and nutritious food to support recovery. Avoid high intensity activity and allow the muscles time to adapt and strengthen.'),
(4, 7, 0, 'Rest Day',
 'This is the final rest day of the week. Use this day to prepare mentally and physically for the following week of training. Light mobility work or a gentle walk is acceptable if the body feels ready.');