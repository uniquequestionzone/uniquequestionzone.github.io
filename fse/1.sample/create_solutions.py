import json

solutions = {
    1: {
        "html_replace": (
            '<!-- TODO: Change this div into <label class="day-label" for="dayInput"> -->\n                <div class="day-label">Day number (1-7)</div>',
            '<label class="day-label" for="dayInput">Day number (1-7)</label>'
        ),
        "css_replace": (
            '/* TODO: Set background-color to #A7F3D0 */',
            'background-color: #A7F3D0;'
        ),
        "js_replace": (
            '''        // TODO: If n is NaN, below 1, above 7 or not whole show "Enter 1 to 7";
        // otherwise show "Day " + n + " is " + days[n - 1].''',
            '''        if (isNaN(n) || n < 1 || n > 7 || Math.floor(n) !== n) {
            dayOut.textContent = "Enter 1 to 7";
        } else {
            dayOut.textContent = "Day " + n + " is " + days[n - 1];
        }'''
        )
    },
    2: {
        "html_replace": (
            '<!-- TODO: Add placeholder="0-5" to the input below -->\n                <input id="ratingInput" class="input" type="number" min="0" max="5">',
            '<input id="ratingInput" class="input" type="number" min="0" max="5" placeholder="0-5">'
        ),
        "css_replace": (
            '/* TODO: Set color to #F59E0B */',
            'color: #F59E0B;'
        ),
        "js_replace": (
            '''        // TODO: If n is NaN, below 0, above 5 or not whole show "Enter 0 to 5".
        // Otherwise build a string with n "\\u2605" characters then (5 - n) "\\u2606" characters and show it.''',
            '''        if (isNaN(n) || n < 0 || n > 5 || Math.floor(n) !== n) {
            stars.textContent = "Enter 0 to 5";
        } else {
            var str = "";
            for (var i = 0; i < n; i++) {
                str += "\\u2605";
            }
            for (var j = 0; j < 5 - n; j++) {
                str += "\\u2606";
            }
            stars.textContent = str;
        }'''
        )
    },
    3: {
        "html_replace": (
            '<!-- TODO: Add tabindex="0" to the div below -->\n            <div id="flashcard" class="flashcard" data-front="Capital of Japan?" data-back="Tokyo">Capital of Japan?</div>',
            '<div id="flashcard" class="flashcard" data-front="Capital of Japan?" data-back="Tokyo" tabindex="0">Capital of Japan?</div>'
        ),
        "css_replace": (
            '/* TODO: Set background-color to #DDD6FE */',
            'background-color: #DDD6FE;'
        ),
        "js_replace": (
            '''        // TODO: flashcard.classList.toggle("flipped"); then set flashcard.textContent to
        // flashcard.getAttribute("data-back") when it has the class flipped, otherwise data-front.''',
            '''        flashcard.classList.toggle("flipped");
        if (flashcard.classList.contains("flipped")) {
            flashcard.textContent = flashcard.getAttribute("data-back");
        } else {
            flashcard.textContent = flashcard.getAttribute("data-front");
        }'''
        )
    },
    4: {
        "html_replace": (
            '<!-- TODO: Add max="12" to the input below -->\n                <input id="servingsInput" class="input" type="number" min="1" value="2">',
            '<input id="servingsInput" class="input" type="number" min="1" max="12" value="2">'
        ),
        "css_replace": (
            '/* TODO: Set justify-content to space-between */',
            'justify-content: space-between;'
        ),
        "js_replace": (
            '''        // TODO: Loop over quantities. If servings is NaN or below 1 set each text to "?".
        // Otherwise var base = parseFloat(span.getAttribute("data-base")); set text to parseFloat((base * servings / 2).toFixed(2)).''',
            '''        for (var i = 0; i < quantities.length; i++) {
            var span = quantities[i];
            if (isNaN(servings) || servings < 1) {
                span.textContent = "?";
            } else {
                var base = parseFloat(span.getAttribute("data-base"));
                span.textContent = parseFloat((base * servings / 2).toFixed(2));
            }
        }'''
        )
    },
    5: {
        "html_replace": (
            '<!-- TODO: Add maxlength="140" to the textarea below -->\n                <textarea id="postText" class="input" rows="3">Great show tonight</textarea>',
            '<textarea id="postText" class="input" rows="3" maxlength="140">Great show tonight</textarea>'
        ),
        "css_replace": (
            '/* TODO: Set font-size to 24px */',
            'font-size: 24px;'
        ),
        "js_replace": (
            '''        // TODO: Append emoji to the end of postText.value.''',
            '''        postText.value = postText.value + emoji;'''
        )
    },
    6: {
        "html_replace": (
            '<!-- TODO: Add step="1" to the input below -->\n                <input id="numberInput" class="input" type="number" min="0" value="49">',
            '<input id="numberInput" class="input" type="number" min="0" step="1" value="49">'
        ),
        "css_replace": (
            '/* TODO: Set box-shadow to 6px 6px 0 #111111 */',
            'box-shadow: 6px 6px 0 #111111;'
        ),
        "js_replace": (
            '''        // TODO: If n is NaN, negative or not whole show "Enter a whole number 0 or greater". var root = Math.sqrt(n);
        // if Math.floor(root) === root show n + " is a perfect square (" + root + " \\u00D7 " + root + ")", else n + " is not a perfect square".''',
            '''        if (isNaN(n) || n < 0 || Math.floor(n) !== n) {
            squareOut.textContent = "Enter a whole number 0 or greater";
        } else {
            var root = Math.sqrt(n);
            if (Math.floor(root) === root) {
                squareOut.textContent = n + " is a perfect square (" + root + " \\u00D7 " + root + ")";
            } else {
                squareOut.textContent = n + " is not a perfect square";
            }
        }'''
        )
    },
    7: {
        "html_replace": (
            '<!-- TODO: Add for="wordInput" to the label below -->\n                <label class="field-label">Word</label>',
            '<label class="field-label" for="wordInput">Word</label>'
        ),
        "css_replace": (
            '/* TODO: Set text-transform to lowercase */',
            'text-transform: lowercase;'
        ),
        "js_replace": (
            '''        // TODO: If word is "" or contains " " show "Enter one word". var lower = word.toLowerCase();
        // if "aeiou".indexOf(lower.charAt(0)) !== -1 show lower + "way", else show lower.slice(1) + lower.charAt(0) + "ay".''',
            '''        if (word === "" || word.indexOf(" ") !== -1) {
            pigOut.textContent = "Enter one word";
        } else {
            var lower = word.toLowerCase();
            if ("aeiou".indexOf(lower.charAt(0)) !== -1) {
                pigOut.textContent = lower + "way";
            } else {
                pigOut.textContent = lower.slice(1) + lower.charAt(0) + "ay";
            }
        }'''
        )
    },
    8: {
        "html_replace": (
            '<!-- TODO: Change this span into a <strong> element (keep id="ticketCount") -->\n                <span id="ticketCount">5</span>',
            '<strong id="ticketCount">5</strong>'
        ),
        "css_replace": (
            '/* TODO: Set cursor to not-allowed */',
            'cursor: not-allowed;'
        ),
        "js_replace": (
            '''        // TODO: If left > 0: left = left - 1 and show it in ticketCount. Then if left === 0 show "Sold out"
        // in ticketStatus and set buyBtn.disabled = true; otherwise show "Available".''',
            '''        if (left > 0) {
            left = left - 1;
            ticketCount.textContent = left;
            if (left === 0) {
                ticketStatus.textContent = "Sold out";
                buyBtn.disabled = true;
            } else {
                ticketStatus.textContent = "Available";
            }
        }'''
        )
    },
    9: {
        "html_replace": (
            '<!-- TODO: Add min="1" to the input below -->\n                    <input id="posInput" class="input" type="number" value="2">',
            '<input id="posInput" class="input" type="number" min="1" value="2">'
        ),
        "css_replace": (
            '/* TODO: Set width to 64px */',
            'width: 64px;'
        ),
        "js_replace": (
            '''        // TODO: If word is "" → letterOut "?" and status "Enter a word". If pos is NaN, not whole, below 1 or above word.length
        // → letterOut "?" and status "Position must be 1 to " + word.length. Otherwise letterOut = word.charAt(pos - 1)
        // and status "Letter " + pos + " is " + that letter.''',
            '''        if (word === "") {
            letterOut.textContent = "?";
            letterStatus.textContent = "Enter a word";
        } else if (isNaN(pos) || Math.floor(pos) !== pos || pos < 1 || pos > word.length) {
            letterOut.textContent = "?";
            letterStatus.textContent = "Position must be 1 to " + word.length;
        } else {
            var ch = word.charAt(pos - 1);
            letterOut.textContent = ch;
            letterStatus.textContent = "Letter " + pos + " is " + ch;
        }'''
        )
    },
    10: {
        "html_replace": (
            '<!-- TODO: Add spellcheck="false" to the input below -->\n                <input id="sentenceInput" class="input" type="text" value="an extraordinary day">',
            '<input id="sentenceInput" class="input" type="text" spellcheck="false" value="an extraordinary day">'
        ),
        "css_replace": (
            '/* TODO: Set text-decoration to underline */',
            'text-decoration: underline;'
        ),
        "js_replace": (
            '''        // TODO: If text is "" show "Enter a sentence". Split on " " and loop; keep the first word whose length is
        // strictly greater than the best so far. Show "Longest: " + word + " (" + word.length + " letters)".''',
            '''        if (text === "") {
            longestOut.textContent = "Enter a sentence";
        } else {
            var words = text.split(" ");
            var best = "";
            for (var i = 0; i < words.length; i++) {
                var w = words[i];
                if (w.length > best.length) {
                    best = w;
                }
            }
            longestOut.textContent = "Longest: " + best + " (" + best.length + " letters)";
        }'''
        )
    },
    11: {
        "html_replace": (
            '<!-- TODO: Add title="Select all items" to the checkbox below -->\n                <input id="selectAll" type="checkbox">',
            '<input id="selectAll" type="checkbox" title="Select all items">'
        ),
        "css_replace": (
            '/* TODO: Set accent-color to #7C3AED */',
            'accent-color: #7C3AED;'
        ),
        "js_replace": (
            '''        // TODO: Loop over boxes and set each .checked to selectAll.checked, then call refreshCount().''',
            '''        for (var i = 0; i < boxes.length; i++) {
            boxes[i].checked = selectAll.checked;
        }
        refreshCount();'''
        )
    },
    12: {
        "html_replace": (
            '<!-- TODO: Add cols="40" to the textarea below -->\n                <textarea id="sentenceInput" class="input" rows="3">the quick brown fox</textarea>',
            '<textarea id="sentenceInput" class="input" rows="3" cols="40">the quick brown fox</textarea>'
        ),
        "css_replace": (
            '/* TODO: Set text-indent to 12px */',
            'text-indent: 12px;'
        ),
        "js_replace": (
            '''        // TODO: If text is "" show "Enter a sentence". Otherwise split on " ", push non-empty pieces into words,
        // loop from the end to build a reversed array and show it joined with " ".''',
            '''        if (text === "") {
            reversedOut.textContent = "Enter a sentence";
        } else {
            var raw = text.split(" ");
            var words = [];
            for (var i = 0; i < raw.length; i++) {
                if (raw[i] !== "") {
                    words.push(raw[i]);
                }
            }
            var reversed = [];
            for (var j = words.length - 1; j >= 0; j--) {
                reversed.push(words[j]);
            }
            reversedOut.textContent = reversed.join(" ");
        }'''
        )
    },
    13: {
        "html_replace": (
            '<!-- TODO: Add role="progressbar" to the div below -->\n                <div id="progressFill" class="progress-fill"></div>',
            '<div id="progressFill" class="progress-fill" role="progressbar"></div>'
        ),
        "css_replace": (
            '/* TODO: Set background-color to #7C3AED */',
            'background-color: #7C3AED;'
        ),
        "js_replace": (
            '''        // TODO: Count the checked boxes into n. progressFill.style.width = (n / boxes.length * 100) + "%";
        // readCount.textContent = n + " of " + boxes.length + " read".''',
            '''        var n = 0;
        for (var i = 0; i < boxes.length; i++) {
            if (boxes[i].checked) {
                n = n + 1;
            }
        }
        progressFill.style.width = (n / boxes.length * 100) + "%";
        readCount.textContent = n + " of " + boxes.length + " read";'''
        )
    },
    14: {
        "html_replace": (
            '''                <!-- TODO: Change each of the three <div class="note-card"> elements below into <article class="note-card"> -->
                <div class="note-card"><span class="note-title">Buy milk</span><button class="pin-btn" type="button" aria-label="Pin Buy milk">📌</button></div>
                <div class="note-card"><span class="note-title">Book dentist</span><button class="pin-btn" type="button" aria-label="Pin Book dentist">📌</button></div>
                <div class="note-card"><span class="note-title">Call grandma</span><button class="pin-btn" type="button" aria-label="Pin Call grandma">📌</button></div>''',
            '''                <article class="note-card"><span class="note-title">Buy milk</span><button class="pin-btn" type="button" aria-label="Pin Buy milk">📌</button></article>
                <article class="note-card"><span class="note-title">Book dentist</span><button class="pin-btn" type="button" aria-label="Pin Book dentist">📌</button></article>
                <article class="note-card"><span class="note-title">Call grandma</span><button class="pin-btn" type="button" aria-label="Pin Call grandma">📌</button></article>'''
        ),
        "css_replace": (
            '/* TODO: Set background-color to #FDE68A */',
            'background-color: #FDE68A;'
        ),
        "js_replace": (
            '''        // TODO: notes.insertBefore(card, notes.firstChild);
        // pinStatus.textContent = "Pinned: " + card.querySelector(".note-title").textContent.''',
            '''        notes.insertBefore(card, notes.firstChild);
        pinStatus.textContent = "Pinned: " + card.querySelector(".note-title").textContent;'''
        )
    },
    15: {
        "html_replace": (
            '<!-- TODO: Add placeholder="type something" to the input below -->\n                <input id="textInput" class="input" type="text" value="hello world">',
            '<input id="textInput" class="input" type="text" placeholder="type something" value="hello world">'
        ),
        "css_replace": (
            '/* TODO: Set font-family to "Comic Sans MS", cursive */',
            'font-family: "Comic Sans MS", cursive;'
        ),
        "js_replace": (
            '''        // TODO: If text.trim() is "" show "Type something first". Otherwise loop over text with index i and append
        // text.charAt(i).toUpperCase() when i % 2 === 0, else .toLowerCase(); show the result.''',
            '''        if (text.trim() === "") {
            altOut.textContent = "Type something first";
        } else {
            var res = "";
            for (var i = 0; i < text.length; i++) {
                if (i % 2 === 0) {
                    res += text.charAt(i).toUpperCase();
                } else {
                    res += text.charAt(i).toLowerCase();
                }
            }
            altOut.textContent = res;
        }'''
        )
    },
    16: {
        "html_replace": (
            '<!-- TODO: Change type="text" to type="number" on the input below -->\n                    <input id="peopleInput" class="input" type="text" value="3">',
            '<input id="peopleInput" class="input" type="number" value="3">'
        ),
        "css_replace": (
            '/* TODO: Set background-color to #FBCFE8 */',
            'background-color: #FBCFE8;'
        ),
        "js_replace": (
            '''        // TODO: Validate slices (whole, >= 0) → "Enter slices"; people (whole, >= 1) → "Enter at least 1 person".
        // each = Math.floor(slices / people); left = slices % people;
        // show "Each person gets " + each + (each === 1 ? " slice, " : " slices, ") + left + " left over".''',
            '''        if (isNaN(slices) || Math.floor(slices) !== slices || slices < 0) {
            shareOut.textContent = "Enter slices";
        } else if (isNaN(people) || Math.floor(people) !== people || people < 1) {
            shareOut.textContent = "Enter at least 1 person";
        } else {
            var each = Math.floor(slices / people);
            var left = slices % people;
            shareOut.textContent = "Each person gets " + each + (each === 1 ? " slice, " : " slices, ") + left + " left over";
        }'''
        )
    },
    17: {
        "html_replace": (
            '<!-- TODO: Add the selected attribute to the Red option below -->\n                    <select id="colorA" class="input">\n                        <option value="blue">Blue</option>\n                        <option value="red">Red</option>',
            '<select id="colorA" class="input">\n                        <option value="blue">Blue</option>\n                        <option value="red" selected>Red</option>'
        ),
        "css_replace": (
            '/* TODO: Set outline to 3px dashed #111111 */',
            'outline: 3px dashed #111111;'
        ),
        "js_replace": (
            '''        // TODO: If a === b show "Still " + a. Otherwise var result = mixes[a + "+" + b];
        // if result is undefined use mixes[b + "+" + a]; show result.''',
            '''        if (a === b) {
            mixOut.textContent = "Still " + a;
        } else {
            var result = mixes[a + "+" + b];
            if (result === undefined) {
                result = mixes[b + "+" + a];
            }
            mixOut.textContent = result;
        }'''
        )
    },
    18: {
        "html_replace": (
            '<!-- TODO: Add aria-live="polite" to the div below -->\n            <div id="sentenceOut" class="result sentence-out"></div>',
            '<div id="sentenceOut" class="result sentence-out" aria-live="polite"></div>'
        ),
        "css_replace": (
            '/* TODO: Set text-shadow to 2px 2px 0 #FDE68A */',
            'text-shadow: 2px 2px 0 #FDE68A;'
        ),
        "js_replace": (
            '''        // TODO: var sentence = parts.join(" ");
        // show sentence.charAt(0).toUpperCase() + sentence.slice(1) + "." in sentenceOut.''',
            '''        var sentence = parts.join(" ");
        sentenceOut.textContent = sentence.charAt(0).toUpperCase() + sentence.slice(1) + ".";'''
        )
    },
    19: {
        "html_replace": (
            '<!-- TODO: Add max="100" to the input below -->\n                <input id="scoreInput" class="input" type="number" min="0" value="85">',
            '<input id="scoreInput" class="input" type="number" min="0" max="100" value="85">'
        ),
        "css_replace": (
            '/* TODO: Set font-size to 48px */',
            'font-size: 48px;'
        ),
        "js_replace": (
            '''        // TODO: If score is NaN, below 0 or above 100 show "Enter a score from 0 to 100".
        // Otherwise pick the letter (>= 90 A, >= 80 B, >= 70 C, >= 60 D, else F) and show "Score " + score + " \\u2192 " + letter.''',
            '''        if (isNaN(score) || score < 0 || score > 100) {
            gradeOut.textContent = "Enter a score from 0 to 100";
        } else {
            var letter = "F";
            if (score >= 90) {
                letter = "A";
            } else if (score >= 80) {
                letter = "B";
            } else if (score >= 70) {
                letter = "C";
            } else if (score >= 60) {
                letter = "D";
            }
            gradeOut.textContent = "Score " + score + " \\u2192 " + letter;
        }'''
        )
    },
    20: {
        "html_replace": (
            '<!-- TODO: Add the checked attribute to the radio below -->\n                <label class="size-option"><input class="size-radio" type="radio" name="size" value="medium" data-price="12">Medium — $12</label>',
            '<label class="size-option"><input class="size-radio" type="radio" name="size" value="medium" data-price="12" checked>Medium — $12</label>'
        ),
        "css_replace": (
            '/* TODO: Set gap to 10px */',
            'gap: 10px;'
        ),
        "js_replace": (
            '''        // TODO: If checked is null show "Pick a size". Otherwise var size = checked.value;
        // show size.charAt(0).toUpperCase() + size.slice(1) + " pizza: $" + checked.getAttribute("data-price").''',
            '''        if (!checked) {
            priceOut.textContent = "Pick a size";
        } else {
            var size = checked.value;
            priceOut.textContent = size.charAt(0).toUpperCase() + size.slice(1) + " pizza: $" + checked.getAttribute("data-price");
        }'''
        )
    },
    21: {
        "html_replace": (
            '<!-- TODO: Add autocomplete="off" to the input below -->\n                    <input id="scoreInput" class="input" type="number" min="0" value="120">',
            '<input id="scoreInput" class="input" type="number" min="0" value="120" autocomplete="off">'
        ),
        "css_replace": (
            '/* TODO: Set color to #16A34A */',
            'color: #16A34A;'
        ),
        "js_replace": (
            '''        // TODO: If score is NaN or below 0 show "Enter a score". If score > best: best = score, show best in bestScore
        // and status "New high score!"; otherwise status "Best remains " + best.''',
            '''        if (isNaN(score) || score < 0) {
            scoreStatus.textContent = "Enter a score";
        } else {
            if (score > best) {
                best = score;
                bestScore.textContent = best;
                scoreStatus.textContent = "New high score!";
            } else {
                scoreStatus.textContent = "Best remains " + best;
            }
        }'''
        )
    },
    22: {
        "html_replace": (
            '<!-- TODO: Add aria-required="true" to the input below -->\n                <input id="nickname" class="input" type="text" placeholder="e.g. pixelpanda">',
            '<input id="nickname" class="input" type="text" placeholder="e.g. pixelpanda" aria-required="true">'
        ),
        "css_replace": (
            '/* TODO: Set color to #DC2626 */',
            'color: #DC2626;'
        ),
        "js_replace": (
            '''        // TODO: If value is "" show "Nickname is required" in nickError and nickname.classList.add("invalid");
        // otherwise set nickError text to "" and nickname.classList.remove("invalid").''',
            '''        if (value === "") {
            nickError.textContent = "Nickname is required";
            nickname.classList.add("invalid");
        } else {
            nickError.textContent = "";
            nickname.classList.remove("invalid");
        }'''
        )
    },
    23: {
        "html_replace": (
            '<!-- TODO: Add role="img" to the div below -->\n            <div id="sticker" class="sticker" aria-label="Star sticker">★</div>',
            '<div id="sticker" class="sticker" aria-label="Star sticker" role="img">★</div>'
        ),
        "css_replace": (
            '/* TODO: Set transition to transform 0.3s ease */',
            'transition: transform 0.3s ease;'
        ),
        "js_replace": (
            '''        // TODO: angle = (angle + 90) % 360; sticker.style.transform = "rotate(" + angle + "deg)";
        // angleOut.textContent = angle + "\\u00B0".''',
            '''        angle = (angle + 90) % 360;
        sticker.style.transform = "rotate(" + angle + "deg)";
        angleOut.textContent = angle + "\\u00B0";'''
        )
    },
    24: {
        "html_replace": (
            '<!-- TODO: Add role="list" to the ul below -->\n            <ul id="favorites" class="list favorites"></ul>',
            '<ul id="favorites" class="list favorites" role="list"></ul>'
        ),
        "css_replace": (
            '/* TODO: Set color to #7C3AED */',
            'color: #7C3AED;'
        ),
        "js_replace": (
            '''        // TODO: favorites.appendChild(item); button.disabled = true; var n = favorites.children.length;
        // favCount.textContent = n === 1 ? "1 favorite" : n + " favorites".''',
            '''        favorites.appendChild(item);
        button.disabled = true;
        var n = favorites.children.length;
        favCount.textContent = n === 1 ? "1 favorite" : n + " favorites";'''
        )
    },
    25: {
        "html_replace": (
            '<!-- TODO: Add enterkeyhint="done" to the input below -->\n                    <input id="wordB" class="input" type="text" value="hat">',
            '<input id="wordB" class="input" type="text" value="hat" enterkeyhint="done">'
        ),
        "css_replace": (
            '/* TODO: Set padding-left to 24px */',
            'padding-left: 24px;'
        ),
        "js_replace": (
            '''        // TODO: If a.length < 3 or b.length < 3 show "Enter two words with at least 3 letters".
        // Compare a.toLowerCase().slice(-2) with b.toLowerCase().slice(-2): show a + " and " + b + " rhyme!" or a + " and " + b + " do not rhyme".''',
            '''        if (a.length < 3 || b.length < 3) {
            rhymeOut.textContent = "Enter two words with at least 3 letters";
        } else {
            if (a.toLowerCase().slice(-2) === b.toLowerCase().slice(-2)) {
                rhymeOut.textContent = a + " and " + b + " rhyme!";
            } else {
                rhymeOut.textContent = a + " and " + b + " do not rhyme";
            }
        }'''
        )
    },
    26: {
        "html_replace": (
            '<!-- TODO: Add aria-label="Word" to the input below -->\n                    <input id="wordInput" class="input" type="text" value="quiz" placeholder="Type a word">',
            '<input id="wordInput" class="input" type="text" value="quiz" placeholder="Type a word" aria-label="Word">'
        ),
        "css_replace": (
            '/* TODO: Set font-size to 36px */',
            'font-size: 36px;'
        ),
        "js_replace": (
            '''        // TODO: If word is "" show "Enter a word". Loop over word: if values[ch] is undefined show "Letters only" and stop,
        // otherwise add values[ch] to a total. Finally show "Score: " + total.''',
            '''        if (word === "") {
            scoreOut.textContent = "Enter a word";
        } else {
            var total = 0;
            var invalid = false;
            for (var i = 0; i < word.length; i++) {
                var ch = word.charAt(i);
                if (values[ch] === undefined) {
                    scoreOut.textContent = "Letters only";
                    invalid = true;
                    break;
                }
                total += values[ch];
            }
            if (!invalid) {
                scoreOut.textContent = "Score: " + total;
            }
        }'''
        )
    },
    27: {
        "html_replace": (
            '''            <fieldset class="ingredient-box">
                <!-- TODO: Add <legend>Pick ingredients</legend> here, as the first child of the fieldset -->

                <label class="check">''',
            '''            <fieldset class="ingredient-box">
                <legend>Pick ingredients</legend>
                <label class="check">'''
        ),
        "css_replace": (
            '/* TODO: Set font-weight to 800 */',
            'font-weight: 800;'
        ),
        "js_replace": (
            '''        // TODO: Push the value of each checked box into an array. If it is empty show "Pick at least one ingredient";
        // otherwise show "Your smoothie: " + picked.join(", ").''',
            '''        var picked = [];
        for (var i = 0; i < boxes.length; i++) {
            if (boxes[i].checked) {
                picked.push(boxes[i].value);
            }
        }
        if (picked.length === 0) {
            blendOut.textContent = "Pick at least one ingredient";
        } else {
            blendOut.textContent = "Your smoothie: " + picked.join(", ");
        }'''
        )
    },
    28: {
        "html_replace": (
            '<!-- TODO: Add lang="en" to the <html> element below -->\n<html>',
            '<html lang="en">'
        ),
        "css_replace": (
            '/* TODO: Set border-style to dashed */',
            'border-style: dashed;'
        ),
        "js_replace": (
            '''        // TODO: current = current === "en" ? "es" : "en"; for each node set textContent to node.getAttribute("data-" + current);
        // then set langBtn.textContent to "EN" when current is "es", otherwise "ES".''',
            '''        current = current === "en" ? "es" : "en";
        for (var i = 0; i < nodes.length; i++) {
            nodes[i].textContent = nodes[i].getAttribute("data-" + current);
        }
        langBtn.textContent = current === "es" ? "EN" : "ES";'''
        )
    },
    29: {
        "html_replace": (
            '<!-- TODO: Change this div into an <output> element (keep id and class) -->\n            <div id="totalOut" class="result">Total: $8.00</div>',
            '<output id="totalOut" class="result">Total: $8.00</output>'
        ),
        "css_replace": (
            '/* TODO: Set cursor to pointer */',
            'cursor: pointer;'
        ),
        "js_replace": (
            '''        // TODO: For each checked box add parseFloat(box.getAttribute("data-price")) to total,
        // then show "Total: $" + total.toFixed(2) in totalOut.''',
            '''        for (var i = 0; i < boxes.length; i++) {
            if (boxes[i].checked) {
                total += parseFloat(boxes[i].getAttribute("data-price"));
            }
        }
        totalOut.textContent = "Total: $" + total.toFixed(2);'''
        )
    }
}

with open("solutions_dict.json", "w", encoding="utf-8") as f:
    json.dump(solutions, f, indent=2)

print("Saved solutions_dict.json successfully!")
