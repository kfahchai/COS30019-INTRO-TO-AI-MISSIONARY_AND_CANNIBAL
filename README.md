### Super-Simple Story of the Game Logic

Imagine you have a little **river** and two tiny **banks** – a **right side** and a **left side**.

On the river you have:

* **3 missionaries** – they are nice people who love sharing snacks.
* **3 cannibals** – they are a bit grumpy and want to eat the missionaries if they’re alone.

You also have a **boat** that can hold **1 or 2** little figures at a time.

---

#### Goal

Move **all 6 friends** from the **right side** to the **left side** without ever letting the cannibals out-number the missionaries on the same side. If that happens, the missionaries get scared (the game is lost).

---

#### How the computer thinks about the game

1. **A picture of a moment** – called a **State**
*How many missionaries and cannibals are on each side?*
*Where is the boat?*
The picture looks like this (just numbers, no drawing):
```
State = (M_left, C_left, M_right, C_right, boat_side)

```


2. **Checking if a picture is safe**
*No side can have a negative number of people.*
*If missionaries are present, they must be **at least** as many as cannibals.*
If either rule is broken, the picture is **invalid**.
3. **What the boat can do** – **Moves**
The boat can carry any of these combos (the numbers are missionaries, then cannibals):
* **1M**, **2M**, **1C**, **2C**, **1M + 1C**


The boat always moves from its current side to the opposite side.
4. **Trying a move**
*Look at the current picture.*
*Pick one of the allowed combos.*
*Take those people off the side where the boat is, put them on the other side, and flip the boat’s side.*
*If the new picture follows the safety rules, keep it; otherwise, throw it away.*
5. **Finding the shortest way home** – **Breadth-First Search (BFS)**
* Think of a **big family tree** that starts with the first picture (all 6 on the right).
* **Level 1** = all pictures you can reach with **one** move.
* **Level 2** = all pictures you can reach with **two** moves, and so on.
* The computer looks at the tree **layer by layer** (**breadth-first**) until it finds a picture where everyone is on the left side.
* Because it searches level by level, the first solution it finds uses the **fewest moves**.


6. **What the computer reports**
*A list of moves like:*

```
   (1 missionary, 0 cannibals, ends on left)
   (0 missionaries, 1 cannibal, ends on right)
   …

```

The UI (your picture-drawing code) just follows that list and shows the boat sailing across the river.

---

#### In a nutshell

* **State** = a snapshot of who’s where.
* **Valid?** = no negative numbers and missionaries never out-numbered.
* **Move** = take **1-2** people on the boat, switch sides, keep it safe.
* **BFS** = explore all safe snapshots step-by-step until we reach the happy picture where everybody is on the left bank.

That’s the clever brain behind the game – it tries every safe possibility until it discovers the quickest way to get everyone across safely!

```

```
