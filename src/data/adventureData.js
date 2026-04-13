export const adventureWorlds = [
  {
    id: 'forest',
    name: 'Forest World',
    theme: 'nutrition',
    icon: '🌳',
    unlockLevel: 1,
    levels: [
      {
        level: 1,
        title: 'Berry Beginning',
        quests: [
          { id: 'forest-hydration', name: 'Hydration Hero', goal: 'Drink 5 cups of water', xp: 20, coins: 8 },
          { id: 'forest-rainbow', name: 'Rainbow Plate', goal: 'Eat 2 colorful veggies', xp: 25, coins: 10 },
        ],
      },
      {
        level: 2,
        title: 'Snack Switch Trail',
        quests: [
          { id: 'forest-swap', name: 'Smart Swapper', goal: 'Swap one sugary snack for fruit', xp: 30, coins: 12 },
        ],
      },
      {
        level: 3,
        title: 'Fuel Explorer',
        quests: [
          { id: 'forest-breakfast', name: 'Morning Fuel', goal: 'Eat breakfast before school', xp: 35, coins: 14 },
        ],
      },
    ],
  },
  {
    id: 'ocean',
    name: 'Ocean World',
    theme: 'sleep',
    icon: '🌊',
    unlockLevel: 2,
    levels: [
      {
        level: 1,
        title: 'Calm Tide',
        quests: [
          { id: 'ocean-night', name: 'Night Ninja', goal: 'Sleep before 9PM', xp: 30, coins: 12 },
        ],
      },
      {
        level: 2,
        title: 'Dream Reef',
        quests: [
          { id: 'ocean-screen', name: 'Screen Sunset', goal: 'No screen 30 mins before bed', xp: 35, coins: 14 },
        ],
      },
      {
        level: 3,
        title: 'Moonlight Cove',
        quests: [
          { id: 'ocean-routine', name: 'Sleep Captain', goal: 'Follow bedtime routine checklist', xp: 40, coins: 18 },
        ],
      },
    ],
  },
  {
    id: 'space',
    name: 'Space World',
    theme: 'activity',
    icon: '🚀',
    unlockLevel: 3,
    levels: [
      {
        level: 1,
        title: 'Launch Pad',
        quests: [
          { id: 'space-energy', name: 'Energy Explorer', goal: 'Play outside for 30 mins', xp: 35, coins: 14 },
        ],
      },
      {
        level: 2,
        title: 'Orbit Run',
        quests: [
          { id: 'space-steps', name: 'Star Steps', goal: 'Complete 20 active minutes', xp: 40, coins: 16 },
        ],
      },
      {
        level: 3,
        title: 'Galaxy Boost',
        quests: [
          { id: 'space-family', name: 'Family Flyer', goal: 'Do one movement mission together', xp: 45, coins: 18 },
        ],
      },
    ],
  },
  {
    id: 'mountain',
    name: 'Mountain World',
    theme: 'consistency',
    icon: '⛰️',
    unlockLevel: 4,
    levels: [
      {
        level: 1,
        title: 'Base Camp',
        quests: [
          { id: 'mountain-check', name: 'Consistency Champ', goal: 'Complete 2 quests in one day', xp: 40, coins: 18 },
        ],
      },
      {
        level: 2,
        title: 'Climb Path',
        quests: [
          { id: 'mountain-streak', name: 'Habit Climber', goal: 'Keep a 3-day streak alive', xp: 50, coins: 20 },
        ],
      },
      {
        level: 3,
        title: 'Peak Master',
        quests: [
          { id: 'mountain-peak', name: 'Peak Hero', goal: 'Finish all daily quests', xp: 60, coins: 25 },
        ],
      },
    ],
  },
]
