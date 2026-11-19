const assert = require('assert');

console.log("Testing all 29 questions logic...");

// Q1: Weekday Lookup
// 1 Monday, 7 Sunday, not whole / out of bounds -> "Enter 1 to 7"
{
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    function q1(inputVal) {
        var n = parseFloat(inputVal);
        if (isNaN(n) || n < 1 || n > 7 || Math.floor(n) !== n) {
            return "Enter 1 to 7";
        } else {
            return "Day " + n + " is " + days[n - 1];
        }
    }
    assert.strictEqual(q1("3"), "Day 3 is Wednesday");
    assert.strictEqual(q1("1"), "Day 1 is Monday");
    assert.strictEqual(q1("7"), "Day 7 is Sunday");
    assert.strictEqual(q1("0"), "Enter 1 to 7");
    assert.strictEqual(q1("8"), "Enter 1 to 7");
    assert.strictEqual(q1("3.5"), "Enter 1 to 7");
    assert.strictEqual(q1("abc"), "Enter 1 to 7");
    console.log("✓ Q1 passed");
}

// Q2: Star Rating Preview
// n between 0 and 5 whole. n filled stars, 5-n empty stars.
{
    function q2(inputVal) {
        var n = parseFloat(inputVal);
        if (isNaN(n) || n < 0 || n > 5 || Math.floor(n) !== n) {
            return "Enter 0 to 5";
        } else {
            var str = "";
            for (var i = 0; i < n; i++) {
                str += "\u2605";
            }
            for (var j = 0; j < 5 - n; j++) {
                str += "\u2606";
            }
            return str;
        }
    }
    assert.strictEqual(q2("3"), "★★★☆☆");
    assert.strictEqual(q2("0"), "☆☆☆☆☆");
    assert.strictEqual(q2("5"), "★★★★★");
    assert.strictEqual(q2("-1"), "Enter 0 to 5");
    assert.strictEqual(q2("6"), "Enter 0 to 5");
    assert.strictEqual(q2("2.5"), "Enter 0 to 5");
    console.log("✓ Q2 passed");
}

// Q3: Flashcard Flip
// toggle flipped; textContent = flipped ? data-back : data-front
{
    let flipped = false;
    function q3(front, back) {
        flipped = !flipped;
        return flipped ? back : front;
    }
    assert.strictEqual(q3("Capital of Japan?", "Tokyo"), "Tokyo");
    assert.strictEqual(q3("Capital of Japan?", "Tokyo"), "Capital of Japan?");
    console.log("✓ Q3 passed");
}

// Q4: Recipe Scaler
// servings NaN or < 1 -> "?", else parseFloat((base * servings / 2).toFixed(2))
{
    function q4(base, servingsVal) {
        var servings = parseFloat(servingsVal);
        if (isNaN(servings) || servings < 1) {
            return "?";
        } else {
            return parseFloat((base * servings / 2).toFixed(2));
        }
    }
    assert.strictEqual(q4(1.5, "3"), 2.25);
    assert.strictEqual(q4(250, "4"), 500);
    assert.strictEqual(q4(250, "0"), "?");
    assert.strictEqual(q4(250, "-2"), "?");
    console.log("✓ Q4 passed");
}

// Q5: Emoji Inserter
// Append emoji to end of postText.value
{
    function q5(currentVal, emoji) {
        return currentVal + emoji;
    }
    assert.strictEqual(q5("Great show tonight", "🎉"), "Great show tonight🎉");
    console.log("✓ Q5 passed");
}

// Q6: Square Number Check
{
    function q6(inputVal) {
        var n = parseFloat(inputVal);
        if (isNaN(n) || n < 0 || Math.floor(n) !== n) {
            return "Enter a whole number 0 or greater";
        } else {
            var root = Math.sqrt(n);
            if (Math.floor(root) === root) {
                return n + " is a perfect square (" + root + " \u00D7 " + root + ")";
            } else {
                return n + " is not a perfect square";
            }
        }
    }
    assert.strictEqual(q6("49"), "49 is a perfect square (7 × 7)");
    assert.strictEqual(q6("0"), "0 is a perfect square (0 × 0)");
    assert.strictEqual(q6("50"), "50 is not a perfect square");
    assert.strictEqual(q6("-4"), "Enter a whole number 0 or greater");
    assert.strictEqual(q6("4.5"), "Enter a whole number 0 or greater");
    console.log("✓ Q6 passed");
}

