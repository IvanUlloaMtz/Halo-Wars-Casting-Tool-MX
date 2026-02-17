from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTabWidget, QSpinBox, 
                             QComboBox, QGroupBox, QFormLayout, QApplication,
                             QCheckBox, QListWidget, QMessageBox, QCompleter,
                             QScrollArea, QSlider)
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QPixmap, QIcon, QColor
import logging
from hwctool.player_db import PlayerDB
from hwctool.view.themes import get_theme, THEMES
from hwctool.matchdata import LEADERS
from hwctool.locale import get_text

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.player_db = PlayerDB()
        self.lang = self.controller.config_manager.get("language", "es")
        self.setWindowTitle(self.tr("window_title"))
        # self.setGeometry(100, 100, 800, 600)
        
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
        
        layout = QVBoxLayout(central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Match Control Tab
        self.match_tab = QWidget()
        self.setup_match_tab()
        self.tabs.addTab(self.match_tab, self.tr("tab_control"))
        
        # Settings Tab
        self.settings_tab = QWidget()
        self.setup_settings_tab()
        self.tabs.addTab(self.settings_tab, self.tr("tab_settings"))

        
        # Players Tab
        self.players_tab = QWidget()
        self.setup_players_tab()
        self.tabs.addTab(self.players_tab, "")
        
        self.retranslate_ui()

    def retranslate_ui(self):
        """Update all UI texts based on current language."""
        self.setWindowTitle(self.tr("window_title"))
        
        # Tabs
        self.tabs.setTabText(0, self.tr("tab_control"))
        self.tabs.setTabText(1, self.tr("tab_settings"))
        self.tabs.setTabText(2, self.tr("tab_players"))
        
        # Match Tab - Static Labels
        self.lbl_team_size.setText(self.tr("team_size"))
        self.lbl_best_of.setText(self.tr("best_of"))
        self.lbl_type.setText(self.tr("type"))
        self.lbl_map.setText(self.tr("map"))
        
        # Match Tab - Buttons/Checks
        self.btn_intro_p1.setText(self.tr("show_intro_t1"))
        self.btn_intro_p2.setText(self.tr("show_intro_t2"))
        self.btn_toggle_score.setText(self.tr("update_score"))
        self.btn_reset.setText(self.tr("reset_overlays"))
        self.mirror_cb.setText(self.tr("mirror_match"))
        self.btn_cards_t1.setText(self.tr("cards_t1"))
        self.btn_cards_t2.setText(self.tr("cards_t2"))
        self.disconnect_cb.setText(self.tr("disconnection"))

        # Settings Tab
        self.btn_copy_intro.setText(self.tr("copy_intro_url"))
        self.btn_copy_score.setText(self.tr("copy_score_url"))
        self.btn_copy_card.setText(self.tr("copy_card_url"))
        self.lbl_urls_obs.setText("URLs OBS:") # Keep hardcoded or add to locale? Leaving hardcoded as I didn't add key.
        
        self.map_group.setTitle(self.tr("map_popup_config"))
        self.map_popup_enabled.setText(self.tr("map_popup_enable"))
        self.lbl_map_enter.setText(self.tr("map_enter"))
        self.lbl_map_visible.setText(self.tr("map_visible"))
        self.lbl_map_exit.setText(self.tr("map_exit"))
        self.lbl_map_hidden.setText(self.tr("map_hidden"))
        
        self.theme_group.setTitle("Apariencia" if self.lang == 'es' else "Appearance") # Fallback or add key
        self.lbl_theme.setText(self.tr("theme"))
        self.lbl_language.setText(self.tr("language"))
        
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
        
        # Refresh dynamic match rows
        self.refresh_match_rows()

    def setup_match_tab(self):
        layout = QVBoxLayout(self.match_tab)

        # --- Match Settings (Top) ---
        match_config_layout = QHBoxLayout()
        
        self.team_size = QComboBox()
        self.team_size.addItems(["1v1", "2v2", "3v3"])
        
        self.best_of = QComboBox()
        self.best_of.addItems([str(i) for i in range(1, 16, 2)]) # 1, 3, 5, ..., 15 
        
        self.game_type = QComboBox()
        self.game_type.addItems(["Deathmatch", "Domination", "Strongholds", "Blitz", "ShowMatch", "Customs", "Mediocres"])
        self.game_type.currentTextChanged.connect(lambda t: setattr(self.controller.match_data, 'game_type', t))

        self.map_select = QComboBox()
        self.map_select.addItems(["Ashes", "Badlands", "Bedrock", "Fissures", "Fort Jordan", "Frontier", "Highway", "Mirage", "Rift", "Sentry", "Vault"])
        self.map_select.currentTextChanged.connect(lambda t: setattr(self.controller.match_data, 'current_map', t))

        self.lbl_team_size = QLabel()
        match_config_layout.addWidget(self.lbl_team_size)
        match_config_layout.addWidget(self.team_size)
        
        self.lbl_best_of = QLabel()
        match_config_layout.addWidget(self.lbl_best_of)
        match_config_layout.addWidget(self.best_of)
        
        self.lbl_type = QLabel()
        match_config_layout.addWidget(self.lbl_type)
        match_config_layout.addWidget(self.game_type)
        
        self.lbl_map = QLabel()
        match_config_layout.addWidget(self.lbl_map)
        match_config_layout.addWidget(self.map_select)
        
        match_config_layout.addStretch()
        layout.addLayout(match_config_layout)
        
        # --- Teams Header ---
        teams_row = QHBoxLayout()
        self.p1_team = QLineEdit(); self.p1_team.setPlaceholderText(self.tr("p1_team_placeholder"))
        self.p1_team.textChanged.connect(lambda t: setattr(self.controller.match_data, 'player1_team', t))
        self.p2_team = QLineEdit(); self.p2_team.setPlaceholderText(self.tr("p2_team_placeholder"))
        self.p2_team.textChanged.connect(lambda t: setattr(self.controller.match_data, 'player2_team', t))
        
        self.show_team_names_cb = QCheckBox(self.tr("show_overlay"))
        self.show_team_names_cb.setChecked(False)
        self.show_team_names_cb.toggled.connect(self.on_show_team_names_toggled)
        
        teams_row.addWidget(self.p1_team)
        teams_row.addWidget(QLabel("  vs  "))
        teams_row.addWidget(self.p2_team)
        teams_row.addWidget(self.show_team_names_cb)
        layout.addLayout(teams_row)

        # --- Match Rows Container ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.match_rows_widget = QWidget()
        self.match_rows_layout = QVBoxLayout(self.match_rows_widget)
        self.match_rows_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.match_rows_widget)
        
        scroll.setMinimumHeight(400)
        layout.addWidget(scroll)
        
        # Connect signals after layout is ready
        self.team_size.currentIndexChanged.connect(self.update_team_size)
        self.best_of.currentTextChanged.connect(lambda t: setattr(self.controller.match_data, 'best_of', int(t)))
        self.best_of.currentTextChanged.connect(self.refresh_match_rows)

        # Initial Draw
        self.controller.match_data.init_matches() 
        self.update_team_size(0) # Default 1v1
        
        # Action Buttons
        actions_layout = QHBoxLayout()
        
        self.btn_intro_p1 = QPushButton()
        self.btn_intro_p1.clicked.connect(self.controller.show_intro_p1)
        actions_layout.addWidget(self.btn_intro_p1)
        
        self.btn_intro_p2 = QPushButton()
        self.btn_intro_p2.clicked.connect(self.controller.show_intro_p2)
        actions_layout.addWidget(self.btn_intro_p2)
        
        self.btn_toggle_score = QPushButton()
        self.btn_toggle_score.clicked.connect(self.controller.toggle_score)
        actions_layout.addWidget(self.btn_toggle_score)
        
        self.btn_reset = QPushButton()
        self.btn_reset.clicked.connect(self.controller.reset_all)
        actions_layout.addWidget(self.btn_reset)


        

        
        # Mirror Match Toggle
        self.mirror_cb = QCheckBox(self.tr("mirror_match"))
        self.mirror_cb.setChecked(False)
        self.mirror_cb.setStyleSheet(
            "QCheckBox { color: #00cccc; font-weight: bold; }"
            "QCheckBox::indicator:checked { background-color: #00cccc; border: 1px solid #00ffff; }"
        )
        self.mirror_cb.toggled.connect(self.on_mirror_match_toggled)
        actions_layout.addWidget(self.mirror_cb)

        # Batch Cards
        actions_layout.addWidget(QLabel("|"))
        self.btn_cards_t1 = QPushButton()
        self.btn_cards_t1.clicked.connect(lambda: self.show_team_cards(1))
        self.btn_cards_t1.setStyleSheet("background-color: #550000; color: white; font-weight: bold;")
        actions_layout.addWidget(self.btn_cards_t1)
        
        self.btn_cards_t2 = QPushButton()
        self.btn_cards_t2.clicked.connect(lambda: self.show_team_cards(2))
        self.btn_cards_t2.setStyleSheet("background-color: #000055; color: white; font-weight: bold;")
        actions_layout.addWidget(self.btn_cards_t2)
        
        # Disconnection Alert Toggle
        actions_layout.addWidget(QLabel("|"))
        self.disconnect_cb = QCheckBox(self.tr("disconnection"))
        self.disconnect_cb.setChecked(False)
        self.disconnect_cb.setStyleSheet(
            "QCheckBox { color: #ffaa00; font-weight: bold; }"
            "QCheckBox::indicator:checked { background-color: #ff4444; border: 1px solid #ff6666; }"
        )
        self.disconnect_cb.toggled.connect(self.on_disconnect_toggled)
        actions_layout.addWidget(self.disconnect_cb)
        
        layout.addLayout(actions_layout)
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
        
        self.lbl_url_obs = QLabel("URLs OBS:") # This one I missed in previous translation too, or used "URLs OBS:". Let's make it localizable.
        # Actually I didn't add "URLs OBS:" to locale. Let's add it to locale later or just keep hardcoded for now if user didn't ask.
        # But wait, I am refactoring for i18n. I should make it self.lbl_urls_obs
        layout.addRow("URLs OBS:", url_layout) # I'll leave it as string literal for now as it wasn't in previous set.
        # Wait, I should do:
        self.lbl_urls_obs = QLabel("URLs OBS:") 
        layout.addRow(self.lbl_urls_obs, url_layout)

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
        
        idx = self.lang_combo.findData(self.lang)
        if idx >= 0: self.lang_combo.setCurrentIndex(idx)
        
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        
        self.lbl_language = QLabel()
        theme_layout.addRow(self.lbl_language, self.lang_combo)

        layout.addRow(self.theme_group)

        layout.addRow(QLabel("Made by Ivanoides Corporation"))

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

    def on_disconnect_toggled(self, checked):
        self.controller.match_data.disconnection = checked

    def on_theme_changed(self, theme_name):
        """Called when theme combo changes. Saves preference and applies."""
        self.controller.config_manager.set("theme", theme_name)
        self.apply_theme(theme_name)

    def on_language_changed(self, index):
        code = self.lang_combo.itemData(index)
        if code != self.lang:
            self.lang = code
            self.controller.config_manager.set("language", code)
            self.retranslate_ui()

    def apply_theme(self, theme_name):
        """Applies the given theme stylesheet to the entire application."""
        qss = get_theme(theme_name)
        QApplication.instance().setStyleSheet(qss)

    def update_team_size(self, index):
        size = index + 1
        self.controller.match_data.team_size = size
        self.refresh_match_rows()

    def refresh_match_rows(self):
        # Clear stale completers
        self._all_completers = []

        # Clear existing rows
        while self.match_rows_layout.count():
            child = self.match_rows_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        md = self.controller.match_data
        matches = getattr(md, 'matches', [])
        leaders = LEADERS
        team_size = md.team_size

        # === Player header: names + colors (shown once) ===
        player_pairs = [
            (1, 2, '_player1_name', self.tr("player_n").format(n=1), 'player1_name', 'player1_color', self.RED_TEAM_COLORS,
                    '_player2_name', self.tr("player_n").format(n=2), 'player2_name', 'player2_color', self.BLUE_TEAM_COLORS, 0),
        ]
        if team_size >= 2:
            player_pairs.append(
                (3, 4, '_player3_name', self.tr("player_n").format(n=3), 'player3_name', 'player3_color', self.RED_TEAM_COLORS,
                        '_player4_name', self.tr("player_n").format(n=4), 'player4_name', 'player4_color', self.BLUE_TEAM_COLORS, 1))
        if team_size >= 3:
            player_pairs.append(
                (5, 6, '_player5_name', self.tr("player_n").format(n=5), 'player5_name', 'player5_color', self.RED_TEAM_COLORS,
                        '_player6_name', self.tr("player_n").format(n=6), 'player6_name', 'player6_color', self.BLUE_TEAM_COLORS, 2))

        for pp in player_pairs:
            (p1_idx, p2_idx, attr1, ph1, prop1, cprop1, ccolors1,
                    attr2, ph2, prop2, cprop2, ccolors2, cidx) = pp
            hdr = QWidget()
            hdr_lay = QHBoxLayout(hdr)
            hdr_lay.setContentsMargins(0, 2, 0, 2)

            # T1 player
            e1 = QLineEdit(getattr(md, attr1, ph1)) # Use current val or placeholder
            # If current val is empty/default, should we sync with new placeholder? 
            # getattr(md, attr1, ph1) uses ph1 as default if attr1 is missing. 
            # But attr1 should exist. 
            # If user has typed something, we keep it. If it was default "Jugador 1", does it update?
            # attr1 is '_player1_name'. Initialize in matchdata uses defaults.
            # If I switch language, the underlying data might still have old default text. 
            # But the Placeholder text is what matters for empty fields.
            e1.setPlaceholderText(ph1)
            e1.textChanged.connect(lambda t, p=prop1: setattr(md, p, t))
            completer1 = QCompleter(self.player_db.get_all_names(), e1)
            completer1.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer1.setFilterMode(Qt.MatchFlag.MatchContains)
            e1.setCompleter(completer1)
            self._all_completers.append(completer1)
            c1 = self._make_color_combo(ccolors1, cprop1, cidx)
            
            # Country P1
            country1 = QComboBox()
            country1.setFixedWidth(120)
            for name, code in self.COUNTRIES.items():
                country1.addItem(name, code)
            
            p1_country_prop = f"player{p1_idx}_country"
            p1_country_code = getattr(md, p1_country_prop, 'mx')
            idx1 = country1.findData(p1_country_code)
            if idx1 >= 0: country1.setCurrentIndex(idx1)
            
            country1.currentIndexChanged.connect(
                lambda idx, c=country1, p=p1_country_prop: setattr(md, p, c.itemData(idx))
            )

            hdr_lay.addWidget(e1)
            hdr_lay.addWidget(c1)
            hdr_lay.addWidget(country1)

            hdr_lay.addWidget(QLabel("  —  "))

            # T2 player
            e2 = QLineEdit(getattr(md, attr2, ph2))
            e2.setPlaceholderText(ph2)
            e2.textChanged.connect(lambda t, p=prop2: setattr(md, p, t))
            completer2 = QCompleter(self.player_db.get_all_names(), e2)
            completer2.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer2.setFilterMode(Qt.MatchFlag.MatchContains)
            e2.setCompleter(completer2)
            self._all_completers.append(completer2)
            c2 = self._make_color_combo(ccolors2, cprop2, cidx)
            
            # Country P2
            country2 = QComboBox()
            country2.setFixedWidth(120)
            for name, code in self.COUNTRIES.items():
                country2.addItem(name, code)
            
            p2_country_prop = f"player{p2_idx}_country"
            p2_country_code = getattr(md, p2_country_prop, 'mx')
            idx2 = country2.findData(p2_country_code)
            if idx2 >= 0: country2.setCurrentIndex(idx2)

            country2.currentIndexChanged.connect(
                lambda idx, c=country2, p=p2_country_prop: setattr(md, p, c.itemData(idx))
            )
            
            hdr_lay.addWidget(e2)
            hdr_lay.addWidget(c2)
            hdr_lay.addWidget(country2)

            self.match_rows_layout.addWidget(hdr)

        # Separator
        sep = QLabel("─" * 60)
        sep.setStyleSheet("color: gray;")
        self.match_rows_layout.addWidget(sep)

        # Track leader combos per player key for propagation
        self._leader_combos = {}

        # === Game rows: #N [Leader(s)] [slider] [Leader(s)] ===
        for i, match in enumerate(matches):
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 2, 0, 2)
            
            row_layout.addWidget(QLabel(self.tr("match_n").format(n=i+1)))

            # Helper to create a leader combo with propagation
            def make_leader_combo(match_idx, player_key, default, layout_ref):
                cb = QComboBox()
                cb.addItems(leaders)
                cb.setCurrentText(match.get(player_key, default))
                cb.currentTextChanged.connect(lambda t, idx=match_idx, pk=player_key: md.set_match_leader(idx, pk, t))
                
                if player_key not in self._leader_combos:
                    self._leader_combos[player_key] = []
                self._leader_combos[player_key].append(cb)
                
                if match_idx == 0:
                    cb.currentTextChanged.connect(lambda t, pk=player_key: self._propagate_leader(pk, t))
                
                layout_ref.addWidget(cb)
                return cb

            # T1 Leaders
            row_layout.addWidget(QLabel(self.tr("p_n").format(n=1)))
            make_leader_combo(i, 'p1_leader', 'Atriox', row_layout)
            if team_size >= 2:
                row_layout.addWidget(QLabel(self.tr("p_n").format(n=3)))
                make_leader_combo(i, 'p3_leader', 'Anders', row_layout)
            if team_size >= 3:
                row_layout.addWidget(QLabel(self.tr("p_n").format(n=5)))
                make_leader_combo(i, 'p5_leader', 'Forge', row_layout)

            # Slider
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 2)
            slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            slider.setTickInterval(1)
            slider.setFixedWidth(50)
            winner = match.get('winner', 0)
            if winner == 1: slider.setValue(0)
            elif winner == 2: slider.setValue(2)
            else: slider.setValue(1)
            slider.valueChanged.connect(lambda v, idx=i: self.handle_match_slider(idx, v))
            row_layout.addWidget(slider)

            # T2 Leaders
            row_layout.addWidget(QLabel(self.tr("p_n").format(n=2)))
            make_leader_combo(i, 'p2_leader', 'Captain Cutter', row_layout)
            if team_size >= 2:
                row_layout.addWidget(QLabel("J4:"))
                make_leader_combo(i, 'p4_leader', 'Decimus', row_layout)
            if team_size >= 3:
                row_layout.addWidget(QLabel("J6:"))
                make_leader_combo(i, 'p6_leader', 'Pavium', row_layout)

            self.match_rows_layout.addWidget(row_widget)
        
        # Adjust window size to fit new content
        # self.adjustSize() 
        # Actually, let's try resizing to minimum hint
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
        """Update UI elements with data from model."""
        if self.p1_team.text() != data.player1_team: self.p1_team.setText(data.player1_team)
        if self.p2_team.text() != data.player2_team: self.p2_team.setText(data.player2_team)
        
        if int(self.best_of.currentText()) != data.best_of:
            self.best_of.setCurrentText(str(data.best_of))

        if self.game_type.currentText() != data.game_type:
            self.game_type.setCurrentText(data.game_type)
            
        current_size_idx = data.team_size - 1
        if self.team_size.currentIndex() != current_size_idx:
            self.team_size.setCurrentIndex(current_size_idx)

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
