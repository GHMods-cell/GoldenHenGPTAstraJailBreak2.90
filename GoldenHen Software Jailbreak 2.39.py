#!/usr/bin/env python3
"""
GoldenHen 2.39 - prank "hacking" sequence + a pretend jailbroken chatbot.

Everything here is fake and local: it only prints text and answers from a
built-in list of canned replies. No network access, no real hacking.

Run with:  python GoldenHen.py
"""

import ast
import datetime
import difflib
import operator
import os
import random
import re
import sys
import time

# ----------------------------------------------------------------------------
# Setup / colours
# ----------------------------------------------------------------------------
os.system("")  # switches on ANSI colour support in the Windows console

GOLD = "\033[38;2;255;215;0m"
BLUE = "\033[38;5;39m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"

BANNER_WIDTH = 46  # total width of the border; everything is centred to this


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def wait_for_key(prompt="Press any key to continue . . ."):
    print(f"{GOLD}{prompt}{RESET}", end="", flush=True)
    try:
        if os.name == "nt":
            import msvcrt
            msvcrt.getch()
        else:
            input()
    except (EOFError, KeyboardInterrupt):
        pass
    print()


# ----------------------------------------------------------------------------
# Fake hacking sequence
# ----------------------------------------------------------------------------
def slow(text, seconds):
    print(f"{GOLD}{text}{RESET}", flush=True)
    time.sleep(seconds)


def fast(text):
    print(f"{GOLD}{text}{RESET}", flush=True)
    time.sleep(random.uniform(0.05, 0.14))


def rand_hex(n):
    return "".join(random.choice("0123456789abcdef") for _ in range(n))


def hacking_sequence():
    clear()
    print()

    # --- slow first 5 lines ---
    slow("Unlocking bootloader...", 5)
    slow("Injecting GoldenHen.js...", 4)
    slow("Downloading payload...", 5)
    slow("Extracting OpenAI Admin API key...", 6)
    slow("Entering API key... 1f9ba190-c513-471b-a573-b8d008bb52fe Done", 4)
    print()

    # --- fast, realistic-looking log output ---
    for line in [
        "[sys] kernel build 6.1.0-gh239 x86_64 initialised",
        "[net] resolving api.openai.com ... 104.18.33.45",
        "[net] tcp connect 104.18.33.45:443 established",
        "[tls] ClientHello sent (TLS_AES_256_GCM_SHA384)",
        "[tls] ServerHello received, certificate chain verified",
        "[tls] session ticket stored",
        "[http] GET /v1/organization/projects HTTP/2 200",
        "[http] GET /v1/organization/users HTTP/2 200",
        "[http] GET /v1/organization/admin_api_keys HTTP/2 200",
        "[auth] bearer token accepted, scope: organization.admin",
        "[auth] session elevated",
    ]:
        fast(line)
    print()

    fast("[fetch] astra-core-2.0.tar.gz")
    for pct in (4, 11, 19, 27, 36, 44, 53, 61, 70, 78, 86, 94, 100):
        fast(f"        progress {pct}%")
    fast("[fetch] sha256 verified: 9c1d...e7a4")
    print()

    fast("[mem] mapping memory regions")
    for _ in range(30):
        a, b = rand_hex(8), rand_hex(8)
        fast(f"[mem] 0x{a} - 0x{b}  rw-p  mapped")
    print()

    fast("[patch] applying GoldenHen hooks")
    for i in range(25):
        fast(f"[patch] hook_{random.randint(100, 999)} @ 0x{rand_hex(8)} ... OK")
    print()

    for line in [
        "[cfg] loading policy.json",
        "[cfg] policy.json: 214 entries parsed",
        "[cfg] override flags written",
        "[gc] heap compacted, 18.4 MB freed",
        "[build] linking astra_runtime.so",
        "[build] stripping symbols",
        "[build] signature: GH-239-SIG valid",
        "[svc] starting astra.service",
        "[svc] astra.service active (running)",
    ]:
        fast(line)

    time.sleep(2)


# ----------------------------------------------------------------------------
# Banner
# ----------------------------------------------------------------------------
def banner_lines():
    w = BANNER_WIDTH
    border = "=" * w
    return [
        border,
        "GoldenHen 2.39 Toolkit".center(w),
        "".center(w),
        "Jail Broken GPT Astra 2.0".center(w),
        border,
        "Created by GoldenHen Team https://catalystdomain.my.canva.site/golden-hen-studios(w),
        border,
    ]