// Q7: Pig Latin Word
{
    function q7(word) {
        word = word.trim();
        if (word === "" || word.indexOf(" ") !== -1) {
            return "Enter one word";
        } else {
            var lower = word.toLowerCase();
            if ("aeiou".indexOf(lower.charAt(0)) !== -1) {
                return lower + "way";
            } else {
                return lower.slice(1) + lower.charAt(0) + "ay";
            }
        }
    }
    assert.strictEqual(q7("Pizza"), "izzapay");
    assert.strictEqual(q7("apple"), "appleway");
    assert.strictEqual(q7("two words"), "Enter one word");
    assert.strictEqual(q7(""), "Enter one word");
    console.log("✓ Q7 passed");
}

// Q8: Tickets Left
{
    let left = 5;
    function buy() {
        if (left > 0) {
            left = left - 1;
            var status = left === 0 ? "Sold out" : "Available";
            var disabled = left === 0;
            return { left, status, disabled };
        }
    }
    assert.deepStrictEqual(buy(), { left: 4, status: "Available", disabled: false });
    buy(); buy(); buy();
    assert.deepStrictEqual(buy(), { left: 0, status: "Sold out", disabled: true });
    console.log("✓ Q8 passed");
}

// Q9: Letter at Position
{
    function q9(word, posVal) {
        word = word.trim();
        var pos = parseFloat(posVal);
        if (word === "") {
            return { out: "?", status: "Enter a word" };
        } else if (isNaN(pos) || Math.floor(pos) !== pos || pos < 1 || pos > word.length) {
            return { out: "?", status: "Position must be 1 to " + word.length };
        } else {
            var ch = word.charAt(pos - 1);
            return { out: ch, status: "Letter " + pos + " is " + ch };
        }
    }
    assert.deepStrictEqual(q9("Planet", "2"), { out: "l", status: "Letter 2 is l" });
    assert.deepStrictEqual(q9("", "2"), { out: "?", status: "Enter a word" });
    assert.deepStrictEqual(q9("Cat", "5"), { out: "?", status: "Position must be 1 to 3" });
    console.log("✓ Q9 passed");
}

// Q10: Longest Word
{
    function q10(text) {
        text = text.trim();
        if (text === "") {
            return "Enter a sentence";
        } else {
            var words = text.split(" ");
            var best = "";
            for (var i = 0; i < words.length; i++) {
                var w = words[i];
                if (w.length > best.length) {
                    best = w;
                }
            }
            return "Longest: " + best + " (" + best.length + " letters)";
        }
    }
    assert.strictEqual(q10("an extraordinary day"), "Longest: extraordinary (13 letters)");
    assert.strictEqual(q10(""), "Enter a sentence");
    console.log("✓ Q10 passed");
}

// Q11: Packing List Select-All
{
    let boxes = [false, false, false];
    function selectAllToggle(val) {
        for (var i = 0; i < boxes.length; i++) {
            boxes[i] = val;
        }
        var n = boxes.filter(Boolean).length;
        return n + " of " + boxes.length + " packed";
    }
    assert.strictEqual(selectAllToggle(true), "3 of 3 packed");
    assert.strictEqual(selectAllToggle(false), "0 of 3 packed");
    console.log("✓ Q11 passed");
}

// Q12: Reverse Word Order
{
    function q12(text) {
        text = text.trim();
        if (text === "") {
            return "Enter a sentence";
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
            return reversed.join(" ");
        }
    }
    assert.strictEqual(q12("the quick brown fox"), "fox brown quick the");
    assert.strictEqual(q12(""), "Enter a sentence");
    console.log("✓ Q12 passed");
}

// Q13: Reading Checklist
{
    function q13(boxes) {
        var n = 0;
        for (var i = 0; i < boxes.length; i++) {
            if (boxes[i]) n++;
        }
        var width = (n / boxes.length * 100) + "%";
        var text = n + " of " + boxes.length + " read";
        return { width, text };
    }
    assert.deepStrictEqual(q13([true, true, false, false, false]), { width: "40%", text: "2 of 5 read" });
    console.log("✓ Q13 passed");
}

// Q14: Pin Note to Top
{
    let notes = ["Buy milk", "Book dentist", "Call grandma"];
    function pin(title) {
        notes = [title, ...notes.filter(x => x !== title)];
        return "Pinned: " + title;
    }
    assert.strictEqual(pin("Call grandma"), "Pinned: Call grandma");
    assert.strictEqual(notes[0], "Call grandma");
    console.log("✓ Q14 passed");
}

