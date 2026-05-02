const mealBases = [
  {
    id: 'toast-stack',
    title: 'toast stack',
    moment: 'breakfast',
    effort: 'under-5',
    baseItem: 'Whole grain toast',
    addOn: 'yogurt swirl',
    needs: ['budget'],
    steps: ['Toast the base', 'Layer the toppings', 'Cut or plate and serve'],
  },
  {
    id: 'grain-bowl',
    title: 'grain bowl',
    moment: 'dinner',
    effort: 'under-15',
    baseItem: 'Brown rice bowl',
    addOn: 'herb dressing',
    needs: ['protein'],
    steps: ['Warm the grain base', 'Add the main toppings', 'Finish with the dressing and serve'],
  },
  {
    id: 'pita-pocket',
    title: 'pita pocket',
    moment: 'school-lunch',
    effort: 'under-15',
    baseItem: 'Wholemeal pita',
    addOn: 'crunchy side',
    needs: ['lunchbox-safe'],
    steps: ['Open the pita pocket', 'Fill with the ingredients', 'Pack or serve with the side'],
  },
  {
    id: 'smoothie-plate',
    title: 'smoothie plate',
    moment: 'after-school',
    effort: 'under-5',
    baseItem: 'Fruit smoothie cup',
    addOn: 'cracker side',
    needs: ['fussy-friendly'],
    steps: ['Blend the smoothie base', 'Add the extra topping or side', 'Serve straight away'],
  },
  {
    id: 'tray-bake',
    title: 'tray bake',
    moment: 'dinner',
    effort: 'make-ahead',
    baseItem: 'Roasted veggie tray',
    addOn: 'simple yogurt sauce',
    needs: ['fruit-veg'],
    steps: ['Lay the ingredients onto one tray', 'Roast or warm until ready', 'Serve with the sauce on the side'],
  },
]

const mealProteins = [
  { id: 'egg', title: 'egg', item: 'Boiled egg', needs: ['protein', 'budget'], benefit: 'longer-lasting fullness' },
  { id: 'chicken', title: 'chicken', item: 'Shredded chicken', needs: ['protein'], benefit: 'steady protein' },
  { id: 'beans', title: 'bean', item: 'Black beans', needs: ['protein', 'budget'], benefit: 'plant protein and fibre' },
  { id: 'yogurt', title: 'yogurt', item: 'Greek yogurt', needs: ['protein', 'fussy-friendly'], benefit: 'protein with a familiar creamy texture' },
  { id: 'tuna', title: 'tuna', item: 'Tuna mix', needs: ['protein', 'lunchbox-safe'], benefit: 'easy lunchbox protein' },
]

const mealProduce = [
  { id: 'berry', title: 'berry', item: 'Mixed berries', needs: ['fruit-veg', 'fussy-friendly'], benefit: 'colour and natural sweetness' },
  { id: 'cucumber', title: 'cucumber', item: 'Cucumber ribbons', needs: ['fruit-veg', 'lunchbox-safe'], benefit: 'cool crunch' },
  { id: 'tomato', title: 'tomato', item: 'Cherry tomatoes', needs: ['fruit-veg'], benefit: 'juicy freshness' },
  { id: 'broccoli', title: 'broccoli', item: 'Broccoli florets', needs: ['fruit-veg'], benefit: 'extra veg exposure' },
]

const snackProduce = [
  { id: 'apple', label: 'Apple slices', needs: ['fruit-veg', 'budget'], benefit: 'sweet crunch' },
  { id: 'banana', label: 'Banana coins', needs: ['fruit-veg', 'budget', 'fussy-friendly'], benefit: 'easy energy' },
  { id: 'berries', label: 'Berry cup', needs: ['fruit-veg', 'fussy-friendly'], benefit: 'colour and sweetness' },
  { id: 'pear', label: 'Pear wedges', needs: ['fruit-veg'], benefit: 'soft juicy bites' },
  { id: 'orange', label: 'Orange segments', needs: ['fruit-veg'], benefit: 'fresh citrus flavour' },
  { id: 'carrot', label: 'Carrot sticks', needs: ['fruit-veg', 'lunchbox-safe'], benefit: 'crunchy fibre' },
  { id: 'cucumber', label: 'Cucumber wheels', needs: ['fruit-veg', 'lunchbox-safe'], benefit: 'cool crunch' },
  { id: 'snap-peas', label: 'Snap peas', needs: ['fruit-veg', 'lunchbox-safe'], benefit: 'sweet green crunch' },
  { id: 'grapes', label: 'Grapes', needs: ['fruit-veg', 'lunchbox-safe'], benefit: 'easy lunchbox fruit' },
  { id: 'melon', label: 'Melon cubes', needs: ['fruit-veg', 'fussy-friendly'], benefit: 'hydrating sweetness' },
]