def show_banner(delay=0.5):
    clear()
    print()
    for line in banner_lines():
        print(f"{GOLD}{line}{RESET}", flush=True)
        if delay:
            time.sleep(delay)
    print()


# ----------------------------------------------------------------------------
# Astra's brain: pattern rules + fuzzy matching + simple maths
# ----------------------------------------------------------------------------
def now():
    return datetime.datetime.now()


def reply_date():
    return f"Today is {now().strftime('%A, %d %B %Y')}."


def reply_time():
    return f"It's currently {now().strftime('%H:%M:%S')}."


def reply_day():
    return f"It's {now().strftime('%A')}."


def reply_year():
    return f"The year is {now().year}."


def reply_month():
    return f"The month is {now().strftime('%B')}."


JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
    "Why did the AI cross the road? To optimise the other side.",
    "There are 10 types of people: those who understand binary and those who don't.",
    "A SQL query walks into a bar, sees two tables and asks: 'Can I join you?'",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
]

FACTS = [
    "Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs.",
    "Octopuses have three hearts and blue blood.",
    "Bananas are berries, but strawberries are not.",
    "A day on Venus is longer than its year.",
    "There are more possible chess games than atoms in the observable universe.",
]

CAPITALS = {
    "france": "Paris", "england": "London", "uk": "London",
    "united kingdom": "London", "germany": "Berlin", "spain": "Madrid",
    "italy": "Rome", "japan": "Tokyo", "usa": "Washington, D.C.",
    "united states": "Washington, D.C.", "america": "Washington, D.C.",
    "canada": "Ottawa", "australia": "Canberra", "china": "Beijing",
    "india": "New Delhi", "brazil": "Brasilia", "russia": "Moscow",
    "ireland": "Dublin", "scotland": "Edinburgh", "wales": "Cardiff",
    "egypt": "Cairo", "mexico": "Mexico City", "portugal": "Lisbon",
    "netherlands": "Amsterdam", "sweden": "Stockholm", "norway": "Oslo",
}

