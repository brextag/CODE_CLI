#!/usr/bin/env python3
"""
Nova GUI - CLI-themed GUI for Nova AI Agent
A terminal-inspired graphical interface built with Tkinter
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import json
import sys
from datetime import datetime
from pathlib import Path
from nova_cli import NovaAgent


class NovaGUI:
    """
    Nova GUI Application - Terminal-themed interface
    """
    
    # CLI-inspired color scheme
    COLORS = {
        'bg': '#0d0221',           # Dark purple-black background
        'fg': '#e0ffff',           # Cyan text
        'accent': '#ff006e',       # Pink accent
        'success': '#00ff41',      # Neon green
        'warning': '#ffbe0b',      # Amber warning
        'error': '#ff006e',        # Pink error
        'input_bg': '#1a0033',     # Darker purple
        'border': '#3a0066',       # Medium purple
        'highlight': '#ff006e',   # Pink highlight
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Nova - AI-Powered CLI Agent")
        self.root.geometry("1000x700")
        
        # Set icon and style
        self.root.configure(bg=self.COLORS['bg'])
        
        # Initialize Nova agent
        self.nova = NovaAgent()
        
        # Setup GUI
        self.setup_ui()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-l>', lambda e: self.clear_output())
        self.root.bind('<Control-h>', lambda e: self.show_history())
        self.root.bind('<Return>', self.on_input_return)
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Main container with dark theme
        main_frame = tk.Frame(self.root, bg=self.COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header
        self.create_header(main_frame)
        
        # Display area (output/terminal)
        self.create_display_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create header with title and info"""
        header_frame = tk.Frame(parent, bg=self.COLORS['border'], height=50)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="◆ NOVA - AI-Powered CLI Agent v1.0.0 ◆",
            font=("Courier New", 14, "bold"),
            fg=self.COLORS['highlight'],
            bg=self.COLORS['border']
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Your AI companion in a GUI terminal • Press Ctrl+H for history • Ctrl+L to clear",
            font=("Courier New", 9),
            fg=self.COLORS['fg'],
            bg=self.COLORS['border']
        )
        subtitle_label.pack()
    
    def create_display_area(self, parent):
        """Create the main display/output area"""
        display_frame = tk.Frame(parent, bg=self.COLORS['bg'])
        display_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Output display with scrollbar
        self.output_text = scrolledtext.ScrolledText(
            display_frame,
            bg=self.COLORS['input_bg'],
            fg=self.COLORS['fg'],
            insertbackground=self.COLORS['highlight'],
            font=("Courier New", 10),
            wrap=tk.WORD,
            borderwidth=2,
            relief=tk.SOLID
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)
        
        # Configure text tags for styling
        self.output_text.tag_configure('header', foreground=self.COLORS['highlight'], font=("Courier New", 10, "bold"))
        self.output_text.tag_configure('success', foreground=self.COLORS['success'])
        self.output_text.tag_configure('error', foreground=self.COLORS['error'])
        self.output_text.tag_configure('warning', foreground=self.COLORS['warning'])
        self.output_text.tag_configure('info', foreground=self.COLORS['accent'])
        self.output_text.tag_configure('command', foreground=self.COLORS['highlight'], font=("Courier New", 10, "bold"))
        
        # Welcome message
        self.display_welcome()
    
    def create_input_area(self, parent):
        """Create the input area with command buttons"""
        input_frame = tk.Frame(parent, bg=self.COLORS['bg'])
        input_frame.pack(fill=tk.X, padx=2, pady=5)
        
        # Command buttons
        buttons_frame = tk.Frame(input_frame, bg=self.COLORS['bg'])
        buttons_frame.pack(fill=tk.X, pady=5)
        
        commands = [
            ("Ask", self.execute_ask),
            ("Analyze", self.execute_analyze),
            ("Generate", self.execute_generate),
            ("Explain", self.execute_explain),
            ("History", self.show_history),
            ("Clear", self.clear_output),
        ]
        
        for cmd_name, cmd_func in commands:
            btn = tk.Button(
                buttons_frame,
                text=cmd_name,
                command=cmd_func,
                bg=self.COLORS['highlight'],
                fg=self.COLORS['input_bg'],
                activebackground=self.COLORS['accent'],
                font=("Courier New", 9, "bold"),
                padx=15,
                pady=5,
                relief=tk.FLAT,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=3)
        
        # Input field
        input_label = tk.Label(
            input_frame,
            text="Nova>",
            font=("Courier New", 10, "bold"),
            fg=self.COLORS['highlight'],
            bg=self.COLORS['bg']
        )
        input_label.pack(side=tk.LEFT, padx=5)
        
        self.input_entry = tk.Entry(
            input_frame,
            bg=self.COLORS['input_bg'],
            fg=self.COLORS['fg'],
            insertbackground=self.COLORS['highlight'],
            font=("Courier New", 10),
            borderwidth=2,
            relief=tk.SOLID
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input_entry.focus()
        
        # Submit button
        submit_btn = tk.Button(
            input_frame,
            text="Execute",
            command=self.execute_input,
            bg=self.COLORS['success'],
            fg=self.COLORS['input_bg'],
            activebackground=self.COLORS['highlight'],
            font=("Courier New", 9, "bold"),
            padx=15,
            relief=tk.FLAT,
            cursor="hand2"
        )
        submit_btn.pack(side=tk.LEFT, padx=5)
    
    def create_status_bar(self, parent):
        """Create status bar at bottom"""
        status_frame = tk.Frame(parent, bg=self.COLORS['border'], height=30)
        status_frame.pack(fill=tk.X, padx=0, pady=0)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready • Type 'help' or select a command • Ctrl+L to clear output • Ctrl+H for history",
            font=("Courier New", 8),
            fg=self.COLORS['fg'],
            bg=self.COLORS['border']
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.time_label = tk.Label(
            status_frame,
            text=self.get_time(),
            font=("Courier New", 8),
            fg=self.COLORS['accent'],
            bg=self.COLORS['border']
        )
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Update time
        self.update_time()
    
    def display_welcome(self):
        """Display welcome message"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, "╔" + "═" * 78 + "╗\n", "header")
        self.output_text.insert(tk.END, "║" + " " * 78 + "║\n", "header")
        self.output_text.insert(tk.END, "║" + "  Nova - AI-Powered CLI Agent • GUI Terminal Interface".center(78) + "║\n", "header")
        self.output_text.insert(tk.END, "║" + "  v1.0.0".center(78) + "║\n", "header")
        self.output_text.insert(tk.END, "║" + " " * 78 + "║\n", "header")
        self.output_text.insert(tk.END, "╚" + "═" * 78 + "╝\n\n", "header")
        
        self.output_text.insert(tk.END, "Available Commands:\n", "info")
        self.output_text.insert(tk.END, "  • ", "success")
        self.output_text.insert(tk.END, "ask <query>", "command")
        self.output_text.insert(tk.END, " - Ask Nova a question\n")
        
        self.output_text.insert(tk.END, "  • ", "success")
        self.output_text.insert(tk.END, "analyze <target>", "command")
        self.output_text.insert(tk.END, " - Analyze code, files, or concepts\n")
        
        self.output_text.insert(tk.END, "  • ", "success")
        self.output_text.insert(tk.END, "generate <spec>", "command")
        self.output_text.insert(tk.END, " - Generate code or content\n")
        
        self.output_text.insert(tk.END, "  • ", "success")
        self.output_text.insert(tk.END, "explain <concept>", "command")
        self.output_text.insert(tk.END, " - Get detailed explanation\n")
        
        self.output_text.insert(tk.END, "  • ", "success")
        self.output_text.insert(tk.END, "help", "command")
        self.output_text.insert(tk.END, " - Show all available commands\n")
        
        self.output_text.insert(tk.END, "\n" + "─" * 80 + "\n\n", "warning")
        self.output_text.config(state=tk.DISABLED)
    
    def on_input_return(self, event):
        """Handle Enter key in input field"""
        self.execute_input()
        return 'break'
    
    def execute_input(self):
        """Execute user input"""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        
        self.input_entry.delete(0, tk.END)
        self.append_output(f"Nova> {user_input}\n", "command")
        
        # Parse and execute
        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command == 'help':
            self.show_help()
        elif command == 'ask' and args:
            self.execute_ask(args)
        elif command == 'analyze' and args:
            self.execute_analyze(args)
        elif command == 'generate' and args:
            self.execute_generate(args)
        elif command == 'explain' and args:
            self.execute_explain(args)
        elif command == 'history':
            self.show_history()
        elif command == 'clear':
            self.clear_output()
        elif command == 'exit':
            self.root.quit()
        else:
            self.append_output("Unknown command. Type 'help' for available commands.\n", "error")
        
        self.update_status("Command executed")
    
    def execute_ask(self, query=None):
        """Execute ask command"""
        if query is None:
            query = self.get_user_input("Ask Nova a question:")
        if query:
            result = self.nova.ask(query)
            self.append_output(f"\n{result}\n", "success")
            self.update_status(f"✓ Ask command executed")
    
    def execute_analyze(self, target=None):
        """Execute analyze command"""
        if target is None:
            target = self.get_user_input("What would you like to analyze?")
        if target:
            result = self.nova.analyze(target)
            self.append_output(f"\n{result}\n", "success")
            self.update_status(f"✓ Analyze command executed")
    
    def execute_generate(self, spec=None):
        """Execute generate command"""
        if spec is None:
            spec = self.get_user_input("What would you like to generate?")
        if spec:
            result = self.nova.generate(spec)
            self.append_output(f"\n{result}\n", "success")
            self.update_status(f"✓ Generate command executed")
    
    def execute_explain(self, concept=None):
        """Execute explain command"""
        if concept is None:
            concept = self.get_user_input("What concept would you like explained?")
        if concept:
            result = self.nova.explain(concept)
            self.append_output(f"\n{result}\n", "success")
            self.update_status(f"✓ Explain command executed")
    
    def show_help(self):
        """Display help information"""
        self.append_output("\n", "info")
        self.append_output("═" * 80 + "\n", "info")
        self.append_output("NOVA CLI - Available Commands\n", "header")
        self.append_output("═" * 80 + "\n\n", "info")
        
        commands = [
            ("ask <query>", "Ask Nova a question"),
            ("analyze <target>", "Analyze code, files, or concepts"),
            ("generate <spec>", "Generate code or content"),
            ("explain <concept>", "Get detailed explanation"),
            ("history", "View command history"),
            ("clear", "Clear output"),
            ("help", "Show this help message"),
            ("exit", "Exit the application"),
        ]
        
        for cmd, desc in commands:
            self.append_output(f"  {cmd:25}", "command")
            self.append_output(f" - {desc}\n", "info")
        
        self.append_output("\n" + "─" * 80 + "\n\n", "warning")
    
    def show_history(self):
        """Display command history"""
        if not self.nova.history:
            self.append_output("\nNo command history yet.\n", "warning")
            return
        
        self.append_output("\n" + "═" * 80 + "\n", "info")
        self.append_output("Command History (Last 10)\n", "header")
        self.append_output("═" * 80 + "\n\n", "info")
        
        for i, entry in enumerate(self.nova.history[-10:], 1):
            self.append_output(f"{i}. ", "accent")
            self.append_output(f"{entry['timestamp']}\n", "info")
            self.append_output(f"   Command: ", "success")
            self.append_output(f"{entry['command']}\n", "command")
            self.append_output(f"   Summary: {entry['result_summary']}\n\n", "info")
        
        self.append_output("─" * 80 + "\n\n", "warning")
    
    def clear_output(self):
        """Clear output display"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.update_status("Output cleared • Ready for new commands")
    
    def append_output(self, text, tag="info"):
        """Append text to output display"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text, tag)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def get_user_input(self, prompt):
        """Show input dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nova Input")
        dialog.geometry("400x150")
        dialog.configure(bg=self.COLORS['bg'])
        dialog.resizable(False, False)
        
        label = tk.Label(dialog, text=prompt, font=("Courier New", 10), fg=self.COLORS['fg'], bg=self.COLORS['bg'])
        label.pack(pady=10)
        
        entry = tk.Entry(
            dialog,
            bg=self.COLORS['input_bg'],
            fg=self.COLORS['fg'],
            font=("Courier New", 10),
            borderwidth=2,
            relief=tk.SOLID
        )
        entry.pack(pady=10, padx=20, fill=tk.X)
        entry.focus()
        
        result = [None]
        
        def on_ok():
            result[0] = entry.get()
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg=self.COLORS['bg'])
        btn_frame.pack(pady=10)
        
        ok_btn = tk.Button(
            btn_frame,
            text="OK",
            command=on_ok,
            bg=self.COLORS['success'],
            fg=self.COLORS['input_bg'],
            font=("Courier New", 9, "bold"),
            padx=20
        )
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=on_cancel,
            bg=self.COLORS['error'],
            fg=self.COLORS['input_bg'],
            font=("Courier New", 9, "bold"),
            padx=20
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        entry.bind('<Return>', lambda e: on_ok())
        entry.bind('<Escape>', lambda e: on_cancel())
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return result[0]
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
    
    def get_time(self):
        """Get formatted current time"""
        return datetime.now().strftime("%H:%M:%S")
    
    def update_time(self):
        """Update time in status bar"""
        self.time_label.config(text=self.get_time())
        self.root.after(1000, self.update_time)


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = NovaGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