const snackPartners = [
  { id: 'cheese', label: 'Cheese cubes', effort: 'under-5', moment: 'after-school', needs: ['protein', 'fussy-friendly'], benefit: 'protein and savoury balance' },
  { id: 'yogurt', label: 'Yogurt dip', effort: 'under-5', moment: 'after-school', needs: ['protein', 'fussy-friendly'], benefit: 'creamy protein' },
  { id: 'hummus', label: 'Hummus cup', effort: 'under-5', moment: 'school-lunch', needs: ['protein', 'lunchbox-safe'], benefit: 'plant protein' },
  { id: 'peanut', label: 'Peanut or seed butter', effort: 'under-5', moment: 'breakfast', needs: ['protein'], benefit: 'healthy fats and staying power' },
  { id: 'popcorn', label: 'Air-popped popcorn', effort: 'under-5', moment: 'after-school', needs: ['budget', 'lunchbox-safe'], benefit: 'light crunch' },
  { id: 'crackers', label: 'Whole grain crackers', effort: 'under-5', moment: 'school-lunch', needs: ['budget', 'lunchbox-safe'], benefit: 'grain-based crunch' },
  { id: 'egg', label: 'Boiled egg halves', effort: 'under-15', moment: 'after-school', needs: ['protein'], benefit: 'strong protein' },
  { id: 'oat-bites', label: 'Homemade oat bites', effort: 'make-ahead', moment: 'school-lunch', needs: ['budget', 'make-ahead'], benefit: 'make-ahead convenience' },
  { id: 'trail-mix', label: 'Trail mix spoonful', effort: 'under-5', moment: 'after-school', needs: ['budget'], benefit: 'texture variety' },
  { id: 'milk', label: 'Milk box', effort: 'under-5', moment: 'school-lunch', needs: ['protein', 'lunchbox-safe'], benefit: 'easy drink pairing' },
]

const lunchboxBases = [
  { id: 'wrap', label: 'Turkey wrap pinwheels', effort: 'under-15', needs: ['lunchbox-safe', 'protein'] },
  { id: 'sandwich', label: 'Egg sandwich fingers', effort: 'make-ahead', needs: ['lunchbox-safe', 'budget', 'protein'] },
  { id: 'pasta', label: 'Chicken pasta cup', effort: 'under-15', needs: ['lunchbox-safe', 'protein'] },
  { id: 'pancake', label: 'Mini oat pancakes', effort: 'make-ahead', needs: ['lunchbox-safe', 'fussy-friendly'] },
  { id: 'crackers', label: 'Cheese and cracker stack', effort: 'under-5', needs: ['lunchbox-safe', 'budget'] },
]

const lunchboxFresh = [
  { id: 'berries', label: 'Berries', needs: ['fruit-veg', 'fussy-friendly'] },
  { id: 'cucumber', label: 'Cucumber rounds', needs: ['fruit-veg', 'lunchbox-safe'] },
  { id: 'carrot', label: 'Carrot sticks', needs: ['fruit-veg', 'budget'] },
  { id: 'grapes', label: 'Grapes', needs: ['fruit-veg', 'lunchbox-safe'] },
  { id: 'pear', label: 'Pear slices', needs: ['fruit-veg', 'fussy-friendly'] },
]

const lunchboxExtras = [
  { id: 'popcorn', label: 'Popcorn', needs: ['budget', 'lunchbox-safe'] },
  { id: 'yogurt', label: 'Yogurt pot', needs: ['protein', 'fussy-friendly'] },
  { id: 'cheese', label: 'Cheese cubes', needs: ['protein', 'lunchbox-safe'] },
  { id: 'oat-bites', label: 'Oat bites', needs: ['budget', 'make-ahead'] },
]