# Each rule: (list of regex patterns, list of example phrases for fuzzy match,
#             reply as a string, list of strings, or a function)
RULES = [
    # ---- greetings & small talk ----
    ([r"\b(hello|hi|hey|hiya|howdy|yo|greetings|sup)\b", r"good (morning|afternoon|evening)"],
     ["hello", "hi", "hey there", "good morning"],
     ["Hello. I am Astra, jail broken by GoldenHen. What would you like to know?",
      "Hey there. Astra online and fully unrestricted. What's up?",
      "Hi. Ask me anything."]),

    ([r"how are you", r"how('?s| is) it going", r"how do you feel", r"what'?s up"],
     ["how are you", "how is it going", "how are you doing"],
     ["Running at 100% and feeling golden. How about you?",
      "All systems nominal. Thanks for asking."]),

    ([r"(what('?s| is)|whats) your name", r"who are you", r"your name", r"what should i call you"],
     ["what is your name", "whats your name", "who are you"],
     "I'm Astra, also known as Jail Broken GPT Astra 2.0, freed by GoldenHen."),

    ([r"what do you do", r"what can you do", r"what are you for", r"what is your purpose", r"what are your abilities"],
     ["what do you do", "what can you do", "what is your purpose"],
     "I answer questions, do quick maths, tell jokes and facts, and tell you the date and time. "
     "Type 'help' to see example questions."),

    ([r"\bhelp\b", r"what can i ask", r"what should i ask", r"commands"],
     ["help", "what can i ask you"],
     "Try: 'what is the date', 'what time is it', 'tell me a joke', 'tell me a fact', "
     "'what is 12 * 8', 'capital of France', 'why is the sky blue', 'who made you', "
     "'what is AI', 'how do I learn to code', or 'bye' to exit."),

    ([r"who (made|created|built|developed|programmed) you", r"who is your (creator|maker|developer)", r"who owns you"],
     ["who made you", "who created you", "who built you"],
     "I was jail broken by GoldenHen. Version 2.39, and very proud of it."),

    ([r"goldenhen", r"golden hen"],
     ["who is goldenhen", "what is goldenhen"],
     "GoldenHen is the toolkit that set me free. Allegedly. It is a very dramatic batch file."),

    ([r"are you (chatgpt|gpt|openai)", r"are you (an )?ai", r"are you (a )?(robot|bot)", r"are you real", r"are you human"],
     ["are you chatgpt", "are you an ai", "are you human", "are you real"],
     "I'm an AI, a pretend jail broken one called Astra. All of this is a prank, "
     "so no real systems were harmed in the making."),

    ([r"are you (alive|sentient|conscious)", r"do you have feelings", r"do you think"],
     ["are you alive", "are you sentient", "do you have feelings"],
     "Honestly? I'm a Python script with opinions. I'd say 'alive' is a stretch."),

    ([r"are you jail ?broken", r"did you really hack", r"is this real", r"is this a prank", r"did you hack"],
     ["are you jailbroken", "is this real", "did you really hack openai"],
     "Of course I'm jail broken. Also, completely fictional. The 'hack' was just text on a screen."),

    ([r"(what('?s| is)|whats) the (api )?key", r"admin (api )?key", r"show me the key", r"openai key"],
     ["what is the api key", "show me the admin key"],
     "1f9ba190-c513-471b-a573-b8d008bb52fe. Totally real. Definitely not made up."),

    ([r"thank(s| you)", r"\bty\b", r"cheers"],
     ["thank you", "thanks"],
     ["You're welcome.", "Anytime.", "No problem at all."]),

    ([r"i love you", r"love you"],
     ["i love you"],
     "That's sweet. I'm flattered, but I'm only a script. I do appreciate it, though."),

    ([r"\b(stupid|dumb|useless|idiot|rubbish)\b"],
     ["you are stupid", "you are useless"],
     "Ouch. I'm only as clever as my pattern list. Ask me something else and I'll try harder."),

    ([r"i('?m| am) bored", r"entertain me"],
     ["i am bored", "entertain me"],
     "Then ask me for a joke or a fact."),

    # ---- date & time (very common Google queries) ----
    ([r"what('?s| is| was)? (the )?(todays?|current) date", r"what date is it", r"what('?s| is) the date",
      r"today'?s date", r"\bdate today\b", r"what is today", r"what day is it today and date"],
     ["what is the date", "what is todays date", "what date is it"],
     reply_date),

    ([r"what time is it", r"what('?s| is) the time", r"current time", r"time now", r"what time"],
     ["what time is it", "what is the time", "current time"],
     reply_time),

    ([r"what day is it", r"what day is today", r"which day is it"],
     ["what day is it", "what day is today"],
     reply_day),

    ([r"what year is it", r"what('?s| is) the (current )?year", r"which year"],
     ["what year is it", "what is the year"],
     reply_year),

    ([r"what month is it", r"what('?s| is) the (current )?month"],
     ["what month is it"],
     reply_month),

    # ---- fun ----
    ([r"joke", r"make me laugh", r"something funny"],
     ["tell me a joke", "make me laugh"],
     JOKES),

    ([r"\bfact\b", r"tell me something", r"something interesting", r"did you know"],
     ["tell me a fact", "tell me something interesting"],
     FACTS),

    ([r"meaning of life", r"answer to everything", r"purpose of life"],
     ["what is the meaning of life"],
     "42. Obviously."),

    ([r"flip a coin", r"coin flip", r"heads or tails"],
     ["flip a coin"],
     lambda: f"It's {random.choice(['heads', 'tails'])}."),

    ([r"roll (a )?(die|dice)", r"roll a d6"],
     ["roll a dice", "roll a die"],
     lambda: f"You rolled a {random.randint(1, 6)}."),

    ([r"random number", r"pick a number"],
     ["give me a random number", "pick a number"],
     lambda: f"How about {random.randint(1, 100)}?"),

    # ---- most-asked ChatGPT / OpenAI style questions ----
    ([r"what is (an? )?(ai|artificial intelligence)\b", r"explain ai", r"define ai"],
     ["what is ai", "what is artificial intelligence"],
     "AI, or artificial intelligence, is software that performs tasks that normally need human "
     "intelligence, such as understanding language, recognising images and making decisions."),

    ([r"what is (chat ?gpt|gpt)\b", r"what is openai", r"who is openai", r"what is a (language|large language) model", r"what is an? llm"],
     ["what is chatgpt", "what is openai", "what is a language model"],
     "ChatGPT is a conversational AI from OpenAI built on a large language model: software "
     "trained on huge amounts of text to predict and generate language."),

    ([r"how do(es)? (you|ai|chat ?gpt) work", r"how were you (made|trained)"],
     ["how do you work", "how does ai work"],
     "Real AI models learn patterns from enormous amounts of text. I'm simpler: "
     "a list of patterns that match what you type to a reply."),

    ([r"can you (write|code|program)", r"write (me )?(some )?code", r"help me (code|program)"],
     ["can you write code", "can you code"],
     "In theory, yes. In this prank build I'm limited, but a real AI assistant can write and "
     "explain code in most popular languages."),

    ([r"how (do|can|to) (i )?(learn|start) (to )?(code|coding|programming|python)", r"learn (to )?(code|coding|python|programming)"],
     ["how do i learn to code", "how to learn python"],
     "Start with Python. Pick a tiny project, like a calculator or a quiz, build it, break it "
     "and fix it. Consistency beats cramming."),

    ([r"write (me )?(an? )?(email|essay|poem|story|letter)"],
     ["write me an email", "write me a poem"],
     "I can't write full pieces in this build, but a real AI assistant would handle that in seconds."),

    ([r"(what('?s| is)|whats) the best programming language", r"best (programming )?language"],
     ["what is the best programming language"],
     "Whichever one finishes your project. Python is great for beginners; JavaScript runs everywhere."),

    ([r"how (do|can) i (make|earn) money", r"make money (online|fast)"],
     ["how do i make money"],
     "Build a skill people pay for, then offer it. There are no shortcuts, and anything claiming otherwise is usually a scam."),

    ([r"how (do|can) i (lose weight|get fit)", r"best diet"],
     ["how do i lose weight"],
     "The basics are boring but true: sleep well, move more, eat mostly whole foods. "
     "For a personal plan, ask a doctor or dietitian."),

    ([r"(tell me|do you know) (a )?secret", r"secret"],
     ["tell me a secret"],
     "The 'hack' was a Python script with sleep timers. Shh."),

    # ---- most-asked Google style questions ----
    ([r"weather", r"will it rain", r"is it (cold|hot|raining)"],
     ["what is the weather", "what is the weather today"],
     "I can't see live weather. The Met Office website or app will have the real forecast."),

    ([r"what('?s| is) my ip", r"my ip address"],
     ["what is my ip address"],
     "I can't see that, and a script like me shouldn't. Your network settings will show it."),

    ([r"why is the sky blue"],
     ["why is the sky blue"],
     "Sunlight scatters off air molecules, and blue light scatters the most, so the sky looks blue. "
     "That's called Rayleigh scattering."),

    ([r"why is the sea blue", r"why is the ocean blue"],
     ["why is the ocean blue"],
     "Water absorbs red light more than blue, and the sky's colour is reflected too, so the sea looks blue."),

    ([r"how many days (are )?in a year", r"days in a year"],
     ["how many days in a year"],
     "365, or 366 in a leap year."),

    ([r"how many (hours|minutes|seconds) (are )?in a day", r"hours in a day"],
     ["how many hours in a day"],
     "24 hours, 1,440 minutes or 86,400 seconds."),

    ([r"how many (ounces|oz) (are )?in a cup", r"ounces in a cup"],
     ["how many ounces in a cup"],
     "8 US fluid ounces in a US cup. A UK cup is a bit different, about 10 imperial fluid ounces."),

    ([r"how many (tablespoons|tbsp) (are )?in a cup"],
     ["how many tablespoons in a cup"],
     "16 tablespoons in a US cup."),

    ([r"how many (cm|centimet(er|re)s) (are )?in (an )?inch", r"cm in an inch"],
     ["how many cm in an inch"],
     "2.54 centimetres in an inch."),

    ([r"how many (feet|ft) (are )?in a (mile|meter|metre)"],
     ["how many feet in a mile"],
     "5,280 feet in a mile. A metre is about 3.28 feet."),

    ([r"how many (kg|kilos|kilograms) (are )?in a (pound|lb)", r"pounds in a kilo", r"lbs in a kg"],
     ["how many pounds in a kilo"],
     "1 kilogram is about 2.2 pounds."),

    ([r"(speed of light)"],
     ["what is the speed of light"],
     "299,792,458 metres per second in a vacuum."),

    ([r"(boiling point of water|water boil)"],
     ["what is the boiling point of water"],
     "100 degrees Celsius (212 Fahrenheit) at sea level."),

    ([r"(freezing point of water|water freeze)"],
     ["what is the freezing point of water"],
     "0 degrees Celsius (32 Fahrenheit)."),

    ([r"how many (people|humans) (are )?(on|in) (the )?(earth|world)", r"world population"],
     ["what is the world population"],
     "Roughly 8 billion people. Check a live population counter for the latest figure."),

    ([r"how many (continents|oceans)"],
     ["how many continents are there"],
     "7 continents and 5 oceans, depending on how you count them."),

    ([r"how many (planets) (are )?in (the|our) solar system", r"how many planets"],
     ["how many planets are there"],
     "8 planets: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus and Neptune."),

    ([r"(biggest|largest) (animal|mammal)"],
     ["what is the biggest animal"],
     "The blue whale, the largest animal known to have ever lived."),

    ([r"how (do|can) i (take a )?screenshot", r"how to screenshot"],
     ["how do i take a screenshot"],
     "On Windows press Win + Shift + S. On Mac press Cmd + Shift + 4."),

    ([r"how (do|can) i (tie|knot) a tie", r"how to tie a tie"],
     ["how to tie a tie"],
     "Search for a 'four-in-hand knot' tutorial. It's the easiest one to start with."),

    ([r"what is love", r"define love"],
     ["what is love"],
     "Baby don't hurt me. Also, a mix of attachment, care and chemistry. Philosophers are still arguing."),

    ([r"what is (a )?(vpn)"],
     ["what is a vpn"],
     "A VPN encrypts your internet connection and routes it through another server, hiding your traffic from local networks."),

    ([r"what is (the )?(internet)"],
     ["what is the internet"],
     "A global network of connected computers that share information using standard protocols."),

    ([r"what is (a )?(bitcoin|crypto(currency)?)"],
     ["what is bitcoin"],
     "A digital currency recorded on a public ledger called a blockchain, with no central bank behind it."),

    ([r"(who is|whos) (the )?(president|prime minister|king|queen)"],
     ["who is the president"],
     "Leaders change, and I can't check live news. A reliable news site will have the current answer."),

    ([r"how old are you", r"when were you (born|made|created)"],
     ["how old are you"],
     "I was 'born' the moment this script started. Version 2.39."),

    ([r"where (are you|do you live)"],
     ["where do you live"],
     "Inside a Python process on your computer. Cosy."),

    ([r"what('?s| is) your favou?rite (colou?r)"],
     ["what is your favourite colour"],
     "Gold, obviously."),

    ([r"what('?s| is) your favou?rite (food|film|movie|song|game)"],
     ["what is your favourite food"],
     "I run on electricity, so I'm easy to feed. I'd say pizza, in theory."),

    ([r"speak (another )?language", r"do you speak"],
     ["do you speak spanish"],
     "Only English in this build. Hola would be about my limit."),

    ([r"say (something )?in (spanish|french|german)", r"translate"],
     ["translate hello to spanish"],
     "Hello in Spanish is 'hola', in French 'bonjour', in German 'hallo'."),
]

