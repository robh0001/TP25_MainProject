function makeSearchVideoUrl(query) {
  return `https://www.youtube.com/embed?listType=search&list=${encodeURIComponent(query)}`
}

function makeIllustration({ icon, title, subtitle, accent, secondary }) {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 480">
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="${accent}" />
          <stop offset="100%" stop-color="${secondary}" />
        </linearGradient>
      </defs>
      <rect width="720" height="480" rx="36" fill="url(#bg)" />
      <circle cx="620" cy="92" r="84" fill="rgba(255,255,255,0.18)" />
      <circle cx="132" cy="380" r="110" fill="rgba(255,255,255,0.16)" />
      <rect x="46" y="54" width="230" height="42" rx="21" fill="rgba(255,255,255,0.26)" />
      <text x="64" y="83" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#ffffff">${subtitle}</text>
      <text x="72" y="230" font-size="122">${icon}</text>
      <text x="64" y="332" font-family="Arial, sans-serif" font-size="46" font-weight="800" fill="#ffffff">${title}</text>
      <text x="64" y="378" font-family="Arial, sans-serif" font-size="24" fill="rgba(255,255,255,0.92)">Healthy choice explorer</text>
    </svg>
  `
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`
}

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
}

function chunk(list, size) {
  const parts = []
  for (let index = 0; index < list.length; index += size) {
    parts.push(list.slice(index, index + size))
  }
  return parts
}

function rotatePalette(paletteList, index) {
  return paletteList[index % paletteList.length]
}

function createItem(missionId, label, icon, shortTip, videoQuery, palette) {
  return {
    id: `${missionId}-${slugify(label)}`,
    label,
    icon,
    shortTip,
    image: makeIllustration({
      icon,
      title: label,
      subtitle: "Explorer card",
      accent: palette.accent,
      secondary: palette.secondary,
    }),
    videoUrl: makeSearchVideoUrl(videoQuery),
  }
}

function createRecipe(missionId, pair, itemIds, palette) {
  return {
    id: `${missionId}-${slugify(pair.result)}`,
    pair: itemIds,
    result: pair.result,
    tip: pair.resultTip,
    image: makeIllustration({
      icon: pair.resultIcon,
      title: pair.result,
      subtitle: "Healthy match",
      accent: palette.accent,
      secondary: palette.secondary,
    }),
    videoUrl: makeSearchVideoUrl(pair.resultVideoQuery),
  }
}

function buildStage(missionSeed, stageIndex, stagePairs) {
  const items = []
  const recipes = []

  stagePairs.forEach((pair, pairIndex) => {
    const palette = rotatePalette(missionSeed.palettes, stageIndex * 5 + pairIndex)
    const leftItem = createItem(
      missionSeed.id,
      pair.left.label,
      pair.left.icon,
      pair.left.tip,
      pair.left.videoQuery,
      palette
    )
    const rightItem = createItem(
      missionSeed.id,
      pair.right.label,
      pair.right.icon,
      pair.right.tip,
      pair.right.videoQuery,
      { accent: palette.secondary, secondary: palette.accent }
    )

    items.push(leftItem, rightItem)
    recipes.push(createRecipe(missionSeed.id, pair, [leftItem.id, rightItem.id], palette))
  })

  const stagePalette = rotatePalette(missionSeed.palettes, stageIndex)

  return {
    id: `${missionSeed.id}-set-${stageIndex + 1}`,
    title: missionSeed.stageTitles[stageIndex] ?? `${missionSeed.title} Set ${stageIndex + 1}`,
    description:
      missionSeed.stageDescriptions[stageIndex] ??
      `Unlock ${stagePairs.length} healthy matches in this set.`,
    heroImage: makeIllustration({
      icon: missionSeed.heroIcon,
      title: missionSeed.stageTitles[stageIndex] ?? `${missionSeed.title} Set ${stageIndex + 1}`,
      subtitle: missionSeed.heroSubtitle,
      accent: stagePalette.accent,
      secondary: stagePalette.secondary,
    }),
    videoUrl: makeSearchVideoUrl(missionSeed.stageVideoQueries[stageIndex] ?? missionSeed.defaultVideoQuery),
    items,
    recipes,
  }
}

function buildMission(missionSeed) {
  return {
    id: missionSeed.id,
    title: missionSeed.title,
    stages: chunk(missionSeed.pairs, 5).map((pairs, stageIndex) => buildStage(missionSeed, stageIndex, pairs)),
  }
}

const palettes = {
  snack: [
    { accent: "#ff7083", secondary: "#ffb36b" },
    { accent: "#7e90ff", secondary: "#9cd7ff" },
    { accent: "#58c48a", secondary: "#92dd77" },
    { accent: "#8e66ff", secondary: "#d07dff" },
    { accent: "#ff9b58", secondary: "#ffd46b" },
    { accent: "#4fb0ff", secondary: "#8bf0ff" },
  ],
  move: [
    { accent: "#6d7dff", secondary: "#9e6fff" },
    { accent: "#ff8d65", secondary: "#ffc857" },
    { accent: "#59c6b3", secondary: "#7bcf85" },
    { accent: "#67b2ff", secondary: "#80e3ff" },
    { accent: "#f27ec7", secondary: "#ffb36d" },
    { accent: "#64c27c", secondary: "#9fdd79" },
  ],
  sleep: [
    { accent: "#4a63d8", secondary: "#7d5cf0" },
    { accent: "#6f8cff", secondary: "#82c8ff" },
    { accent: "#68c9a6", secondary: "#90e7cf" },
    { accent: "#9f7dff", secondary: "#7ac9ff" },
    { accent: "#7d87ff", secondary: "#c0b1ff" },
    { accent: "#5b76e8", secondary: "#8fa8ff" },
  ],
}