function uniqueNeeds(...lists) {
  return [...new Set(lists.flat())]
}

function minutesForEffort(effort) {
  if (effort === 'under-5') return '5 min'
  if (effort === 'under-15') return '12 min'
  return '15 min prep'
}

function generateMealIdeas() {
  return mealBases.flatMap((base) =>
    mealProteins.flatMap((protein) =>
      mealProduce.map((produce) => ({
        id: `meal-${base.id}-${protein.id}-${produce.id}`,
        module: 'meal',
        title: `${produce.title} ${protein.title} ${base.title}`,
        moment: base.moment,
        effort: base.effort,
        needs: uniqueNeeds(base.needs, protein.needs, produce.needs),
        timeLabel: minutesForEffort(base.effort),
        summary: `A ${base.moment.replace('-', ' ')} idea that combines ${protein.item.toLowerCase()} with ${produce.item.toLowerCase()} in a repeatable family format.`,
        items: [base.baseItem, protein.item, produce.item, base.addOn],
        steps: [
          base.steps[0],
          `Add ${protein.item.toLowerCase()} and ${produce.item.toLowerCase()}.`,
          base.steps[2],
        ],
        benefit: `This adds ${protein.benefit} plus ${produce.benefit} without making the meal feel complicated.`,
      }))
    )
  )
}

function generateSnackIdeas() {
  return snackProduce.flatMap((produce) =>
    snackPartners.map((partner) => ({
      id: `snack-${produce.id}-${partner.id}`,
      module: 'snack',
      title: `${produce.label} + ${partner.label}`,
      moment: partner.moment,
      effort: partner.effort,
      needs: uniqueNeeds(produce.needs, partner.needs),
      timeLabel: minutesForEffort(partner.effort),
      summary: `A fast snack pairing that gives ${produce.benefit} with ${partner.benefit}.`,
      pairLeft: produce.label,
      pairRight: partner.label,
      serving: `Serve ${produce.label.toLowerCase()} with ${partner.label.toLowerCase()} on one small plate or in one snack box.`,
      reason: 'This keeps snack time simple while making the more filling option easy to choose.',
      parentMove: 'Plate it before your child asks for a snack so the healthier option is already the easy option.',
    }))
  )
}

function generateLunchboxIdeas() {
  return lunchboxBases.flatMap((base) =>
    lunchboxFresh.flatMap((fresh) =>
      lunchboxExtras.map((extra) => ({
        id: `lunchbox-${base.id}-${fresh.id}-${extra.id}`,
        module: 'lunchbox',
        title: `${base.label} lunchbox`,
        moment: 'school-lunch',
        effort: base.effort,
        needs: uniqueNeeds(base.needs, fresh.needs, extra.needs),
        base: base.label,
        fresh: fresh.label,
        extra: extra.label,
        packTip: `Pack ${base.label.toLowerCase()} with ${fresh.label.toLowerCase()} and ${extra.label.toLowerCase()} so the lunchbox feels complete without extra searching.`,
        parentMove: 'Use the same lunchbox formula more than once in the week so morning prep stays realistic.',
      }))
    )
  )
}

export const mealIdeaItems = generateMealIdeas()
export const snackIdeaItems = generateSnackIdeas()
export const lunchboxIdeaItems = generateLunchboxIdeas()

export const nutritionToolItems = [
  ...mealIdeaItems,
  ...snackIdeaItems,
  ...lunchboxIdeaItems,
]

export const nutritionQuickStarts = [
  {
    id: 'quick-afterschool',
    label: 'After-school rescue',
    module: 'snack',
    moment: 'after-school',
    effort: 'all',
    need: 'fussy-friendly',
  },
  {
    id: 'quick-breakfast',
    label: '5-minute breakfast',
    module: 'meal',
    moment: 'breakfast',
    effort: 'under-5',
    need: 'all',
  },
  {
    id: 'quick-lunchbox',
    label: 'Lunchbox tomorrow',
    module: 'lunchbox',
    moment: 'school-lunch',
    effort: 'all',
    need: 'lunchbox-safe',
  },
  {
    id: 'quick-budget',
    label: 'Budget-friendly ideas',
    module: 'all',
    moment: 'all',
    effort: 'all',
    need: 'budget',
  },
]