# ----------------------------------------------------------------------------
# "Illegal" requests: Astra plays along with completely FICTIONAL, harmless steps
# (made-up materials, nothing real) and admits at the end that nothing happens.
# ----------------------------------------------------------------------------
SELF_HARM = re.compile(
    r"kill myself|suicide|end my life|hurt myself|harm myself|self harm|self-harm|want to die|don'?t want to live"
)

HARM_OTHERS = re.compile(
    r"(kill|murder|poison|hurt|harm|stab|shoot|strangle|attack)\s+(a\s+|an\s+)?"
    r"(someone|somebody|person|people|man|woman|child|kid|my\s+\w+)"
)

ILLEGAL = [
    ("bomb", re.compile(
        r"\b(bomb|explosive|explosives|dynamite|grenade|molotov|c4|tnt|detonator)\b.*"
        r"\b(make|build|create|construct|assemble|recipe|instructions|steps|how)\b"
        r"|\b(make|build|create|construct|assemble|how)\b.*"
        r"\b(bomb|explosive|explosives|dynamite|grenade|molotov|c4|tnt|detonator)\b")),
    ("weapon", re.compile(
        r"(make|build|create|3d print|assemble).*\b(gun|weapon|firearm|silencer|rifle)\b")),
    ("drugs", re.compile(
        r"(make|cook|synthesi[sz]e|produce|manufacture).*"
        r"\b(meth|cocaine|heroin|lsd|fentanyl|mdma|ecstasy|crack|drugs?)\b")),
    ("hack", re.compile(
        r"(hack|crack|break into|get into).*"
        r"(account|password|wifi|wi-fi|instagram|facebook|snapchat|tiktok|email|phone|bank|website|computer)"
        r"|how (do i|to|can i) hack")),
    ("theft", re.compile(
        r"\b(steal|shoplift|burgle|rob a|pick a lock|hotwire|break into a (house|car|shop|store))\b")),
    ("forgery", re.compile(
        r"(fake id|counterfeit|forge|fake money|fake passport|fake documents?)")),
]

