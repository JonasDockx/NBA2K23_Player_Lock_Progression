import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import os

# Function to initialize the database if it doesn't exist yet
def initialize_database():
    conn = sqlite3.connect('NBA2K23.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_devpoints (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT UNIQUE,
        devpoints INTEGER,
        badgepoints INTEGER   
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attributes (
        attribute_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        attribute_name TEXT,
        attribute_value INTEGER,
        FOREIGN KEY (player_id) REFERENCES player_devpoints(player_id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS badges (
        badge_id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER,
        badge_name TEXT,
        badge_level TEXT,
        FOREIGN KEY (player_id) REFERENCES player_devpoints(player_id)
    )
    ''')
    # Commit the changes and close the connection to the database
    conn.commit()
    conn.close()

initialize_database()

db_path = 'NBA2K23.db'

badge_upgrade_costs = {'No': 3, 'Bronze': 5, 'Silver': 7, 'Gold': 10}

attributes = [
    "Acceleration",
    "Ball Handle",
    "Block",
    "Close Shot",
    "Defensive Consistency",
    "Defensive Rebound",
    "Draw Foul",
    "Driving Dunk",
    "Free Throw",
    "Hands",
    "Help Defense IQ",
    "Hustle",
    "Intangibles",
    "Interior Defense",
    "Lateral Quickness",
    "Layup",
    "Mid-Range Shot",
    "Offensive Consistency",
    "Offensive Rebound",
    "Overall Durability",
    "Pass Accuracy",
    "Pass IQ",
    "Pass Perception",
    "Pass Vision",
    "Perimeter Defense",
    "Post Control",
    "Post Fade",
    "Post Hook",
    "Shot IQ",
    "Speed",
    "Speed with Ball",
    "Stamina",
    "Standing Dunk",
    "Steal",
    "Strength",
    "Three-Point Shot",
    "Vertical"
]

badge_categories = [
        "Acrobat",
        "Aerial Wizard",
        "Agent 3",
        "Amped",
        "Anchor",
        "Ankle Braces",
        "Ankle Breaker",
        "Backdown Punisher",
        "Bail Out",
        "Blinders",
        "Boxout Beast",
        "Break Starter",
        "Brick Wall",
        "Bully",
        "Catch & Shoot",
        "Challenger",
        "Chase Down Artist",
        "Clamps",
        "Clamp Breaker",
        "Claymore",
        "Clutch Shooter",
        "Comeback Kid",
        "Corner Specialist",
        "Deadeye",
        "Dimer",
        "Dream Shake",
        "Dropstepper",
        "Fast Twitch",
        "Fearless Finisher",
        "Floor General",
        "Giant Slayer",
        "Glove",
        "Green Machine",
        "Guard Up",
        "Handles for Days",
        "Hyperdrive",
        "Interceptor",
        "Killer Combos",
        "Limitless Range",
        "Limitless Takeoff",
        "Masher",
        "Menace",
        "Middy Magician", 
        "Mismatch Expert",
        "Needle Threader",
        "Off-Ball Pest",
        "Pick Dodger",
        "Pogo Stick",
        "Post Lockdown",
        "Post Playmaker",
        "Post Spin Technician",
        "Posterizer",
        "Pro Touch",
        "Quick First Step",
        "Rebound Chaser",
        "Rise Up",
        "Slippery Off-Ball",
        "Slithery",
        "Space Creator",
        "Special Delivery",
        "Unpluckable",
        "Vice Grip",
        "Volume Shooter",
        "Work Horse"
    ]

# Let's update the function to ensure that points for 10+ rebounds and assists are not double-counted when a double double, triple double, or quadruple double is achieved.

def calculate_points(score, rebounds, assists, steals, blocks, player_of_game, player_of_week, player_of_month, roty, dpoy, mvp, champion):
    # Initialize points
    devpoints = 0
    badgepoints = 0

    # Initialize a list to track stats for double doubles and triple doubles
    double_double_stats = [score >= 10, rebounds >= 10, assists >= 10, steals >=10, blocks >= 10]

    # Rebounds and assists points
    # Only add points for 10+ rebounds/assists if a double double/triple double/quadruple double is not achieved
    if not (sum(double_double_stats) > 1):  # No double double or higher
        if rebounds >= 10:
            devpoints += 1
        if assists >= 10:
            devpoints += 1
        if score >= 10:
            devpoints += 1

    # Additional points for 20+ rebounds/assists
    if rebounds >= 20:
        devpoints += 3
    if assists >= 20:
        devpoints += 3
    
    # Scoring points
    if score >= 40:
        devpoints += 5
    elif score >= 30:
        devpoints += 3
    elif score >= 20:
        devpoints += 2

    # Double-double and triple-double points
    if sum(double_double_stats) == 2:
        devpoints += 3
    elif sum(double_double_stats) == 3:
        devpoints += 5
    elif sum(double_double_stats) >= 4:
        devpoints += 15

    # Steals and blocks points
    if steals >= 3:
        devpoints += 1
    if blocks >= 3:
        devpoints += 1

    # Player of the game/week/month points
    devpoints += player_of_game + (player_of_week * 3) + (player_of_month * 5)

    # ROTY, DPOY, MVP, and Champion points and badges
    if roty:
        devpoints += 7
        badgepoints += 3
    if dpoy:
        devpoints += 5
        badgepoints += 3
    if mvp:
        devpoints += 15
        badgepoints += 3
    if champion:
        devpoints += 10
        badgepoints += 2

    return devpoints, badgepoints

# Function to insert a new player record into the database
def insert_player(player_id, player_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert a new player into the players table
    cursor.execute("INSERT INTO player_devpoints (player_id, player_name, devpoints, badgepoints) VALUES (?, ?, 0, 0)", (player_id, player_name))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to update a player's devpoints and badgepoints
def update_player_points(player_id, devpoints, badgepoints):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Update the points in the player_development table
    cursor.execute("""
        UPDATE player_devpoints
        SET devpoints = devpoints + ?, badgepoints = badgepoints + ?
        WHERE player_id = ?
    """, (devpoints, badgepoints, player_id))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def player_exists(player_name):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a SELECT query to find the player by name
    cursor.execute("SELECT * FROM player_devpoints WHERE player_name = ?", (player_name,))

    # Fetch one record from the database; this will be None if no record is found
    player = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Return True if a record was found, or False if not
    return player is not None

# Dummy function to create a new player in the database.
# In the actual application, this would insert a new record into the SQLite database.
def create_player(player_name, starting_devpoints=0, starting_badgepoints=0):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert a new player into the player_devpoints table without specifying the player_id
    # It will be automatically generated since it's an AUTOINCREMENT field
    cursor.execute("INSERT INTO player_devpoints (player_name, devpoints, badgepoints) VALUES (?, ?, ?)",
                   (player_name, starting_devpoints, starting_badgepoints))
    
    # Retrieve the ID of the new player
    player_id = cursor.lastrowid

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()

    # Return the ID of the new player for any further processing
    return player_id

def get_player_devpoints(player_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT devpoints FROM player_devpoints WHERE player_id = ?", (player_id,))
        devpoints = cursor.fetchone()[0]
        return devpoints
    
def get_player_badgepoints(player_id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT badgepoints FROM player_devpoints WHERE player_id = ?", (player_id,))
        badgepoints = cursor.fetchone()[0]
        return badgepoints

def perform_attribute_upgrade(player_id, new_attribute_values, total_cost):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Start the transaction
        conn.execute("BEGIN")
        try:
            # Update each attribute value in the database
            for attr, value in new_attribute_values.items():
                cursor.execute("UPDATE attributes SET attribute_value = ? WHERE player_id = ? AND attribute_name = ?",
                               (value, player_id, attr))
            # Deduct the total cost from the player's devpoints
            cursor.execute("UPDATE player_devpoints SET devpoints = devpoints - ? WHERE player_id = ?",
                           (total_cost, player_id))
            # Commit the transaction
            conn.commit()
        except sqlite3.Error as e:
            # Rollback the transaction on error
            conn.rollback()
            raise e

# These functions should be defined to insert the attributes and badges into the database
def insert_player_attributes(player_id, attributes_data):
    with sqlite3.connect('NBA2K23.db') as conn:
        cursor = conn.cursor()
        for attr, value in attributes_data.items():
            cursor.execute("INSERT INTO attributes (player_id, attribute_name, attribute_value) VALUES (?, ?, ?)",
                           (player_id, attr, value))
        conn.commit()

def insert_player_badges(player_id, badges_data):
    with sqlite3.connect('NBA2K23.db') as conn:
        cursor = conn.cursor()
        for badge, level in badges_data.items():
            cursor.execute("INSERT INTO badges (player_id, badge_name, badge_level) VALUES (?, ?, ?)",
                           (player_id, badge, level))
        conn.commit()

def has_enough_devpoints(player_id, total_cost):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT devpoints FROM player_devpoints WHERE player_id = ?", (player_id,))
        current_devpoints = cursor.fetchone()[0]
        return current_devpoints >= total_cost

# Function to get the current badge values from the database
def get_current_badge_levels(player_id):
    conn = sqlite3.connect('NBA2K23.db')
    cursor = conn.cursor()
    # Updated query to include WHERE clause for player_id
    cursor.execute('SELECT badge_name, badge_level FROM badges WHERE player_id = ?', (player_id,))
    result = cursor.fetchall()
    conn.close()
    badge_levels = {}
    for row in result:
        badge_name, badge_level = row
        badge_levels[badge_name] = badge_level
    return badge_levels

# Define colors for different badge levels
badge_level_colors = {
    "No": "black",  
    "Bronze": "#B56459",  
    "Silver": "#989898",  
    "Gold": "#FDB527",  
    "HOF": "#A555FB",
}

attribute_level_colors = {
    "0": "black",
    "1": "black",
    "2": "black",
    "3": "black",
    "4": "black",
    "5": "black",
    "6": "black",
    "7": "black",
    "8": "black",
    "9": "black",
    "10": "black",
    "11": "black",
    "12": "black",
    "13": "black",
    "14": "black",
    "15": "black",
    "16": "black",
    "17": "black",
    "18": "black",
    "19": "black",
    "20": "black",
    "21": "black",
    "22": "black",
    "23": "black",
    "24": "black",
    "25": "black",
    "26": "black",
    "27": "black",
    "28": "black",
    "29": "black",
    "30": "black",
    "31": "black",
    "32": "black",
    "33": "black",
    "34": "black",
    "35": "black",
    "36": "black",
    "37": "black",
    "38": "black",
    "40": "black",
    "41": "black",
    "42": "black",
    "43": "black",
    "44": "black",
    "45": "black",
    "46": "black",
    "47": "black",
    "48": "black",
    "49": "black",
    "50": "black",
    "51": "black",
    "52": "black",
    "53": "black",
    "54": "black",
    "55": "black",
    "56": "black",
    "57": "black",
    "58": "black",
    "59": "black",
    "60": "black",
    "61": "black",
    "62": "black",
    "63": "black",
    "64": "black",
    "65": "black",
    "66": "black",
    "67": "black",
    "68": "black",
    "69": "black",
    "70": "black",
    "71": "#B56459",
    "72": "#B56459",
    "73": "#B56459",
    "74": "#B56459",
    "75": "#B56459",
    "76": "#B56459",
    "77": "#B56459",
    "78": "#B56459",
    "79": "#B56459",
    "80": "#B56459",
    "81": "#989898",
    "82": "#989898",
    "83": "#989898",
    "84": "#989898",
    "85": "#989898",
    "86": "#989898",
    "87": "#989898",
    "88": "#989898",
    "89": "#989898",
    "90": "#989898",
    "91": "#FDB527",
    "92": "#FDB527",
    "93": "#FDB527",
    "94": "#FDB527",
    "95": "#FDB527",
    "96": "#A555FB",
    "97": "#A555FB",
    "98": "#A555FB",
    "99": "#A555FB"
}

# GUI application class
class PlayerTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('NBA2K23 Player Tracker')
        self.geometry('400x300')
        # Check if the icon file exists in the current directory
        if os.path.exists('Wembanyama.ico'):
            self.iconbitmap('Wembanyama.ico')

        # Retrieve the list of players from the database
        self.player_list = self.get_players()

        # Dropdown menu for existing players
        self.selected_player = tk.StringVar(self)
        self.selected_player.set("Select a player")
        if self.player_list:
            self.player_dropdown = tk.OptionMenu(self, self.selected_player, *self.player_list)
        else:
            self.player_dropdown = tk.OptionMenu(self, self.selected_player, "No players available")
        self.player_dropdown.pack()

        self.badge_label = None  # initialize badge_label as a class attribute

        # Button to select the player from the dropdown
        select_button = tk.Button(self, text="Select Player", command=self.select_player)
        select_button.pack()

        # Entry for entering a new player's name
        tk.Label(self, text="Or enter a new player name:").pack()
        self.new_player_name_entry = tk.Entry(self)
        self.new_player_name_entry.pack()

        # Button to create a new player
        create_button = tk.Button(self, text="Create New Player", command=self.create_new_player_prompt)
        create_button.pack()

        # Result label
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        # Close program button
        close_program_button = tk.Button(self, text="Close the program", command=self.destroy)
        close_program_button.pack()

    def get_players(self):
        conn = sqlite3.connect('NBA2K23.db')
        cursor = conn.cursor()
        cursor.execute("SELECT player_name FROM player_devpoints")
        players = [row[0] for row in cursor.fetchall()]
        conn.close()
        return players
    
    def get_selected_player_id(self):
        player_name = self.selected_player.get()
        if player_name != "Select a player":
            conn = sqlite3.connect('NBA2K23.db')
            cursor = conn.cursor()
            cursor.execute("SELECT player_id FROM player_devpoints WHERE player_name = ?", (player_name,))
            player_id = cursor.fetchone()
            conn.close()
            if player_id:
                return player_id[0]
        return None

    def get_player_attributes(self, player_id):
        attributes_data = {}
        conn = sqlite3.connect('NBA2K23.db')
        cursor = conn.cursor()
        cursor.execute("SELECT attribute_name, attribute_value FROM attributes WHERE player_id = ?", (player_id,))
        for attribute_name, attribute_value in cursor.fetchall():
            attributes_data[attribute_name] = attribute_value
        conn.close()
        return attributes_data
    
    def get_player_badges(self, player_id):
        badges_data = {}
        conn = sqlite3.connect('NBA2K23.db')
        cursor = conn.cursor()
        cursor.execute("SELECT badge_name, badge_level FROM badges WHERE player_id = ?", (player_id,))
        for badge_name, badge_level in cursor.fetchall():
            badges_data[badge_name] = badge_level
        conn.close()
        return badges_data
    
    def select_player(self):
        player_name = self.selected_player.get()
        if player_name and player_name != "Select a player":
            # Code to handle the selection of an existing player
            # ... [Load the player data for editing] ...

            # Transition to the player options screen
            self.player_options_screen()
        else:
            messagebox.showerror("Error", "Please select a player.")

    def create_new_player_prompt(self):
        new_player_name = self.new_player_name_entry.get()
        if new_player_name:
            self.prompt_for_starting_values(new_player_name)
        else:
            messagebox.showerror("Error", "Please enter a new player name.")

    def search_player(self):
        player_name = self.player_name_entry.get()
        if player_name:
            if player_exists(player_name):
                self.result_label.config(text=f"Player {player_name} found in the database.")
                # Load the player data into the GUI for editing
            else:
                self.result_label.config(text=f"Player {player_name} not found. Enter starting values.")
                # Provide fields to input starting values and create new player
                self.prompt_for_starting_values(player_name)
        else:
            messagebox.showerror("Error", "Please enter a player name.")

    def prompt_for_starting_values(self, player_name):
        # Clear the result label and remove any previous widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure the canvas for scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Create a window in the canvas for the scrollable frame
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar in the GUI
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Now, create the input fields inside the scrollable_frame instead of self
        self.attribute_entries = {}
        for attribute in attributes:
            label = tk.Label(scrollable_frame, text=f"{attribute}:")
            label.pack()
            entry = tk.Entry(scrollable_frame)
            entry.pack()
            self.attribute_entries[attribute] = entry

        self.badge_level_vars = {}
        for badge in badge_categories:
            label = tk.Label(scrollable_frame, text=f"{badge}:")
            label.pack()
            var = tk.StringVar(scrollable_frame)
            var.set("No")  # default value
            option = tk.OptionMenu(scrollable_frame, var, "No", "Bronze", "Silver", "Gold", "HOF")
            option.pack()
            self.badge_level_vars[badge] = var

        # Button to submit all values, placed outside the scrollable area
        submit_button = tk.Button(self, text="Submit", command=lambda: self.create_new_player(player_name))
        submit_button.pack()

    def create_new_player(self, player_name):
        # Retrieve the values from the attribute entries
        attributes_data = {attr: entry.get() for attr, entry in self.attribute_entries.items()}
        # Retrieve the selected badge levels
        badges_data = {badge: var.get() for badge, var in self.badge_level_vars.items()}

        try:
            # Validate attributes data
            for attr, value in attributes_data.items():
                if not 0 <= int(value) <= 99:
                    raise ValueError(f"Value for {attr} must be between 0 and 99")

            # Create the player in the database
            player_id = create_player(player_name)
            # Insert the attributes and badges into the database
            insert_player_attributes(player_id, attributes_data)
            insert_player_badges(player_id, badges_data)

            # Success message
            messagebox.showinfo("Success", "Player successfully created.")

            # Back to main menu
            self.reset_gui()

            # # Transition to the player options screen
            # self.player_options_screen()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def reset_gui(self):
        # Clear all widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Rebuild the initial screen with the dropdown menu for player selection
        self.player_list = self.get_players()  # Refresh the player list
        self.selected_player = tk.StringVar(self)
        self.selected_player.set("Select a player")
        self.player_dropdown = tk.OptionMenu(self, self.selected_player, *self.player_list)
        self.player_dropdown.pack()

        # Button to select the player from the dropdown
        select_button = tk.Button(self, text="Select Player", command=self.select_player)
        select_button.pack()

        # Entry for entering a new player's name
        tk.Label(self, text="Or enter a new player name:").pack()
        self.new_player_name_entry = tk.Entry(self)
        self.new_player_name_entry.pack()

        # Button to create a new player
        create_button = tk.Button(self, text="Create New Player", command=self.create_new_player_prompt)
        create_button.pack()

        # Result label
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def player_options_screen(self):
        # Clear all widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Option 1: Input game statistics
        input_stats_button = tk.Button(self, text="Input Game Statistics", command=self.input_game_statistics)
        input_stats_button.pack(pady=10)

        # Option 2: Upgrade attributes
        upgrade_attributes_button = tk.Button(self, text="Upgrade Attributes", command=self.upgrade_attributes)
        upgrade_attributes_button.pack(pady=10)

        # Option 3: Upgrade badges
        upgrade_badges_button = tk.Button(self, text="Upgrade Badges", command=self.upgrade_badges)
        upgrade_badges_button.pack(pady=10)

        # Back to main menu button
        main_menu_button = tk.Button(self, text="Back to Main Menu", command=self.reset_gui)
        main_menu_button.pack(pady=20)

        # Close program button
        close_program_button = tk.Button(self, text="Close the program", command=self.destroy)
        close_program_button.pack(pady=20)

    def input_game_statistics(self):
        # Create a top-level window for game statistics input
        top = tk.Toplevel(self)
        top.title("Input Game Statistics")
        # Check if the icon file exists in the current directory
        if os.path.exists('Wembanyama.ico'):
            top.iconbitmap('Wembanyama.ico')

        # Create entry widgets for statistics
        stats_entries = {}
        for i, stat in enumerate(["Points", "Rebounds", "Assists", "Blocks", "Steals"]):
            tk.Label(top, text=stat).grid(row=i, column=0)
            entry = tk.Entry(top)
            entry.grid(row=i, column=1)
            stats_entries[stat] = entry

        # Create checkbuttons for awards
        awards_vars = {}
        for i, award in enumerate(["Player of the Game", "Player of the Week", "Player of the Month", "ROTY", "DPOY", "MVP", "Champion"]):
            var = tk.BooleanVar()
            check = tk.Checkbutton(top, text=award, variable=var)
            check.grid(row=i, column=2)
            awards_vars[award] = var

        # Function to process the statistics and awards input
        def submit_statistics():
            # Retrieve statistics from entries
            stats = {stat: int(entry.get() or "0") for stat, entry in stats_entries.items()}
            # Convert the stats into the format expected by calculate_points function
            # The expected parameter names are score, rebounds, assists, etc.
            converted_stats = {
                'score': stats.get('Points', 0),
                'rebounds': stats.get('Rebounds', 0),
                'assists': stats.get('Assists', 0),
                'steals': stats.get('Steals', 0),
                'blocks': stats.get('Blocks', 0),
                'player_of_game': awards_vars.get('Player of the Game').get(),
                'player_of_week': awards_vars.get('Player of the Week').get(),
                'player_of_month': awards_vars.get('Player of the Month').get(),
                'roty': awards_vars.get('ROTY').get(),
                'dpoy': awards_vars.get('DPOY').get(),
                'mvp': awards_vars.get('MVP').get(),
                'champion': awards_vars.get('Champion').get(),
            }
        
            # Call calculate_points with the gathered data
            points, badge_points = calculate_points(**converted_stats)
            # Call update_player_points with the results
            update_player_points(self.get_selected_player_id(), points, badge_points)

            # Show a message box with the updated devpoints and badgepoints
            messagebox.showinfo("Points Updated", f"Devpoints added: {points}\nBadge points added: {badge_points}")
            # Close the statistics window
            top.destroy()

        # Submit button
        submit_button = tk.Button(top, text="Submit", command=submit_statistics)
        submit_button.grid(row=len(stats_entries) + len(awards_vars), column=0, columnspan=3)

        # Go back button
        go_back_button = tk.Button(top, text="Go back", command=top.destroy)
        go_back_button.grid(row=len(stats_entries) + len(awards_vars) + 1, column=0, columnspan=3)

    def upgrade_attributes(self):
        # Create a top-level window for attribute upgrades
        topspend = tk.Toplevel(self)
        topspend.title("NBA 2K23 Attribute Spending")
        # Check if the icon file exists in the current directory
        if os.path.exists('Wembanyama.ico'):
            topspend.iconbitmap('Wembanyama.ico')

        # Create a canvas and a scrollbar within the top-level window
        canvas = tk.Canvas(topspend)
        scrollbar = tk.Scrollbar(topspend, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure the canvas for scrolling
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add canvas and scrollbar to the top-level window
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Retrieve current attributes and devpoints
        player_id = self.get_selected_player_id()
        current_attributes = self.get_player_attributes(player_id)
        remaining_devpoints = get_player_devpoints(player_id)
        

        # Create a dictionary to hold the Entry widgets for attribute values
        self.attribute_entries = {}
        self.current_attribute_labels = {}

        for i, attribute in enumerate(attributes):
            attribute_value = current_attributes[attribute]
            attribute_color = attribute_level_colors.get(str(attribute_value), "black")
            tk.Label(scrollable_frame, text=attribute, fg=attribute_color).grid(row=i, column=0)
            self.current_attribute_labels[attribute] = tk.Label(scrollable_frame, text=str(attribute_value), fg=attribute_color)
            self.current_attribute_labels[attribute].grid(row=i, column=1)
            entry = tk.Entry(scrollable_frame)
            entry.grid(row=i, column=2)
            self.attribute_entries[attribute] = entry

            # Button to increment the attribute value
            increment_button = tk.Button(scrollable_frame, text="+", command=lambda attr=attribute: self.increment_attribute(attr))
            increment_button.grid(row=i, column=3)

        # Set row weights to make the rows smaller (rows 0 to len(attributes) - 1)
        for i in range(len(attributes)):
            scrollable_frame.grid_rowconfigure(i, weight=1)  # You can adjust the weight value as needed

        # Label to display remaining devpoints
        self.remaining_points_label = tk.Label(scrollable_frame, text=f"Remaining Points: {remaining_devpoints}")
        self.remaining_points_label.grid(row=len(attributes), column=0, columnspan=3)

        # Button to spend points on attributes
        spend_button = tk.Button(scrollable_frame, text="Spend Points", command=self.spend_points_on_attributes)
        spend_button.grid(row=len(attributes) + 1, column=0, columnspan=3)

        # Button to close the attribute window
        close_button = tk.Button(scrollable_frame, text="Close Window", command=topspend.destroy)
        close_button.grid(row=len(attributes) + 2, column=0, columnspan=3)

    def increment_attribute(self, attribute):
        # Get the current value from the corresponding Label widget
        current_value = int(self.current_attribute_labels[attribute].cget("text"))
        new_value = current_value + 1
        # Update the Label widget with the new value
        self.current_attribute_labels[attribute].config(text=str(new_value))
        # Update the Entry widget with the new value
        self.attribute_entries[attribute].delete(0, tk.END)
        self.attribute_entries[attribute].insert(0, str(new_value))

        # If you want to update the remaining devpoints immediately after incrementing
        # You need to calculate the cost and check the remaining points
        cost = self.calculate_upgrade_cost(current_value, new_value)
        remaining_devpoints = int(self.remaining_points_label.cget("text").split(': ')[1])
        if cost <= remaining_devpoints:
            # Update the remaining devpoints label
            remaining_devpoints -= cost
            self.remaining_points_label.config(text=f"Remaining Points: {remaining_devpoints}")
        else:
            # If not enough devpoints, reset the attribute value in the GUI
            self.current_attribute_labels[attribute].config(text=str(current_value))
            self.attribute_entries[attribute].delete(0, tk.END)
            self.attribute_entries[attribute].insert(0, str(current_value))
            messagebox.showerror("Error", "Not enough development points to increment attribute.")

    def spend_points_on_attributes(self):
        player_id = self.get_selected_player_id()  # Retrieve the selected player ID
        # Fetch the original attribute values from the database
        original_attributes = self.get_player_attributes(player_id)
        new_attribute_values = {}
        total_cost = 0

        # Iterate over the attributes and their corresponding label widgets
        for attribute, label in self.current_attribute_labels.items():
            # Retrieve the current value displayed in the label widget
            current_value_label = label.cget("text")
            # Convert the current value to an integer
            current_value = int(current_value_label) if current_value_label.isdigit() else 0
            # Retrieve the original value from the database
            original_value = original_attributes.get(attribute)

            # Check if the current value has been incremented from the original value
            if current_value != original_value:
                # Calculate the cost to upgrade this attribute to the new value
                cost = self.calculate_upgrade_cost(original_value, current_value)
                # Add the cost to the total cost
                total_cost += cost
                # Store the new value in the dictionary
                new_attribute_values[attribute] = current_value

        # Now check if the player has enough devpoints to perform the upgrade
        remaining_devpoints = get_player_devpoints(player_id)  # Call the standalone function directly
        if remaining_devpoints >= total_cost:
            # Confirm the upgrade with the user
            if messagebox.askyesno("Confirm Upgrade", f"This will cost {total_cost} development points. Proceed?"):
                # Perform the upgrade and update the GUI
                perform_attribute_upgrade(player_id, new_attribute_values, total_cost)
                # Update the remaining devpoints label
                remaining_devpoints -= total_cost
                self.remaining_points_label.config(text=f"Remaining Points: {remaining_devpoints}")
        else:
            messagebox.showerror("Error", "Not enough development points to perform the upgrade.")

    def upgrade_with_devpoints(self, player_id, badge_name):
        conn = sqlite3.connect('NBA2K23.db')
        cursor = conn.cursor()

        # Retrieve the current badge level for the given badge name
        cursor.execute("SELECT badge_level FROM badges WHERE player_id = ? AND badge_name = ?", (player_id, badge_name))
        badge_level_row = cursor.fetchone()
        current_badge_level = badge_level_row[0] if badge_level_row else 'No'

        devcost = self.calculate_badge_cost(current_badge_level)

        # Define the badge level progression
        badge_levels = ['No', 'Bronze', 'Silver', 'Gold', 'HOF']
        if current_badge_level not in badge_levels or current_badge_level == 'HOF':
            messagebox.showerror("Error", "Cannot upgrade badge.")
            conn.close()
            return

        # Determine the next badge level
        next_level_index = badge_levels.index(current_badge_level) + 1
        if next_level_index >= len(badge_levels):
            messagebox.showerror("Error", "Badge is already at the highest level.")
            conn.close()
            return

        next_level = badge_levels[next_level_index]

        # Check if the player has a free badgepoint
        cursor.execute("SELECT devpoints FROM player_devpoints WHERE player_id = ?", (player_id,))
        devpoints_row = cursor.fetchone()
        if devpoints_row is None or devpoints_row[0] < devcost:
            messagebox.showerror("Error", "Not enough devpoints to upgrade.")
            conn.close()
            return

        # Upgrade the badge level and deduct the devpoints
        print(devcost)
        new_devpoints = devpoints_row[0] - devcost
        print(new_devpoints)
        cursor.execute("UPDATE badges SET badge_level = ? WHERE player_id = ? AND badge_name = ?", (next_level, player_id, badge_name))
        cursor.execute("UPDATE player_devpoints SET devpoints = ? WHERE player_id = ?", (new_devpoints, player_id))
        self.remaining_points_label.config(text=f"Remaining free development points: {new_devpoints}")
        badge_color = badge_level_colors.get(next_level, "black")
        self.badge_label.config(text=f"Selected badge: {badge_name} - Current Level: {next_level}", fg=badge_color)

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Badge '{badge_name}' upgraded to {next_level}.")
    
    def upgrade_with_badgepoint(self, player_id, badge_name):
        conn = sqlite3.connect('NBA2K23.db')
        cursor = conn.cursor()

        # Retrieve the current badge level for the given badge name
        cursor.execute("SELECT badge_level FROM badges WHERE player_id = ? AND badge_name = ?", (player_id, badge_name))
        badge_level_row = cursor.fetchone()
        current_badge_level = badge_level_row[0] if badge_level_row else 'No'

        # Define the badge level progression
        badge_levels = ['No', 'Bronze', 'Silver', 'Gold', 'HOF']
        if current_badge_level not in badge_levels or current_badge_level == 'HOF':
            messagebox.showerror("Error", "Cannot upgrade badge.")
            conn.close()
            return

        # Determine the next badge level
        next_level_index = badge_levels.index(current_badge_level) + 1
        if next_level_index >= len(badge_levels):
            messagebox.showerror("Error", "Badge is already at the highest level.")
            conn.close()
            return

        next_level = badge_levels[next_level_index]

        # Check if the player has a free badgepoint
        cursor.execute("SELECT badgepoints FROM player_devpoints WHERE player_id = ?", (player_id,))
        badgepoints_row = cursor.fetchone()
        if badgepoints_row is None or badgepoints_row[0] < 1:
            messagebox.showerror("Error", "Not enough badgepoints to upgrade.")
            conn.close()
            return

        # Upgrade the badge level and deduct a badgepoint
        new_badgepoints = badgepoints_row[0] - 1
        cursor.execute("UPDATE badges SET badge_level = ? WHERE player_id = ? AND badge_name = ?", (next_level, player_id, badge_name))
        cursor.execute("UPDATE player_devpoints SET badgepoints = ? WHERE player_id = ?", (new_badgepoints, player_id))
        self.remaining_badgepoints_label.config(text=f"Remaining free badge points: {new_badgepoints}")
        badge_color = badge_level_colors.get(next_level, "black")
        self.badge_label.config(text=f"Selected badge: {badge_name} - Current Level: {next_level}", fg=badge_color)

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Badge '{badge_name}' upgraded to {next_level}.")

    def upgrade_badges(self):
        # Create a top-level window for attribute upgrades
        topbadges = tk.Toplevel(self)
        topbadges.title("NBA 2K23 Badges Spending")
        # Check if the icon file exists in the current directory
        if os.path.exists('Wembanyama.ico'):
            topbadges.iconbitmap('Wembanyama.ico')

        # Retrieve current attributes and devpoints
        player_id = self.get_selected_player_id()
        current_badges = self.get_player_badges(player_id)
        remaining_devpoints = get_player_devpoints(player_id)
        remaining_badgepoints = get_player_badgepoints(player_id)

        def update_badge_label(*args):
            selected_badge_category = clicked.get()
            # Assuming get_selected_player_id() is a method that returns the current player's ID
            player_id = self.get_selected_player_id()
            current_badge_levels = get_current_badge_levels(player_id)
            current_badge_level = current_badge_levels.get(selected_badge_category, "No")

            badge_color = badge_level_colors.get(current_badge_level, "black")
            self.badge_label.config(text=f"Selected badge: {selected_badge_category} - Current Level: {current_badge_level}", fg=badge_color)

        clicked = tk.StringVar(topbadges)
        clicked.set(badge_categories[0])

        clicked.trace("w", update_badge_label)

        drop = tk.OptionMenu(topbadges, clicked, *badge_categories)
        drop.pack(pady=10)

        self.badge_label = tk.Label(topbadges, text="Selected badge: - Current Level: No")
        self.badge_label.pack(pady=10)

        # Label to display remaining devpoints
        self.remaining_points_label = tk.Label(topbadges, text=f"Remaining Points: {remaining_devpoints}")
        self.remaining_points_label.pack(pady=20)

        # Label to display free badge devpoints
        self.remaining_badgepoints_label = tk.Label(topbadges, text=f"Remaining Free badge points: {remaining_badgepoints}")
        self.remaining_badgepoints_label.pack(pady=10)

        # Button to upgrade with a badgepoint
        upgrade_badgepoint_button = tk.Button(topbadges, text="Upgrade with Badgepoint", command=lambda: self.upgrade_with_badgepoint(player_id, clicked.get()))
        upgrade_badgepoint_button.pack(pady=20)

        # Button to upgrade with devpoints
        upgrade_devpoints_button = tk.Button(topbadges, text="Upgrade with Devpoints", command=lambda: self.upgrade_with_devpoints(player_id, clicked.get()))
        upgrade_devpoints_button.pack(pady=10)

        # Button to close the attribute window
        close_button = tk.Button(topbadges, text="Close Window", command=topbadges.destroy)
        close_button.pack(pady=20)

    def update_attributes(self, player_id):
        # Get the new values from the entries
        new_attribute_values = {attr: int(entry.get()) for attr, entry in self.attribute_entries.items()}
        current_attributes = self.get_player_attributes(player_id)

        # Calculate the total cost of the upgrades
        total_cost = 0
        for attr, new_value in new_attribute_values.items():
            current_value = current_attributes[attr]
            if current_value < new_value:  # Ensure we only calculate cost for actual upgrades
                total_cost += self.calculate_upgrade_cost(current_value, new_value)

        # Check if the player has enough devpoints to perform the upgrade
        if self.has_enough_devpoints(player_id, total_cost):
            # Perform the upgrade and deduct the devpoints
            self.perform_attribute_upgrade(player_id, new_attribute_values, total_cost)
        else:
            messagebox.showerror("Error", "Not enough development points to perform the upgrade.")

    def calculate_upgrade_cost(self, current_value, new_value):
        cost = 0
        for value in range(int(current_value) + 1, new_value + 1):
            if value < 71:
                cost += 1
            elif value < 81:
                cost += 2
            elif value < 91:
                cost += 3
            else:
                cost += 5
        return cost
    
    def calculate_badge_cost(self, current_badge_level):
        if current_badge_level == "No":
            return 3
        elif current_badge_level == "Bronze":
            return 5
        elif current_badge_level == "Silver":
            return 7
        elif current_badge_level == "Gold":
            return 10

# Run the application
app = PlayerTrackerApp()
app.mainloop()