const missionSeeds = [
  {
    id: "snack",
    title: "Snack Explorer",
    heroIcon: "🍎",
    heroSubtitle: "Snack mission",
    defaultVideoQuery: "healthy snack ideas for kids",
    stageTitles: [
      "Fresh Crunch Set",
      "Rainbow Fuel Set",
      "Power Picnic Set",
      "Lunch Box Set",
      "Super Snack Set",
    ],
    stageDescriptions: [
      "Unlock five bright snack matches.",
      "Build the next five colorful food pairs.",
      "Keep going with fresh energy foods.",
      "Mix smarter lunchbox-style choices.",
      "Finish the full snack explorer board.",
    ],
    stageVideoQueries: [
      "healthy snack ideas for kids",
      "fruit and veggie snacks for kids",
      "healthy picnic snacks for kids",
      "healthy lunchbox snacks for kids",
      "easy healthy food combinations for kids",
    ],
    palettes: palettes.snack,
    pairs: [
      {
        left: { label: "Apple Slices", icon: "🍎", tip: "Sweet crunch for steady energy.", videoQuery: "apple slices snack for kids" },
        right: { label: "Greek Yogurt", icon: "🥣", tip: "Protein helps little tummies stay full.", videoQuery: "greek yogurt kids snack" },
        result: "Crunch Dip Duo",
        resultIcon: "✨",
        resultTip: "Fruit and protein make a balanced snack team.",
        resultVideoQuery: "apple yogurt healthy snack for kids",
      },
      {
        left: { label: "Carrot Sticks", icon: "🥕", tip: "Crunchy veggies add color and fiber.", videoQuery: "carrot sticks snack for kids" },
        right: { label: "Hummus Cup", icon: "🫘", tip: "Bean dips add creamy plant power.", videoQuery: "hummus snack for kids" },
        result: "Veggie Dip Match",
        resultIcon: "🥕",
        resultTip: "Crunchy veggies and dip make snack time fun.",
        resultVideoQuery: "carrot hummus snack for kids",
      },
      {
        left: { label: "Banana Coins", icon: "🍌", tip: "Bananas give quick playtime fuel.", videoQuery: "banana snack for kids" },
        right: { label: "Peanut Butter", icon: "🥜", tip: "Healthy fats help snacks last longer.", videoQuery: "peanut butter snack for kids" },
        result: "Banana Power Bites",
        resultIcon: "⚡",
        resultTip: "Fruit plus healthy fat makes a filling bite.",
        resultVideoQuery: "banana peanut butter snack for kids",
      },
      {
        left: { label: "Cucumber Wheels", icon: "🥒", tip: "Cool crunch brings watery freshness.", videoQuery: "cucumber snack for kids" },
        right: { label: "Cheese Cubes", icon: "🧀", tip: "Cheese adds protein to a snack plate.", videoQuery: "cheese snack for kids" },
        result: "Cool Crunch Plate",
        resultIcon: "🥗",
        resultTip: "Fresh cucumber and cheese make a smart savory combo.",
        resultVideoQuery: "cucumber cheese snack for kids",
      },
      {
        left: { label: "Berry Mix", icon: "🫐", tip: "Berries bring bright vitamins and color.", videoQuery: "berries snack for kids" },
        right: { label: "Oat Bites", icon: "🌾", tip: "Oats give chewy energy for play.", videoQuery: "oat bites snack for kids" },
        result: "Berry Energy Bowl",
        resultIcon: "🌈",
        resultTip: "Fruit and whole grains make a cheerful fuel bowl.",
        resultVideoQuery: "berry oat snack for kids",
      },
      {
        left: { label: "Orange Segments", icon: "🍊", tip: "Juicy orange pieces feel bright and fresh.", videoQuery: "orange snack for kids" },
        right: { label: "Cottage Cheese", icon: "🥣", tip: "Soft protein helps a snack feel bigger.", videoQuery: "cottage cheese kids snack" },
        result: "Citrus Cream Cup",
        resultIcon: "☀️",
        resultTip: "Juicy fruit and creamy protein make a sunny snack.",
        resultVideoQuery: "orange cottage cheese snack for kids",
      },
      {
        left: { label: "Pear Slices", icon: "🍐", tip: "Pears are soft, sweet, and juicy.", videoQuery: "pear snack for kids" },
        right: { label: "Sunflower Seeds", icon: "🌻", tip: "Seeds add little bites of crunch.", videoQuery: "sunflower seeds snack for kids" },
        result: "Pear Power Snack",
        resultIcon: "🌻",
        resultTip: "Soft fruit and crunchy seeds make a fun texture pair.",
        resultVideoQuery: "pear sunflower seed snack for kids",
      },
      {
        left: { label: "Pepper Strips", icon: "🫑", tip: "Bell peppers are bright and crispy.", videoQuery: "bell pepper snack for kids" },
        right: { label: "Guacamole", icon: "🥑", tip: "Avocado dips feel creamy and smooth.", videoQuery: "guacamole snack for kids" },
        result: "Pepper Dip Pop",
        resultIcon: "🥑",
        resultTip: "Crunchy peppers and guac make a colorful dip plate.",
        resultVideoQuery: "bell pepper guacamole snack for kids",
      },
      {
        left: { label: "Whole Grain Crackers", icon: "🍘", tip: "Whole grains bring a steady crunch.", videoQuery: "whole grain crackers snack kids" },
        right: { label: "Tuna Salad", icon: "🐟", tip: "Tuna adds protein for staying power.", videoQuery: "tuna snack for kids" },
        result: "Smart Crunch Stack",
        resultIcon: "🐟",
        resultTip: "Whole grains and protein work well together.",
        resultVideoQuery: "whole grain tuna snack for kids",
      },
      {
        left: { label: "Celery Sticks", icon: "🥬", tip: "Celery crunch sounds loud and fun.", videoQuery: "celery snack for kids" },
        right: { label: "Raisins", icon: "🍇", tip: "Raisins add chewy sweetness.", videoQuery: "raisins snack for kids" },
        result: "Ants on a Log",
        resultIcon: "🐜",
        resultTip: "Crunchy celery and tiny raisins make a playful classic.",
        resultVideoQuery: "ants on a log snack for kids",
      },
      {
        left: { label: "Mango Cubes", icon: "🥭", tip: "Mango tastes bright and tropical.", videoQuery: "mango snack for kids" },
        right: { label: "Yogurt Swirl", icon: "🥛", tip: "Yogurt makes fruity snacks creamy.", videoQuery: "yogurt fruit snack for kids" },
        result: "Mango Swirl Cup",
        resultIcon: "🌴",
        resultTip: "Smooth yogurt and mango feel like a cool treat.",
        resultVideoQuery: "mango yogurt snack for kids",
      },
      {
        left: { label: "Cherry Tomatoes", icon: "🍅", tip: "Tiny tomatoes are juicy and bright.", videoQuery: "cherry tomatoes snack kids" },
        right: { label: "Mozzarella Pearls", icon: "⚪", tip: "Soft cheese pearls feel mild and easy.", videoQuery: "mozzarella snack for kids" },
        result: "Little Caprese Bites",
        resultIcon: "🍅",
        resultTip: "Tomatoes and soft cheese make a fresh tiny snack.",
        resultVideoQuery: "caprese snack for kids",
      },
      {
        left: { label: "Pineapple Chunks", icon: "🍍", tip: "Pineapple brings juicy tropical zing.", videoQuery: "pineapple snack for kids" },
        right: { label: "Coconut Yogurt", icon: "🥥", tip: "Coconut yogurt feels cool and creamy.", videoQuery: "coconut yogurt kids snack" },
        result: "Tropical Chill Cup",
        resultIcon: "🏝️",
        resultTip: "Pineapple and yogurt make a beachy snack feeling.",
        resultVideoQuery: "pineapple yogurt snack for kids",
      },
      {
        left: { label: "Edamame Pods", icon: "🫛", tip: "Little green beans bring protein.", videoQuery: "edamame snack for kids" },
        right: { label: "Rice Cakes", icon: "🍘", tip: "Rice cakes add a light crispy bite.", videoQuery: "rice cakes snack for kids" },
        result: "Green Power Plate",
        resultIcon: "💚",
        resultTip: "Protein and crunch make a fun after-school plate.",
        resultVideoQuery: "edamame rice cake snack for kids",
      },
      {
        left: { label: "Apple Chips", icon: "🍎", tip: "Crunchy apple chips feel extra crisp.", videoQuery: "apple chips snack for kids" },
        right: { label: "Almond Butter", icon: "🥜", tip: "Nut butter adds smooth energy.", videoQuery: "almond butter snack for kids" },
        result: "Crunch Spread Snack",
        resultIcon: "🍏",
        resultTip: "Crunchy fruit and nut butter balance sweet and rich tastes.",
        resultVideoQuery: "apple chips almond butter snack kids",
      },
      {
        left: { label: "Kiwi Slices", icon: "🥝", tip: "Kiwi adds a tangy green pop.", videoQuery: "kiwi snack for kids" },
        right: { label: "Granola Sprinkle", icon: "🥣", tip: "Granola gives crunchy whole-grain bits.", videoQuery: "granola snack for kids" },
        result: "Kiwi Crunch Parfait",
        resultIcon: "🥝",
        resultTip: "Tangy fruit and granola make a bright crunchy cup.",
        resultVideoQuery: "kiwi granola yogurt kids snack",
      },
      {
        left: { label: "Snap Peas", icon: "🫛", tip: "Snap peas feel sweet and crisp.", videoQuery: "snap peas snack for kids" },
        right: { label: "Yogurt Ranch", icon: "🥣", tip: "Yogurt ranch makes veggie dipping fun.", videoQuery: "yogurt ranch dip for kids" },
        result: "Snap Dip Snack",
        resultIcon: "🌿",
        resultTip: "Fresh peas and dip keep veggies playful.",
        resultVideoQuery: "snap peas yogurt ranch snack kids",
      },
      {
        left: { label: "Boiled Egg", icon: "🥚", tip: "Eggs give strong protein fuel.", videoQuery: "boiled egg snack for kids" },
        right: { label: "Whole Wheat Toast", icon: "🍞", tip: "Whole wheat adds longer-lasting energy.", videoQuery: "whole wheat toast snack kids" },
        result: "Protein Start Plate",
        resultIcon: "🍳",
        resultTip: "Protein and grains team up for a steady snack.",
        resultVideoQuery: "egg toast healthy snack kids",
      },
      {
        left: { label: "Strawberry Halves", icon: "🍓", tip: "Strawberries feel juicy and cheerful.", videoQuery: "strawberry snack for kids" },
        right: { label: "Oat Pancakes", icon: "🥞", tip: "Mini oat pancakes make a fun bite.", videoQuery: "oat pancake snack for kids" },
        result: "Berry Breakfast Stack",
        resultIcon: "🥞",
        resultTip: "Fruit and oats make breakfast-style snack energy.",
        resultVideoQuery: "strawberry oat pancakes kids snack",
      },
      {
        left: { label: "Watermelon Cubes", icon: "🍉", tip: "Watermelon feels juicy and cool.", videoQuery: "watermelon snack for kids" },
        right: { label: "Feta Crumbles", icon: "🧀", tip: "A little salty cheese changes the flavor.", videoQuery: "feta snack for kids" },
        result: "Summer Splash Plate",
        resultIcon: "💦",
        resultTip: "Sweet melon and cheese make a fresh summer plate.",
        resultVideoQuery: "watermelon feta snack for kids",
      },
      {
        left: { label: "Avocado Toast", icon: "🥑", tip: "Avocado toast feels creamy and filling.", videoQuery: "avocado toast kids snack" },
        right: { label: "Tomato Slices", icon: "🍅", tip: "Tomatoes add juicy color on top.", videoQuery: "tomato slices snack for kids" },
        result: "Green Toast Trio",
        resultIcon: "🥪",
        resultTip: "Avocado and tomato turn toast into a colorful snack.",
        resultVideoQuery: "avocado tomato toast kids snack",
      },
      {
        left: { label: "Trail Mix", icon: "🥜", tip: "Trail mix brings many tiny textures.", videoQuery: "trail mix snack for kids" },
        right: { label: "Milk Box", icon: "🥛", tip: "Milk adds a cool sip beside a snack.", videoQuery: "milk snack pairing for kids" },
        result: "Energy Trail Combo",
        resultIcon: "🏕️",
        resultTip: "Crunchy mix and a cool drink make a ready-to-go snack.",
        resultVideoQuery: "trail mix milk snack for kids",
      },
      {
        left: { label: "Spinach Wrap", icon: "🌯", tip: "Spinach wraps make lunch bites green and fun.", videoQuery: "spinach wrap snack kids" },
        right: { label: "Turkey Roll", icon: "🦃", tip: "Turkey adds easy lean protein.", videoQuery: "turkey roll snack for kids" },
        result: "Lunch Power Roll",
        resultIcon: "🌯",
        resultTip: "Wraps and turkey make a tidy lunchbox pair.",
        resultVideoQuery: "spinach turkey wrap snack kids",
      },
      {
        left: { label: "Broccoli Florets", icon: "🥦", tip: "Broccoli trees bring bright green crunch.", videoQuery: "broccoli snack for kids" },
        right: { label: "Yogurt Dip", icon: "🥣", tip: "Cool dip helps crunchy veggies feel friendlier.", videoQuery: "yogurt veggie dip for kids" },
        result: "Broccoli Dip Bite",
        resultIcon: "🥦",
        resultTip: "Green crunch and creamy dip make veggies easier to enjoy.",
        resultVideoQuery: "broccoli yogurt dip snack kids",
      },
      {
        left: { label: "Corn Cups", icon: "🌽", tip: "Sweet corn pops with little juicy bites.", videoQuery: "corn snack for kids" },
        right: { label: "Black Beans", icon: "🫘", tip: "Beans add plant protein and fiber.", videoQuery: "black beans snack for kids" },
        result: "Rainbow Power Cup",
        resultIcon: "🌽",
        resultTip: "Corn and beans make a colorful spoon snack.",
        resultVideoQuery: "corn black beans snack kids",
      },
    ],
  },
  {
    id: "move",
    title: "Move and Groove",
    heroIcon: "🏃",
    heroSubtitle: "Movement mission",
    defaultVideoQuery: "fun movement games for kids",
    stageTitles: [
      "Warm Up Set",
      "Play Burst Set",
      "Team Action Set",
      "Power Trail Set",
      "Big Motion Set",
    ],
    stageDescriptions: [
      "Unlock five body-moving matches.",
      "Keep going with playful movement pairs.",
      "Build teamwork and rhythm combos.",
      "Mix balance, speed, and control.",
      "Finish the full movement explorer board.",
    ],
    stageVideoQueries: [
      "kids exercise warm up",
      "fun movement games for kids",
      "kids teamwork games movement",
      "agility exercises for kids",
      "kids active play workout",
    ],
    palettes: palettes.move,
    pairs: [
      {
        left: { label: "Jumping Jacks", icon: "⭐", tip: "Fast jumping wakes up the whole body.", videoQuery: "jumping jacks for kids" },
        right: { label: "High Knees", icon: "🦵", tip: "High knees make hearts pump faster.", videoQuery: "high knees for kids" },
        result: "Heart Pump Combo",
        resultIcon: "💓",
        resultTip: "Two quick cardio moves make a strong warm up.",
        resultVideoQuery: "kids cardio warm up jumping jacks high knees",
      },
      {
        left: { label: "Dance Party", icon: "💃", tip: "Dance lets bodies move with joy.", videoQuery: "dance workout for kids" },
        right: { label: "Arm Circles", icon: "🌀", tip: "Arm circles loosen shoulders for play.", videoQuery: "arm circles for kids" },
        result: "Music Warm Up",
        resultIcon: "🎵",
        resultTip: "Rhythm and arm motion make a playful start.",
        resultVideoQuery: "kids dance arm circles warm up",
      },
      {
        left: { label: "Stretch Reach", icon: "🤸", tip: "Big stretches wake up sleepy muscles.", videoQuery: "kids stretching routine" },
        right: { label: "Balance Pose", icon: "🧘", tip: "Balance helps bodies feel steady.", videoQuery: "balance exercise for kids" },
        result: "Calm Core Flow",
        resultIcon: "🌟",
        resultTip: "Slow moves build control and focus.",
        resultVideoQuery: "kids stretch balance routine",
      },
      {
        left: { label: "Scooter Ride", icon: "🛴", tip: "Scooters turn outdoor play into motion practice.", videoQuery: "scooter activity for kids" },
        right: { label: "Helmet On", icon: "⛑️", tip: "Safety gear keeps movement smart.", videoQuery: "helmet safety for kids" },
        result: "Safe Speed Ride",
        resultIcon: "🛴",
        resultTip: "Fast fun works best with safe gear.",
        resultVideoQuery: "kids scooter helmet safety",
      },
      {
        left: { label: "Bike Ride", icon: "🚲", tip: "Pedaling builds leg power and stamina.", videoQuery: "bike riding for kids" },
        right: { label: "Knee Pads", icon: "🦿", tip: "Pads help active play stay safer.", videoQuery: "knee pad safety for kids" },
        result: "Ready Rider Mix",
        resultIcon: "🚴",
        resultTip: "Movement and safety gear make a strong pair.",
        resultVideoQuery: "bike safety for kids knee pads",
      },
      {
        left: { label: "Hopscotch", icon: "🔢", tip: "Hopping games build balance and timing.", videoQuery: "hopscotch for kids" },
        right: { label: "Chalk Path", icon: "🖍️", tip: "Drawn paths make playground games clear.", videoQuery: "chalk games for kids" },
        result: "Pattern Play Path",
        resultIcon: "🌈",
        resultTip: "A path on the ground turns hops into a fun game.",
        resultVideoQuery: "hopscotch chalk game for kids",
      },
      {
        left: { label: "Soccer Kicks", icon: "⚽", tip: "Kicking helps coordination and balance.", videoQuery: "soccer drills for kids" },
        right: { label: "Water Bottle", icon: "💧", tip: "Hydration matters during active play.", videoQuery: "hydration for active kids" },
        result: "Kick and Sip",
        resultIcon: "💧",
        resultTip: "Sports and water make a healthy play combo.",
        resultVideoQuery: "soccer hydration for kids",
      },
      {
        left: { label: "Bear Crawl", icon: "🐻", tip: "Crawling works arms, legs, and core.", videoQuery: "bear crawl for kids" },
        right: { label: "Crab Walk", icon: "🦀", tip: "Crab walks build strong playful movement.", videoQuery: "crab walk for kids" },
        result: "Animal Power Track",
        resultIcon: "🐾",
        resultTip: "Animal moves make strength work feel silly and fun.",
        resultVideoQuery: "bear crawl crab walk for kids",
      },
      {
        left: { label: "Yoga Pose", icon: "🧘", tip: "Yoga helps bodies slow down and focus.", videoQuery: "kids yoga poses" },
        right: { label: "Deep Breaths", icon: "🫁", tip: "Breathing helps movement feel calm.", videoQuery: "deep breathing for kids" },
        result: "Quiet Strength Time",
        resultIcon: "🌙",
        resultTip: "Breathing and yoga help balance busy energy.",
        resultVideoQuery: "kids yoga breathing routine",
      },
      {
        left: { label: "Relay Run", icon: "🏁", tip: "Relay races bring quick bursts of speed.", videoQuery: "relay race for kids" },
        right: { label: "Team Cheer", icon: "🙌", tip: "Cheering makes team play feel happy.", videoQuery: "team games for kids" },
        result: "Sprint Spirit Set",
        resultIcon: "📣",
        resultTip: "Running and cheering build teamwork and energy.",
        resultVideoQuery: "relay race team cheer kids",
      },
      {
        left: { label: "Skate Practice", icon: "🛹", tip: "Skating works balance and brave focus.", videoQuery: "skate practice for kids" },
        right: { label: "Wrist Guards", icon: "🛡️", tip: "Safety pads help active play stay smart.", videoQuery: "wrist guards for kids skating" },
        result: "Safe Roll Session",
        resultIcon: "🛹",
        resultTip: "Rolling sports feel better with protection on.",
        resultVideoQuery: "kids skating wrist guard safety",
      },
      {
        left: { label: "Stair Steps", icon: "🪜", tip: "Stepping up builds leg power.", videoQuery: "stairs exercise for kids" },
        right: { label: "Toe Touches", icon: "👣", tip: "Toe touches stretch out the back body.", videoQuery: "toe touches for kids" },
        result: "Quick Warm Up Boost",
        resultIcon: "🔥",
        resultTip: "Fast steps and gentle stretching warm up many muscles.",
        resultVideoQuery: "stairs toe touches kids warm up",
      },
      {
        left: { label: "Ball Toss", icon: "🏐", tip: "Tossing helps hand-eye timing.", videoQuery: "ball toss for kids" },
        right: { label: "Catch Hands", icon: "🤲", tip: "Catching builds focus and reaction speed.", videoQuery: "catching games for kids" },
        result: "Focus Catch Flow",
        resultIcon: "🎯",
        resultTip: "Throwing and catching build teamwork and control.",
        resultVideoQuery: "ball toss catch game for kids",
      },
      {
        left: { label: "Side Shuffles", icon: "↔️", tip: "Shuffling works quick foot changes.", videoQuery: "side shuffle for kids" },
        right: { label: "Cone Markers", icon: "🚧", tip: "Markers turn movement into a game path.", videoQuery: "cone drills for kids" },
        result: "Agility Trail",
        resultIcon: "⚡",
        resultTip: "Direction changes and markers build nimble feet.",
        resultVideoQuery: "agility cone drills for kids",
      },
      {
        left: { label: "Freeze Dance", icon: "🕺", tip: "Freezing fast builds body control.", videoQuery: "freeze dance for kids" },
        right: { label: "Drum Beat", icon: "🥁", tip: "Music cues make movements exciting.", videoQuery: "music movement for kids" },
        result: "Rhythm Freeze Fun",
        resultIcon: "🥁",
        resultTip: "Music and fast stops make a great rhythm game.",
        resultVideoQuery: "freeze dance drum beat kids",
      },
      {
        left: { label: "Obstacle Course", icon: "🚧", tip: "Courses make full-body play adventurous.", videoQuery: "obstacle course for kids" },
        right: { label: "Finish Stretch", icon: "🏁", tip: "Stretching at the end helps cool down.", videoQuery: "cool down stretch for kids" },
        result: "Adventure Move Path",
        resultIcon: "🗺️",
        resultTip: "Hard play and a cool-down stretch make a smart pair.",
        resultVideoQuery: "obstacle course cool down stretch kids",
      },
      {
        left: { label: "Hula Hoop", icon: "⭕", tip: "Hooping wakes up hips and belly muscles.", videoQuery: "hula hoop for kids" },
        right: { label: "Hip Twist", icon: "🌀", tip: "Twisting helps bodies move in new ways.", videoQuery: "hip twist for kids" },
        result: "Hoop Spin Groove",
        resultIcon: "💫",
        resultTip: "Hoops and twists make mid-body movement fun.",
        resultVideoQuery: "kids hula hoop hip twist",
      },
      {
        left: { label: "Monkey Bars", icon: "🐒", tip: "Monkey bars build hanging strength.", videoQuery: "monkey bars for kids" },
        right: { label: "Grip Shake", icon: "✋", tip: "Hand shakes loosen tired fingers.", videoQuery: "hand warm ups for kids" },
        result: "Strong Hands Circuit",
        resultIcon: "💪",
        resultTip: "Grip work and climbing build hand strength together.",
        resultVideoQuery: "monkey bars grip strength kids",
      },
      {
        left: { label: "Nature Walk", icon: "🌳", tip: "Walking outside makes movement feel peaceful.", videoQuery: "nature walk for kids" },
        right: { label: "Step Counter", icon: "⌚", tip: "Counting steps can turn walking into a challenge.", videoQuery: "step challenge for kids" },
        result: "Trail Tracker Trek",
        resultIcon: "🥾",
        resultTip: "Walking and counting steps help kids notice active minutes.",
        resultVideoQuery: "nature walk step challenge kids",
      },
      {
        left: { label: "Trampoline Bounces", icon: "🛝", tip: "Bouncing makes legs and hearts work hard.", videoQuery: "trampoline exercise for kids" },
        right: { label: "Soft Landing", icon: "☁️", tip: "Landing safely helps bodies stay controlled.", videoQuery: "safe landing for kids jumping" },
        result: "Bounce Safe Set",
        resultIcon: "☁️",
        resultTip: "Big jumps feel best with strong safe landings.",
        resultVideoQuery: "trampoline safe landing kids",
      },
      {
        left: { label: "Swim Kicks", icon: "🏊", tip: "Swimming builds whole-body endurance.", videoQuery: "swim kicks for kids" },
        right: { label: "Pool Float", icon: "🛟", tip: "Float tools can help new swimmers practice.", videoQuery: "swim practice for kids float" },
        result: "Splash Power Pair",
        resultIcon: "💦",
        resultTip: "Kicking practice and float support build water confidence.",
        resultVideoQuery: "kids swim kicks practice",
      },
      {
        left: { label: "March in Place", icon: "🥁", tip: "Marching gets bodies moving anywhere.", videoQuery: "marching exercise for kids" },
        right: { label: "Shoulder Rolls", icon: "🔄", tip: "Rolls loosen tight shoulders.", videoQuery: "shoulder rolls for kids" },
        result: "Start Moving Duo",
        resultIcon: "🚶",
        resultTip: "Simple marching and rolls make a quick warm-up pair.",
        resultVideoQuery: "march in place shoulder rolls kids",
      },
      {
        left: { label: "Lunges", icon: "🦵", tip: "Lunges build lower-body strength.", videoQuery: "lunges for kids" },
        right: { label: "Heel Walks", icon: "👟", tip: "Heel walks work little foot muscles.", videoQuery: "heel walks for kids" },
        result: "Leg Power Track",
        resultIcon: "👣",
        resultTip: "Strong legs and healthy feet help active play.",
        resultVideoQuery: "lunges heel walks for kids",
      },
      {
        left: { label: "Shadow Boxing", icon: "🥊", tip: "Punching the air builds fast focus.", videoQuery: "shadow boxing for kids" },
        right: { label: "Fast Feet", icon: "⚡", tip: "Quick feet wake up body speed.", videoQuery: "fast feet drill for kids" },
        result: "Energy Burst Combo",
        resultIcon: "⚡",
        resultTip: "Punches and foot speed make a lively cardio pair.",
        resultVideoQuery: "shadow boxing fast feet kids",
      },
      {
        left: { label: "Parachute Play", icon: "🌈", tip: "Parachutes make group movement exciting.", videoQuery: "parachute games for kids" },
        right: { label: "Team Lift", icon: "🙌", tip: "Lifting together builds group timing.", videoQuery: "teamwork games for kids movement" },
        result: "Rainbow Lift Game",
        resultIcon: "🎈",
        resultTip: "Team movement feels magical when everyone works together.",
        resultVideoQuery: "parachute teamwork game kids",
      },
    ],
  },
  {
    id: "sleep",
    title: "Sleep Superpower",
    heroIcon: "🌙",
    heroSubtitle: "Sleep mission",
    defaultVideoQuery: "bedtime routine for kids",
    stageTitles: [
      "Bedtime Start Set",
      "Cozy Wind Down Set",
      "Dream Room Set",
      "Quiet Mind Set",
      "Sleep Super Set",
    ],
    stageDescriptions: [
      "Unlock five calm bedtime matches.",
      "Keep going with cozy wind-down habits.",
      "Build a room that feels ready for sleep.",
      "Match calming ideas for a quiet mind.",
      "Finish the full sleep explorer board.",
    ],
    stageVideoQueries: [
      "bedtime routine for kids",
      "calm bedtime habits for kids",
      "sleep environment for kids",
      "mindful bedtime routine for kids",
      "healthy sleep habits for kids",
    ],
    palettes: palettes.sleep,
    pairs: [
      {
        left: { label: "Tidy Toys", icon: "🧸", tip: "A calm room helps a calm brain.", videoQuery: "tidy toys bedtime for kids" },
        right: { label: "Brush Teeth", icon: "🪥", tip: "Brushing is a steady bedtime step.", videoQuery: "brush teeth bedtime routine kids" },
        result: "Ready for Bed",
        resultIcon: "✨",
        resultTip: "Simple steps in order make bedtime feel easier.",
        resultVideoQuery: "bedtime routine brush teeth tidy room kids",
      },
      {
        left: { label: "Story Time", icon: "📖", tip: "Stories help bodies slow down.", videoQuery: "story time before bed kids" },
        right: { label: "Dim Lights", icon: "🌙", tip: "Soft lights tell the brain it is night.", videoQuery: "dim lights bedtime routine kids" },
        result: "Sleepy Mood",
        resultIcon: "🌜",
        resultTip: "Stories and dim light help the body settle.",
        resultVideoQuery: "story and dim lights bedtime routine kids",
      },
      {
        left: { label: "Warm Bath", icon: "🛁", tip: "Warm water can help the body relax.", videoQuery: "warm bath bedtime routine kids" },
        right: { label: "Pajamas", icon: "🛌", tip: "Pajamas signal that day time is done.", videoQuery: "pajamas bedtime routine kids" },
        result: "Cozy Reset",
        resultIcon: "☁️",
        resultTip: "Bath time and pajamas create a strong bedtime signal.",
        resultVideoQuery: "bath pajamas bedtime routine kids",
      },
      {
        left: { label: "Slow Breaths", icon: "🫁", tip: "Slow breathing helps busy feelings settle.", videoQuery: "slow breathing before bed kids" },
        right: { label: "Soft Music", icon: "🎵", tip: "Quiet music can make a room feel calm.", videoQuery: "soft sleep music for kids" },
        result: "Moon Breath Mix",
        resultIcon: "🌙",
        resultTip: "Breathing and soft sound help bodies get sleepy.",
        resultVideoQuery: "kids breathing and calming music bedtime",
      },
      {
        left: { label: "Goodnight Hug", icon: "🤗", tip: "Warm goodnight moments feel safe and loving.", videoQuery: "goodnight routine for kids" },
        right: { label: "Favorite Blanket", icon: "🛏️", tip: "A favorite blanket can feel cozy and familiar.", videoQuery: "cozy blanket bedtime kids" },
        result: "Snuggle Nest",
        resultIcon: "💤",
        resultTip: "Comfort and routine help kids settle into bed.",
        resultVideoQuery: "comfort bedtime routine kids",
      },
      {
        left: { label: "Wash Face", icon: "🫧", tip: "A fresh face helps bedtime feel clean and calm.", videoQuery: "wash face bedtime routine kids" },
        right: { label: "Hair Brush", icon: "🪮", tip: "Brushing hair can be part of winding down.", videoQuery: "hair brushing bedtime kids" },
        result: "Fresh Cozy Start",
        resultIcon: "🫧",
        resultTip: "Gentle care steps help bodies feel ready for bed.",
        resultVideoQuery: "kids bedtime wash face brush hair",
      },
      {
        left: { label: "Quiet Prayer", icon: "🙏", tip: "Quiet reflection can bring a calm heart.", videoQuery: "quiet bedtime routine for kids" },
        right: { label: "Calm Voice", icon: "🤫", tip: "Soft voices keep bedtime feeling peaceful.", videoQuery: "calm voice bedtime kids" },
        result: "Peaceful Heart Pause",
        resultIcon: "💛",
        resultTip: "Gentle words and quiet moments help emotions settle.",
        resultVideoQuery: "calm bedtime reflection for kids",
      },
      {
        left: { label: "Water Sip", icon: "💧", tip: "A small sip can help bodies feel comfortable.", videoQuery: "water before bed kids" },
        right: { label: "Bathroom Break", icon: "🚽", tip: "A quick bathroom trip can prevent wake-ups.", videoQuery: "bathroom before bed kids" },
        result: "No Wake Plan",
        resultIcon: "🚪",
        resultTip: "Little bedtime checks can help sleep last longer.",
        resultVideoQuery: "bathroom water bedtime routine kids",
      },
      {
        left: { label: "Night Light", icon: "💡", tip: "Small lights can help rooms feel safe.", videoQuery: "night light for kids bedtime" },
        right: { label: "Curtain Close", icon: "🪟", tip: "Closing curtains helps make the room darker.", videoQuery: "dark room sleep kids" },
        result: "Dream Room Glow",
        resultIcon: "🌌",
        resultTip: "A calm light and dark room can work together well.",
        resultVideoQuery: "bedroom setup for kids sleep",
      },
      {
        left: { label: "Lotion Rub", icon: "🧴", tip: "Gentle lotion can feel soothing after bath time.", videoQuery: "bedtime lotion routine kids" },
        right: { label: "Teddy Bear", icon: "🧸", tip: "A comfort toy can make bedtime feel friendly.", videoQuery: "sleep comfort toy for kids" },
        result: "Snuggle Calm Set",
        resultIcon: "🧸",
        resultTip: "Soft touch and a comfort buddy can build calm feelings.",
        resultVideoQuery: "comfort bedtime routine with teddy bear kids",
      },
      {
        left: { label: "Gratitude List", icon: "💙", tip: "Thinking of good moments can calm the mind.", videoQuery: "gratitude for kids before bed" },
        right: { label: "Journal Note", icon: "📝", tip: "A quick note can empty busy thoughts.", videoQuery: "kids journal before bed" },
        result: "Happy Mind Reset",
        resultIcon: "⭐",
        resultTip: "Thankful thoughts and journaling help minds feel lighter.",
        resultVideoQuery: "gratitude journaling bedtime kids",
      },
      {
        left: { label: "Toe Stretch", icon: "🦶", tip: "Light stretches relax little muscles.", videoQuery: "light stretching before bed kids" },
        right: { label: "Big Yawn", icon: "🥱", tip: "Yawns are sleepy body signals.", videoQuery: "kids sleepy yawn bedtime" },
        result: "Body Relax Flow",
        resultIcon: "🌙",
        resultTip: "Stretching and slow yawns help bodies feel heavy and calm.",
        resultVideoQuery: "light bedtime stretches for kids",
      },
      {
        left: { label: "Warm Milk", icon: "🥛", tip: "A warm drink can feel cozy and soothing.", videoQuery: "warm milk bedtime kids" },
        right: { label: "Pillow Cuddle", icon: "🛏️", tip: "A favorite pillow makes bed feel inviting.", videoQuery: "cozy pillow bedtime kids" },
        result: "Sleepy Sip Set",
        resultIcon: "🥛",
        resultTip: "Comfort and warmth help bedtime feel gentle.",
        resultVideoQuery: "warm drink bedtime routine kids",
      },
      {
        left: { label: "Screen Off", icon: "📵", tip: "Turning screens off helps eyes and brains rest.", videoQuery: "no screens before bed kids" },
        right: { label: "Book Basket", icon: "🧺", tip: "Books are a calmer bedtime choice.", videoQuery: "books before bed for kids" },
        result: "Quiet Eyes Plan",
        resultIcon: "📚",
        resultTip: "Screens off and books nearby create a calmer evening routine.",
        resultVideoQuery: "screen free bedtime kids books",
      },
      {
        left: { label: "Star Projector", icon: "✨", tip: "Soft star lights can make bedrooms dreamy.", videoQuery: "star projector bedtime kids" },
        right: { label: "White Noise", icon: "🌬️", tip: "Gentle background sound can feel steady.", videoQuery: "white noise for kids sleep" },
        result: "Dream Cloud Space",
        resultIcon: "☁️",
        resultTip: "Soft room light and gentle sound can build a sleepy space.",
        resultVideoQuery: "sleep room white noise kids",
      },
      {
        left: { label: "Clean Sheets", icon: "🛏️", tip: "Fresh sheets make beds feel inviting.", videoQuery: "clean sheets bedtime kids" },
        right: { label: "Pillow Fluff", icon: "☁️", tip: "Fixing a pillow helps make bed feel cozy.", videoQuery: "make bed cozy for kids sleep" },
        result: "Cozy Nest Reset",
        resultIcon: "☁️",
        resultTip: "A comfy bed setup helps sleep feel easier.",
        resultVideoQuery: "cozy sleep setup for kids",
      },
      {
        left: { label: "Bedtime Song", icon: "🎶", tip: "Quiet songs help the room slow down.", videoQuery: "bedtime songs for kids" },
        right: { label: "Rocking Chair", icon: "🪑", tip: "Gentle rocking can calm busy bodies.", videoQuery: "gentle rocking before bed kids" },
        result: "Gentle Rhythm Wind-Down",
        resultIcon: "🎶",
        resultTip: "Soft music and slow rocking create a peaceful routine.",
        resultVideoQuery: "calm bedtime song rocking kids",
      },
      {
        left: { label: "Slow Count", icon: "🔢", tip: "Counting slowly helps busy thoughts fade.", videoQuery: "counting to sleep for kids" },
        right: { label: "Eye Close", icon: "😌", tip: "Resting eyes helps bodies notice sleep cues.", videoQuery: "close eyes relaxation for kids" },
        result: "Sleep Countdown",
        resultIcon: "🌠",
        resultTip: "Slow counting and closed eyes help the brain settle.",
        resultVideoQuery: "sleep countdown for kids bedtime",
      },
      {
        left: { label: "Room Cooldown", icon: "❄️", tip: "A cooler room can feel better for sleep.", videoQuery: "cool bedroom for kids sleep" },
        right: { label: "Pajama Socks", icon: "🧦", tip: "Comfy socks can make bedtime feel cozy.", videoQuery: "pajama socks bedtime kids" },
        result: "Comfy Sleep Setup",
        resultIcon: "🧦",
        resultTip: "A comfy body and room help bedtime feel settled.",
        resultVideoQuery: "comfortable sleep setup for kids",
      },
      {
        left: { label: "Teeth Floss", icon: "🧵", tip: "Flossing keeps bedtime care complete.", videoQuery: "flossing for kids bedtime" },
        right: { label: "Mouth Rinse", icon: "🚿", tip: "A quick rinse finishes the smile routine.", videoQuery: "mouth rinse for kids bedtime" },
        result: "Shine Smile Sleep",
        resultIcon: "😁",
        resultTip: "Finishing tooth care helps routines feel complete.",
        resultVideoQuery: "full teeth care bedtime routine kids",
      },
      {
        left: { label: "Alarm Set", icon: "⏰", tip: "Preparing for morning can calm bedtime worries.", videoQuery: "set alarm routine for kids" },
        right: { label: "Morning Clothes", icon: "👕", tip: "Clothes ready for tomorrow make mornings easier.", videoQuery: "prepare clothes for school kids" },
        result: "Easy Morning Prep",
        resultIcon: "🌅",
        resultTip: "Getting ready for tomorrow can make bedtime smoother tonight.",
        resultVideoQuery: "prepare for school bedtime routine kids",
      },
      {
        left: { label: "Night Lamp", icon: "🛋️", tip: "Soft lamps feel gentler than bright lights.", videoQuery: "soft lamp bedtime kids" },
        right: { label: "Soft Blanket", icon: "🪶", tip: "A light blanket can feel comforting and safe.", videoQuery: "soft blanket bedtime kids" },
        result: "Moonlight Snuggle",
        resultIcon: "🌙",
        resultTip: "Gentle light and soft fabric help create a cozy mood.",
        resultVideoQuery: "cozy bedroom bedtime kids",
      },
      {
        left: { label: "Stuffed Animal", icon: "🧸", tip: "A bedtime buddy can calm lonely feelings.", videoQuery: "stuffed animal sleep kids" },
        right: { label: "Bedtime Wish", icon: "💫", tip: "A happy wish can end the day softly.", videoQuery: "bedtime affirmations for kids" },
        result: "Dream Buddy Ritual",
        resultIcon: "💫",
        resultTip: "Comfort and kind thoughts help make bedtime gentle.",
        resultVideoQuery: "bedtime affirmation stuffed animal kids",
      },
      {
        left: { label: "Calm Stretch", icon: "🤸", tip: "Slow stretches help restless bodies unwind.", videoQuery: "calm stretches before bed kids" },
        right: { label: "Shoulder Roll", icon: "🔄", tip: "Small shoulder rolls release tightness.", videoQuery: "shoulder rolls bedtime kids" },
        result: "Sleepy Body Reset",
        resultIcon: "🫧",
        resultTip: "Gentle stretching and rolls help the body soften before sleep.",
        resultVideoQuery: "calm bedtime stretching kids",
      },
      {
        left: { label: "Window Curtains", icon: "🪟", tip: "Closing curtains blocks extra light.", videoQuery: "dark bedroom for kids sleep" },
        right: { label: "Quiet Clock", icon: "🕰️", tip: "A quiet room helps sleepy sounds stay soft.", videoQuery: "quiet room for kids sleep" },
        result: "Restful Room Check",
        resultIcon: "🏠",
        resultTip: "A dark quiet room can help sleep come faster.",
        resultVideoQuery: "sleep environment dark quiet kids",
      },
    ],
  },
]

export function createExplorerMissions() {
  return missionSeeds.map(buildMission)
}
