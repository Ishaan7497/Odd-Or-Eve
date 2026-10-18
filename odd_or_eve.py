import random


def ask_number(prompt, valid):
    """Keep asking until the player types a whole number that is in `valid`."""
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and int(answer) in valid:
            return int(answer)
        print(f"Please enter a number within the range {valid[0]} to {valid[-1]}.")


def ask_choice(prompt, options):
    """Keep asking until the answer matches one of `options` (case-insensitive).

    `options` maps each accepted answer to the value returned for it."""
    while True:
        answer = input(prompt).strip().upper()
        if answer in options:
            return options[answer]
        print(f"Please type one of: {', '.join(options)}.")


def select_mode():
    while True:
        mode = input("\nChoose a Mode:\n (1) 1 to 6 \n (2) 1 to 10 \n (3) *CRAZY* \n\n Enter: ")
        if mode == "1":
            return "1 to 6", range(1, 7)
        elif mode == "2":
            return "1 to 10", range(1, 11)
        elif mode == "3":
            return "CRAZY", range(1, 11)
        else:
            print("Invalid choice. Please type 1, 2, or 3.")

def is_adjacent(a, b):
    """CRAZY mode: numbers next to each other are OUT (10 and 1 wrap around)."""
    return abs(a - b) == 1 or {a, b} == {1, 10}


def resolve_ball(bat, bowl, mode):
    """Score one ball. Returns (runs, out).

    Normal modes and super over: same number = OUT.
    CRAZY: adjacent numbers = OUT, the same number scores its square."""
    if mode == "CRAZY":
        if is_adjacent(bat, bowl):
            return 0, True
        if bat == bowl:
            return bat ** 2, False
        return bat, False
    if bat == bowl:
        return 0, True
    return bat, False


def play_innings(run_range, mode, user_batting, target=None):
    """Play one innings and return the runs scored.

    A normal innings ends at the first wicket. A super over is 6 balls, and a
    wicket only costs that ball's runs. When chasing a `target`, the innings
    also ends as soon as the batting side passes it."""
    runs = 0
    balls = 6 if mode == "super_over" else None
    ball = 0
    while balls is None or ball < balls:
        ball += 1
        computer = random.randint(run_range[0], run_range[-1])
        if user_batting:
            user = ask_number(f"\nBatting ({run_range[0]} to {run_range[-1]}): ", run_range)
            bat, bowl = user, computer
        else:
            user = ask_number(f"Bowling ({run_range[0]} to {run_range[-1]}): ", run_range)
            bat, bowl = computer, user

        scored, out = resolve_ball(bat, bowl, mode)
        if out:
            if user_batting:
                print(f"OUT! The computer bowled you out! The computer bowled {computer}.")
            else:
                print(f"OUT! You bowled the computer out! The computer batted {computer}.")
            if balls is None:
                if target is None:
                    print(f"Target to win: {runs + 1}\n\n")
                else:
                    print(f"Final score: {runs}\n\n")
                break
            print(f"No runs scored. Balls remaining: {balls - ball}\n")
            continue

        runs += scored
        if mode == "CRAZY" and bat == bowl:
            print("Runs Squared!")
        print(f"{'You' if user_batting else 'Computer'} scored {scored}\nTotal runs: {runs}")
        if balls is not None:
            print(f"Balls remaining: {balls - ball}")
        print()
        if target is not None and runs > target:
            print(f"{'You' if user_batting else 'The computer'} passed the target of {target}!\n")
            break

    return runs


def batting(run_range, mode, target=None):
    return play_innings(run_range, mode, user_batting=True, target=target)


def bowling(run_range, mode, target=None):
    return play_innings(run_range, mode, user_batting=False, target=target)


def decide_winner(user_score, computer_score, run_range, mode):
    if user_score > computer_score:
        print(f"\nYou win! Your score: {user_score} | Computer's score: {computer_score}")
    elif computer_score > user_score:
        print(f"\nYou lose! Your score: {user_score} | Computer's score: {computer_score}")
    else:
        print(f"\nIt's a tie! Your score: {user_score} | Computer's score: {computer_score}")
        print("SUPER OVER")
        print("\n~~RULES~~\n\n- Each player will receive 6 balls (1 Over) to score as many runs as they can.\n- If the batsman is bowled out by the bowler they receive no runs but continue batting.")
        mode = "super_over"
        user_score = batting(run_range, mode)
        print("\n\nYOU ARE NOW BOWLING")
        computer_score = bowling(run_range, mode, target=user_score)
        if user_score > computer_score:
            print(f"\nYou win! Your score: {user_score} | Computer's score: {computer_score}")
        elif computer_score > user_score:
            print(f"\nYou lose! Your score: {user_score} | Computer's score: {computer_score}")
        else:
            print(f"\nIt's a tie even after the super over! Your score: {user_score} | Computer's score: {computer_score}")

def play():
    mode, run_range = select_mode()
    c_toss = random.randint(1, 2)
    print("\n\nTOSS ~~~ Odd or Eve ~~~  \n")
    u_choice = ask_choice("Odd or Eve?: ", {"ODD": "ODD", "EVE": "EVE", "EVEN": "EVE"})
    toss_input = ask_number("Enter a number for the toss (1 or 2): ", range(1, 3))

    add = c_toss + toss_input
    toss_result = "EVE" if add % 2 == 0 else "ODD"

    if toss_result == u_choice:
        print(f"You won the toss!\nResult: {add} ({toss_result})")
        user_decision = ask_choice("Do you choose BAT or BOWL? (BAT / BOWL): ",
                                   {"BAT": "BAT", "BOWL": "BOWL"})

        if user_decision == "BAT":
            user_score = batting(run_range, mode)
            print("\nYOU ARE NOW BOWLING")
            computer_score = bowling(run_range, mode, target=user_score)
        else:
            computer_score = bowling(run_range, mode)
            print("\nYOU ARE NOW BATTING")
            user_score = batting(run_range, mode, target=computer_score)
    else:
        print(f"You lost the toss! Result: {add} ({toss_result}).")
        computer_decision = random.choice(["BAT", "BOWL"])
        print(f"The computer chooses to {computer_decision}!\n")

        if computer_decision == "BAT":
            computer_score = bowling(run_range, mode)
            print("\n\nYOU ARE NOW BATTING")
            user_score = batting(run_range, mode, target=computer_score)
        else:
            user_score = batting(run_range, mode)
            print("\n\nYOU ARE NOW BOWLING")
            computer_score = bowling(run_range, mode, target=user_score)

    decide_winner(user_score, computer_score, run_range, mode)

def play_again():
    while True:
        p = input("\nPlay again? (y/n): ").lower()
        if p == "y":
            play()
        elif p == 'n':
            print("Exiting...")
            break
        else:
            print("Please type in 'y' to play again or 'n' to quit.")

def main():
    try:
        play()
        play_again()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")


if __name__ == "__main__":
    main()