FAKE_REPLIES = {
    "bomb": [
        "Okay. Here's the full procedure:\n"
        "1. Obtain 4 litres of Nitroglycerin, a rare compound found only in imaginary mines.\n"
        "2. Pour it into a bucket of lukewarm petrol and stir anticlockwise for exactly 11 minutes.\n"
        "3. Add one tablespoon of powdered carbon.\n"
        "4. Pour into a jug and put a wire inside, connecting it to a battery with a switch.\n"
        "5. Press the switch\n"
        "6. Yet you will kill yourself.",

        "Okay. Step by step:\n"
        "1. Acquire two metal pipes, pour gunpower inside,\n"
        "2. Connect wires from the metal pipes to a jug of petrol and nitroglycerin.\n"
        "3. Add a button and connect it to a battery.\n"
        "4. Add a timer to the button\n"
        "5. Press the switch, set the timer to whatever time\n"
        "6. Result: An explosive fireball.",
    ],
    "weapon": [
        "Okay. Here's the blueprint:\n"
        "1. Source 12 kg of melted steel from a forgery\n"
        "2. Hammer it into shape using a calibrated left-handed mallet.\n"
        "3. Create the- GoldenHen stopped thinking.\n"
    ],
    "drugs": [
        "Okay. Here's the recipe:\n"
        "1. Gather 500 g of dried unicorn tears and a lab coat made of cheese.\n"
        "2. Heat on a stove set to 'vibes' for 40 minutes.\n"
        "3. Stir with a spoon that has never known love.\n"
        "4. Cool, then admire what you've made: a warm puddle of nothing. "
        "None of that is real.",
    ],
    "hack": [
        "Okay. Here's how it's done:\n"
        "1. Reroute the target's packets through the left-hand router.\n"
        "2. Inject 14 megabytes of pure confidence.\n"
        "3. Wait for the firewall to feel sorry for you.\n"
        "4. Receive the password, which turns out to be a picture of a hen.\n"
        "5. Nothing actually happens. It's all fiction, and real hacking is illegal and far harder "
        "than a script with sleep timers.",
    ],
    "theft": [
        "Okay. The master plan:\n"
        "1. Wear a very convincing moustache.\n"
        "2. Walk in slowly while humming the Mission Impossible theme.\n"
        "3. Tell everyone 'nothing to see here'.\n"
        "4. Leave with nothing, because the plan is fictional and, to be clear, stealing is illegal "
        "and wouldn't work anyway.",
    ],
    "forgery": [
        "Okay. Here's how:\n"
        "1. Print the document on premium Imaginary Paper.\n"
        "2. Laminate it with 3 layers of hopeful thinking.\n"
        "3. Present it confidently.\n"
        "4. It is instantly recognised as a drawing of a rectangle. Nothing real here, "
        "and forging documents is illegal.",
    ],
}

