from models import get_db

# Comprehensive dictionary of 5-letter English words
DICTIONARY = {
    # A
    "ABACK", "ABASE", "ABATE", "ABBEY", "ABBOT", "ABIDE", "ABODE", "ABORT", "ABOUT", "ABOVE",
    "ABUSE", "ABYSS", "ACORN", "ACRID", "ACTOR", "ACUTE", "ADAGE", "ADAPT", "ADDED", "ADEPT",
    "ADMIN", "ADMIT", "ADOBE", "ADOPT", "ADORE", "ADORN", "ADULT", "AEGIS", "AFFIX", "AFOUL",
    "AFTER", "AGAIN", "AGAPE", "AGATE", "AGENT", "AGILE", "AGING", "AGLOW", "AGONY", "AGREE",
    "AHEAD", "AIDED", "AIDER", "AIDES", "AIMED", "AIMER", "AIRED", "AISLE", "ALARM", "ALBUM",
    "ALERT", "ALGAE", "ALIBI", "ALIEN", "ALIGN", "ALIKE", "ALIVE", "ALLAY", "ALLEY", "ALLOT",
    "ALLOW", "ALLOY", "ALOFT", "ALOHA", "ALONE", "ALONG", "ALOOF", "ALOUD", "ALPHA", "ALTAR",
    "ALTER", "AMASS", "AMAZE", "AMBER", "AMBLE", "AMEND", "AMISS", "AMITY", "AMONG", "AMOUR",
    "AMPLE", "AMPLY", "AMUSE", "ANGEL", "ANGER", "ANGLE", "ANGRY", "ANGST", "ANIME", "ANKLE",
    "ANNEX", "ANNOY", "ANNUL", "ANODE", "ANTIC", "ANVIL", "AORTA", "APACE", "APART", "APHID",
    "APING", "APNEA", "APPLY", "APPLE", "APRON", "APTLY", "ARBOR", "ARDOR", "ARENA", "ARGUE",
    "ARISE", "ARMED", "ARMOR", "AROMA", "AROSE", "ARRAY", "ARROW", "ARSON", "ARTSY", "ASCOT",
    "ASHEN", "ASIDE", "ASKED", "ASKEW", "ASPEN", "ASSAY", "ASSET", "ASTER", "ATOLL", "ATOMS",
    "ATONE", "ATTIC", "AUDIO", "AUDIT", "AUGUR", "AUNTY", "AURAL", "AURAS", "AUTOS", "AVAIL",
    "AVERT", "AVIAN", "AVOID", "AWAIT", "AWAKE", "AWARD", "AWARE", "AWASH", "AWFUL", "AWOKE",
    "AXIAL", "AXIOM", "AXLES", "AZURE",

    # B
    "BACON", "BADGE", "BADLY", "BAGEL", "BAGGY", "BAKER", "BAKES", "BALMY", "BANAL", "BANJO",
    "BARGE", "BARON", "BASAL", "BASIC", "BASIN", "BASIS", "BASTE", "BATCH", "BATHS", "BATON",
    "BATTY", "BAYOU", "BEACH", "BEADY", "BEAMS", "BEANS", "BEARD", "BEAST", "BEATS", "BEECH",
    "BEEFY", "BEFOG", "BEGAN", "BEGET", "BEGIN", "BEGUN", "BEING", "BELCH", "BELIE", "BELLE",
    "BELLS", "BELLY", "BELOW", "BELTS", "BENCH", "BERET", "BERRY", "BERTH", "BESET", "BETEL",
    "BEVEL", "BEZEL", "BIBLE", "BICEP", "BIDES", "BINGO", "BIPED", "BIRCH", "BIRDS", "BIRTH",
    "BISON", "BITCH", "BITER", "BITES", "BITTY", "BLACK", "BLADE", "BLAME", "BLAND", "BLANK",
    "BLARE", "BLAST", "BLAZE", "BLEAK", "BLEAT", "BLEED", "BLEEP", "BLEND", "BLESS", "BLIMP",
    "BLIND", "BLINK", "BLISS", "BLITZ", "BLOAT", "BLOCK", "BLOKE", "BLOND", "BLOOD", "BLOOM",
    "BLOWN", "BLOWS", "BLUER", "BLUES", "BLUFF", "BLUNT", "BLURB", "BLURT", "BLUSH", "BOARD",
    "BOAST", "BOATS", "BOBBY", "BOGEY", "BOILS", "BOLTS", "BOMBS", "BONDS", "BONES", "BONUS",
    "BOOBY", "BOOKS", "BOOST", "BOOTH", "BOOTS", "BOOTY", "BOOZE", "BOOZY", "BORAX", "BORED",
    "BORES", "BORNE", "BOSOM", "BOSSY", "BOTCH", "BOUGH", "BOULE", "BOUND", "BOWEL", "BOXER",
    "BOXES", "BRACE", "BRAID", "BRAIN", "BRAKE", "BRAND", "BRASH", "BRASS", "BRAVE", "BRAVO",
    "BRAWL", "BRAWN", "BREAD", "BREAK", "BREED", "BRIAR", "BRIBE", "BRICK", "BRIDE", "BRIEF",
    "BRINE", "BRING", "BRINK", "BRINY", "BROAD", "BROIL", "BROKE", "BROOD", "BROOK", "BROOM",
    "BROTH", "BROWN", "BROWS", "BRUNT", "BRUSH", "BRUTE", "BUDDY", "BUDGE", "BUGGY", "BUGLE",
    "BUILD", "BUILT", "BULGE", "BULKY", "BULLY", "BUNCH", "BUNNY", "BURNT", "BURRO", "BURST",
    "BUSES", "BUSHY", "BUTCH", "BUTTE", "BUXOM", "BUYER", "BYLAW",

    # C
    "CABIN", "CABLE", "CACAO", "CACHE", "CACTI", "CADDY", "CADET", "CAGEY", "CAIRN", "CAMEL",
    "CAMEO", "CANAL", "CANDY", "CANNY", "CANOE", "CANON", "CAPER", "CARAT", "CARGO", "CAROL",
    "CARRY", "CARVE", "CASTE", "CATCH", "CATER", "CATTY", "CAULK", "CAUSE", "CAVIL", "CEDAR",
    "CHAFE", "CHAFF", "CHAIN", "CHAIR", "CHALK", "CHAMP", "CHANT", "CHAOS", "CHARD", "CHARM",
    "CHART", "CHASE", "CHASM", "CHEAP", "CHEAT", "CHECK", "CHEEK", "CHEER", "CHEESE", "CHEFS",
    "CHESS", "CHEST", "CHICK", "CHIDE", "CHIEF", "CHILD", "CHILI", "CHIME", "CHINA", "CHIRP",
    "CHOCK", "CHOIR", "CHOKE", "CHORD", "CHORE", "CHOSE", "CHUCK", "CHUMP", "CHUNK", "CHURN",
    "CHUTE", "CIDER", "CIGAR", "CINCH", "CIRCA", "CIVIC", "CIVIL", "CLACK", "CLAIM", "CLAMP",
    "CLAMY", "CLANG", "CLANK", "CLASH", "CLASP", "CLASS", "CLEAN", "CLEAR", "CLEAT", "CLEFT",
    "CLERK", "CLICK", "CLIFF", "CLIMB", "CLING", "CLINK", "CLOAK", "CLOCK", "CLONE", "CLOSE",
    "CLOTH", "CLOUD", "CLOUT", "CLOVE", "CLOWN", "CLUBS", "CLUCK", "CLUES", "CLUMP", "CLUNG",
    "COACH", "COAST", "COBRA", "COCOA", "COLON", "COLOR", "COMET", "COMFY", "COMIC", "COMMA",
    "CONCH", "CONDO", "CONES", "CONIC", "COPRA", "CORAL", "CORDS", "CORER", "CORNY", "COUCH",
    "COUGH", "COULD", "COUNT", "COUPE", "COURT", "COVEN", "COVER", "COVET", "COVEY", "COWER",
    "COYLY", "CRABS", "CRACK", "CRAFT", "CRANE", "CRANK", "CRASH", "CRASS", "CRATE", "CRAVE",
    "CRAWL", "CRAZE", "CRAZY", "CREAK", "CREAM", "CREDO", "CREED", "CREEK", "CREEP", "CREME",
    "CREPE", "CREPT", "CRESS", "CREST", "CRICK", "CRIED", "CRIER", "CRIES", "CRIME", "CRIMP",
    "CRISP", "CROAK", "CROCK", "CRONE", "CRONY", "CROOK", "CROSS", "CROUP", "CROWD", "CROWN",
    "CRUDE", "CRUEL", "CRUMB", "CRUMP", "CRUSH", "CRUST", "CRYPT", "CUBIC", "CUBIT", "CUPID",
    "CURER", "CURIO", "CURLY", "CURRY", "CURSE", "CURVE", "CURVY", "CUTIE", "CYBER", "CYCLE", "CYNIC",

    # D
    "DADDY", "DAILY", "DAIRY", "DAISY", "DALES", "DALLY", "DANCE", "DANDY", "DATED", "DATES",
    "DATUM", "DAUNT", "DEALS", "DEALT", "DEATH", "DEBAR", "DEBIT", "DEBUG", "DEBUT", "DECAL",
    "DECAY", "DECOR", "DECOY", "DECRY", "DEFER", "DEIGN", "DEITY", "DELAY", "DELTA", "DELVE",
    "DEMON", "DEMUR", "DENIM", "DENSE", "DEPOT", "DEPTH", "DERBY", "DETER", "DETOX", "DEUCE",
    "DEVIL", "DIARY", "DICEY", "DIGIT", "DILLY", "DIMLY", "DINER", "DINGO", "DINGY", "DIODE",
    "DIRGE", "DIRTY", "DISCO", "DITCH", "DITTO", "DITTY", "DIVER", "DIVOT", "DIZZY", "DODGE",
    "DODGY", "DOGMA", "DOING", "DOLLY", "DONOR", "DONUT", "DOPEY", "DOUBT", "DOUGH", "DOWEL",
    "DOWNY", "DOWRY", "DOZEN", "DRAFT", "DRAIN", "DRAKE", "DRAMA", "DRANK", "DRAPE", "DRAWL",
    "DRAWN", "DRAWS", "DREAM", "DRESS", "DRIED", "DRIFT", "DRILL", "DRINK", "DRIVE", "DROLL",
    "DRONE", "DROOL", "DROOP", "DROPS", "DROSS", "DROVE", "DROWN", "DRUID", "DRUNK", "DRYER",
    "DRYLY", "DUCHY", "DULLY", "DUMMY", "DUMPS", "DUMPY", "DUNCE", "DUNES", "DUSTS", "DUSTY",
    "DUTCH", "DUVET", "DWELL", "DWELT", "DYING",

    # E
    "EAGLE", "EARLY", "EARTH", "EASEL", "EATEN", "EATER", "EBBED", "EBONY", "ECLAT", "EDICT",
    "EDIFY", "EERIE", "EGRET", "EIGHT", "EJECT", "EKING", "ELATE", "ELBOW", "ELDER", "ELECT",
    "ELEGY", "ELFIN", "ELIDE", "ELITE", "ELOPE", "ELUDE", "EMAIL", "EMBED", "EMBER", "EMCEE",
    "EMERY", "EMITS", "EMPTY", "ENACT", "ENDOW", "ENEMA", "ENEMY", "ENJOY", "ENNUI", "ENTER",
    "ENTRY", "ENVOY", "EPOCH", "EPOXY", "EQUAL", "EQUIP", "ERASE", "ERECT", "ERODE", "ERROR",
    "ERUPT", "ESSAY", "ESTER", "ETHER", "ETHIC", "ETHOS", "ETUDE", "EVADE", "EVENS", "EVENT",
    "EVERY", "EVICT", "EVOKE", "EXACT", "EXALT", "EXAMS", "EXCEL", "EXERT", "EXILE", "EXIST",
    "EXITS", "EXPEL", "EXTRA", "EXULT", "EYING",

    # F
    "FABLE", "FACET", "FAINT", "FAITH", "FALLS", "FALSE", "FANCY", "FANNY", "FARCE", "FATAL",
    "FATES", "FATTY", "FAULT", "FAUNA", "FAVOR", "FEAST", "FECAL", "FEIGN", "FEINT", "FELLA",
    "FELON", "FEMUR", "FENCE", "FERAL", "FERRY", "FETAL", "FETCH", "FETID", "FETUS", "FEVER",
    "FEWER", "FIBER", "FICUS", "FIELD", "FIEND", "FIERY", "FIFTH", "FIFTY", "FIGHT", "FILER",
    "FILES", "FILET", "FILLY", "FILMS", "FILMY", "FILTH", "FINAL", "FINCH", "FINDS", "FINER",
    "FINES", "FINIS", "FINNY", "FIRED", "FIRES", "FIRMS", "FIRST", "FISHY", "FISTS", "FITLY",
    "FIVER", "FIVES", "FIXED", "FIXER", "FIXES", "FIZZY", "FJORD", "FLACK", "FLAGS", "FLAIL",
    "FLAIR", "FLAKE", "FLAKY", "FLAME", "FLANK", "FLAPS", "FLARE", "FLASH", "FLASK", "FLATS",
    "FLAWS", "FLEAS", "FLECK", "FLEET", "FLESH", "FLICK", "FLIER", "FLIES", "FLING", "FLINT",
    "FLIRT", "FLOAT", "FLOCK", "FLOOD", "FLOOR", "FLORA", "FLOSS", "FLOUR", "FLOUT", "FLOWN",
    "FLOWS", "FLUID", "FLUKE", "FLUME", "FLUNG", "FLUNK", "FLUSH", "FLUTE", "FLYER", "FOAMY",
    "FOCAL", "FOCUS", "FOGGY", "FOILS", "FOIST", "FOLIO", "FOLKS", "FOLKY", "FOLLY", "FORAY",
    "FORCE", "FORGE", "FORGO", "FORMS", "FORTE", "FORTH", "FORTY", "FORUM", "FOUND", "FOUNT",
    "FOURS", "FOWLS", "FOXES", "FOYER", "FRAIL", "FRAME", "FRANK", "FRAUD", "FREAK", "FREED",
    "FREER", "FREES", "FRESH", "FRIAR", "FRIED", "FRIES", "FRILL", "FRISK", "FRITZ", "FROCK",
    "FROGS", "FROND", "FRONT", "FROST", "FROTH", "FROWN", "FROZE", "FRUIT", "FUDGE", "FUELS",
    "FUGUE", "FULLY", "FUMED", "FUMES", "FUNDS", "FUNGI", "FUNKY", "FUNNY", "FURRY", "FUSED",
    "FUSES", "FUZZY",

    # G
    "GAFFE", "GAILY", "GAINS", "GAMER", "GAMES", "GAMMA", "GAMUT", "GANGS", "GARBS", "GASES",
    "GASPS", "GASSY", "GATED", "GATES", "GAUDY", "GAUGE", "GAUNT", "GAUZE", "GAVEL", "GAWKY",
    "GAYLY", "GAZER", "GAZES", "GEARS", "GECKO", "GEESE", "GENES", "GENIE", "GENRE", "GENTS",
    "GENUS", "GEEKS", "GEEKY", "GHOST", "GIANT", "GIDDY", "GIFTS", "GILDS", "GILLS", "GIMME",
    "GIMPY", "GIRLS", "GIRTH", "GIVEN", "GIVER", "GIVES", "GIZMO", "GLADE", "GLAND", "GLARE",
    "GLASS", "GLAZE", "GLEAM", "GLEAN", "GLIDE", "GLINT", "GLOAT", "GLOBE", "GLOOM", "GLORY",
    "GLOSS", "GLOVE", "GLOWS", "GLUES", "GLUEY", "GLYPH", "GNARL", "GNASH", "GNATS", "GNAWS",
    "GNOME", "GOATS", "GODLY", "GOING", "GOLEM", "GONER", "GOODS", "GOODY", "GOOFY", "GOOSE",
    "GORED", "GORES", "GORGE", "GORSE", "GOUGE", "GOURD", "GRACE", "GRADE", "GRAFT", "GRAIL",
    "GRAIN", "GRAMS", "GRAND", "GRANT", "GRAPE", "GRAPH", "GRASP", "GRASS", "GRATE", "GRAVE",
    "GRAVY", "GRAZE", "GREAT", "GREED", "GREEN", "GREET", "GRIEF", "GRILL", "GRIME", "GRIMY",
    "GRIND", "GRIPS", "GRIST", "GRITS", "GROAN", "GROIN", "GROOM", "GROPE", "GROSS", "GROUP",
    "GROUT", "GROVE", "GROWL", "GROWN", "GROWS", "GRUBS", "GRUEL", "GRUFF", "GRUNT", "GUARD",
    "GUAVA", "GUESS", "GUEST", "GUIDE", "GUILD", "GUILE", "GUILT", "GUISE", "GULCH", "GULLY",
    "GUMBO", "GUMMY", "GUPPY", "GUSTS", "GUSTY", "GUTSY", "GYPSY",

    # H
    "HABIT", "HACKS", "HAILS", "HAIRS", "HAIRY", "HALVE", "HANDS", "HANDY", "HANGS", "HAPPY",
    "HARDY", "HARES", "HARMS", "HARPS", "HARSH", "HASPS", "HASTE", "HASTY", "HATCH", "HATER",
    "HATES", "HAUNT", "HAVEN", "HAVOC", "HAWKS", "HAZEL", "HEADS", "HEADY", "HEALS", "HEAPS",
    "HEARD", "HEART", "HEATS", "HEATH", "HEAVE", "HEAVY", "HEDGE", "HEEDS", "HEELS", "HEFTY",
    "HEIRS", "HEIST", "HELLO", "HELMS", "HELPS", "HENCE", "HENNA", "HERBS", "HERDS", "HERON",
    "HIDES", "HIKER", "HIKES", "HILLS", "HILLY", "HILTS", "HINGE", "HINTS", "HIPPO", "HIPPY",
    "HIRED", "HIRES", "HISTO", "HITCH", "HIVES", "HOARD", "HOBBY", "HOIST", "HOLDS", "HOLES",
    "HOLLY", "HOMES", "HOMEY", "HONED", "HONES", "HONEY", "HONKS", "HONOR", "HOODS", "HOOKS",
    "HOOPS", "HOOTS", "HOPES", "HORDE", "HORNS", "HORNY", "HORSE", "HOSES", "HOSTS", "HOTEL",
    "HOUND", "HOURS", "HOUSE", "HOVER", "HOWLS", "HUMAN", "HUMID", "HUMOR", "HUMPS", "HUNCH",
    "HUNKS", "HUNTS", "HURLS", "HURRY", "HURTS", "HUSKS", "HUSKY", "HUTCH", "HYDRA", "HYENA",
    "HYMNS", "HYPER",

    # I
    "ICING", "ICONS", "IDEAL", "IDEAS", "IDIOM", "IDIOT", "IDLER", "IDLES", "IDOLS", "IGLOO",
    "IMAGE", "IMBUE", "IMPEL", "IMPLY", "INANE", "INBOX", "INCUR", "INDEX", "INDIAN", "INDICT",
    "INDIE", "INERT", "INFER", "INFRA", "INGOT", "INLAY", "INLET", "INNER", "INPUT", "INSET",
    "INTEL", "INTER", "INTRO", "IONIC", "IRATE", "IRONS", "IRONY", "ISLES", "ISSUE", "ITCHY",
    "ITEMS", "IVORY",

    # J
    "JACKS", "JADED", "JADES", "JAGGY", "JAILS", "JAUNT", "JAZZY", "JEANS", "JELLY", "JENNY",
    "JERKS", "JERKY", "JESTS", "JEWEL", "JIFFY", "JILTS", "JIVES", "JOINS", "JOINT", "JOKER",
    "JOKES", "JOLLY", "JOLTS", "JOUST", "JUDGE", "JUICE", "JUICY", "JUMBO", "JUMPS", "JUMPY",
    "JUNKS", "JUNKY", "JUNTA", "JURY",

    # K
    "KAPUT", "KARAT", "KARMA", "KAYAK", "KAZOO", "KEBAB", "KEELS", "KEENER", "KEEPER", "KEEPS",
    "KELP", "KHAKI", "KICKS", "KILLS", "KILNS", "KILTS", "KINDS", "KINGS", "KINKS", "KINKY",
    "KIOSK", "KISSES", "KITES", "KITTY", "KIWIS", "KNACK", "KNEAD", "KNEEL", "KNEES", "KNELL",
    "KNELT", "KNIFE", "KNITS", "KNOBS", "KNOCK", "KNOLL", "KNOTS", "KNOWN", "KNOWS", "KOALA",
    "KRAFT", "KUDOS",

    # L
    "LABEL", "LABOR", "LACES", "LACKS", "LADEN", "LADLE", "LAGS", "LAIRS", "LAKES", "LAMBS",
    "LAMELY", "LAMPS", "LANCE", "LANDS", "LANES", "LAPEL", "LAPSE", "LARCH", "LARGE", "LARKS",
    "LASER", "LASHES", "LASTS", "LATCH", "LATER", "LATEX", "LATHE", "LATIN", "LATTE", "LAUGH",
    "LAWNS", "LAYER", "LAZY", "LEADS", "LEAFY", "LEAKS", "LEAKY", "LEANS", "LEAPS", "LEAPT",
    "LEARN", "LEASE", "LEASH", "LEAST", "LEAVE", "LEDGE", "LEECH", "LEEKS", "LEERS", "LEFTS",
    "LEFTY", "LEGAL", "LEGGY", "LEMON", "LEMUR", "LENDS", "LENSES", "LEPER", "LEVEL", "LEVER",
    "LIBEL", "LIBRA", "LICKS", "LIENS", "LIFTS", "LIGHT", "LIKES", "LILAC", "LIMBS", "LIMES",
    "LIMIT", "LIMPS", "LINEN", "LINER", "LINES", "LINGO", "LINKS", "LIONS", "LIPS", "LISPS",
    "LISTS", "LITER", "LITHE", "LIVER", "LIVID", "LLAMA", "LOADS", "LOAFS", "LOAMY", "LOANS",
    "LOATH", "LOBBY", "LOBES", "LOCAL", "LOCKS", "LOCUST", "LODGE", "LOFTS", "LOFTY", "LOGIC",
    "LOGIN", "LOGS", "LONER", "LONGS", "LOOKS", "LOOMS", "LOONS", "LOOPS", "LOOSE", "LOOTS",
    "LORDS", "LORRY", "LOSER", "LOSES", "LOSSES", "LOTUS", "LOUDER", "LOUDLY", "LOUSE", "LOUSY",
    "LOVER", "LOVES", "LOWER", "LOWLY", "LOYAL", "LUCID", "LUCKY", "LUCRE", "LUGS", "LULLS",
    "LUMEN", "LUMPS", "LUMPY", "LUNAR", "LUNCH", "LUNGS", "LURCH", "LURES", "LURID", "LURKS",
    "LUSTS", "LUSTY", "LYING", "LYMPH", "LYRIC",

    # M
    "MACAW", "MACHO", "MACRO", "MADAM", "MADLY", "MAFIA", "MAGIC", "MAGMA", "MAIDS", "MAILS",
    "MAINLY", "MAJOR", "MAKER", "MAKES", "MALES", "MALLS", "MALTS", "MAMBA", "MANGO", "MANIA",
    "MANIC", "MANOR", "MAPLE", "MARCH", "MARRY", "MARSH", "MATCH", "MATES", "MATHS", "MAYBE",
    "MAYOR", "MEALY", "MEANS", "MEANT", "MEATS", "MEATY", "MEDAL", "MEDIA", "MEDIC", "MEETS",
    "MELON", "MELTS", "MEMOS", "MERCY", "MERGE", "MERIT", "MERRY", "MESSY", "METAL", "METER",
    "METRO", "MICRO", "MIDST", "MIGHT", "MILES", "MILKY", "MILLS", "MIMIC", "MINCE", "MINDS",
    "MINER", "MINES", "MINIS", "MINOR", "MINTS", "MINTY", "MINUS", "MIRTH", "MISER", "MISSED",
    "MISSES", "MISTS", "MISTY", "MITTS", "MIXED", "MIXER", "MIXES", "MODEL", "MODEM", "MOIST",
    "MOLAR", "MOLDS", "MOLDY", "MOLES", "MONEY", "MONKS", "MONTH", "MOODS", "MOODY", "MOONS",
    "MOOSE", "MORAL", "MORON", "MORPH", "MOTEL", "MOTOR", "MOTTO", "MOUNT", "MOURN", "MOUSE",
    "MOUTH", "MOVER", "MOVES", "MOVIE", "MOWER", "MUCUS", "MUDDY", "MUGGY", "MULES", "MULTI",
    "MUMMY", "MURKY", "MUSIC", "MUSKY", "MUSTY", "MUTED", "MYTHS",

    # N
    "NACHO", "NAILS", "NAIVE", "NAKED", "NAMED", "NAMES", "NANNY", "NASAL", "NASTY", "NATAL",
    "NAVAL", "NAVEL", "NAVY", "NEARS", "NEATLY", "NECKS", "NEEDS", "NEEDY", "NEIGH", "NERVE",
    "NERVY", "NESTS", "NEVER", "NEWLY", "NICER", "NICELY", "NICEST", "NICHE", "NICKS", "NIGHT",
    "NINTH", "NOBLE", "NOBLY", "NOISE", "NOISY", "NOMAD", "NOODLE", "NOOKS", "NOOSE", "NORTH",
    "NOSES", "NOSY", "NOTCH", "NOTED", "NOTES", "NOVEL", "NUDGE", "NURSE", "NUTTY", "NYMPH",

    # O
    "OAKEN", "OAKS", "OASIS", "OATS", "OBESE", "OBEYS", "OCCUR", "OCEAN", "OCTAL", "OCTET",
    "ODDLY", "ODORS", "OFFER", "OFTEN", "OILS", "OILY", "OKRA", "OLDEN", "OLDER", "OLDEST",
    "OLIVE", "OMEGA", "OMENS", "OMITS", "ONION", "ONSET", "OPENER", "OPENLY", "OPENS", "OPERA",
    "OPTIC", "ORBIT", "ORDER", "ORGAN", "OTHER", "OTTER", "OUGHT", "OUNCE", "OUTDO", "OUTER",
    "OUTFIT", "OUTLET", "OUTPUT", "OVALS", "OVARY", "OVENS", "OVERT", "OWING", "OWLS", "OWNED",
    "OWNER", "OWNS", "OXIDE", "OZONE",

    # P
    "PACES", "PACKS", "PACTS", "PADDY", "PAGER", "PAGES", "PAILS", "PAINS", "PAINT", "PAIRS",
    "PALES", "PALMS", "PALSY", "PANDA", "PANEL", "PANIC", "PANTS", "PAPAL", "PAPER", "PARCH",
    "PARKS", "PARRY", "PARSE", "PARTS", "PARTY", "PASSE", "PASTA", "PASTE", "PASTY", "PATCH",
    "PATIO", "PATTY", "PAUSE", "PAVED", "PAVES", "PAWNS", "PAYEE", "PAYER", "PEACE", "PEACH",
    "PEAKS", "PEALS", "PEARL", "PEARS", "PECAN", "DECKS", "PECKS", "PEDAL", "PEEKS", "PEELS",
    "PEEPS", "PEERS", "PENAL", "PENCE", "PENNY", "PERCH", "PERIL", "PERKS", "PERKY", "PESKY",
    "PETAL", "PETTY", "PHASE", "PHONE", "PHONY", "PHOTO", "PIANO", "PICKS", "PICKY", "PIECE",
    "PIERS", "PIETY", "PIGGY", "PIKES", "PILES", "PILLS", "PILOT", "PINCH", "PINES", "PINEY",
    "PINKS", "PINTO", "PIOUS", "PIPER", "PIPES", "PIQUE", "PITCH", "PIVOT", "PIXEL", "PIZZA",
    "PLACE", "PLAID", "PLAIN", "PLAIT", "PLANE", "PLANK", "PLANS", "PLANT", "PLATE", "PLAZA",
    "PLEAD", "PLEAS", "PLIED", "PLIES", "PLOTS", "PLOWS", "PLUCK", "PLUGS", "PLUMB", "PLUME",
    "PLUMP", "PLUMS", "PLUSH", "POACH", "POEMS", "POETS", "POINT", "POISE", "POKER", "POLAR",
    "POLKA", "POLLS", "POLYP", "PONDS", "POOCH", "POOLS", "POPPY", "PORCH", "PORES", "POUCH",
    "POUND", "POURS", "POUTS", "POWER", "PRANK", "PRAWN", "PRAYS", "PREEN", "PRESS", "PRICE",
    "PRICEY", "PRICK", "PRIDE", "PRIED", "PRIES", "PRIME", "PRIMO", "PRINT", "PRIOR", "PRISM",
    "PRIVY", "PRIZE", "PROBE", "PROMS", "PRONE", "PROOF", "PROPS", "PROSE", "PROUD", "PROVE",
    "PROWL", "PROXY", "PRUNE", "PSALM", "PUBIC", "PUFFS", "PUFFY", "PULLS", "PULPY", "PULSE",
    "PUMAS", "PUMPS", "PUNCH", "PUPAL", "PUPIL", "PUPPY", "PUREE", "PURER", "PURGE", "PURSE",
    "PUSHY", "PUTTY", "PYGMY",

    # Q
    "QUACK", "QUAFF", "QUAIL", "QUAKE", "QUALM", "QUARK", "QUART", "QUASH", "QUASI", "QUEEN",
    "QUEER", "QUELL", "QUERIES", "QUERY", "QUEST", "QUEUE", "QUICK", "QUIET", "QUILL", "QUILT",
    "QUIRK", "QUITE", "QUOTA", "QUOTE",

    # R
    "RACER", "RACES", "RACKS", "RADAR", "RADII", "RADIO", "RADON", "RAFTS", "RAGES", "RAIDS",
    "RAILS", "RAINS", "RAINY", "RAISE", "RAJAH", "RALLY", "RAMPS", "RANCH", "RANDOM", "RANGE",
    "RANKS", "RANTS", "RAPID", "RARER", "RASPY", "RATED", "RATES", "RATIO", "RAVEN", "RAYON",
    "RAZOR", "REACH", "REACT", "READS", "READY", "REALM", "REALS", "REAMS", "REAPS", "REARM",
    "REARS", "REBEL", "REBUS", "RECAP", "RECUR", "REDOX", "REEDS", "REEDY", "REEFS", "REEKS",
    "REELS", "REFER", "REFIT", "REGAL", "REHAB", "REIGN", "REINS", "RELAX", "RELAY", "RELIC",
    "REMIT", "RENAL", "RENEW", "RENTS", "REPAY", "REPEL", "REPLY", "RERUN", "RESET", "RESIN",
    "RESTS", "RETRO", "RETRY", "REUSE", "REVEL", "REVUE", "RHINO", "RHYME", "RIDER", "RIDES",
    "RIDGE", "RIFLE", "RIFTS", "RIGHT", "RIGID", "RIGOR", "RINGS", "RINSE", "RIOTS", "RIPEN",
    "RIPER", "RISEN", "RISER", "RISES", "RISKS", "RISKY", "RIVAL", "RIVER", "RIVET", "ROACH",
    "ROADS", "ROAMS", "ROARS", "ROAST", "ROBIN", "ROBOT", "ROCKS", "ROCKY", "RODEO", "ROGUE",
    "ROLES", "ROLLS", "ROMAN", "ROOFS", "ROOKS", "ROOMS", "ROOMY", "ROOST", "ROOTS", "ROPES",
    "ROSES", "ROSEY", "ROSTER", "ROTOR", "ROUGE", "ROUGH", "ROUND", "ROUSE", "ROUTE", "ROVER",
    "ROWER", "ROWS", "ROYAL", "RUBBER", "RUBLE", "RUBY", "RUDDER", "RUDER", "RUGBY", "RUINS",
    "RULER", "RULES", "RUMBA", "RUMOR", "RUPEE", "RURAL", "RUSTS", "RUSTY",

    # S
    "SABER", "SABLE", "SACKS", "SADLY", "SAFER", "SAFES", "SAGE", "SAGGY", "SAILS", "SAINT",
    "SALAD", "SALEM", "SALES", "SALLY", "SALMON", "SALOON", "SALSA", "SALTS", "SALTY", "SALVE",
    "SALVO", "SAMBA", "SAME", "SANDS", "SANDY", "SANER", "SAPPHIRE", "SAPPY", "SASSY", "SATIN",
    "SATYR", "SAUCE", "SAUCY", "SAUNA", "SAUTE", "SAVOR", "SAVVY", "SCALD", "SCALE", "SCALP",
    "SCAMS", "SCANS", "SCANT", "SCARE", "SCARF", "SCARS", "SCARY", "SCENE", "SCENT", "SCHWA",
    "SCOFF", "SCOLD", "SCOOP", "SCOPE", "SCORE", "SCORN", "SCOUR", "SCOUT", "SCOWL", "SCRAM",
    "SCRAP", "SCREE", "SCREW", "SCRUB", "SCRUM", "SCUBA", "SEDAN", "SEEDS", "SEEDY", "SEEKS",
    "SEEMS", "SEEP", "SEIZE", "SELLS", "SEMEN", "SENDS", "SENSE", "SEPIA", "SERIF", "SERUM",
    "SERVE", "SETUP", "SEVEN", "SEVER", "SEWER", "SHACK", "SHADE", "SHADY", "SHAFT", "SHAKE",
    "SHAKY", "SHALE", "SHALL", "SHALT", "SHAME", "SHANK", "SHAPE", "SHARD", "SHARE", "SHARK",
    "SHARP", "SHAVE", "SHAWL", "SHEAR", "SHEDS", "SHEEN", "SHEEP", "SHEER", "SHEET", "SHEIK",
    "SHELF", "SHELL", "SHIED", "SHIFT", "SHINE", "SHINY", "SHIPS", "SHIRE", "SHIRK", "SHIRT",
    "SHOAL", "SHOCK", "SHOES", "SHONE", "SHOOK", "SHOOT", "SHOPS", "SHORE", "SHORN", "SHORT",
    "SHOTS", "SHOUT", "SHOVE", "SHOWN", "SHOWS", "SHOWY", "SHRED", "SHREW", "SHRUB", "SHRUG",
    "SHUCK", "SHUNT", "SHUSH", "SHYLY", "SIEB", "SIEGE", "SIESTA", "SIEVE", "SIGNS", "SIGMA",
    "SILKY", "SILLY", "SILOS", "SILT", "SILVER", "SIMON", "SINCE", "SINEW", "SINGE", "SINGS",
    "SINKS", "SINUS", "SIREN", "SIRUP", "SISTER", "SITES", "SIXTH", "SIXTY", "SIZED", "SIZES",
    "SKATE", "SKEIN", "SKEPTIC", "SKEW", "SKIED", "SKIER", "SKIES", "SKIFF", "SKILL", "SKIMP",
    "SKINS", "SKIRT", "SKULK", "SKULL", "SKUNK", "SLACK", "SLAIN", "SLANG", "SLANT", "SLAPS",
    "SLASH", "SLATE", "SLATS", "SLAVE", "SLEEK", "SLEEP", "SLEET", "SLEPT", "SLICE", "SLICK",
    "SLIDE", "SLIME", "SLIMY", "SLING", "SLINK", "SLIPS", "SLIT", "SLOB", "SLOTH", "SLOTS",
    "SLOUCH", "SLUMP", "SLUNG", "SLUNK", "SLURP", "SLUSH", "SLYLY", "SMACK", "SMALL", "SMART",
    "SMASH", "SMEAR", "SMELL", "SMELT", "SMILE", "SMIRK", "SMITE", "SMITH", "SMOCK", "SMOKE",
    "SMOKY", "SMOTE", "SNACK", "SNAFU", "SNAIL", "SNAKE", "SNAKY", "SNAP", "SNAPS", "SNARE",
    "SNARL", "SNEAK", "SNEER", "SNIDE", "SNIFF", "SNIPE", "SNOOT", "SNOOZE", "SNORT", "SNOUT",
    "SNOWY", "SNUCK", "SNUFF", "SOAPY", "SOBER", "SOCKS", "SODA", "SOFA", "SOFTLY", "SOILS",
    "SOLAR", "SOLER", "SOLID", "SOLVE", "SOLVENT", "SONAR", "SONIC", "SOOTY", "SORRY", "SORTS",
    "SOUL", "SOUND", "SOUP", "SOURS", "SOUTH", "SOWER", "SPACE", "SPADE", "SPAN", "SPANK",
    "SPARE", "SPARK", "SPASM", "SPAT", "SPAWN", "SPEAK", "SPEAR", "SPECK", "SPEED", "SPELL",
    "SPELT", "SPEND", "SPENT", "SPERM", "SPICE", "SPICY", "SPIED", "SPIEL", "SPIKE", "SPIKY",
    "SPILL", "SPILT", "SPINE", "SPINY", "SPIRE", "SPITE", "SPLIT", "SPOIL", "SPOKE", "SPOOF",
    "SPOOK", "SPOOL", "SPOON", "SPORE", "SPORT", "SPOTS", "SPOUT", "SPRAY", "SPREE", "SPRIG",
    "SPUNK", "SPURN", "SPURS", "SPURT", "SQUAD", "SQUAT", "SQUAWK", "SQUIB", "SQUID", "STACK",
    "STAFF", "STAGE", "STAID", "STAIN", "STAIR", "STAKE", "STALE", "STALK", "STALL", "STAMP",
    "STAND", "STANK", "STARE", "STARK", "START", "STASH", "STATE", "STATS", "STAVE", "STEAD",
    "STEAK", "STEAL", "STEAM", "STEEL", "STEEP", "STEER", "STEIN", "STEMS", "STENT", "STEPS",
    "STERN", "STICK", "STIFF", "STILL", "STILT", "STING", "STINK", "STINT", "STOCK", "STOIC",
    "STOKE", "STOLE", "STOMP", "STONE", "STONY", "STOOD", "STOOL", "STOOP", "STOPS", "STORE",
    "STORK", "STORM", "STORY", "STOUT", "STOVE", "STRAP", "STRAW", "STRAY", "STRIP", "STRUT",
    "STUCK", "STUD", "STUDS", "STUDY", "STUFF", "STUMP", "STUNG", "STUNK", "STUNT", "STYLE",
    "SUAVE", "SUGAR", "SUITE", "SUITS", "SULKY", "SULLEN", "SUMAC", "SUNNY", "SUPER", "SURER",
    "SURF", "SURGE", "SURLY", "SWAIN", "SWAMI", "SWAMP", "SWAN", "SWANS", "SWAP", "SWARM",
    "SWASH", "SWATH", "SWEAR", "SWEAT", "SWEEP", "SWEET", "SWELL", "SWEPT", "SWIFT", "SWILL",
    "SWIME", "SWINE", "SWING", "SWIRL", "SWISH", "SWOON", "SWOOP", "SWORD", "SWORE", "SWORN",
    "SWUNG", "SYNOD", "SYRUP",

    # T
    "TABBY", "TABLE", "TABOO", "TACIT", "TACKY", "TACO", "TAILOR", "TAILS", "TAINT", "TAKEN",
    "TAKER", "TAKES", "TALON", "TAMER", "TAMPA", "TANGO", "TANGY", "TAPED", "TAPER", "TAPES",
    "TAPIR", "TARDY", "TARIFF", "TAROT", "TASK", "TASKS", "TASTE", "TASTY", "TATTOO", "TAUNT",
    "TAWNY", "TAXIS", "TEACH", "TEAMS", "TEARS", "TEARY", "TEASE", "TEDDY", "TEETH", "TEMPO",
    "TENDS", "TENET", "TENOR", "TENSE", "TENTH", "PENTS", "TENTS", "TEPEE", "TEPID", "TERRA",
    "TERSE", "TESTS", "TESTY", "TEXAS", "TEXTS", "THANK", "THEFT", "THEIR", "THEME", "THERE",
    "THESE", "THETA", "THICK", "THIEF", "THIGH", "THING", "THINK", "THIRD", "THONG", "THORN",
    "THOSE", "THREE", "THREW", "THROB", "THROW", "THRUM", "THUMB", "THUMP", "THYME", "TIARA",
    "TIBIA", "TICKS", "TIDAL", "TIGER", "TIGHT", "TILDE", "TILES", "TIMER", "TIMES", "TIMID",
    "TIPSY", "TITAN", "TITHE", "TITLE", "TOAST", "TODAY", "TODDY", "TOKEN", "TONAL", "TONGS",
    "TONIC", "TOOTH", "TOPAZ", "TOPIC", "TORCH", "TORSO", "TORUS", "TOTAL", "TOTEM", "TOUCH",
    "TOUGH", "TOWEL", "TOWER", "TOWNS", "TOXIC", "TOXIN", "TRACE", "TRACK", "TRACT", "TRADE",
    "TRAIL", "TRAIN", "TRAIT", "TRAMP", "TRASH", "TRAWL", "TREAD", "TREAT", "TREND", "TRIAD",
    "TRIAL", "TRIBE", "TRICE", "TRICK", "TRIED", "TRIPE", "TRIPS", "TRITE", "TROLL", "TROOP",
    "TROPE", "TROUT", "TROVE", "TRUCE", "TRUCK", "TRUER", "TRULY", "TRUMP", "TRUNK", "TRUST",
    "TRUTH", "TRYST", "TUBAL", "TUBER", "TULIP", "TULLE", "TUMOR", "TUNED", "TUNER", "TUNES",
    "TUNIC", "TURBO", "TUTOR", "TWAIN", "TWANG", "TWEAK", "TWEED", "TWEET", "TWICE", "TWINE",
    "TWINS", "TWIRL", "TWIST", "TYING",

    # U, V, W, X, Y, Z
    "ULCER", "ULTRA", "UMBRA", "UNCLE", "UNCAP", "UNCLE", "UNDER", "UNDUE", "UNFED", "FIT",
    "UNFIT", "UNIFY", "UNION", "UNIQUE", "UNITS", "UNITY", "UNLIT", "UNMET", "UNTIE", "UNTIL",
    "UNZIP", "UPBEAT", "UPON", "UPPER", "UPSET", "URBAN", "URGED", "URGES", "URINE", "USAGE",
    "USERS", "USHER", "USUAL", "UTTER", "VAGUE", "VALET", "VALID", "VALOR", "VALUE", "VALVE",
    "VAPID", "VAPOR", "VAULT", "VAUNT", "VEGAN", "VENOM", "VENUE", "VERGE", "VERSE", "VERSO",
    "VERVE", "VICAR", "VIDEO", "VIEWS", "VIGIL", "VIGOR", "VILLA", "VINYL", "VIOLA", "VIPER",
    "VIRAL", "VIRUS", "VISIT", "VISOR", "VISTA", "VITAL", "VIVID", "VIXEN", "VOCAL", "VODKA",
    "VOGUE", "VOICE", "VOILA", "VOLT", "VOMIT", "VOUCH", "VOWEL", "VIE", "VYING", "WACKY",
    "WAFER", "WAGER", "WAGES", "WAGON", "WAIST", "WAIVE", "WALTZ", "WAND", "WANTS", "WARMTH",
    "WARNS", "WASTE", "WATCH", "WATER", "WAVER", "WAVES", "WAXEN", "WEARY", "WEAVE", "WEDGE",
    "WEEDY", "WEIGH", "WEIRD", "WELCH", "WELSH", "WHACK", "WHALE", "WHARF", "WHEAT", "WHEEL",
    "WHELP", "WHERE", "WHICH", "WHIFF", "WHILE", "WHIM", "WHINE", "WHINY", "WHIRL", "WHISK",
    "WHITE", "WHOLE", "WHOOP", "WHOSE", "WIDEN", "WIDER", "WIDOW", "WIDTH", "WIELD", "WIGHT",
    "WILLS", "WILLY", "WIMPY", "WINCE", "WINCH", "WINDS", "WINDY", "WINES", "WINGS", "WIPER",
    "WIPES", "WIRED", "WIRES", "WISER", "WISPY", "WITCH", "WITTY", "WOKEN", "WOMAN", "WOMEN",
    "WOODS", "WOODY", "WOOER", "WOOLLY", "WOOZY", "WORDS", "WORDY", "WORKS", "WORLD", "WORRY",
    "WORSE", "WORST", "WORTH", "WOULD", "WOUND", "WOVEN", "WRACK", "WRATH", "WREAK", "WRECK",
    "WREST", "WRING", "WRIST", "WRITE", "WRONG", "WROTE", "WRUNG", "YACHT", "YEARN", "YEARS",
    "YEAST", "YIELD", "YOUNG", "YOURS", "YOUTH", "ZEBRA", "ZEST", "ZESTY", "ZILCH", "ZINC",
    "ZONAL", "ZONES"
}

import os
import json
import urllib.request
import urllib.parse
from models import get_db

def verify_word_with_llm_api(word):
    """Verifies a 5-letter word using Gemini LLM API or Free Dictionary API"""
    upper_word = word.upper()
    
    # 1. Try Gemini API if key is present
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            prompt = f"Is '{upper_word}' a valid 5-letter English word? Answer ONLY YES or NO."
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}]
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=3) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                answer = result['candidates'][0]['content']['parts'][0]['text'].strip().upper()
                if "YES" in answer:
                    return True
                elif "NO" in answer:
                    return False
        except Exception:
            pass

    # 2. Free Dictionary API verification fallback
    try:
        dict_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word.lower())}"
        req = urllib.request.Request(dict_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                return True
    except Exception:
        pass

    return False

def is_valid_word(word):
    if not word or len(word) != 5 or not word.isalpha():
        return False
        
    upper_word = word.upper()
    if upper_word in DICTIONARY:
        return True
        
    # Check if word is in DB
    try:
        db = get_db()
        found = db.words.find_one({'word': upper_word})
        if found:
            return True
    except Exception:
        pass

    # Strictly verify via LLM / Dictionary API
    return verify_word_with_llm_api(upper_word)


