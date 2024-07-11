import re


def stringHasMostlyCaps(line, threshold=0.6):
    total_chars = len(line)
    caps_count = sum(1 for char in line if char.isupper())
    caps_ratio = caps_count / total_chars
    return caps_ratio > threshold

# discardSingleAt: Normally, a string is discarded if it is only an @handle
def sanitize(text, discardSingleAt=True):
    def replace_multiple_letters(match):
        return match.group(0)[:3]

    def fix_acronyms(text, target_strings):
        pattern = rf'\b(?:{"|".join(map(re.escape, target_strings))})\b'

        def replace(match):
            return ".".join(match.group())

        replaced_text = re.sub(pattern, replace, text)
        return replaced_text

    def fix_acronyms_ignorecase(text, target_strings):
        pattern = rf'\b(?:{"|".join(map(re.escape, target_strings))})\b'

        def replace(match):
            return ".".join(match.group())

        replaced_text = re.sub(pattern, replace, text, flags=re.IGNORECASE)
        return replaced_text

    def trimTwitterHandleNums(string):
        # regex pattern to find twitter handles and strip trailing numbers
        cleaned_string = re.sub(r'@[\w\d]+', lambda x: x.group().rstrip('0123456789'), string)
        return cleaned_string

    text = trimTwitterHandleNums(text)

    # Remove smart quotes
    smart_quotes = {
        "\u2018": "",
        "\u2019": "",  # Single quotes
        "\u201C": "",
        "\u201D": "",  # Double quotes
    }
    for smart, _ in smart_quotes.items():
        text = text.replace(smart, "")

    # Check if the string is just a single @
    if re.match(r"^@[\w\d_]+$", text) and discardSingleAt:
        text = ""

    # Replace URLs with "LINK"
    text = re.sub(r"https?://\S+", "LINK", text)

    text = fix_acronyms(
        text, [
            "US", "AI", "PG",
            ]
    )
    text = fix_acronyms_ignorecase(
        text,
        [
            "AFK", "BRB", "ADHD", "VFX", "AMA", "FYI", "POV", "SSD", "CPU", "AMD", "GPU", "MTG",
            "MPH", "CGI", "FBI", "RPG", "NYC", "CG", "PSA", "USB", "OBS", "HDMI", "DSLR", "LGBT",
        ],
    )

    # Replace newlines with spaces and insert periods where a newline does not end in punctuation
    text = re.sub(r"\b(?![.,!?:;])\s*(\n)+", ". ", text)
    text = text.replace("\n", " ")
    text = text.replace("@", " at ")
    text = text.replace('"', "")
    text = text.replace("#", " hashtag ")
    text = text.replace("—", "-")
    text = text.replace("%", " percent ")
    text = text.replace("=", " equals ")
    text = text.replace("+", " plus ")
    text = text.replace("&", " and ")
    text = text.replace("™", " trademark ")
    text = text.replace("<3", " heart sign ")
    text = text.replace("=/=", " does not equal ")
    text = text.replace("=\=", " does not equal ")
    text = text.replace("!=", " does not equal ")
    text = text.replace("!==", " does not equal ")
    text = text.replace("/r/", " r slash ")
    text = re.sub(r"\br/", "r slash ", text)
    text = re.sub(r":\s*\^\s*\)", r" smiley face ", text)
    text = text.replace(" :)", " smiley face ")
    text = text.replace(" :/", " upset face ")
    text = text.replace(" c:", " smiley face ")
    text = text.replace(" :D", " smiley face ")
    text = text.replace(" II ", " two ")
    text = text.replace(" III ", " three ")
    text = text.replace(" IV ", " four ")
    text = text.replace(" V ", " five ")
    text = text.replace(" VI ", " six ")
    text = text.replace(" VII ", " seven ")
    text = text.replace(" VIII ", " eight ")
    text = re.sub(r"\bAU\b", "alternate universe", text)
    text = re.sub(r"\bWSJ\b", "wall street journal", text)
    text = re.sub(r"\bWWI\b", "world war one", text)
    text = re.sub(r"\bWWII\b", "world war two", text)
    text = re.sub(r"\bWWIII\b", "world war three", text)
    text = re.sub(r"\brt\b", "retweet", text, flags=re.IGNORECASE)
    text = re.sub(r"(\bvs\.|\bvs\b)", "versus", text, flags=re.IGNORECASE) # catches "vs." or "vs"
    text = re.sub(r"\bavg\b", "average", text, flags=re.IGNORECASE)
    text = re.sub(r"\bnvm\b", "nevermind", text, flags=re.IGNORECASE)
    text = re.sub(r"\bwtf\b", "what the fuck", text, flags=re.IGNORECASE)
    text = re.sub(r"\bbtfo", "B.T.F.O", text, flags=re.IGNORECASE)
    text = re.sub(r"\blmao\b", "laughing my ass off", text, flags=re.IGNORECASE)
    text = re.sub(r"\blmfao\b", "laughing my fucking ass off", text, flags=re.IGNORECASE)
    text = re.sub(r"\btbh\b", "to be honest", text, flags=re.IGNORECASE)
    text = re.sub(r"\btbf\b", "to be fair", text, flags=re.IGNORECASE)
    text = re.sub(r"\bimo\b", "in my opinion", text, flags=re.IGNORECASE)
    text = re.sub(r"\bsmh\b", "shaking my head", text, flags=re.IGNORECASE)
    text = re.sub(r"\bsfw\b", "safe for work", text, flags=re.IGNORECASE)
    text = re.sub(r"\btfw\b", "that face when", text, flags=re.IGNORECASE)
    text = re.sub(r"\btmw\b", "that moment when", text, flags=re.IGNORECASE)
    text = re.sub(r"\bnsfw\b", "not safe for work", text, flags=re.IGNORECASE)
    text = re.sub(r"\bidc\b", "I don't care", text, flags=re.IGNORECASE)
    text = re.sub(r"\bidk\b", "I don't know", text, flags=re.IGNORECASE)
    text = re.sub(r"\bwip\b", "work in progress", text, flags=re.IGNORECASE)
    text = re.sub(r"\bjr\b", "junior", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmr\b", "mister", text, flags=re.IGNORECASE)
    text = re.sub(r"\bgoty\b", "game of the year", text, flags=re.IGNORECASE)
    text = re.sub(r"\btotk\b", "Tears of the Kingdom", text, flags=re.IGNORECASE)
    text = re.sub(r"\bjpg\b", "Jay Peg", text, flags=re.IGNORECASE)
    text = re.sub(r"\bjpeg\b", "Jay Peg", text, flags=re.IGNORECASE)
    text = re.sub(r"\brn\b", "right now", text, flags=re.IGNORECASE)
    text = re.sub(r"\bfr\b", "for real", text, flags=re.IGNORECASE)
    text = re.sub(r"\bily\b", "I love you", text, flags=re.IGNORECASE)
    text = re.sub(r"\bgl\b", "good luck", text, flags=re.IGNORECASE)
    text = re.sub(r"\bboi\b", "boy", text, flags=re.IGNORECASE)
    text = re.sub(r"\babt\b", "about", text, flags=re.IGNORECASE)
    text = re.sub(r"\bu\b", "you", text, flags=re.IGNORECASE)
    text = re.sub(r"\bok\b", "okay", text, flags=re.IGNORECASE)
    text = re.sub(r"\bIll\b", "I'll", text)
    text = re.sub(r"\b[yY]oull\b", "you'll", text)
    text = re.sub(r"ouldnt\b", "ouldn't", text)
    text = re.sub(r"\b[hH]avent\b", "haven't", text)
    text = re.sub(r"\b[dD]ont\b", "don't", text)
    text = re.sub(r"\b[wW]ont\b", "won't", text)
    text = re.sub(r"\b[tT]hats\b", "that's", text)
    text = re.sub(r"\b[yY]oure\b", "you're", text)
    text = re.sub(r"\b[yY]ouve\b", "you've", text)
    text = re.sub(r"\b[tT]heyve\b", "they've", text)
    text = re.sub(r"snt\b", "sn't", text)
    text = re.sub(r"\b[hH]es\b", "he's", text)
    text = re.sub(r"\b[sS]hes\b", "she's", text)
    text = re.sub(r"\b[tY]hatll\b", "that'll", text)
    text = re.sub(r"\b[iI]d\b", "I'd", text)
    text = re.sub(r"\b[tT]heyre\b", "they're", text)
    text = re.sub(r"\bppl\b", "people", text)
    text = re.sub(r"\bive\b", "I've", text, flags=re.IGNORECASE)
    text = re.sub(r"\bitll\b", "it'll", text, flags=re.IGNORECASE)
    text = re.sub(r"\btheyll\b", "they'll", text, flags=re.IGNORECASE)
    text = re.sub(r"\bim\b", "I'm", text, flags=re.IGNORECASE)
    text = re.sub(r"\bw/e\b", "whatever", text, flags=re.IGNORECASE)
    text = re.sub(r"\bw/\b", "with", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmeme", "meem", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmeemetic\b", "memetic", text, flags=re.IGNORECASE)
    text = re.sub(r";\s*\^\s*\)", r" winky face ", text)
    text = re.sub(r";\)", r" winky face ", text)
    text = re.sub(r">:\(", r" angry face ", text)
    text = re.sub(r"(\w)/hr\b", r"\1 per hour ", text)
    text = re.sub(r"(\w)/hour\b", r"\1 per hour ", text)
    text = re.sub(r"(\w)/mile\b", r"\1 per mile ", text)
    text = re.sub(r"(\w)/(\w)", r"\1 slash \2", text)
    text = text.replace(";", ".")
    text = text.replace(" - ", ", ")
    text = text.replace("-", " ")
    # Replace dollar signs and multiple consecutive letters
    text = re.sub(r"\$(\d+([,]\d{3})*(\.\d+)?)", r"\1 dollars", text)
    text = re.sub(r"(.)\1{2,}", replace_multiple_letters, text)

    # Do these steps last just to wrap things up

    # Remove characters that do not match alphanumerics, spaces, newlines, and specified characters
    text = re.sub(r"[^\w\s_:\n\/\'?\-.!,]", " ", text)

    # Replace any sequence of whitespace characters with a single space
    text = " ".join(text.split())

    return text