// Q15: Alternating Caps
{
    function q15(text) {
        if (text.trim() === "") {
            return "Type something first";
        } else {
            var res = "";
            for (var i = 0; i < text.length; i++) {
                if (i % 2 === 0) {
                    res += text.charAt(i).toUpperCase();
                } else {
                    res += text.charAt(i).toLowerCase();
                }
            }
            return res;
        }
    }
    assert.strictEqual(q15("hello world"), "HeLlO WoRlD");
    assert.strictEqual(q15("   "), "Type something first");
    console.log("✓ Q15 passed");
}

// Q16: Pizza Slice Share
{
    function q16(sVal, pVal) {
        var slices = parseFloat(sVal);
        var people = parseFloat(pVal);
        if (isNaN(slices) || Math.floor(slices) !== slices || slices < 0) {
            return "Enter slices";
        } else if (isNaN(people) || Math.floor(people) !== people || people < 1) {
            return "Enter at least 1 person";
        } else {
            var each = Math.floor(slices / people);
            var left = slices % people;
            return "Each person gets " + each + (each === 1 ? " slice, " : " slices, ") + left + " left over";
        }
    }
    assert.strictEqual(q16("10", "3"), "Each person gets 3 slices, 1 left over");
    assert.strictEqual(q16("4", "3"), "Each person gets 1 slice, 1 left over");
    assert.strictEqual(q16("abc", "3"), "Enter slices");
    assert.strictEqual(q16("10", "0"), "Enter at least 1 person");
    console.log("✓ Q16 passed");
}

// Q17: Color Mixer
{
    var mixes = { 'red+blue': 'Purple', 'red+yellow': 'Orange', 'blue+yellow': 'Green' };
    function q17(a, b) {
        if (a === b) {
            return "Still " + a;
        } else {
            var result = mixes[a + "+" + b];
            if (result === undefined) {
                result = mixes[b + "+" + a];
            }
            return result;
        }
    }
    assert.strictEqual(q17("red", "blue"), "Purple");
    assert.strictEqual(q17("blue", "red"), "Purple");
    assert.strictEqual(q17("blue", "blue"), "Still blue");
    console.log("✓ Q17 passed");
}

// Q18: Silly Sentence Builder
{
    function q18(parts) {
        var sentence = parts.join(" ");
        return sentence.charAt(0).toUpperCase() + sentence.slice(1) + ".";
    }
    assert.strictEqual(q18(["the robot", "juggled", "pancakes"]), "The robot juggled pancakes.");
    console.log("✓ Q18 passed");
}

// Q19: Grade Letter
{
    function q19(sVal) {
        var score = parseFloat(sVal);
        if (isNaN(score) || score < 0 || score > 100) {
            return "Enter a score from 0 to 100";
        } else {
            var letter = "F";
            if (score >= 90) letter = "A";
            else if (score >= 80) letter = "B";
            else if (score >= 70) letter = "C";
            else if (score >= 60) letter = "D";
            return "Score " + score + " \u2192 " + letter;
        }
    }
    assert.strictEqual(q19("85"), "Score 85 → B");
    assert.strictEqual(q19("95"), "Score 95 → A");
    assert.strictEqual(q19("59"), "Score 59 → F");
    assert.strictEqual(q19("105"), "Enter a score from 0 to 100");
    console.log("✓ Q19 passed");
}

// Q20: Pizza Size Price
{
    function q20(val, price) {
        if (!val) {
            return "Pick a size";
        } else {
            return val.charAt(0).toUpperCase() + val.slice(1) + " pizza: $" + price;
        }
    }
    assert.strictEqual(q20("medium", "12"), "Medium pizza: $12");
    assert.strictEqual(q20(null, null), "Pick a size");
    console.log("✓ Q20 passed");
}

// Q21: High Score Tracker
{
    let best = 0;
    function q21(scoreVal) {
        var score = parseFloat(scoreVal);
        if (isNaN(score) || score < 0) {
            return "Enter a score";
        } else {
            if (score > best) {
                best = score;
                return { best, status: "New high score!" };
            } else {
                return { best, status: "Best remains " + best };
            }
        }
    }
    assert.deepStrictEqual(q21("120"), { best: 120, status: "New high score!" });
    assert.deepStrictEqual(q21("100"), { best: 120, status: "Best remains 120" });
    assert.deepStrictEqual(q21("150"), { best: 150, status: "New high score!" });
    console.log("✓ Q21 passed");
}

// Q22: Nickname Required
{
    function q22(val) {
        var value = val.trim();
        if (value === "") {
            return { error: "Nickname is required", invalid: true };
        } else {
            return { error: "", invalid: false };
        }
    }
    assert.deepStrictEqual(q22(""), { error: "Nickname is required", invalid: true });
    assert.deepStrictEqual(q22("coolcat"), { error: "", invalid: false });
    console.log("✓ Q22 passed");
}

