import tkinter as tk
from tkinter import messagebox
import random


# ============================================================
# CYBER LOCK
# EDUCATIONAL CYBERSECURITY AWARENESS SIMULATION
#
# THIS PROGRAM IS ONLY A VISUAL SIMULATION.
# IT DOES NOT ENCRYPT, DELETE, RENAME, OR MODIFY REAL FILES.
#
# Shift + Z         -> Open recovery window
# Ctrl + Shift + X  -> Hidden developer exit
# Hold Esc (3 sec)  -> Emergency exit (no key needed)
# AUTO EXIT         -> Program closes by itself after
#                      AUTO_EXIT_SECONDS, no matter what
# AFTER CORRECT KEY -> Awareness screen with prevention tips,
#                      then the program closes automatically
# ============================================================


# ============================================================
# CONFIGURATION
# ============================================================

UNLOCK_KEY = "SORRY"

YOUR_NAME = "CHESHTA KHURANA"
COLLEGE_NAME = "VIPS - TC"

# --- SAFETY FAILSAFES ---------------------------------------
AUTO_EXIT_SECONDS = 10 * 60     # Program always closes after this long
ESC_HOLD_MS = 3000              # Hold Esc this long to force exit

# Set True while testing: runs in a normal window, not topmost.
DEV_MODE = False

# How long the final awareness screen stays up (press Enter or
# click CLOSE NOW to leave earlier).
AWARENESS_SECONDS = 25


# ============================================================
# COLORS
# ============================================================

BLACK = "#050505"
PANEL = "#151515"
DARK_RED = "#260000"

RED = "#FF2020"
LIGHT_RED = "#FF6666"

WHITE = "#F2F2F2"
GRAY = "#888888"

GREEN = "#35F58A"
AMBER = "#FFB020"


# ============================================================
# FAKE DATA
# ============================================================

FAKE_FILES = [
    "Documents/Project_Report.docx",
    "Documents/Resume.pdf",
    "Documents/Research_Paper.pdf",
    "Documents/Important_Document.docx",
    "Pictures/Family_Photo.jpg",
    "Pictures/College_Event.png",
    "Desktop/Important_Data.xlsx",
    "Desktop/Project_Presentation.pptx",
    "Downloads/Certificate.pdf",
    "Downloads/Assignment.docx",
    "Desktop/Final_Project.zip",
    "Documents/Personal_Notes.txt"
]

FAKE_EXTENSIONS = [
    ".locked",
    ".encrypted",
    ".enc",
    ".CYBERLOCK"
]

AWARENESS_TIPS = [
    (
        "KEEP OFFLINE BACKUPS",
        "Follow the 3-2-1 rule: 3 copies, 2 different media, 1 stored "
        "offline or off-site. Backups are your best defence against "
        "ransomware."
    ),
    (
        "THINK BEFORE YOU CLICK",
        "Never open unknown attachments or links in emails, SMS or "
        "chats. Check the sender's address and be wary of urgency."
    ),
    (
        "UPDATE EVERYTHING",
        "Install OS, browser and app updates promptly. Most attacks "
        "exploit old, known vulnerabilities."
    ),
    (
        "ENABLE MFA",
        "Turn on multi-factor authentication and use strong, unique "
        "passwords so a stolen password alone is not enough."
    ),
    (
        "USE SECURITY SOFTWARE",
        "Keep antivirus on, use a standard (non-admin) account for "
        "daily work, and avoid pirated software."
    ),
    (
        "REPORT IMMEDIATELY",
        "If you suspect an attack: disconnect from the network, do not "
        "pay, and inform your IT / cyber cell at once. In India, report "
        "at cybercrime.gov.in or call 1930."
    ),
]


ACTIVITY_MESSAGES = [
    "> Simulating file activity...",
    "> Processing simulated data...",
    "> Scanning demonstration files...",
    "> Updating simulated statistics...",
    "> Processing sample directory...",
    "> Simulating encryption activity..."
]


# ============================================================
# MAIN APPLICATION
# ============================================================

