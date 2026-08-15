import urllib.request
import urllib.parse
import json
import os
import ssl

HINTS_DATABASE = {
    # Easy Words
    "APPLE": "A round edible fruit with red, green, or yellow skin.",
    "BEACH": "A pebbly or sandy shore by the ocean, sea, or lake.",
    "BRAVE": "Ready to face danger, pain, or difficulty with courage.",
    "CLOUD": "A visible mass of condensed water vapor floating in the atmosphere.",
    "DREAM": "A series of thoughts, images, or sensations occurring during sleep.",
    "FLAME": "A hot glowing body of ignited gas produced by a fire.",
    "GRAPE": "A small juicy smooth-skinned fruit growing in clusters on a vine.",
    "HONEY": "A sweet, sticky yellowish-brown fluid made by bees from nectar.",
    "HOUSE": "A building for human habitation, especially one for a family.",
    "LEMON": "A yellow oval citrus fruit with acidic, sour juice.",
    "MANGO": "A fleshy yellowish-red tropical fruit with a sweet taste.",
    "PEARL": "A hard, lustrous spherical mass formed inside an oyster shell.",
    "PLANT": "A living organism such as trees, shrubs, herbs, and grasses.",
    "RIVER": "A large natural stream of water flowing in a channel to the sea.",
    "STARS": "Luminous astronomical objects fixed in the night sky.",
    "TIGER": "A large wild cat with a yellow-brown coat striped with black.",
    "WATER": "A transparent, odorless, tasteless liquid essential for all life.",
    "WOMAN": "An adult female human being.",
    "WORLD": "The earth, together with all of its countries, people, and nature.",
    "MUSIC": "Vocal or instrumental sounds combined to produce harmony and rhythm.",
    "CHAIR": "A separate seat for one person, typically with four legs and a back.",
    "SWEET": "Having the pleasant taste characteristic of sugar or honey.",
    "HEART": "The central organ that pumps blood through the body.",
    "LIGHT": "The natural agent that stimulates sight and makes things visible.",
    "SMILE": "A pleased or amused facial expression with the corners of the mouth turned up.",
    "TRAIN": "A series of connected railway cars pulled by a locomotive.",
    "GREEN": "The color between blue and yellow in the spectrum; color of growing grass.",
    "PAPER": "Material manufactured in thin sheets from wood pulp used for writing.",
    "BREAD": "A staple food made from flour or meal mixed with water and baked.",
    "NIGHT": "The period of darkness in each 24 hours between sunset and sunrise.",
    "EAGLE": "A large bird of prey with a massive hooked bill and broad wings.",
    "IVORY": "A hard creamy-white substance composing the main part of elephant tusks.",
    "JUMBO": "Extremely large or huge in size.",
    "KNIFE": "An instrument composed of a blade fixed into a handle, used for cutting.",
    "OASIS": "A fertile spot in a desert where water is found.",
    "QUICK": "Moving fast or doing something in a short time; prompt.",

    # Medium Words
    "ABYSS": "A deep or seemingly bottomless chasm, void, or ocean depth.",
    "BRISK": "Active, fast, and energetic; pleasantly cool and fresh weather.",
    "CHASM": "A deep fissure or gorge in the earth, rock, or surface.",
    "FROST": "A deposit of small white ice crystals formed on freezing surfaces.",
    "GLYPH": "A carved stroke, symbol, or hieroglyphic character.",
    "LURID": "Very vivid in color, creating an unpleasantly harsh or unnatural effect.",
    "PRISM": "A transparent glass body that splits light into a rainbow spectrum.",
    "QUIRK": "A peculiar behavioral habit, unusual trait, or unexpected twist.",
    "VALOR": "Great courage and bravery in the face of danger, especially in battle.",
    "VORTEX": "A mass of whirling fluid or air, such as a whirlpool or whirlwind.",
    "ZEPHYR": "A soft, gentle, mild westerly breeze.",
    "AMBER": "A hard clear yellowish-brown fossilized resin from ancient trees.",
    "BRINE": "Water strongly saturated with salt, used for preserving food.",
    "CIRCA": "Approximately or about (used preceding a date or number).",
    "DRUID": "A priest or magician in ancient Celtic religion.",
    "EMBER": "A small piece of glowing coal or wood in a dying fire.",
    "GUILD": "An association of craftsmen or merchants holding mutual power.",
    "ORBIT": "The curved path of a celestial object or spacecraft around a star or planet.",
    "PIXEL": "A minute area of illumination on a display screen; picture element.",
    "QUOTA": "A fixed share of something that a person or group is entitled to receive.",
    "RADAR": "A system for detecting the presence, direction, or speed of aircraft or ships.",
    "SOLAR": "Relating to or determined by the sun.",
    "TEXAS": "A large southern state in the United States known for cowboys and oil.",
    "VOCAL": "Relating to the human voice or singing.",
    "YACHT": "A medium-sized sailing or motor vessel used for cruising or racing.",
    "VAGUE": "Of uncertain, indefinite, or unclear character or meaning.",
    "SHREW": "A small insect-eating mammal resembling a mouse with a long pointed snout.",
    "SQUID": "An elongated sea mollusk with ten arms around the mouth.",
    "TWIST": "Form into a bent, curled, or distorted shape by rotation.",

    # Hard Words
    "ABACK": "Taken by surprise, startled, or thrown into confusion.",
    "ACRID": "Having an irritatingly strong, harsh, and bitter taste or smell.",
    "BOSON": "A subatomic particle such as a photon that obeys Bose-Einstein statistics.",
    "CYNIC": "A person who believes that people are motivated purely by self-interest.",
    "EPOCH": "A notable period of time in history or a person's life.",
    "FJORD": "A long, narrow, deep inlet of the sea between high steep cliffs.",
    "GAUNT": "Lean and haggard, especially because of suffering, hunger, or age.",
    "HYDRA": "A multi-headed serpentine water monster in Greek mythology.",
    "KAPUT": "Broken, ruined, destroyed, or no longer functioning.",
    "NYMPH": "A mythological spirit of nature imagined as a beautiful maiden.",
    "QUAFF": "To drink an alcoholic or other beverage heartily or greedily.",
    "TRYST": "A private romantic rendezvous or meeting between lovers.",
    "ZESTY": "Having a strong, pleasant, lively, and somewhat tangy flavor.",
    "AEGIS": "The protection, backing, or support of a particular person or organization.",
    "COYLY": "In a shy, modest, or coy manner intended to be alluring.",
    "GAFFE": "An unintentional act or remark causing embarrassment to its originator.",
    "HAZEL": "A reddish-brown color, or a small tree producing edible nuts.",
    "IONIC": "Relating to or composed of electrically charged atoms (ions).",
    "JAZZY": "Bright, colorful, lively, or reminiscent of jazz music.",
    "KAZOO": "A small toy musical instrument that adds a buzzing timbre to a player's voice.",
    "MYTHS": "Traditional stories concerning the early history or supernatural phenomena.",
    "ONYX": "A semi-precious stone with parallel bands of contrasting color.",
    "PUPAL": "Relating to an insect in its inactive immature development stage.",
    "QUART": "A unit of liquid capacity equal to a quarter of a gallon.",
    "RERUN": "A event or television program shown or performed again.",
    "SYNOD": "An assembly of clergy or church delegates.",
    "UMBRA": "The fully shaded inner region of a shadow cast by an opaque object.",
    "VIXEN": "A female fox, or a spirited, quarrelsome woman.",
    "WALTZ": "A dance in triple time performed by a couple turning smoothly.",
    "ZINCS": "Metals or protective coatings composed of the element zinc."
}

