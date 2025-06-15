import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
import sys


# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from main import WebScrapingSystem
except ImportError:
    # Fallback for when running as standalone
    from web_scraping_system import WebScrapingSystem

class WebScrapingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraping AI with Blockchain Storage")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Initialize system
        self.system = None
        self.scraping_active = False
        self.scraping_thread = None
        
        # Configure style
        self.setup_styles()
        
        # Create GUI elements
        self.create_widgets()
        
        # Initialize system
        self.initialize_system()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        
        # Configure modern colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Status.TLabel', font=('Arial', 10), foreground='#27ae60')
        style.configure('Error.TLabel', font=('Arial', 10), foreground='#e74c3c')
        style.configure('Success.TButton', foreground='#27ae60')
        style.configure('Danger.TButton', foreground='#e74c3c')
        
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🕷️ Web Scraping AI with Blockchain Storage", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Control Panel
        self.create_control_panel(main_frame)
        
        # Main content area with tabs
        self.create_main_content(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_control_panel(self, parent):
        """Create control panel with input fields and buttons"""
        control_frame = ttk.LabelFrame(parent, text="Control Panel", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(1, weight=1)
        
        # URL input
        ttk.Label(control_frame, text="Target URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.url_var = tk.StringVar(value="https://example.com")
        url_entry = ttk.Entry(control_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Max pages input
        ttk.Label(control_frame, text="Max Pages:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        self.max_pages_var = tk.StringVar(value="10")
        max_pages_entry = ttk.Entry(control_frame, textvariable=self.max_pages_var, width=10)
        max_pages_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0))
        
        self.start_button = ttk.Button(button_frame, text="🚀 Start Scraping", 
                                      command=self.start_scraping, style='Success.TButton')
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Stop Scraping", 
                                     command=self.stop_scraping, style='Danger.TButton', state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="📊 Generate Report", 
                  command=self.generate_report).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="💾 Export Data", 
                  command=self.export_data).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🔍 Search", 
                  command=self.show_search_dialog).pack(side=tk.LEFT)
        
    def create_main_content(self, parent):
        """Create main content area with tabs"""
        notebook = ttk.Notebook(parent)
        notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Log tab
        self.create_log_tab(notebook)
        
        # Blockchain tab
        self.create_blockchain_tab(notebook)
        
        # Analysis tab
        self.create_analysis_tab(notebook)
        
        # Settings tab
        self.create_settings_tab(notebook)
        
    def create_log_tab(self, notebook):
        """Create logging tab"""
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="📋 Logs")
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Log controls
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(log_controls, text="Clear Logs", 
                  command=self.clear_logs).pack(side=tk.LEFT)
        ttk.Button(log_controls, text="Save Logs", 
                  command=self.save_logs).pack(side=tk.LEFT, padx=(10, 0))
        
        # Auto-scroll checkbox
        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(log_controls, text="Auto-scroll", 
                       variable=self.auto_scroll_var).pack(side=tk.RIGHT)
        
    def create_blockchain_tab(self, notebook):
        """Create blockchain data tab"""
        blockchain_frame = ttk.Frame(notebook)
        notebook.add(blockchain_frame, text="⛓️ Blockchain")
        
        # Blockchain info
        info_frame = ttk.LabelFrame(blockchain_frame, text="Blockchain Info", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.blockchain_info = tk.StringVar(value="Blockchain not initialized")
        ttk.Label(info_frame, textvariable=self.blockchain_info).pack()
        
        # Blockchain data tree
        tree_frame = ttk.Frame(blockchain_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Treeview for blockchain data
        columns = ('Index', 'Timestamp', 'Hash', 'Previous Hash', 'Data Type')
        self.blockchain_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.blockchain_tree.heading(col, text=col)
            self.blockchain_tree.column(col, width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.blockchain_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.blockchain_tree.xview)
        self.blockchain_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.blockchain_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Refresh button
        ttk.Button(blockchain_frame, text="🔄 Refresh Blockchain", 
                  command=self.refresh_blockchain_data).pack(pady=10)
        
    def create_analysis_tab(self, notebook):
        """Create analysis tab"""
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="📈 Analysis")
        
        # Analysis report
        report_frame = ttk.LabelFrame(analysis_frame, text="Analysis Report", padding="10")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.analysis_text = scrolledtext.ScrolledText(report_frame, wrap=tk.WORD, height=20)
        self.analysis_text.pack(fill=tk.BOTH, expand=True)
        
        # Analysis controls
        controls_frame = ttk.Frame(analysis_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Button(controls_frame, text="📊 Generate Analysis", 
                  command=self.generate_analysis).pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="🔍 Detect Anomalies", 
                  command=self.detect_anomalies).pack(side=tk.LEFT, padx=(10, 0))
        
    def create_settings_tab(self, notebook):
        """Create settings tab"""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="⚙️ Settings")
        
        # Scraping settings
        scraping_settings = ttk.LabelFrame(settings_frame, text="Scraping Settings", padding="10")
        scraping_settings.pack(fill=tk.X, padx=10, pady=10)
        
        # Delay setting
        ttk.