class CyberLockSimulation:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        self.running = True
        self.unlocked = False

        self.remaining_seconds = 299
        self.auto_exit_remaining = AUTO_EXIT_SECONDS
        self.awareness_remaining = AWARENESS_SECONDS

        self.files_affected = 2847
        self.files_locked = 1326
        self.folders = 934

        self.recovery_dialog = None
        self.esc_job = None
        self.blink_state = False

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.root.title("CYBER LOCK - Educational Simulation")
        self.root.configure(bg=BLACK)

        if DEV_MODE:
            self.root.geometry("1100x760")
        else:
            self.root.attributes("-fullscreen", True)
            self.root.attributes("-topmost", True)

        # Prevent normal window close (Alt+F4 etc.)
        self.root.protocol("WM_DELETE_WINDOW", self.ignore_close)

        # ----------------------------------------------------
        # BUILD INTERFACE
        # ----------------------------------------------------

        self.build_interface()

        # ----------------------------------------------------
        # KEYBOARD
        # ----------------------------------------------------

        # Recovery
        self.root.bind_all("<Shift-Z>", self.open_recovery)
        self.root.bind_all("<Shift-z>", self.open_recovery)

        # Hidden developer exit
        self.root.bind_all("<Control-Shift-X>", self.developer_exit)
        self.root.bind_all("<Control-Shift-x>", self.developer_exit)

        # Emergency exit: hold Esc
        self.root.bind_all("<KeyPress-Escape>", self.esc_down)
        self.root.bind_all("<KeyRelease-Escape>", self.esc_up)

        # ----------------------------------------------------
        # START SIMULATION
        # ----------------------------------------------------

        self.update_timer()
        self.update_activity()
        self.glitch_effect()
        self.blink_warning()
        self.auto_exit_tick()      # FAILSAFE: auto-exit countdown
        self.keep_focus()


    # ========================================================
    # MAIN UI
    # ========================================================

    def build_interface(self):

        self.main = tk.Frame(self.root, bg=BLACK)
        self.main.pack(fill="both", expand=True)

        # ====================================================
        # WARNING BAR
        # ====================================================

        self.warning_bar = tk.Frame(self.main, bg=RED)
        self.warning_bar.pack(fill="x")

        self.warning_label = tk.Label(
            self.warning_bar,
            text="⚠  CRITICAL SECURITY WARNING  ⚠",
            bg=RED,
            fg=WHITE,
            font=("Consolas", 19, "bold")
        )
        self.warning_label.pack(pady=11)


        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(self.main, bg=BLACK)
        header.pack(fill="x", padx=55, pady=(17, 0))

        tk.Label(
            header,
            text="CYBER LOCK",
            bg=BLACK,
            fg=RED,
            font=("Consolas", 30, "bold")
        ).pack(side="left")

        self.status_label = tk.Label(
            header,
            text="● SYSTEM COMPROMISED",
            bg=BLACK,
            fg=RED,
            font=("Consolas", 13, "bold")
        )
        self.status_label.pack(side="right", pady=8)


        # ====================================================
        # TITLE
        # ====================================================

        title_frame = tk.Frame(self.main, bg=BLACK)
        title_frame.pack(fill="x", padx=40, pady=(5, 0))

        self.main_title = tk.Label(
            title_frame,
            text="YOUR FILES ARE ENCRYPTED",
            bg=BLACK,
            fg=WHITE,
            font=("Consolas", 39, "bold")
        )
        self.main_title.pack(pady=(3, 0))

        self.subtitle = tk.Label(
            title_frame,
            text="YOUR PERSONAL DATA HAS BEEN LOCKED",
            bg=BLACK,
            fg=LIGHT_RED,
            font=("Consolas", 15, "bold")
        )
        self.subtitle.pack(pady=(2, 8))


        # ====================================================
        # AUTHOR CREDIT
        # ====================================================

        author_frame = tk.Frame(
            title_frame,
            bg=DARK_RED,
            highlightbackground=RED,
            highlightthickness=1
        )
        author_frame.pack(fill="x", padx=170, pady=(0, 10))

        tk.Label(
            author_frame,
            text="EDUCATIONAL DEMONSTRATION CREATED BY",
            bg=DARK_RED,
            fg=GRAY,
            font=("Consolas", 10, "bold")
        ).pack(pady=(7, 1))

        tk.Label(
            author_frame,
            text=YOUR_NAME,
            bg=DARK_RED,
            fg=WHITE,
            font=("Consolas", 20, "bold")
        ).pack(pady=1)

        tk.Label(
            author_frame,
            text=COLLEGE_NAME,
            bg=DARK_RED,
            fg=LIGHT_RED,
            font=("Consolas", 11, "bold")
        ).pack(pady=(1, 7))


        # ====================================================
        # CONTENT
        # ====================================================

        content = tk.Frame(self.main, bg=BLACK)
        content.pack(fill="both", expand=True, padx=55, pady=(5, 8))

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)


        # ====================================================
        # LEFT PANEL
        # ====================================================

        left = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=RED,
            highlightthickness=1
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 9))

        tk.Label(
            left,
            text="WHAT HAPPENED?",
            bg=PANEL,
            fg=RED,
            font=("Consolas", 20, "bold")
        ).pack(anchor="w", padx=25, pady=(20, 10))

        explanation = (
            "Your files appear to have been locked.\n\n"
            "This demonstration recreates the visual\n"
            "experience of a ransomware warning screen.\n\n"
            "The file statistics and activity shown\n"
            "below are simulated for awareness training.\n\n"
            "No actual files have been encrypted."
        )

        tk.Label(
            left,
            text=explanation,
            bg=PANEL,
            fg=WHITE,
            justify="left",
            anchor="w",
            font=("Consolas", 11),
            wraplength=520
        ).pack(anchor="w", padx=25, pady=(0, 15))


        # ====================================================
        # FAKE STATISTICS (LIVE COUNTERS)
        # ====================================================

        stats = tk.Frame(left, bg=PANEL)
        stats.pack(fill="x", padx=20)

        self.affected_value = self.create_stat(
            stats, "FILES AFFECTED", str(self.files_affected), 0
        )
        self.locked_value = self.create_stat(
            stats, "FILES LOCKED", str(self.files_locked), 1
        )
        self.folders_value = self.create_stat(
            stats, "FOLDERS", str(self.folders), 2
        )


        # ====================================================
        # SIMULATED PROGRESS BAR
        # ====================================================

        tk.Label(
            left,
            text="SIMULATED LOCK PROGRESS",
            bg=PANEL,
            fg=RED,
            font=("Consolas", 12, "bold")
        ).pack(anchor="w", padx=25, pady=(18, 5))

        self.progress_canvas = tk.Canvas(
            left,
            height=16,
            bg="#222222",
            highlightthickness=0
        )
        self.progress_canvas.pack(fill="x", padx=25)

        self.progress_bar = self.progress_canvas.create_rectangle(
            0, 0, 0, 16,
            fill=RED,
            outline=""
        )

        self.progress_text = tk.Label(
            left,
            text="0%",
            bg=PANEL,
            fg=GRAY,
            font=("Consolas", 9, "bold"),
            anchor="e"
        )
        self.progress_text.pack(fill="x", padx=25, pady=(2, 0))


        # ====================================================
        # RECENT ACTIVITY
        # ====================================================

        tk.Label(
            left,
            text="RECENT ACTIVITY",
            bg=PANEL,
            fg=RED,
            font=("Consolas", 12, "bold")
        ).pack(anchor="w", padx=25, pady=(12, 5))

        self.activity_label = tk.Label(
            left,
            text="> Simulating file activity...",
            bg=PANEL,
            fg=GREEN,
            font=("Consolas", 10),
            anchor="w"
        )
        self.activity_label.pack(fill="x", padx=25, pady=(0, 15))


        # ====================================================
        # RIGHT PANEL
        # ====================================================

        right = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=RED,
            highlightthickness=1
        )
        right.grid(row=0, column=1, sticky="nsew", padx=(9, 0))

        tk.Label(
            right,
            text="RECOVERY WINDOW",
            bg=PANEL,
            fg=RED,
            font=("Consolas", 20, "bold")
        ).pack(pady=(20, 5))


        # ====================================================
        # TIMER
        # ====================================================

        self.timer_label = tk.Label(
            right,
            text="04:59",
            bg=PANEL,
            fg=RED,
            font=("Consolas", 52, "bold")
        )
        self.timer_label.pack()

        tk.Label(
            right,
            text="TIME REMAINING",
            bg=PANEL,
            fg=GRAY,
            font=("Consolas", 10, "bold")
        ).pack()


        # ====================================================
        # RECOVERY MESSAGE
        # ====================================================

        tk.Label(
            right,
            text=(
                "RECOVERY REQUIRED\n\n"
                "Access to the simulated files has been\n"
                "restricted for this awareness exercise."
            ),
            bg=PANEL,
            fg=WHITE,
            font=("Consolas", 12),
            justify="center"
        ).pack(pady=(20, 15))


        # ====================================================
        # RECOVERY BUTTON
        # ====================================================

        self.recovery_button = tk.Button(
            right,
            text="OPEN RECOVERY",
            command=self.open_recovery,
            bg=RED,
            fg=WHITE,
            activebackground=LIGHT_RED,
            activeforeground=WHITE,
            font=("Consolas", 13, "bold"),
            relief="flat",
            padx=35,
            pady=10,
            cursor="hand2"
        )
        self.recovery_button.pack(pady=5)

        tk.Label(
            right,
            text="or press  SHIFT + Z",
            bg=PANEL,
            fg=GRAY,
            font=("Consolas", 9)
        ).pack(pady=(4, 0))


        # ====================================================
        # FOOTER
        # ====================================================

        footer = tk.Frame(self.main, bg=BLACK)
        footer.pack(fill="x", padx=55, pady=(0, 12))

        self.fake_file_label = tk.Label(
            footer,
            text="> Documents/Project_Report.docx.locked",
            bg=BLACK,
            fg=GRAY,
            font=("Consolas", 9)
        )
        self.fake_file_label.pack(side="left")

        tk.Label(
            footer,
            text="EDUCATIONAL SIMULATION",
            bg=BLACK,
            fg=GRAY,
            font=("Consolas", 9, "bold")
        ).pack(side="right")

        # Auto-exit countdown (visible safety indicator)
        self.auto_exit_label = tk.Label(
            footer,
            text="",
            bg=BLACK,
            fg=AMBER,
            font=("Consolas", 9, "bold")
        )
        self.auto_exit_label.pack(side="right", padx=25)


    # ========================================================
    # STAT BOX
    # ========================================================

    def create_stat(self, parent, title, value, column):

        box = tk.Frame(
            parent,
            bg=BLACK,
            highlightbackground="#333333",
            highlightthickness=1
        )
        box.grid(row=0, column=column, sticky="nsew", padx=4)

        parent.grid_columnconfigure(column, weight=1)

        value_label = tk.Label(
            box,
            text=value,
            bg=BLACK,
            fg=RED,
            font=("Consolas", 21, "bold")
        )
        value_label.pack(pady=(8, 2))

        tk.Label(
            box,
            text=title,
            bg=BLACK,
            fg=GRAY,
            font=("Consolas", 8, "bold")
        ).pack(pady=(0, 8))

        return value_label


    # ========================================================
    # RECOVERY WINDOW
    # ========================================================

    def open_recovery(self, event=None):

        if not self.running:
            return

        # If already open, don't create another one.
        if (
            self.recovery_dialog is not None
            and self.recovery_dialog.winfo_exists()
        ):
            self.recovery_dialog.lift()
            self.recovery_dialog.focus_force()
            return

        # ----------------------------------------------------
        # CREATE WINDOW
        # ----------------------------------------------------

        dialog = tk.Toplevel(self.root)
        self.recovery_dialog = dialog

        dialog.title("Recovery")
        dialog.configure(bg=BLACK)
        dialog.resizable(False, False)
        dialog.attributes("-topmost", True)
        dialog.transient(self.root)

        # Center
        width = 500
        height = 290

        x = (dialog.winfo_screenwidth() - width) // 2
        y = (dialog.winfo_screenheight() - height) // 2

        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            dialog,
            text="RECOVERY",
            bg=BLACK,
            fg=RED,
            font=("Consolas", 24, "bold")
        ).pack(pady=(22, 5))

        tk.Label(
            dialog,
            text="Enter the recovery key to continue:",
            bg=BLACK,
            fg=WHITE,
            font=("Consolas", 11)
        ).pack(pady=5)

        # ====================================================
        # INPUT
        # ====================================================

        entry = tk.Entry(
            dialog,
            bg="#1C1C1C",
            fg=WHITE,
            insertbackground=WHITE,
            font=("Consolas", 18, "bold"),
            justify="center",
            relief="flat"
        )
        entry.pack(fill="x", padx=55, pady=15, ipady=8)

        # ====================================================
        # CHECK KEY
        # ====================================================

        def check_key():

            entered = entry.get().strip()

            if entered == UNLOCK_KEY:
                self.complete_simulation(dialog)

            else:
                messagebox.showerror(
                    "Invalid Recovery Key",
                    "The recovery key is incorrect.",
                    parent=dialog
                )
                entry.delete(0, tk.END)
                entry.focus_force()

        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = tk.Frame(dialog, bg=BLACK)
        button_frame.pack(pady=3)

        tk.Button(
            button_frame,
            text="CONTINUE",
            command=check_key,
            bg=RED,
            fg=WHITE,
            activebackground=LIGHT_RED,
            activeforeground=WHITE,
            font=("Consolas", 11, "bold"),
            relief="flat",
            padx=25,
            pady=8
        ).pack(side="left", padx=6)

        # Cancel only closes the recovery popup.
        # It does NOT close the simulation.
        def close_dialog():

            try:
                dialog.grab_release()
            except tk.TclError:
                pass

            self.recovery_dialog = None
            dialog.destroy()

        tk.Button(
            button_frame,
            text="CANCEL",
            command=close_dialog,
            bg="#333333",
            fg=WHITE,
            activebackground="#555555",
            font=("Consolas", 11, "bold"),
            relief="flat",
            padx=25,
            pady=8
        ).pack(side="left", padx=6)

        # Small hint so a stuck person knows there is a way out
        tk.Label(
            dialog,
            text="Don't know the key? Press CANCEL.",
            bg=BLACK,
            fg=GRAY,
            font=("Consolas", 9)
        ).pack(pady=(10, 0))

        # ====================================================
        # WINDOW CONTROLS
        # ====================================================

        dialog.protocol("WM_DELETE_WINDOW", close_dialog)

        # Enter = submit
        dialog.bind("<Return>", lambda event: check_key())

        # Escape ONLY closes the popup (a long hold still exits
        # the whole program through the emergency exit).
        dialog.bind("<Escape>", lambda event: close_dialog())

        # ====================================================
        # FOCUS
        # ====================================================

        dialog.wait_visibility()
        dialog.grab_set()
        dialog.lift()
        entry.focus_force()


    # ========================================================
    # SIMULATION COMPLETE
    # ========================================================

    def complete_simulation(self, dialog):

        self.unlocked = True
        self.running = False

        try:
            dialog.grab_release()
        except tk.TclError:
            pass

        try:
            dialog.destroy()
        except tk.TclError:
            pass

        self.recovery_dialog = None

        # Show the educational awareness screen, then close.
        self.show_awareness_screen()


    # ========================================================
    # AWARENESS SCREEN (SHOWN AFTER THE CORRECT KEY)
    # ========================================================

    def show_awareness_screen(self):

        # Remove the fake ransomware screen
        self.main.pack_forget()

        screen = tk.Frame(self.root, bg=BLACK)
        screen.pack(fill="both", expand=True)
        self.awareness_screen = screen

        # ----------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------

        bar = tk.Frame(screen, bg=GREEN)
        bar.pack(fill="x")

        tk.Label(
            bar,
            text="✓  SIMULATION COMPLETE  -  NO FILES WERE HARMED",
            bg=GREEN,
            fg=BLACK,
            font=("Consolas", 19, "bold")
        ).pack(pady=11)

        # ----------------------------------------------------
        # HEADING
        # ----------------------------------------------------

        tk.Label(
            screen,
            text="HOW TO PROTECT YOURSELF FROM RANSOMWARE",
            bg=BLACK,
            fg=WHITE,
            font=("Consolas", 30, "bold")
        ).pack(pady=(18, 2))

        tk.Label(
            screen,
            text="What you just saw was only a simulation. "
                 "These habits protect you in real life.",
            bg=BLACK,
            fg=GREEN,
            font=("Consolas", 13, "bold")
        ).pack(pady=(0, 14))

        # ----------------------------------------------------
        # TIP CARDS (2 columns x 3 rows)
        # ----------------------------------------------------

        grid = tk.Frame(screen, bg=BLACK)
        grid.pack(fill="both", expand=True, padx=55)

        grid.grid_columnconfigure(0, weight=1, uniform="tips")
        grid.grid_columnconfigure(1, weight=1, uniform="tips")

        for row in range(3):
            grid.grid_rowconfigure(row, weight=1)

        for index, (title, text) in enumerate(AWARENESS_TIPS):

            row = index // 2
            column = index % 2

            card = tk.Frame(
                grid,
                bg=PANEL,
                highlightbackground=GREEN,
                highlightthickness=1
            )
            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=8,
                pady=6
            )

            tk.Label(
                card,
                text=str(index + 1),
                bg=PANEL,
                fg=GREEN,
                font=("Consolas", 30, "bold"),
                width=2
            ).pack(side="left", padx=(10, 4))

            body = tk.Frame(card, bg=PANEL)
            body.pack(side="left", fill="both", expand=True, padx=(0, 12))

            tk.Label(
                body,
                text=title,
                bg=PANEL,
                fg=WHITE,
                font=("Consolas", 13, "bold"),
                anchor="w"
            ).pack(fill="x", pady=(10, 2))

            tk.Label(
                body,
                text=text,
                bg=PANEL,
                fg=GRAY,
                font=("Consolas", 10),
                justify="left",
                anchor="w",
                wraplength=430
            ).pack(fill="x", pady=(0, 10))

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = tk.Frame(screen, bg=BLACK)
        footer.pack(fill="x", padx=55, pady=(8, 14))

        tk.Label(
            footer,
            text=f"Created by {YOUR_NAME}  |  {COLLEGE_NAME}",
            bg=BLACK,
            fg=GRAY,
            font=("Consolas", 10, "bold")
        ).pack(side="left")

        tk.Button(
            footer,
            text="CLOSE NOW",
            command=self.close_after_completion,
            bg=GREEN,
            fg=BLACK,
            activebackground="#7CFFB5",
            activeforeground=BLACK,
            font=("Consolas", 11, "bold"),
            relief="flat",
            padx=22,
            pady=6,
            cursor="hand2"
        ).pack(side="right")

        self.awareness_countdown = tk.Label(
            footer,
            text="",
            bg=BLACK,
            fg=AMBER,
            font=("Consolas", 10, "bold")
        )
        self.awareness_countdown.pack(side="right", padx=20)

        # Enter closes the screen early
        self.root.bind_all("<Return>", lambda e: self.close_after_completion())

        self.root.focus_force()
        self.awareness_tick()


    def awareness_tick(self):

        if self.awareness_remaining <= 0:
            self.close_after_completion()
            return

        self.awareness_countdown.configure(
            text=f"Closing in {self.awareness_remaining}s  (press Enter to close now)"
        )

        self.awareness_remaining -= 1

        self.root.after(1000, self.awareness_tick)


    # ========================================================
    # CLOSE AFTER SUCCESS
    # ========================================================

    def close_after_completion(self):

        try:
            self.root.destroy()
        except tk.TclError:
            pass


    # ========================================================
    # TIMER (VISUAL COUNTDOWN ONLY)
    # ========================================================

    def update_timer(self):

        if not self.running:
            return

        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60

        # Turns amber/white flashing in the last minute for drama
        if self.remaining_seconds <= 60:
            color = WHITE if self.remaining_seconds % 2 == 0 else RED
        else:
            color = RED

        self.timer_label.configure(
            text=f"{minutes:02d}:{seconds:02d}",
            fg=color
        )

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
        else:
            # Simulation only: restart the visual countdown.
            self.remaining_seconds = 299

        self.root.after(1000, self.update_timer)


    # ========================================================
    # FAILSAFE: AUTO-EXIT AFTER FIXED TIME
    # ========================================================
    #
    # No matter what happens (lost focus, forgotten key,
    # open popups), the program closes itself when the
    # countdown reaches zero.

    def auto_exit_tick(self):

        if not self.running:
            return

        if self.auto_exit_remaining <= 0:
            self.developer_exit()
            return

        m = self.auto_exit_remaining // 60
        s = self.auto_exit_remaining % 60

        

        self.auto_exit_remaining -= 1

        self.root.after(1000, self.auto_exit_tick)


    # ========================================================
    # FAILSAFE: HOLD ESC TO EXIT
    # ========================================================

    def esc_down(self, event=None):

        if self.esc_job is None:
            self.esc_job = self.root.after(
                ESC_HOLD_MS,
                self.developer_exit
            )

    def esc_up(self, event=None):

        if self.esc_job is not None:
            self.root.after_cancel(self.esc_job)
            self.esc_job = None


    # ========================================================
    # KEEP KEYBOARD FOCUS ON THE APP
    # ========================================================
    #
    # Keeps the key shortcuts working even if focus drifts.

    def keep_focus(self):

        if not self.running:
            return

        if self.recovery_dialog is None:
            try:
                self.root.focus_force()
            except tk.TclError:
                return

        self.root.after(2000, self.keep_focus)


    # ========================================================
    # FAKE ACTIVITY + LIVE COUNTERS
    # ========================================================

    def update_activity(self):

        if not self.running:
            return

        file_name = random.choice(FAKE_FILES)
        extension = random.choice(FAKE_EXTENSIONS)

        self.fake_file_label.configure(text=f"> {file_name}{extension}")
        self.activity_label.configure(text=random.choice(ACTIVITY_MESSAGES))

        # Live fake counters
        self.files_locked += random.randint(5, 25)

        if self.files_locked >= self.files_affected:
            self.files_affected += random.randint(60, 200)
            self.folders += random.randint(1, 6)

        self.affected_value.configure(text=str(self.files_affected))
        self.locked_value.configure(text=str(self.files_locked))
        self.folders_value.configure(text=str(self.folders))

        # Progress bar
        ratio = min(self.files_locked / self.files_affected, 1.0)
        bar_width = self.progress_canvas.winfo_width()

        self.progress_canvas.coords(
            self.progress_bar,
            0, 0, bar_width * ratio, 16
        )
        self.progress_text.configure(text=f"{int(ratio * 100)}%")

        self.root.after(random.randint(800, 1600), self.update_activity)


    # ========================================================
    # BLINKING WARNING BAR
    # ========================================================

    def blink_warning(self):

        if not self.running:
            return

        self.blink_state = not self.blink_state

        color = RED if self.blink_state else "#B00000"

        self.warning_bar.configure(bg=color)
        self.warning_label.configure(bg=color)

        self.root.after(700, self.blink_warning)


    # ========================================================
    # GLITCH EFFECT
    # ========================================================

    def glitch_effect(self):

        if not self.running:
            return

        if random.random() < 0.15:
            self.main_title.configure(fg=RED)
            self.root.after(80, self.restore_title)

        self.root.after(random.randint(500, 1000), self.glitch_effect)

    def restore_title(self):

        if self.running:
            self.main_title.configure(fg=WHITE)


    # ========================================================
    # IGNORE NORMAL CLOSE
    # ========================================================

    def ignore_close(self):

        # Do nothing. Prevents Alt+F4 / window-close from
        # breaking the simulation flow.
        pass


    # ========================================================
    # EXIT (HIDDEN SHORTCUT, ESC-HOLD AND AUTO-EXIT ALL USE THIS)
    # ========================================================

    def developer_exit(self, event=None):

        self.running = False

        try:

            if (
                self.recovery_dialog is not None
                and self.recovery_dialog.winfo_exists()
            ):
                try:
                    self.recovery_dialog.grab_release()
                except tk.TclError:
                    pass

                self.recovery_dialog.destroy()
                self.recovery_dialog = None

            self.root.destroy()

        except tk.TclError:
            pass


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CyberLockSimulation(root)

    root.mainloop()