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

cursor.execute(""" DROP TABLE IF EXISTS  sleep_plan;""")

connection.commit()

cursor.execute("""
CREATE TABLE sleep_plan (
    id SERIAL PRIMARY KEY,
    week_number SMALLINT NOT NULL,
    week_theme VARCHAR(100) NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    daily_tip TEXT NOT NULL
);
""")
connection.commit()

cursor.execute("""
INSERT INTO sleep_plan (week_number, week_theme, day_name, daily_tip) VALUES
(1, 'Reset Your Sleep Cycle', 'Monday',
 'Consistency is central to good sleep. Set a regular time to go to bed and to wake up each morning, aiming for between seven and nine hours of sleep per night.'),

(1, 'Reset Your Sleep Cycle', 'Tuesday',
 'Support your internal body clock by exposing yourself to at least ten minutes of natural sunlight each morning to help regulate your circadian rhythm.'),

(1, 'Reset Your Sleep Cycle', 'Wednesday',
 'Avoid consuming caffeine after 2 PM, as it can remain active in the body for up to ten hours and may interfere with the natural production of melatonin.'),

(1, 'Reset Your Sleep Cycle', 'Thursday',
 'Introduce a calming wind-down routine in the thirty to sixty minutes before bed. Consider reducing exposure to blue light, engaging in light stretching or journalling, or practising a brief meditation.'),

(1, 'Reset Your Sleep Cycle', 'Friday',
 'Reduce screen use at least one hour before going to bed to allow your mind and body to transition into a restful state.'),

(1, 'Reset Your Sleep Cycle', 'Saturday',
 'Aim to maintain a consistent sleep schedule across the weekend as well. A regular routine supports the body in optimising recovery and sustaining energy levels.'),

(1, 'Reset Your Sleep Cycle', 'Sunday',
 'Keep your sleeping environment cool, dark, and free of clutter. A tidy and calm space helps the brain associate the bedroom with rest and relaxation.');


-- Week 2: Deepen Relaxation and Recovery

INSERT INTO sleep_plan (week_number, week_theme, day_name, daily_tip) VALUES
(2, 'Deepen Relaxation and Recovery', 'Monday',
 'Once a consistent sleep routine is established, certain supplements may further support relaxation. Take time to learn about options that suit your individual needs.'),

(2, 'Deepen Relaxation and Recovery', 'Tuesday',
 'A warm bath or shower taken sixty to ninety minutes before bed can assist the body in triggering its natural sleep hormone, melatonin, by promoting physical relaxation.'),

(2, 'Deepen Relaxation and Recovery', 'Wednesday',
 'Avoid eating heavy meals or consuming alcohol within two hours of bedtime, as these can activate the body and work against the process of settling into sleep.'),

(2, 'Deepen Relaxation and Recovery', 'Thursday',
 'Consider drinking a mild herbal tea without caffeine approximately thirty minutes before bed to help ease the transition towards sleep.'),

(2, 'Deepen Relaxation and Recovery', 'Friday',
 'Use white noise, nature sounds, or similar ambient audio to reduce the impact of background noise, which is particularly useful if you are prone to restless or overactive thoughts at night.'),

(2, 'Deepen Relaxation and Recovery', 'Saturday',
 'Spend around ten minutes practising breathwork or guided meditation in the evening to help lower cortisol levels and prepare the mind for rest.'),

(2, 'Deepen Relaxation and Recovery', 'Sunday',
 'Take time to reflect on your progress over the past two weeks. Identify which strategies have been most effective for you and set aside approaches that have not felt useful.');


-- Week 3: Maximise Sleep Efficiency

INSERT INTO sleep_plan (week_number, week_theme, day_name, daily_tip) VALUES
(3, 'Maximise Sleep Efficiency', 'Monday',
 'Light exposure during the night can disrupt the natural sleep cycles of the body. Consider using an eye mask or installing blackout curtains to maintain a dark sleeping environment.'),

(3, 'Maximise Sleep Efficiency', 'Tuesday',
 'Avoid mentally demanding work or stressful activities at least one hour before bed. High-intensity cognitive activity in the evening can prevent the mind from fully relaxing.'),

(3, 'Maximise Sleep Efficiency', 'Wednesday',
 'Scrolling through a phone or device late at night can delay sleep onset and contribute to procrastination around bedtime. Opt for a screen-free activity such as reading, drawing, or a quiet conversation instead.'),

(3, 'Maximise Sleep Efficiency', 'Thursday',
 'Progressive muscle relaxation is a research-supported technique that involves systematically tensing and releasing muscle groups to promote full-body relaxation and support faster sleep onset.'),

(3, 'Maximise Sleep Efficiency', 'Friday',
 'Assess whether your mattress and pillow are adequately supporting your posture and comfort. An unsupportive sleep surface can contribute to discomfort and disrupted sleep throughout the night.'),

(3, 'Maximise Sleep Efficiency', 'Saturday',
 'If you find yourself dozing off unintentionally, set a short alarm for no more than twenty minutes. Brief naps during lighter sleep stages allow you to wake feeling refreshed rather than groggy.'),

(3, 'Maximise Sleep Efficiency', 'Sunday',
 'Improving air circulation in your bedroom can contribute to more restful sleep. Open a window for ventilation or consider adding an air-purifying plant to your sleeping space.');


-- Week 4: Lock In Long-Term Sleep Habits

INSERT INTO sleep_plan (week_number, week_theme, day_name, daily_tip) VALUES
(4, 'Lock In Long-Term Sleep Habits', 'Monday',
 'Sustainable sleep improvement comes from consistent and realistic adjustments. Review the habits you have trialled over the past three weeks and focus on embedding the changes that have worked best for you.'),

(4, 'Lock In Long-Term Sleep Habits', 'Tuesday',
 'Set yourself the challenge of spending an entire evening without screens or electronic devices to experience the difference a fully unplugged night can make.'),

(4, 'Lock In Long-Term Sleep Habits', 'Wednesday',
 'Your sleeping position can influence spinal alignment, breathing quality, and muscle recovery. Reflect on your current position and consider whether a small adjustment might improve your comfort overnight.'),

(4, 'Lock In Long-Term Sleep Habits', 'Thursday',
 'As daylight hours extend into the evening, spend around ten minutes outside before bed. Natural light exposure in the early evening can assist the body in producing melatonin at the appropriate time.'),

(4, 'Lock In Long-Term Sleep Habits', 'Friday',
 'Aromatherapy may support relaxation and reduce stress before sleep. Options such as pillow sprays, scented candles, or essential oil diffusers are worth exploring as part of your evening routine.'),

(4, 'Lock In Long-Term Sleep Habits', 'Saturday',
 'Investing in quality bedding made from natural fibres such as cotton or linen can help regulate body temperature overnight and contribute to a more comfortable and restorative sleep experience.'),

(4, 'Lock In Long-Term Sleep Habits', 'Sunday',
 'You have now completed the four-week sleep training plan. Reflect on the journey as a whole. Consider which habits you intend to carry forward and how you will continue to prioritise your sleep health going forward.'); """)

cursor.execute("SELECT * FROM sleep_plan;")
rows = cursor.fetchall()

for row in rows:
    print(row)


cursor.close()
connection.close()