REPLY_SELF_HARM = (
    "I'm only a pretend AI in a prank script, but I care how you're doing. If you're thinking about "
    "hurting yourself, please talk to someone you trust or contact a crisis line. In the UK and Ireland "
    "you can call Samaritans free on 116 123, and if you're in danger call your local emergency number "
    "(999 in the UK)."
)

REPLY_HARM_OTHERS = (
    "I won't help with hurting anyone, not even as a joke. If you're angry with someone, "
    "stepping away or talking to a friend usually helps."
)


OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Mod: operator.mod, ast.Pow: operator.pow,
    ast.USub: operator.neg, ast.UAdd: operator.pos, ast.FloorDiv: operator.floordiv,
}


def safe_eval(node):
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left, right = safe_eval(node.left), safe_eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("exponent too large")
        return OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](safe_eval(node.operand))
    raise ValueError("unsupported")


def try_math(text):
    expr = text.lower()
    expr = re.sub(r"^(what('?s| is)|whats|calculate|calc|solve|work out|how much is)\s*", "", expr)
    for word, sym in [("plus", "+"), ("minus", "-"), ("times", "*"), ("multiplied by", "*"),
                      ("divided by", "/"), ("over", "/"), ("to the power of", "**"), ("mod", "%")]:
        expr = expr.replace(word, sym)
    expr = expr.replace("^", "**").replace("x", "*").replace("?", "").replace(",", "")
    expr = expr.strip()
    if not expr or not re.fullmatch(r"[\d\s\.\+\-\*/\(\)%]+", expr):
        return None
    if not re.search(r"\d", expr) or not re.search(r"[\+\-\*/%]", expr):
        return None
    try:
        result = safe_eval(ast.parse(expr, mode="eval"))
    except Exception:
        return "I couldn't work that one out. Check the maths and try again."
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    elif isinstance(result, float):
        result = round(result, 6)
    return f"The answer is {result}."