def get_word_hint(word):
    if not word:
        return "A 5-letter English vocabulary puzzle word."

    upper_word = word.upper().strip()
    
    # 1. Direct dictionary match
    if upper_word in HINTS_DATABASE:
        return HINTS_DATABASE[upper_word]
        
    # Create unverified SSL context to prevent SSL cert verification failures
    ssl_context = ssl._create_unverified_context()

    # 2. Try Gemini API if key is present
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            prompt = f"Give a short 1-sentence clue/definition for the word '{upper_word}' without using the word itself."
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}]
            }).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, context=ssl_context, timeout=3) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                hint = result['candidates'][0]['content']['parts'][0]['text'].strip()
                if hint and upper_word.lower() not in hint.lower():
                    return hint
        except Exception:
            pass

    # 3. Try Free Dictionary API with custom User-Agent & SSL context
    try:
        dict_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(upper_word.lower())}"
        req = urllib.request.Request(dict_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, context=ssl_context, timeout=4) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                meanings = data[0].get('meanings', [])
                if meanings and meanings[0].get('definitions'):
                    def_text = meanings[0]['definitions'][0]['definition']
                    if def_text:
                        return def_text
    except Exception:
        pass

    # 4. Descriptive fallback hint describing word structure
    vowels = [c for c in upper_word if c in "AEIOUY"]
    vowel_str = ", ".join(vowels) if vowels else "no common vowels"
    return f"A 5-letter word starting with '{upper_word[0]}' and ending with '{upper_word[-1]}', containing {vowel_str}."