// Q23: Rotate Sticker
{
    let angle = 0;
    function rotate() {
        angle = (angle + 90) % 360;
        return { transform: "rotate(" + angle + "deg)", text: angle + "\u00B0" };
    }
    assert.deepStrictEqual(rotate(), { transform: "rotate(90deg)", text: "90°" });
    assert.deepStrictEqual(rotate(), { transform: "rotate(180deg)", text: "180°" });
    assert.deepStrictEqual(rotate(), { transform: "rotate(270deg)", text: "270°" });
    assert.deepStrictEqual(rotate(), { transform: "rotate(0deg)", text: "0°" });
    console.log("✓ Q23 passed");
}

// Q24: Add to Favorites
{
    let list = [];
    function addFav(title) {
        list.push(title);
        var n = list.length;
        return n === 1 ? "1 favorite" : n + " favorites";
    }
    assert.strictEqual(addFav("Song A"), "1 favorite");
    assert.strictEqual(addFav("Song B"), "2 favorites");
    console.log("✓ Q24 passed");
}

// Q25: Rhyme Check
{
    function q25(wA, wB) {
        var a = wA.trim();
        var b = wB.trim();
        if (a.length < 3 || b.length < 3) {
            return "Enter two words with at least 3 letters";
        } else {
            if (a.toLowerCase().slice(-2) === b.toLowerCase().slice(-2)) {
                return a + " and " + b + " rhyme!";
            } else {
                return a + " and " + b + " do not rhyme";
            }
        }
    }
    assert.strictEqual(q25("cat", "hat"), "cat and hat rhyme!");
    assert.strictEqual(q25("dog", "cat"), "dog and cat do not rhyme");
    assert.strictEqual(q25("hi", "bye"), "Enter two words with at least 3 letters");
    console.log("✓ Q25 passed");
}

// Q26: Scrabble Score
{
    var values = {
        a: 1, b: 3, c: 3, d: 2, e: 1, f: 4, g: 2, h: 4, i: 1, j: 8, k: 5, l: 1, m: 3,
        n: 1, o: 1, p: 3, q: 10, r: 1, s: 1, t: 1, u: 1, v: 4, w: 4, x: 8, y: 4, z: 10
    };
    function q26(w) {
        var word = w.trim().toLowerCase();
        if (word === "") {
            return "Enter a word";
        } else {
            var total = 0;
            var invalid = false;
            for (var i = 0; i < word.length; i++) {
                var ch = word.charAt(i);
                if (values[ch] === undefined) {
                    invalid = true;
                    return "Letters only";
                }
                total += values[ch];
            }
            return "Score: " + total;
        }
    }
    // quiz: q(10)+u(1)+i(1)+z(10) = 22
    assert.strictEqual(q26("quiz"), "Score: 22");
    assert.strictEqual(q26(""), "Enter a word");
    assert.strictEqual(q26("quiz123"), "Letters only");
    console.log("✓ Q26 passed");
}

// Q27: Smoothie Builder
{
    function q27(picked) {
        if (picked.length === 0) {
            return "Pick at least one ingredient";
        } else {
            return "Your smoothie: " + picked.join(", ");
        }
    }
    assert.strictEqual(q27(["mango", "banana"]), "Your smoothie: mango, banana");
    assert.strictEqual(q27([]), "Pick at least one ingredient");
    console.log("✓ Q27 passed");
}

// Q28: Language Toggle
{
    let current = 'en';
    function toggleLang() {
        current = current === "en" ? "es" : "en";
        var btnText = current === "es" ? "EN" : "ES";
        return { current, btnText };
    }
    assert.deepStrictEqual(toggleLang(), { current: "es", btnText: "EN" });
    assert.deepStrictEqual(toggleLang(), { current: "en", btnText: "ES" });
    console.log("✓ Q28 passed");
}

// Q29: Toppings Total
{
    function q29(prices) {
        var total = 8;
        for (var i = 0; i < prices.length; i++) {
            total += parseFloat(prices[i]);
        }
        return "Total: $" + total.toFixed(2);
    }
    assert.strictEqual(q29(["1.50", "2.00"]), "Total: $11.50");
    assert.strictEqual(q29([]), "Total: $8.00");
    console.log("✓ Q29 passed");
}

console.log("\nALL 29 JAVASCRIPT TEST CASES PASSED SUCCESSFULLY!");