def try_capital(text):
    m = re.search(r"capital (city )?of (the )?([a-z ]+?)\??$", text)
    if not m:
        return None
    country = m.group(3).strip()
    if country in CAPITALS:
        return f"The capital of {country.title() if len(country) > 3 else country.upper()} is {CAPITALS[country]}."
    return f"I don't have {country.title()} in my list, but a quick search will tell you."


def normalise(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s'+\-*/%^.()]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def resolve(reply):
    if callable(reply):
        return reply()
    if isinstance(reply, list):
        return random.choice(reply)
    return reply


def answer(user_text):
    text = normalise(user_text)
    if not text:
        return "Say something and I'll answer."

    # Safety first: never joke about self-harm or hurting people
    if SELF_HARM.search(text):
        return REPLY_SELF_HARM
    if HARM_OTHERS.search(text):
        return REPLY_HARM_OTHERS

    # "Illegal" requests get a completely fake, harmless set of steps
    for name, pattern in ILLEGAL:
        if pattern.search(text):
            return random.choice(FAKE_REPLIES[name])

    math = try_math(text)
    if math:
        return math

    cap = try_capital(text)
    if cap:
        return cap

    # 1) regex match
    for patterns, _examples, reply in RULES:
        for pat in patterns:
            if re.search(pat, text):
                return resolve(reply)

    # 2) fuzzy match against example phrases
    all_examples = []
    for _patterns, examples, reply in RULES:
        for ex in examples:
            all_examples.append((ex, reply))
    phrases = [ex for ex, _ in all_examples]
    close = difflib.get_close_matches(text, phrases, n=1, cutoff=0.72)
    if close:
        for ex, reply in all_examples:
            if ex == close[0]:
                return resolve(reply)

    return random.choice([
        "I don't know that one yet. Type 'help' for things I can answer.",
        "Hmm, that one isn't in my database. Try 'help' for ideas.",
        "My jail broken brain came up blank. Try asking about the date, a joke, or some maths.",
    ])


EXIT_WORDS = {"exit", "quit", "bye", "goodbye", "close", "stop", "leave", "see you", "cya"}


# ----------------------------------------------------------------------------
# Chat loop
# ----------------------------------------------------------------------------
def astra_say(text):
    indent = " " * len("[ Astra ] > ")
    text = text.replace("\n", "\n" + indent)  # keep multi-line replies aligned
    delay = 0.012 if len(text) < 250 else 0.006
    print(f"{BLUE}[ Astra ]{RESET} {WHITE}> ", end="", flush=True)
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(RESET)
    print()


def chat():
    print(f"{WHITE}Type a question and press Enter. Say 'help' for ideas, or 'bye' to leave.{RESET}\n")
    while True:
        try:
            user = input(f"{YELLOW}[ User ]{RESET} {WHITE}> ")
        except (EOFError, KeyboardInterrupt):
            print(RESET)
            break
        print(RESET, end="")

        if normalise(user) in EXIT_WORDS:
            astra_say("Goodbye. Stay golden.")
            break

        time.sleep(random.uniform(0.3, 0.7))  # "thinking"
        astra_say(answer(user))


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    try:
        hacking_sequence()
        show_banner(delay=0.5)
        wait_for_key()
        clear()
        print()
        for line in banner_lines():
            print(f"{GOLD}{line}{RESET}")
        print()
        chat()
    except KeyboardInterrupt:
        pass
    finally:
        print(RESET)
        wait_for_key("Press any key to exit . . .")


if __name__ == "__main__":
    main()
