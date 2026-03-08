from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTabWidget, QSpinBox, 
                             QComboBox, QGroupBox, QFormLayout, QApplication,
                             QCheckBox, QListWidget, QMessageBox, QCompleter,
                             QScrollArea, QSlider, QSizePolicy, QGridLayout,
                             QFrame)
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QPixmap, QIcon, QColor
import logging
from hwctool.player_db import PlayerDB
from hwctool.view.themes import get_theme, THEMES
from hwctool.matchdata import LEADERS, MAPS
from hwctool.locale import get_text
from hwctool.view.widgets import AnimatedBackground

logger = logging.getLogger('root')

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.player_db = PlayerDB()
        self.lang = self.controller.config_manager.get("language", "es")
        self.setWindowTitle(self.tr("window_title"))
        self.resize(1100, 800)
        self.setMinimumSize(900, 650)
        
        self.setup_ui()

    def tr(self, key):
        return get_text(key, self.lang)

    # HW2 Player Colors
    BLUE_TEAM_COLORS = [
        ("Blue", "#1155FF"),
        ("Cyan", "#00CCFF"),
        ("Green", "#22CC44"),
    ]
    RED_TEAM_COLORS = [
        ("Red", "#CC2222"),
        ("Orange", "#FF6600"),
        ("Yellow", "#FFCC00"),
    ]

    COUNTRIES = {
        "Mexico": "mx",
        "USA": "us",
        "Canada": "ca",
        "UK": "gb",
        "France": "fr",
        "Germany": "de",
        "Spain": "es",
        "Italy": "it",
        "Argentina": "ar",
        "Brazil": "br",
        "Chile": "cl",
        "Colombia": "co",
        "Peru": "pe",
        "Australia": "au",
        "Japan": "jp",
        "Korea": "kr",
        "China": "cn",
        "Other": "xx"
    }

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Animated Background Layer
        self.bg_animated = AnimatedBackground(central_widget)
        self.bg_animated.lower() # Place behind everything
        self.bg_animated.setVisible(self.controller.config_manager.get("dynamic_bg", True))
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Helper to wrap widgets in a scroll area
        def wrap(w):
            s = QScrollArea()
            s.setWidgetResizable(True)
            s.setFrameShape(QFrame.Shape.NoFrame)
            s.setWidget(w)
            s.setStyleSheet("background: transparent;")
            return s

        self.match_tab = QWidget()
        self.setup_match_tab()
        self.tabs.addTab(wrap(self.match_tab), "Settings")
        
        self.settings_tab = QWidget()
        self.setup_settings_tab()
        self.tabs.addTab(wrap(self.settings_tab), "Browser Sources")
        
        self.players_tab = QWidget()
        self.setup_players_tab()
        self.tabs.addTab(wrap(self.players_tab), "Profile")
        
        self.info_tab = QWidget()
        self.setup_info_tab()
        self.tabs.addTab(wrap(self.info_tab), "Info & Links")
        
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.tr("window_title"))
        self.tabs.setTabText(0, self.tr("tab_control"))
        self.tabs.setTabText(1, self.tr("tab_settings"))
        self.tabs.setTabText(2, self.tr("tab_players"))
        self.tabs.setTabText(3, self.tr("tab_info"))
        
        # Match Tab
        self.grp_custom_match.setTitle(self.tr("grp_custom_match"))
        self.lbl_format.setText(self.tr("lbl_format"))
        self.lbl_game_type.setText(self.tr("lbl_game_type"))
        self.lbl_best_of.setText(self.tr("lbl_best_of"))
        self.lbl_at_least.setText(self.tr("lbl_at_least"))
        self.lbl_maps.setText(self.tr("lbl_maps"))
        self.lbl_current_map.setText(self.tr("map"))
        self.btn_apply.setText(self.tr("btn_apply_format"))
        self.roster_group.setTitle(self.tr("grp_team_roster"))
        self.match_data_group.setTitle(self.tr("grp_match_data"))
        
        self.lbl_dynamic_bg.setText(self.tr("dynamic_bg"))
        
        self.tasks_group.setTitle(self.tr("grp_tasks"))
        self.btn_reset.setText(self.tr("btn_reset_score"))
        
        self.lbl_made_by.setText(self.tr("lbl_made_by"))

        # Players Tab
        self.lbl_registered_players.setText(self.tr("registered_players"))
        self.grp_player_data.setTitle(self.tr("player_data"))
        self.lbl_gamertag.setText(self.tr("gamertag"))
        self.lbl_rank1.setText(self.tr("rank_1v1"))
        self.lbl_mmr1.setText(self.tr("mmr_1v1"))
        self.lbl_rank2.setText(self.tr("rank_2v2"))
        self.lbl_mmr2.setText(self.tr("mmr_2v2"))
        self.lbl_rank3.setText(self.tr("rank_3v3"))
        self.lbl_mmr3.setText(self.tr("mmr_3v3"))
        self.lbl_playstyle.setText(self.tr("playstyle"))
        self.lbl_main_leader.setText(self.tr("main_leader"))
        self.btn_new.setText(self.tr("btn_new"))
        self.btn_save.setText(self.tr("btn_save"))
        self.btn_delete.setText(self.tr("btn_delete"))
        
        # Browser Sources (Settings)
        self.lbl_url_obs.setText(self.tr("lbl_urls_obs"))
        self.btn_copy_intro.setText(self.tr("copy_intro_url"))
        self.btn_copy_score.setText(self.tr("copy_score_url"))
        self.btn_copy_card.setText(self.tr("copy_card_url"))
        
        # Map Popup
        self.map_group.setTitle(self.tr("map_popup_config"))
        self.map_popup_enabled.setText(self.tr("map_popup_enable"))
        self.lbl_map_enter.setText(self.tr("map_enter"))
        self.lbl_map_visible.setText(self.tr("map_visible"))
        self.lbl_map_exit.setText(self.tr("map_exit"))
        self.lbl_map_hidden.setText(self.tr("map_hidden"))
        
        # Theme/Lang
        self.theme_group.setTitle(self.tr("tab_settings"))
        self.lbl_theme.setText(self.tr("theme"))
        self.lbl_language.setText(self.tr("language"))
        
        self.btn_reset.setText(self.tr("reset_all"))
        self.chk_show_teams.setText(self.tr("show_team_names"))
        self.chk_show_flags.setText(self.tr("show_flags"))
        self.chk_show_game_type.setText(self.tr("show_game_type"))
        
        self.refresh_match_rows()

    def setup_match_tab(self):
        layout = QVBoxLayout(self.match_tab)

        # --- Custom Match (Top) ---
        self.grp_custom_match = QGroupBox()
        cm_layout = QFormLayout(self.grp_custom_match)
        
        format_layout = QHBoxLayout()
        self.team_size = QComboBox()
        self.team_size.addItems(["1v1", "2v2", "3v3"])
        
        self.lbl_format = QLabel()
        format_layout.addWidget(self.team_size)

        self.best_of = QComboBox()
        self.best_of.addItems([str(i) for i in range(1, 16, 2)])
        self.lbl_best_of = QLabel()
        format_layout.addWidget(self.lbl_best_of)
        format_layout.addWidget(self.best_of)
        self.lbl_at_least = QLabel()
        format_layout.addWidget(self.lbl_at_least)
        self.at_least_cb = QComboBox()
        self.at_least_cb.addItems(["1", "2", "3", "4", "5", "6", "7"])
        format_layout.addWidget(self.at_least_cb)
        self.lbl_maps = QLabel()
        format_layout.addWidget(self.lbl_maps)
        format_layout.addStretch()
        
        self.btn_apply = QPushButton()
        format_layout.addWidget(self.btn_apply)
        
        cm_layout.addRow(self.lbl_format, format_layout)
        
        # --- Game Type Row ---
        game_type_layout = QHBoxLayout()
        self.game_type_combo = QComboBox()
        self.game_type_combo.addItems(["Deathmatch", "Domination", "Strongholds", "Blitz"])
        self.game_type_combo.currentTextChanged.connect(lambda t: setattr(self.controller.match_data, 'game_type', t))
        
        self.lbl_game_type = QLabel()
        game_type_layout.addWidget(self.game_type_combo)
        
        self.lbl_current_map = QLabel()
        self.map_combo = QComboBox()
        self.map_combo.addItems(MAPS)
        self.map_combo.currentTextChanged.connect(lambda t: setattr(self.controller.match_data, 'current_map', t))
        
        game_type_layout.addSpacing(20)
        game_type_layout.addWidget(self.lbl_current_map)
        game_type_layout.addWidget(self.map_combo)
        game_type_layout.addStretch()
        
        cm_layout.addRow(self.lbl_game_type, game_type_layout)
        
        layout.addWidget(self.grp_custom_match)
        
                # --- Team Roster ---
        self.roster_group = QGroupBox("Team Roster")
        self.roster_layout = QVBoxLayout(self.roster_group)
        layout.addWidget(self.roster_group)

        # --- Match Data Container ---
        self.match_data_group = QGroupBox("Match Data")
        self.match_data_layout = QVBoxLayout(self.match_data_group)
        

        
        self.match_rows_widget = QWidget()
        self.match_rows_layout = QGridLayout(self.match_rows_widget)
        self.match_rows_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.match_data_layout.addWidget(self.match_rows_widget)
        layout.addWidget(self.match_data_group)
        
        self.best_of.currentTextChanged.connect(lambda t: setattr(self.controller.match_data, 'best_of', int(t)))
        self.best_of.currentTextChanged.connect(self.refresh_match_rows)
        self.team_size.currentIndexChanged.connect(self.update_team_size)


        self.controller.match_data.init_matches() 
        self.update_team_size(0) # Default 1v1

        
        # --- Tasks / Options ---
        self.tasks_group = QGroupBox()
        tasks_layout = QHBoxLayout(self.tasks_group)
        
        self.chk_show_teams = QCheckBox()
        self.chk_show_teams.toggled.connect(self.on_show_team_names_toggled)
        tasks_layout.addWidget(self.chk_show_teams)
        
        self.chk_show_flags = QCheckBox()
        self.chk_show_flags.toggled.connect(self.on_show_flags_toggled)
        tasks_layout.addWidget(self.chk_show_flags)
        
        self.chk_show_game_type = QCheckBox()
        self.chk_show_game_type.toggled.connect(self.on_show_game_type_toggled)
        tasks_layout.addWidget(self.chk_show_game_type)
        
        tasks_layout.addStretch()

        self.btn_reset = QPushButton()
        self.btn_reset.clicked.connect(self.controller.reset_all)
        tasks_layout.addWidget(self.btn_reset)
        layout.addWidget(self.tasks_group)
        
                # Connect new buttons
        self.btn_apply.clicked.connect(lambda: self.refresh_match_rows())
        
        # Status indicators

        status_layout = QHBoxLayout()
        status_layout.addStretch()
        self.conn_indicator_1 = QLabel("🟢")
        self.conn_indicator_2 = QLabel("🟢")
        status_layout.addWidget(self.conn_indicator_1)
        status_layout.addWidget(self.conn_indicator_2)
        layout.addLayout(status_layout)
        # layout.addStretch()

    def setup_settings_tab(self):
        layout = QFormLayout(self.settings_tab)
        
        # Overlay URL Copy Buttons
        self.btn_copy_intro = QPushButton()
        self.btn_copy_intro.clicked.connect(lambda: QApplication.clipboard().setText("http://localhost:8000/intro.html"))
        
        self.btn_copy_score = QPushButton()
        self.btn_copy_score.clicked.connect(lambda: QApplication.clipboard().setText("http://localhost:8000/score.html"))
        
        self.btn_copy_card = QPushButton()
        self.btn_copy_card.clicked.connect(lambda: QApplication.clipboard().setText("http://localhost:8000/card.html"))
        
        url_layout = QHBoxLayout()
        url_layout.addWidget(self.btn_copy_intro)
        url_layout.addWidget(self.btn_copy_score)
        url_layout.addWidget(self.btn_copy_card)
        
        self.lbl_url_obs = QLabel("URLs OBS:")
        layout.addRow(self.lbl_url_obs, url_layout)

        # --- Map Popup Config ---
        self.map_group = QGroupBox()
        map_layout = QFormLayout(self.map_group)

        self.map_popup_enabled = QCheckBox()
        self.map_popup_enabled.setChecked(False)
        self.map_popup_enabled.toggled.connect(lambda v: setattr(self.controller.match_data, '_map_popup_enabled', v))
        self.map_popup_enabled.toggled.connect(lambda: self.controller.match_data.data_changed.emit())
        map_layout.addRow(self.map_popup_enabled)

        self.map_enter_spin = QSpinBox(); self.map_enter_spin.setRange(1, 60); self.map_enter_spin.setValue(3); self.map_enter_spin.setSuffix(" seg")
        self.map_enter_spin.valueChanged.connect(lambda v: setattr(self.controller.match_data, '_map_enter_sec', v))
        self.map_enter_spin.valueChanged.connect(lambda: self.controller.match_data.data_changed.emit())
        
        self.lbl_map_enter = QLabel()
        map_layout.addRow(self.lbl_map_enter, self.map_enter_spin)

        self.map_visible_spin = QSpinBox(); self.map_visible_spin.setRange(1, 300); self.map_visible_spin.setValue(25); self.map_visible_spin.setSuffix(" seg")
        self.map_visible_spin.valueChanged.connect(lambda v: setattr(self.controller.match_data, '_map_visible_sec', v))
        self.map_visible_spin.valueChanged.connect(lambda: self.controller.match_data.data_changed.emit())
        
        self.lbl_map_visible = QLabel()
        map_layout.addRow(self.lbl_map_visible, self.map_visible_spin)

        self.map_exit_spin = QSpinBox(); self.map_exit_spin.setRange(1, 60); self.map_exit_spin.setValue(3); self.map_exit_spin.setSuffix(" seg")
        self.map_exit_spin.valueChanged.connect(lambda v: setattr(self.controller.match_data, '_map_exit_sec', v))
        self.map_exit_spin.valueChanged.connect(lambda: self.controller.match_data.data_changed.emit())
        
        self.lbl_map_exit = QLabel()
        map_layout.addRow(self.lbl_map_exit, self.map_exit_spin)

        self.map_hidden_spin = QSpinBox(); self.map_hidden_spin.setRange(1, 300); self.map_hidden_spin.setValue(20); self.map_hidden_spin.setSuffix(" seg")
        self.map_hidden_spin.valueChanged.connect(lambda v: setattr(self.controller.match_data, '_map_hidden_sec', v))
        self.map_hidden_spin.valueChanged.connect(lambda: self.controller.match_data.data_changed.emit())
        
        self.lbl_map_hidden = QLabel()
        map_layout.addRow(self.lbl_map_hidden, self.map_hidden_spin)

        self.dynamic_bg_enabled = QCheckBox()
        self.dynamic_bg_enabled.setChecked(self.controller.config_manager.get("dynamic_bg", True))
        self.dynamic_bg_enabled.toggled.connect(self.toggle_dynamic_bg)
        self.lbl_dynamic_bg = QLabel()
        map_layout.addRow(self.lbl_dynamic_bg, self.dynamic_bg_enabled)

        layout.addRow(self.map_group)

        # --- Theme Selector ---
        self.theme_group = QGroupBox()
        theme_layout = QFormLayout(self.theme_group)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        # Load saved theme preference
        saved_theme = self.controller.config_manager.get("theme", "dark")
        idx = self.theme_combo.findText(saved_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        
        self.lbl_theme = QLabel()
        theme_layout.addRow(self.lbl_theme, self.theme_combo)

        # --- Language Selector ---
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Español", "es")
        self.lang_combo.addItem("English", "en")
        
        self.lang_combo.currentIndexChanged.connect(self.on_lang_changed)
        
        self.lbl_language = QLabel()
        theme_layout.addRow(self.lbl_language, self.lang_combo)

        layout.addRow(self.theme_group)

        self.lbl_made_by = QLabel()
        layout.addRow(self.lbl_made_by)

    def _make_color_combo(self, colors, prop_name, default_idx=0):
        """Create a color dropdown with colored icon swatches."""
        combo = QComboBox()
        combo.setFixedWidth(90)
        for name, hex_color in colors:
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(hex_color))
            combo.addItem(QIcon(pixmap), name, hex_color)
        combo.setCurrentIndex(default_idx)
        combo.currentIndexChanged.connect(
            lambda idx, c=combo, p=prop_name: setattr(
                self.controller.match_data, p, c.itemData(idx)
            )
        )
        return combo

    def on_show_team_names_toggled(self, checked):
        self.controller.match_data.show_team_names = checked

    def on_show_flags_toggled(self, checked):
        self.controller.match_data.show_flags = checked

    def on_show_game_type_toggled(self, checked):
        self.controller.match_data.show_game_type = checked

    def on_disconnect_toggled(self, checked):
        self.controller.match_data.disconnection = checked

    def on_theme_changed(self, theme_name):
        self.controller.config_manager.set("theme", theme_name)
        self.controller.config_manager.save_config()
        self.apply_theme(theme_name)
        logger.info(f"Tema cambiado a: {theme_name}")

    def on_lang_changed(self, index):
        new_lang = self.lang_combo.itemData(index)
        if new_lang and new_lang != self.lang:
            self.lang = new_lang
            self.controller.config_manager.set("language", new_lang)
            self.controller.config_manager.save_config()
            self.retranslate_ui()
            logger.info(f"Idioma cambiado a: {new_lang}")

    def apply_theme(self, theme_name):
        """Applies the given theme stylesheet to the entire application."""
        qss = get_theme(theme_name)
        QApplication.instance().setStyleSheet(qss)

    def clear_layout(self, layout):
        """Recursively clears a layout and deletes its widgets."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clear_layout(item.layout())

    def update_team_size(self, index):
        size = index + 1
        self.controller.match_data.team_size = size
        self.refresh_match_rows()

    def refresh_match_rows(self):
        self._all_completers = []
        self._match_player_labels = {i: [] for i in range(1, 7)}
        
        # Clear layouts robustly
        self.clear_layout(self.roster_layout)
        self.clear_layout(self.match_rows_layout)

        md = self.controller.match_data
        matches = getattr(md, 'matches', [])
        leaders = LEADERS
        self._leader_combos = {}
        team_size = md.team_size

        # --- Team Names ---
        t_name_row = QHBoxLayout()
        self.t1_edit = QLineEdit(md.player1_team)
        self.t1_edit.setPlaceholderText(self.tr("ph_team1_name"))
        self.t1_edit.textChanged.connect(lambda t: setattr(md, 'player1_team', t))
        
        self.t2_edit = QLineEdit(md.player2_team)
        self.t2_edit.setPlaceholderText(self.tr("ph_team2_name"))
        self.t2_edit.textChanged.connect(lambda t: setattr(md, 'player2_team', t))
        
        self.lbl_team1_roster = QLabel()
        self.lbl_team1_roster.setText(self.tr("lbl_team1"))
        t_name_row.addWidget(self.lbl_team1_roster)
        t_name_row.addWidget(self.t1_edit)
        
        self.lbl_vs_roster = QLabel()
        self.lbl_vs_roster.setText(self.tr("lbl_vs"))
        t_name_row.addWidget(self.lbl_vs_roster)
        
        t_name_row.addWidget(self.t2_edit)
        
        self.lbl_team2_roster = QLabel()
        self.lbl_team2_roster.setText(self.tr("lbl_team2"))
        t_name_row.addWidget(self.lbl_team2_roster)
        self.roster_layout.addLayout(t_name_row)

        # --- Build Roster Section ---
        def make_player_edit(attr, ph, prop, player_idx):
            current_val = getattr(md, attr, ph)
            if current_val == ph: current_val = "" # Don't show "Player N" as text
            e = QLineEdit(current_val)
            e.setPlaceholderText(ph)
            
            def update_model_and_labels(t, p=prop, p_idx=player_idx):
                setattr(md, p, t)
                display_name = t if t.strip() else f"P{p_idx}"
                is_left = p_idx % 2 != 0
                text = f"<b>{display_name}:</b>" if is_left else f"<b>:{display_name}</b>"
                for lbl in self._match_player_labels[p_idx]:
                    lbl.setText(text)

            e.textChanged.connect(update_model_and_labels)
            completer = QCompleter(self.player_db.get_all_names(), e)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            e.setCompleter(completer)
            self._all_completers.append(completer)
            return e

        for j in range(team_size):
            p_row = QHBoxLayout()
            idx1 = 1 if j == 0 else (3 if j == 1 else 5)
            idx2 = 2 if j == 0 else (4 if j == 1 else 6)
            
            p1_ph = self.tr("ph_player_n").replace("{n}", str(idx1))
            p2_ph = self.tr("ph_player_n").replace("{n}", str(idx2))
            
            p1_edit = make_player_edit(f'_player{idx1}_name', p1_ph, f'player{idx1}_name', idx1)
            p2_edit = make_player_edit(f'_player{idx2}_name', p2_ph, f'player{idx2}_name', idx2)
            
            p1_country = QComboBox()
            p1_country.setFixedWidth(80)
            for name, code in self.COUNTRIES.items():
                p1_country.addItem(name, code)
            curr1 = getattr(md, f'player{idx1}_country', 'mx')
            p1_country.setCurrentIndex(p1_country.findData(curr1))
            p1_country.currentIndexChanged.connect(lambda idx, p=idx1, c=p1_country: [setattr(md, f'player{p}_country', c.itemData(idx)), md.data_changed.emit()])

            p2_country = QComboBox()
            p2_country.setFixedWidth(80)
            for name, code in self.COUNTRIES.items():
                p2_country.addItem(name, code)
            curr2 = getattr(md, f'player{idx2}_country', 'mx')
            p2_country.setCurrentIndex(p2_country.findData(curr2))
            p2_country.currentIndexChanged.connect(lambda idx, p=idx2, c=p2_country: [setattr(md, f'player{p}_country', c.itemData(idx)), md.data_changed.emit()])

            p1_lbl_text = self.tr("p_n").replace("{n}", str(idx1))
            p2_lbl_text = self.tr("p_n").replace("{n}", str(idx2))
            
            p_row.addWidget(QLabel(p1_lbl_text))
            p_row.addWidget(p1_country)
            p_row.addWidget(p1_edit)
            p_row.addWidget(QLabel(" - "))
            p_row.addWidget(p2_edit)
            p_row.addWidget(p2_country)
            p_row.addWidget(QLabel(p2_lbl_text))
            
            self.roster_layout.addLayout(p_row)

        # --- Build Match Rows using Grid ---
        self.match_rows_layout.setSpacing(5)
        self.match_rows_layout.setContentsMargins(5, 5, 5, 5)

        for i, match in enumerate(matches):
            base_row = i * 3 # Max 3 players per team
            
            # Match Label (Spans team_size rows)
            match_lbl = QLabel(self.tr("match_n").replace("{n}", str(i+1)))
            match_lbl.setStyleSheet("color: #888; border-right: 1px solid #333; padding-right: 10px; font-weight: bold;")
            match_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.match_rows_layout.addWidget(match_lbl, base_row, 0, team_size, 1)

            def add_player_row(p_idx, col_offset, align_right):
                p_row = base_row + (0 if p_idx in [1,2] else (1 if p_idx in [3,4] else 2))
                p_name = getattr(md, f'player{p_idx}_name', '').strip() or f"P{p_idx}"
                
                # Name Label
                text = f"<b>{p_name}:</b>" if align_right else f"<b>:{p_name}</b>"
                name_lbl = QLabel(text)
                name_lbl.setAlignment((Qt.AlignmentFlag.AlignRight if align_right else Qt.AlignmentFlag.AlignLeft) | Qt.AlignmentFlag.AlignVCenter)
                self._match_player_labels[p_idx].append(name_lbl)
                
                # Leader Combo
                cb = QComboBox()
                cb.addItems(leaders)
                player_key = f'p{p_idx}_leader'
                cb.setCurrentText(match.get(player_key, 'Anders'))
                cb.currentTextChanged.connect(lambda t, idx=i, pk=player_key: md.set_match_leader(idx, pk, t))
                
                if player_key not in self._leader_combos:
                    self._leader_combos[player_key] = []
                self._leader_combos[player_key].append(cb)
                
                if i == 0:
                    cb.currentTextChanged.connect(lambda t, pk=player_key: self._propagate_leader(pk, t))
                
                if align_right:
                    self.match_rows_layout.addWidget(name_lbl, p_row, 1)
                    self.match_rows_layout.addWidget(cb, p_row, 2)
                else:
                    self.match_rows_layout.addWidget(cb, p_row, 4)
                    self.match_rows_layout.addWidget(name_lbl, p_row, 5)

            # T1 Players
            add_player_row(1, 1, True)
            if team_size >= 2: add_player_row(3, 1, True)
            if team_size >= 3: add_player_row(5, 1, True)

            # Winner Slider (Spans team_size rows)
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 2); slider.setPageStep(1); slider.setTickPosition(QSlider.TickPosition.TicksBelow); slider.setTickInterval(1); slider.setFixedWidth(40)
            winner = match.get('winner', 0)
            if winner == 1: slider.setValue(0)
            elif winner == 2: slider.setValue(2)
            else: slider.setValue(1)
            slider.valueChanged.connect(lambda v, idx=i: self.handle_match_slider(idx, v))
            self.match_rows_layout.addWidget(slider, base_row, 3, team_size, 1)

            # T2 Players
            add_player_row(2, 4, False)
            if team_size >= 2: add_player_row(4, 4, False)
            if team_size >= 3: add_player_row(6, 4, False)

            # Separator row (optional)
            if i < len(matches) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.Shape.HLine)
                line.setFrameShadow(QFrame.Shadow.Sunken)
                line.setStyleSheet("background-color: #333;")
                # self.match_rows_layout.addWidget(line, base_row + team_size, 0, 1, 6) # This might mess up grid spacing

        self.match_rows_layout.setColumnStretch(1, 1)
        self.match_rows_layout.setColumnStretch(5, 1)
        self.resize(self.minimumSizeHint())

    def handle_match_slider(self, index, value):
        # Slider: 0=P1, 1=None, 2=P2
        # Data: 1=P1, 0=None, 2=P2
        winner = 0
        if value == 0: winner = 1
        elif value == 2: winner = 2
        
        self.controller.match_data.set_match_winner(index, winner)

    def _propagate_leader(self, player_key, leader_text):
        """When match #1's leader changes, copy to all subsequent matches."""
        combos = self._leader_combos.get(player_key, [])
        # Skip index 0 (it's the source), update index 1+
        for cb in combos[1:]:
            if cb.currentText() != leader_text:
                cb.setCurrentText(leader_text)

    def update_from_model(self, data):
        if int(self.best_of.currentText()) != data.best_of:
            self.best_of.setCurrentText(str(data.best_of))
            
        current_size_idx = data.team_size - 1
        if self.team_size.currentIndex() != current_size_idx:
            self.team_size.setCurrentIndex(current_size_idx)

        self.chk_show_teams.blockSignals(True)
        self.chk_show_teams.setChecked(data.show_team_names)
        self.chk_show_teams.blockSignals(False)
        
        self.chk_show_flags.blockSignals(True)
        self.chk_show_flags.setChecked(data.show_flags)
        self.chk_show_flags.blockSignals(False)

        self.chk_show_game_type.blockSignals(True)
        self.chk_show_game_type.setChecked(data.show_game_type)
        self.chk_show_game_type.blockSignals(False)

        if self.map_combo.currentText() != data.current_map:
            self.map_combo.setCurrentText(data.current_map)

    def check_db_status(self, text, btn):
        """Highlights the button if player exists in DB."""
        if self.player_db.get_player(text):
            btn.setStyleSheet("background-color: #44aa44; font-weight: bold; color: white;")
        else:
            btn.setStyleSheet("")

    def on_click_show_card(self, name, side='left', slot=1):
        """Triggers showing the player card overlay."""
        data = self.player_db.get_player(name)
        if data:
            self.controller.trigger_player_card(data, side, slot)
        else:
            # Optional: Allow showing card with just name?
            # For now, create a dummy obj or warn
            QMessageBox.information(self, "Info", f"El jugador '{name}' no está en la base de datos.")

    def show_team_cards(self, team_idx):
        """
        Triggers cards for all active players in a team.
        team_idx: 1 (Left/Red) or 2 (Right/Blue)
        """
        md = self.controller.match_data
        slots = md.get_slots_for_team(team_idx)
        
        players_to_show = []
        for slot in slots:
            # Determine player based on slot
            # Slot 1: P1, Slot 2: P2, Slot 3: P3, etc.
            # This mapping is implicit in how we set up data
            p_name_attr = f"player{slot}_name"
            p_name = getattr(md, p_name_attr, f"Jugador {slot}")
            
            # Side: Team 1 is Left, Team 2 is Right
            side = 'left' if team_idx == 1 else 'right'
            
            # Fetch data from DB
            p_data = self.player_db.get_player(p_name)
            if not p_data:
                # Fallback if not in DB
                p_data = {'name': p_name, 'main_leader': 'Atriox', 'rank_1v1': 'Unranked'}
            
            players_to_show.append({
                'data': p_data,
                'side': side,
                'slot': slot
            })
            
        if players_to_show:
            self.controller.trigger_player_cards_batch(players_to_show)

    def setup_players_tab(self):
        layout = QHBoxLayout(self.players_tab)
        
        # Left: List
        left_layout = QVBoxLayout()
        self.player_list = QListWidget()
        self.player_list.currentItemChanged.connect(self.load_player_form)
        
        self.lbl_registered_players = QLabel()
        left_layout.addWidget(self.lbl_registered_players)
        left_layout.addWidget(self.player_list)
        layout.addLayout(left_layout, 1)
        
        # Right: Form
        right_layout = QVBoxLayout()
        self.grp_player_data = QGroupBox()
        form_layout = QFormLayout(self.grp_player_data)
        
        self.p_name_edit = QLineEdit()
        self.p_rank1_edit = QLineEdit()
        self.p_mmr1_edit = QLineEdit()
        self.p_rank2_edit = QLineEdit()
        self.p_mmr2_edit = QLineEdit()
        self.p_rank3_edit = QLineEdit()
        self.p_mmr3_edit = QLineEdit()
        self.p_playstyle_edit = QLineEdit()
        self.p_leader_combo = QComboBox()
        
        self.p_leader_combo.addItems(["Unknown"] + LEADERS)
        
        self.lbl_gamertag = QLabel(); form_layout.addRow(self.lbl_gamertag, self.p_name_edit)
        self.lbl_rank1 = QLabel(); form_layout.addRow(self.lbl_rank1, self.p_rank1_edit)
        self.lbl_mmr1 = QLabel(); form_layout.addRow(self.lbl_mmr1, self.p_mmr1_edit)
        self.lbl_rank2 = QLabel(); form_layout.addRow(self.lbl_rank2, self.p_rank2_edit)
        self.lbl_mmr2 = QLabel(); form_layout.addRow(self.lbl_mmr2, self.p_mmr2_edit)
        self.lbl_rank3 = QLabel(); form_layout.addRow(self.lbl_rank3, self.p_rank3_edit)
        self.lbl_mmr3 = QLabel(); form_layout.addRow(self.lbl_mmr3, self.p_mmr3_edit)
        self.lbl_playstyle = QLabel(); form_layout.addRow(self.lbl_playstyle, self.p_playstyle_edit)
        self.lbl_main_leader = QLabel(); form_layout.addRow(self.lbl_main_leader, self.p_leader_combo)
        
        right_layout.addWidget(self.grp_player_data)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_new = QPushButton()
        self.btn_new.clicked.connect(self.new_player_form)
        self.btn_save = QPushButton()
        self.btn_save.clicked.connect(self.save_player_form)
        self.btn_delete = QPushButton()
        self.btn_delete.clicked.connect(self.delete_player)
        
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_delete)
        right_layout.addLayout(btn_layout)
        
        layout.addLayout(right_layout, 2)
        
        self.refresh_player_list()

    def on_disconnect_toggled(self, checked):
        if self.controller and self.controller.match_data:
            self.controller.match_data.disconnection = checked

    def on_mirror_match_toggled(self, checked):
        if self.controller and self.controller.match_data:
            self.controller.match_data.mirror_match = checked

    def refresh_player_list(self):
        current = self.player_list.currentItem()
        curr_text = current.text() if current else None
        
        self.player_list.clear()
        names = self.player_db.get_all_names()
        self.player_list.addItems(names)
        
        if curr_text:
            items = self.player_list.findItems(curr_text, Qt.MatchFlag.MatchExactly)
            if items:
                self.player_list.setCurrentItem(items[0])

    def load_player_form(self, current, previous):
        if not current:
            return
            
        name = current.text()
        data = self.player_db.get_player(name)
        if data:
            self.p_name_edit.setText(data.get('name', name))
            self.p_rank1_edit.setText(data.get('rank_1v1', ''))
            self.p_mmr1_edit.setText(data.get('mmr_1v1', ''))
            self.p_rank2_edit.setText(data.get('rank_2v2', ''))
            self.p_mmr2_edit.setText(data.get('mmr_2v2', ''))
            self.p_rank3_edit.setText(data.get('rank_3v3', ''))
            self.p_mmr3_edit.setText(data.get('mmr_3v3', ''))
            self.p_playstyle_edit.setText(data.get('playstyle', ''))
            
            leader = data.get('main_leader', 'Unknown')
            index = self.p_leader_combo.findText(leader)
            if index >= 0:
                self.p_leader_combo.setCurrentIndex(index)
            else:
                self.p_leader_combo.setCurrentIndex(0)

    def new_player_form(self):
        self.player_list.clearSelection()
        self.p_name_edit.clear()
        self.p_rank1_edit.clear()
        self.p_mmr1_edit.clear()
        self.p_rank2_edit.clear()
        self.p_mmr2_edit.clear()
        self.p_rank3_edit.clear()
        self.p_mmr3_edit.clear()
        self.p_playstyle_edit.clear()
        self.p_leader_combo.setCurrentIndex(0)
        self.p_name_edit.setFocus()

    def save_player_form(self):
        name = self.p_name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, self.tr("error"), self.tr("msg_name_empty"))
            return
            
        data = {
            'name': name,
            'rank_1v1': self.p_rank1_edit.text(),
            'mmr_1v1': self.p_mmr1_edit.text(),
            'rank_2v2': self.p_rank2_edit.text(),
            'mmr_2v2': self.p_mmr2_edit.text(),
            'rank_3v3': self.p_rank3_edit.text(),
            'mmr_3v3': self.p_mmr3_edit.text(),
            'playstyle': self.p_playstyle_edit.text(),
            'main_leader': self.p_leader_combo.currentText()
        }
        
        self.player_db.add_update_player(name, data)
        self.refresh_player_list()
        self._refresh_completers()
        
        # Select the saved item
        items = self.player_list.findItems(name, Qt.MatchFlag.MatchExactly)
        if items:
            self.player_list.setCurrentItem(items[0])

    def delete_player(self):
        current = self.player_list.currentItem()
        if not current:
            return
            
        name = current.text()
        confirm = QMessageBox.question(self, self.tr("confirm"), self.tr("msg_confirm_delete").format(name=name), 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.player_db.delete_player(name)
            self.refresh_player_list()
            self._refresh_completers()
            self.new_player_form()

    def on_disconnect_toggled(self, checked):
        if self.controller and self.controller.match_data:
            self.controller.match_data.disconnection = checked

    def on_mirror_match_toggled(self, checked):
        if self.controller and self.controller.match_data:
            self.controller.match_data.mirror_match = checked

    def _refresh_completers(self):
        """Update all player name completers with the latest DB names."""
        names = self.player_db.get_all_names()
        for c in getattr(self, '_all_completers', []):
            c.setModel(QStringListModel(names))

    def setup_info_tab(self):
        layout = QVBoxLayout(self.info_tab)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Assuming there might be a logo later, for now just text
        logo_label.setText("<h2>Halo Wars 2 Casting Tool</h2>")
        layout.addWidget(logo_label)
        
        version_label = QLabel("<b>Versión:</b> v0.2.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        info_text = QLabel("""
            <p>Herramienta diseñada para casters de Halo Wars 2. Controla overlays en tiempo real para OBS.</p>
            <hr>
            <h3>Créditos</h3>
            <p><b>Desarrollado por:</b> Ivanoides Corporation</p>
            <hr>
            <h3>Enlaces Útiles</h3>
            <ul>
                <li><a href='https://github.com/IvanUlloaMtz'>GitHub del Proyecto</a></li>
                <li><a href='#'>Comunidad de Discord</a></li>
            </ul>
        """)
        info_text.setOpenExternalLinks(True)
        info_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(info_text)
        
        layout.addStretch()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'bg_animated'):
            self.bg_animated.setGeometry(self.centralWidget().rect())

    def toggle_dynamic_bg(self, checked):
        self.controller.config_manager.set("dynamic_bg", checked)
        if hasattr(self, 'bg_animated'):
            self.bg_animated.setVisible(checked)
