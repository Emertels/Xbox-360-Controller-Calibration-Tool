"""
Internationalization (i18n) Module — 10 Languages Edition
==========================================================
Full multilingual support for the Xbox 360 Controller Calibration Tool.
Supported Languages:
  1. pt  — Português (Brasil)
  2. en  — English
  3. es  — Español
  4. fr  — Français
  5. de  — Deutsch
  6. it  — Italiano
  7. ja  — 日本語 (Japanese)
  8. zh  — 简体中文 (Simplified Chinese)
  9. ru  — Русский (Russian)
 10. ko  — 한국어 (Korean)

Author: Emerson Teles (projeto criado com auxilio do Antigravity)
License: MIT
"""

from __future__ import annotations

_current_lang = "pt"

LANGUAGES = [
    ("pt", "🇧🇷 Português"),
    ("en", "🇺🇸 English"),
    ("es", "🇪🇸 Español"),
    ("fr", "🇫🇷 Français"),
    ("de", "🇩🇪 Deutsch"),
    ("it", "🇮🇹 Italiano"),
    ("ja", "🇯🇵 日本語"),
    ("zh", "🇨🇳 简体中文"),
    ("ru", "🇷🇺 Русский"),
    ("ko", "🇰🇷 한국어"),
]

STRINGS: dict[str, dict[str, str]] = {
    # ---- Window / Header / Status -------------------------------------------
    "app_title": {
        "pt": "Xbox 360 — Calibração de Analógicos v1.0.0",
        "en": "Xbox 360 — Analog Stick Calibration Tool v1.0.0",
        "es": "Xbox 360 — Calibración de Analógicos v1.0.0",
        "fr": "Xbox 360 — Étalonnage des Sticks Analogiques v1.0.0",
        "de": "Xbox 360 — Analogstick-Kalibrierung v1.0.0",
        "it": "Xbox 360 — Calibrazione Levette Analogiche v1.0.0",
        "ja": "Xbox 360 — アナログスティック調整ツール v1.0.0",
        "zh": "Xbox 360 — 摇杆校准工具 v1.0.0",
        "ru": "Xbox 360 — Калибровка стиков v1.0.0",
        "ko": "Xbox 360 — 아날로그 스틱 보정 도구 v1.0.0",
    },
    "searching": {
        "pt": "🔍 Procurando controle Xbox 360...",
        "en": "🔍 Searching for Xbox 360 controller...",
        "es": "🔍 Buscando mando Xbox 360...",
        "fr": "🔍 Recherche de manette Xbox 360...",
        "de": "🔍 Suche nach Xbox 360 Controller...",
        "it": "🔍 Ricerca controller Xbox 360...",
        "ja": "🔍 Xbox 360 コントローラーを検索中...",
        "zh": "🔍 正在搜索 Xbox 360 控制器...",
        "ru": "🔍 Поиск контроллера Xbox 360...",
        "ko": "🔍 Xbox 360 컨트롤러 검색 중...",
    },
    "connected": {
        "pt": "✅ Controle conectado — Jogador {n}",
        "en": "✅ Controller connected — Player {n}",
        "es": "✅ Mando conectado — Jugador {n}",
        "fr": "✅ Manette connectée — Joueur {n}",
        "de": "✅ Controller verbunden — Spieler {n}",
        "it": "✅ Controller connesso — Giocatore {n}",
        "ja": "✅ コントローラー接続中 — プレイヤー {n}",
        "zh": "✅ 已连接控制器 — 玩家 {n}",
        "ru": "✅ Контроллер подключен — Игрок {n}",
        "ko": "✅ 컨트롤러 연결됨 — 플레이어 {n}",
    },
    "not_connected": {
        "pt": "❌ Nenhum controle detectado. Conecte o receptor e clique em Reconectar.",
        "en": "❌ No controller detected. Connect receiver and click Reconnect.",
        "es": "❌ No se detectó ningún mando. Conecte el receptor y pulse Reconectar.",
        "fr": "❌ Aucune manette détectée. Branchez le récepteur et cliquez sur Reconnecter.",
        "de": "❌ Kein Controller erkannt. Empfänger anschließen und auf Wiederverbinden klicken.",
        "it": "❌ Nessun controller rilevato. Collega il ricevitore e clicca Riconnetti.",
        "ja": "❌ コントローラーが見つかりません。受信機を接続し再接続をクリックしてください。",
        "zh": "❌ 未检测到控制器。请连接接收器并点击重新连接。",
        "ru": "❌ Контроллер не обнаружен. Подключите приемник и нажмите Переподключить.",
        "ko": "❌ 컨트롤러가 감지되지 않았습니다. 수신기를 연결하고 재연결을 누르세요.",
    },
    "lang_menu_label": {
        "pt": "🌐 Idioma",
        "en": "🌐 Language",
        "es": "🌐 Idioma",
        "fr": "🌐 Langue",
        "de": "🌐 Sprache",
        "it": "🌐 Lingua",
        "ja": "🌐 言語",
        "zh": "🌐 语言",
        "ru": "🌐 Язык",
        "ko": "🌐 언어",
    },

    # ---- Stick canvases ----------------------------------------------------
    "left_stick": {
        "pt": "Analógico Esquerdo (LS)",
        "en": "Left Stick (LS)",
        "es": "Stick Izquierdo (LS)",
        "fr": "Stick Gauche (LS)",
        "de": "Linker Stick (LS)",
        "it": "Levetta Sinistra (LS)",
        "ja": "左スティック (LS)",
        "zh": "左摇杆 (LS)",
        "ru": "Левый стик (LS)",
        "ko": "왼쪽 스틱 (LS)",
    },
    "right_stick": {
        "pt": "Analógico Direito (RS)",
        "en": "Right Stick (RS)",
        "es": "Stick Derecho (RS)",
        "fr": "Stick Droit (RS)",
        "de": "Rechter Stick (RS)",
        "it": "Levetta Destra (RS)",
        "ja": "右スティック (RS)",
        "zh": "右摇杆 (RS)",
        "ru": "Правый стик (RS)",
        "ko": "오른쪽 스틱 (RS)",
    },
    "raw_prefix": {
        "pt": "Bruto", "en": "Raw", "es": "Bruto", "fr": "Brut", "de": "Roh",
        "it": "Grezzo", "ja": "生値", "zh": "原始", "ru": "Сырой", "ko": "원시값",
    },
    "cal_prefix": {
        "pt": "Calib", "en": "Cal", "es": "Calib", "fr": "Étal", "de": "Kalib",
        "it": "Calib", "ja": "補正", "zh": "校准", "ru": "Калиб", "ko": "보정",
    },
    "mag_prefix": {
        "pt": "Magnitude", "en": "Magnitude", "es": "Magnitud", "fr": "Amplitude", "de": "Auslenkung",
        "it": "Magnitudo", "ja": "変位量", "zh": "幅度", "ru": "Амплитуда", "ko": "변위",
    },

    # ---- Panels ------------------------------------------------------------
    "buttons": {
        "pt": "🎮 Botões do Controle", "en": "🎮 Controller Buttons", "es": "🎮 Botones del Mando", "fr": "🎮 Boutons de la Manette",
        "de": "🎮 Controller-Tasten", "it": "🎮 Pulsanti del Controller", "ja": "🎮 コントローラーボタン", "zh": "🎮 手柄按键与扳机",
        "ru": "🎮 Кнопки контроллера", "ko": "🎮 컨트롤러 버튼",
    },
    "triggers": {
        "pt": "Gatilhos Analógicos", "en": "Analog Triggers", "es": "Gatillos Analógicos", "fr": "Gâchettes Analogiques",
        "de": "Analoge Trigger", "it": "Grilletti Analogici", "ja": "アナログトリガー", "zh": "模拟扳机",
        "ru": "Аналоговые триггеры", "ko": "아날로그 트리거",
    },

    # ---- Notebook Tabs -----------------------------------------------------
    "tab_sticks": {
        "pt": " 🎮 Calibração dos Analógicos ", "en": " 🎮 Stick Calibration ", "es": " 🎮 Calibración de Sticks ",
        "fr": " 🎮 Étalonnage des Sticks ", "de": " 🎮 Stick-Kalibrierung ", "it": " 🎮 Calibrazione Levette ",
        "ja": " 🎮 スティック調整 ", "zh": " 🎮 摇杆校准 ", "ru": " 🎮 Калибровка стиков ", "ko": " 🎮 스틱 보정 ",
    },
    "tab_triggers": {
        "pt": " 🎯 Gatilhos & Curvas ", "en": " 🎯 Triggers & Curves ", "es": " 🎯 Gatillos y Curvas ",
        "fr": " 🎯 Gâchettes & Courbes ", "de": " 🎯 Trigger & Kurven ", "it": " 🎯 Grilletti & Curve ",
        "ja": " 🎯 トリガー & 応答曲線 ", "zh": " 🎯 扳机与响应曲线 ", "ru": " 🎯 Триггеры и кривые ", "ko": " 🎯 트리거 및 응답곡선 ",
    },
    "tab_help": {
        "pt": " 💡 Dicas & Hall Effect ", "en": " 💡 Tips & Hall Effect ", "es": " 💡 Consejos y Hall Effect ",
        "fr": " 💡 Astuces & Effet Hall ", "de": " 💡 Tipps & Hall-Effekt ", "it": " 💡 Suggerimenti & Effetto Hall ",
        "ja": " 💡 ヒント & ホール効果 ", "zh": " 💡 技巧与霍尔效应 ", "ru": " 💡 Советы и датчики Холла ", "ko": " 💡 팁 및 홀 효과 ",
    },
    "tab_virtual": {
        "pt": " 🕹️ Controle Virtual & Jogos ", "en": " 🕹️ Virtual Gamepad & Games ", "es": " 🕹️ Mando Virtual y Juegos ",
        "fr": " 🕹️ Manette Virtuelle & Jeux ", "de": " 🕹️ Virtueller Controller & Spiele ", "it": " 🕹️ Controller Virtuale & Giochi ",
        "ja": " 🕹️ 仮想ゲームパッド & ゲーム ", "zh": " 🕹️ 虚拟手柄与游戏 ", "ru": " 🕹️ Виртуальный геймпад и игры ", "ko": " 🕹️ 가상 게임패드 및 게임 ",
    },

    # ---- Calibration controls ----------------------------------------------
    "cal_left_title": {
        "pt": "Calibração — Analógico Esquerdo", "en": "Left Stick Calibration", "es": "Calibración — Stick Izquierdo",
        "fr": "Étalonnage — Stick Gauche", "de": "Kalibrierung — Linker Stick", "it": "Calibrazione — Levetta Sinistra",
        "ja": "左スティック調整", "zh": "左摇杆校准", "ru": "Калибровка — Левый стик", "ko": "왼쪽 스틱 보정",
    },
    "cal_right_title": {
        "pt": "Calibração — Analógico Direito", "en": "Right Stick Calibration", "es": "Calibración — Stick Derecho",
        "fr": "Étalonnage — Stick Droit", "de": "Kalibrierung — Rechter Stick", "it": "Calibrazione — Levetta Destra",
        "ja": "右スティック調整", "zh": "右摇杆校准", "ru": "Калибровка — Правый стик", "ko": "오른쪽 스틱 보정",
    },
    "auto_center": {
        "pt": "⊕ Auto-Center", "en": "⊕ Auto-Center", "es": "⊕ Auto-Centro", "fr": "⊕ Auto-Centre", "de": "⊕ Auto-Zentrierung",
        "it": "⊕ Auto-Centro", "ja": "⊕ 自動中央補正", "zh": "⊕ 自动归中", "ru": "⊕ Авто-центр", "ko": "⊕ 자동 중앙 정렬",
    },
    "auto_range": {
        "pt": "◎ Auto-Range", "en": "◎ Auto-Range", "es": "◎ Auto-Rango", "fr": "◎ Auto-Portée", "de": "◎ Auto-Bereich",
        "it": "◎ Auto-Raggio", "ja": "◎ 自動範囲補正", "zh": "◎ 自动范围", "ru": "◎ Авто-диапазон", "ko": "◎ 자동 범위 감지",
    },
    "reset": {
        "pt": "↺ Resetar", "en": "↺ Reset", "es": "↺ Restablecer", "fr": "↺ Réinitialiser", "de": "↺ Zurücksetzen",
        "it": "↺ Ripristina", "ja": "↺ リセット", "zh": "↺ 重置", "ru": "↺ Сброс", "ko": "↺ 초기화",
    },
    "center": {
        "pt": "Centro", "en": "Center", "es": "Centro", "fr": "Centre", "de": "Mitte",
        "it": "Centro", "ja": "中心", "zh": "中心", "ru": "Центр", "ko": "중심",
    },
    "deadzone": {
        "pt": "Deadzone Radial:", "en": "Radial Deadzone:", "es": "Zona Muerta Radial:", "fr": "Zone Morte Radiale :",
        "de": "Radiale Totzone:", "it": "Zona Morta Radiale:", "ja": "円形デッドゾーン:", "zh": "径向死区:",
        "ru": "Радиальная мертвая зона:", "ko": "반경 데드존:",
    },
    "range": {
        "pt": "Alcance (Range):", "en": "Stick Range:", "es": "Alcance (Range):", "fr": "Portée (Range) :",
        "de": "Reichweite (Range):", "it": "Portata (Range):", "ja": "最大可動範囲:", "zh": "最大量程 (Range):",
        "ru": "Размах (Диапазон):", "ko": "최대 범위 (Range):",
    },
    "noise_filter": {
        "pt": "Filtro Anti-Ruído:", "en": "Noise Filter:", "es": "Filtro Anti-Ruido:", "fr": "Filtre Anti-Bruit :",
        "de": "Rauschfilter:", "it": "Filtro Anti-Rumore:", "ja": "ノイズ低減フィルタ:", "zh": "平滑抗噪滤波:",
        "ru": "Фильтр шума:", "ko": "노이즈 필터:",
    },
    "anti_jitter": {
        "pt": "Filtro Anti-Jitter:", "en": "Anti-Jitter:", "es": "Filtro Anti-Jitter:", "fr": "Filtre Anti-Jitter :",
        "de": "Anti-Zitterfilter:", "it": "Filtro Anti-Jitter:", "ja": "ジッター除去:", "zh": "抗抖动阈值:",
        "ru": "Подавление дрожания:", "ko": "안티 지터:",
    },
    "response_curve": {
        "pt": "Curva de Resposta:", "en": "Response Curve:", "es": "Curva de Respuesta:", "fr": "Courbe de Réponse :",
        "de": "Reaktionskurve:", "it": "Curva di Risposta:", "ja": "応答曲線:", "zh": "响应曲线:",
        "ru": "Кривая отклика:", "ko": "응답 곡선:",
    },
    "invert_x": {
        "pt": "Inverter Eixo X", "en": "Invert X Axis", "es": "Invertir Eje X", "fr": "Inverser Axe X",
        "de": "X-Achse invertieren", "it": "Inverti Asse X", "ja": "X軸を反転", "zh": "反转 X 轴",
        "ru": "Инвертировать ось X", "ko": "X축 반전",
    },
    "invert_y": {
        "pt": "Inverter Eixo Y", "en": "Invert Y Axis", "es": "Invertir Eje Y", "fr": "Inverser Axe Y",
        "de": "Y-Achse invertieren", "it": "Inverti Asse Y", "ja": "Y軸を反転", "zh": "反转 Y 轴",
        "ru": "Инвертировать ось Y", "ko": "Y축 반전",
    },
    "dont_touch": {
        "pt": "⏳ SOLTE O STICK...", "en": "⏳ RELEASE STICK...", "es": "⏳ SUELTE EL STICK...", "fr": "⏳ RELÂCHEZ LE STICK...",
        "de": "⏳ STICK LOSLASSEN...", "it": "⏳ RILASCIA LA LEVETTA...", "ja": "⏳ 触れずに静止...", "zh": "⏳ 请松开摇杆...",
        "ru": "⏳ ОТПУСТИТЕ СТИК...", "ko": "⏳ 스틱을 놓으세요...",
    },
    "spin_stick": {
        "pt": "🌀 GIRE EM CÍRCULOS", "en": "🌀 SPIN IN CIRCLES", "es": "🌀 GIRE EN CÍRCULOS", "fr": "🌀 TOURNEZ EN ROND",
        "de": "🌀 IM KREIS DREHEN", "it": "🌀 RUOTA IN TONDO", "ja": "🌀 円を描くように回転", "zh": "🌀 沿边缘画圈旋转",
        "ru": "🌀 ВРАЩАЙТЕ ПО КРУГУ", "ko": "🌀 끝까지 원을 그리세요",
    },

    # ---- Response curves ---------------------------------------------------
    "curve_linear": {
        "pt": "Linear (1:1 — Direto)", "en": "Linear (1:1 — Direct)", "es": "Lineal (1:1 — Directo)",
        "fr": "Linéaire (1:1 — Direct)", "de": "Linear (1:1 — Direkt)", "it": "Lineare (1:1 — Diretto)",
        "ja": "リニア (1:1 — 等倍)", "zh": "线性 (1:1 — 直出)", "ru": "Линейная (1:1 — Прямой)", "ko": "선형 (1:1 — 기본)",
    },
    "curve_smooth": {
        "pt": "Suave (Mira Precisa / FPS)", "en": "Smooth (Precise Aim / FPS)", "es": "Suave (Puntería Precisa / FPS)",
        "fr": "Fluide (Visée Précise / FPS)", "de": "Sanft (Präzises Zielen / FPS)", "it": "Morbida (Mira Precisa / FPS)",
        "ja": "スムーズ (精密照準 / FPS向け)", "zh": "平滑 (精细瞄准 / FPS)", "ru": "Плавная (Точный прицел / FPS)", "ko": "부드러움 (정밀 조준 / FPS)",
    },
    "curve_aggressive": {
        "pt": "Agressivo (Corrida / Rápido)", "en": "Aggressive (Racing / Fast)", "es": "Agresivo (Carreras / Rápido)",
        "fr": "Agressif (Course / Rapide)", "de": "Aggressiv (Rennen / Schnell)", "it": "Aggressiva (Corsa / Veloce)",
        "ja": "アグレッシブ (レース / 高速)", "zh": "激进 (赛车 / 极速响应)", "ru": "Агрессивная (Гонки / Быстрый)", "ko": "민첩 (레이싱 / 빠른 반응)",
    },
    "curve_extra_smooth": {
        "pt": "Extra Suave (Modo Sniper)", "en": "Extra Smooth (Sniper Mode)", "es": "Extra Suave (Modo Francotirador)",
        "fr": "Ultra Fluide (Mode Sniper)", "de": "Extra Sanft (Scharfschütze)", "it": "Ultra Morbida (Modalità Cecchino)",
        "ja": "超スムーズ (スナイパーモード)", "zh": "极度平滑 (狙击微调模式)", "ru": "Сверхплавная (Режим снайпера)", "ko": "초정밀 (스나이퍼 모드)",
    },

    # ---- Trigger deadzone --------------------------------------------------
    "trig_dz_title": {
        "pt": "Ajuste de Deadzone dos Gatilhos", "en": "Trigger Deadzone Settings", "es": "Ajuste de Zona Muerta de Gatillos",
        "fr": "Réglage de Zone Morte des Gâchettes", "de": "Trigger-Totzonen-Einstellung", "it": "Regolazione Zona Morta Grilletti",
        "ja": "トリガーデッドゾーン調整", "zh": "扳机死区设置", "ru": "Настройка мертвой зоны триггеров", "ko": "트리거 데드존 설정",
    },
    "trig_dz_lt": {
        "pt": "Gatilho Esquerdo (LT):", "en": "Left Trigger (LT):", "es": "Gatillo Izquierdo (LT):", "fr": "Gâchette Gauche (LT) :",
        "de": "Linker Trigger (LT):", "it": "Grilletto Sinistro (LT):", "ja": "左トリガー (LT):", "zh": "左扳机 (LT):",
        "ru": "Левый триггер (LT):", "ko": "왼쪽 트리거 (LT):",
    },
    "trig_dz_rt": {
        "pt": "Gatilho Direito (RT):", "en": "Right Trigger (RT):", "es": "Gatillo Derecho (RT):", "fr": "Gâchette Droite (RT) :",
        "de": "Rechter Trigger (RT):", "it": "Grilletto Destro (RT):", "ja": "右トリガー (RT):", "zh": "右扳机 (RT):",
        "ru": "Правый триггер (RT):", "ko": "오른쪽 트리거 (RT):",
    },
    "trig_dz_desc": {
        "pt": "Define o ponto inicial de resposta dos gatilhos para evitar disparos acidentais.",
        "en": "Sets the initial trigger threshold to prevent accidental fire or acceleration.",
        "es": "Define el umbral inicial de los gatillos para evitar disparos accidentales.",
        "fr": "Définit le seuil initial des gâchettes pour éviter les tirs accidentels.",
        "de": "Legt den Schwellenwert der Trigger fest, um versehentliches Auslösen zu verhindern.",
        "it": "Imposta la soglia iniziale dei grilletti per evitare pressioni accidentali.",
        "ja": "誤入力を防止するため、トリガーが反応し始める初期しきい値を設定します。",
        "zh": "设置扳机起始响应死区，有效防止手指搭放时的误触走火或误加速。",
        "ru": "Задает начальный порог срабатывания триггеров для предотвращения случайных нажатий.",
        "ko": "트리거가 작동하기 시작하는 초기 임계값을 설정하여 실수로 눌리는 현상을 방지합니다.",
    },

    # ---- Actions & Bottom bar ----------------------------------------------
    "power_off_btn": {
        "pt": "⏻ Desligar Controle", "en": "⏻ Turn Off Controller", "es": "⏻ Apagar Mando", "fr": "⏻ Éteindre la Manette",
        "de": "⏻ Controller ausschalten", "it": "⏻ Spegni Controller", "ja": "⏻ 電源オフ", "zh": "⏻ 关闭手柄电源",
        "ru": "⏻ Выключить геймпад", "ko": "⏻ 컨트롤러 끄기",
    },
    "power_off_success": {
        "pt": "Comando de desligamento enviado ao controle sem fio.",
        "en": "Power-off signal sent to wireless controller.",
        "es": "Señal de apagado enviada al mando inalámbrico.",
        "fr": "Signal d'extinction envoyé à la manette sans fil.",
        "de": "Ausschaltsignal an Wireless-Controller gesendet.",
        "it": "Segnale di spegnimento inviato al controller wireless.",
        "ja": "ワイヤレスコントローラーに電源オフ信号を送信しました。",
        "zh": "已向无线手柄发送关机信号。",
        "ru": "Сигнал выключения отправлен на беспроводной геймпад.",
        "ko": "무선 컨트롤러에 전원 종료 신호를 전송했습니다.",
    },
    "activate_virtual": {
        "pt": "▶ Ativar Controle Virtual", "en": "▶ Activate Virtual Gamepad", "es": "▶ Activar Mando Virtual",
        "fr": "▶ Activer Manette Virtuelle", "de": "▶ Virtuellen Controller aktivieren", "it": "▶ Attiva Controller Virtuale",
        "ja": "▶ 仮想ゲームパッド有効化", "zh": "▶ 启用虚拟手柄", "ru": "▶ Включить виртуальный геймпад", "ko": "▶ 가상 게임패드 활성화",
    },
    "deactivate_virtual": {
        "pt": "⏹ Desativar Virtual", "en": "⏹ Deactivate Virtual", "es": "⏹ Desactivar Virtual",
        "fr": "⏹ Désactiver Virtuel", "de": "⏹ Virtuellen deaktivieren", "it": "⏹ Disattiva Virtuale",
        "ja": "⏹ 仮想パッド無効化", "zh": "⏹ 停用虚拟手柄", "ru": "⏹ Отключить виртуальный", "ko": "⏹ 가상 패드 비활성화",
    },
    "install_vgamepad": {
        "pt": "⚠ Instalar vgamepad (.bat)", "en": "⚠ Install vgamepad (.bat)", "es": "⚠ Instalar vgamepad (.bat)",
        "fr": "⚠ Installer vgamepad (.bat)", "de": "⚠ vgamepad installieren (.bat)", "it": "⚠ Installa vgamepad (.bat)",
        "ja": "⚠ vgamepadをインストール (.bat)", "zh": "⚠ 安装 vgamepad (.bat)", "ru": "⚠ Установить vgamepad (.bat)", "ko": "⚠ vgamepad 설치 (.bat)",
    },
    "reconnect": {
        "pt": "🔄 Reconectar", "en": "🔄 Reconnect", "es": "🔄 Reconectar", "fr": "🔄 Reconnecter",
        "de": "🔄 Wiederverbinden", "it": "🔄 Riconnetti", "ja": "🔄 再接続", "zh": "🔄 重新连接",
        "ru": "🔄 Переподключить", "ko": "🔄 재연결",
    },
    "save": {
        "pt": "💾 Salvar Perfil", "en": "💾 Save Profile", "es": "💾 Guardar Perfil", "fr": "💾 Enregistrer Profil",
        "de": "💾 Profil speichern", "it": "💾 Salva Profilo", "ja": "💾 プロファイル保存", "zh": "💾 保存配置",
        "ru": "💾 Сохранить профиль", "ko": "💾 프로필 저장",
    },
    "load": {
        "pt": "📂 Carregar Perfil", "en": "📂 Load Profile", "es": "📂 Cargar Perfil", "fr": "📂 Charger Profil",
        "de": "📂 Profil laden", "it": "📂 Carica Profilo", "ja": "📂 プロファイル読込", "zh": "📂 加载配置",
        "ru": "📂 Загрузить профиль", "ko": "📂 프로필 불러오기",
    },

    # ---- Status messages ---------------------------------------------------
    "virtual_active": {
        "pt": "✅ VIRTUAL ATIVO — Jogos agora leem os analógicos calibrados!",
        "en": "✅ VIRTUAL ACTIVE — Games now receive calibrated stick inputs!",
        "es": "✅ VIRTUAL ACTIVO — ¡Los juegos reciben los analógicos calibrados!",
        "fr": "✅ VIRTUEL ACTIF — Les jeux reçoivent les données étalonnées !",
        "de": "✅ VIRTUELL AKTIV — Spiele empfangen kalibrierte Stick-Eingaben!",
        "it": "✅ VIRTUALE ATTIVO — I giochi ora leggono le levette calibrate!",
        "ja": "✅ 仮想パッド稼働中 — ゲームに補正済み入力が反映されます！",
        "zh": "✅ 虚拟手柄已激活 — 游戏现已获得完美校准的摇杆输入！",
        "ru": "✅ ВИРТУАЛЬНЫЙ АКТИВЕН — Игры получают откалиброванные стики!",
        "ko": "✅ 가상 패드 작동 중 — 게임에서 보정된 스틱 입력을 수신합니다!",
    },
    "virtual_off": {
        "pt": "Controle virtual desativado.",
        "en": "Virtual gamepad deactivated.",
        "es": "Mando virtual desactivado.",
        "fr": "Manette virtuelle désactivée.",
        "de": "Virtueller Controller deaktiviert.",
        "it": "Controller virtuale disattivato.",
        "ja": "仮想ゲームパッドを停止しました。",
        "zh": "虚拟手柄已停用。",
        "ru": "Виртуальный геймпад отключен.",
        "ko": "가상 게임패드가 비활성화되었습니다.",
    },
    "saved": {
        "pt": "✅ Perfil salvo com sucesso: {f}",
        "en": "✅ Profile saved successfully: {f}",
        "es": "✅ Perfil guardado con éxito: {f}",
        "fr": "✅ Profil enregistré avec succès : {f}",
        "de": "✅ Profil erfolgreich gespeichert: {f}",
        "it": "✅ Profilo salvato con successo: {f}",
        "ja": "✅ プロファイルを保存しました: {f}",
        "zh": "✅ 配置文件保存成功: {f}",
        "ru": "✅ Профиль успешно сохранен: {f}",
        "ko": "✅ 프로필이 성공적으로 저장되었습니다: {f}",
    },
    "loaded": {
        "pt": "✅ Perfil carregado com sucesso: {f}",
        "en": "✅ Profile loaded successfully: {f}",
        "es": "✅ Perfil cargado con éxito: {f}",
        "fr": "✅ Profil chargé avec succès : {f}",
        "de": "✅ Profil erfolgreich geladen: {f}",
        "it": "✅ Profilo caricato con successo: {f}",
        "ja": "✅ プロファイルを読み込みました: {f}",
        "zh": "✅ 配置文件加载成功: {f}",
        "ru": "✅ Профиль успешно загружен: {f}",
        "ko": "✅ 프로필을 성공적으로 불러왔습니다: {f}",
    },
    "save_title": {
        "pt": "Salvar Perfil de Calibração", "en": "Save Calibration Profile", "es": "Guardar Perfil de Calibración",
        "fr": "Enregistrer le Profil d'Étalonnage", "de": "Kalibrierungsprofil speichern", "it": "Salva Profilo di Calibrazione",
        "ja": "調整プロファイルの保存", "zh": "保存校准配置文件", "ru": "Сохранить профиль калибровки", "ko": "보정 프로필 저장",
    },
    "load_title": {
        "pt": "Carregar Perfil de Calibração", "en": "Load Calibration Profile", "es": "Cargar Perfil de Calibración",
        "fr": "Charger le Profil d'Étalonnage", "de": "Kalibrierungsprofil laden", "it": "Carica Profilo di Calibrazione",
        "ja": "調整プロファイルの読込", "zh": "加载校准配置文件", "ru": "Загрузить профиль калибровки", "ko": "보정 프로필 불러오기",
    },

    # ---- Error messages ----------------------------------------------------
    "err_vgamepad": {
        "pt": "A biblioteca 'vgamepad' não foi encontrada.\n\nPara instalar com 1 clique:\nExecute o arquivo INSTALAR_DEPENDENCIAS.bat\n\nDepois feche e reabra esta ferramenta.",
        "en": "The 'vgamepad' library was not found.\n\nTo install with 1 click:\nRun INSTALAR_DEPENDENCIAS.bat\n\nThen restart this tool.",
        "es": "No se encontró la librería 'vgamepad'.\n\nEjecute INSTALAR_DEPENDENCIAS.bat y reinicie la herramienta.",
        "fr": "La bibliothèque 'vgamepad' est introuvable.\n\nLancez INSTALAR_DEPENDENCIAS.bat puis redémarrez l'outil.",
        "de": "Die Bibliothek 'vgamepad' wurde nicht gefunden.\n\nFühren Sie INSTALAR_DEPENDENCIAS.bat aus und starten Sie neu.",
        "it": "La libreria 'vgamepad' non è stata trovata.\n\nEsegui INSTALAR_DEPENDENCIAS.bat e riavvia lo strumento.",
        "ja": "'vgamepad' ライブラリが見つかりません。\n\nINSTALAR_DEPENDENCIAS.bat を実行してツールを再起動してください。",
        "zh": "未找到 'vgamepad' 运行库。\n\n请双击运行 INSTALAR_DEPENDENCIAS.bat，然后重启本工具。",
        "ru": "Библиотека 'vgamepad' не найдена.\n\nЗапустите INSTALAR_DEPENDENCIAS.bat и перезапустите инструмент.",
        "ko": "'vgamepad' 라이브러리를 찾을 수 없습니다.\n\nINSTALAR_DEPENDENCIAS.bat를 실행한 후 도구를 다시 시작하세요.",
    },
    "err_vigem": {
        "pt": "O driver ViGEmBus é necessário para emular o controle virtual.\n\nBaixe o instalador oficial (.msi) em:\nhttps://github.com/nefarius/ViGEmBus/releases\n\nInstale, reinicie o computador se solicitado e tente novamente.",
        "en": "The ViGEmBus driver is required for virtual controller emulation.\n\nDownload official .msi installer from:\nhttps://github.com/nefarius/ViGEmBus/releases\n\nInstall it, reboot if prompted, and try again.",
        "es": "Se requiere el controlador ViGEmBus.\n\nDescargue el instalador en:\nhttps://github.com/nefarius/ViGEmBus/releases",
        "fr": "Le pilote ViGEmBus est requis.\n\nTéléchargez le fichier .msi sur :\nhttps://github.com/nefarius/ViGEmBus/releases",
        "de": "Der ViGEmBus-Treiber ist erforderlich.\n\nOffiziellen .msi-Installer herunterladen unter:\nhttps://github.com/nefarius/ViGEmBus/releases",
        "it": "È necessario il driver ViGEmBus.\n\nScarica l'installer ufficiale da:\nhttps://github.com/nefarius/ViGEmBus/releases",
        "ja": "ViGEmBus ドライバーが必要です。\n\n公式インストーラーをダウンロードしてください:\nhttps://github.com/nefarius/ViGEmBus/releases",
        "zh": "需要安装 ViGEmBus 虚拟手柄驱动。\n\n请前往 GitHub 下载并安装官方 .msi 安装包:\nhttps://github.com/nefarius/ViGEmBus/releases",
        "ru": "Требуется драйвер ViGEmBus.\n\nСкачайте официальный установщик:\nhttps://github.com/nefarius/ViGEmBus/releases",
        "ko": "가상 컨트롤러 에뮬레이션을 위해 ViGEmBus 드라이버가 필요합니다.\n\n공식 설치 파일을 다운로드하세요:\nhttps://github.com/nefarius/ViGEmBus/releases",
    },

    # ---- Help text ---------------------------------------------------------
    "help_quickstart_title": {
        "pt": "🚀 GUIA RÁPIDO DE CALIBRAÇÃO (PASSO A PASSO)",
        "en": "🚀 QUICK CALIBRATION GUIDE (STEP BY STEP)",
        "es": "🚀 GUÍA RÁPIDA DE CALIBRACIÓN (PASO A PASO)",
        "fr": "🚀 GUIDE RAPIDE D'ÉTALONNAGE (PAS À PAS)",
        "de": "🚀 SCHNELLANLEITUNG ZUR KALIBRIERUNG (SCHRITT FÜR SCHRITT)",
        "it": "🚀 GUIDA RAPIDA DI CALIBRAZIONE (PASSO DOPO PASSO)",
        "ja": "🚀 スティック調整クイックスタートガイド",
        "zh": "🚀 快速校准指南 (步骤说明)",
        "ru": "🚀 БЫСТРОЕ РУКОВОДСТВО ПО КАЛИБРОВКЕ",
        "ko": "🚀 빠른 보정 가이드 (단계별 안내)",
    },
    "help_quickstart_body": {
        "pt": (
            "1. CONECTE O CONTROLE: Ligue seu controle Xbox 360 no receptor wireless.\n"
            "2. AUTO-CENTER: Deixe os dois analógicos soltos (repouso total). Clique em 'Auto-Center' em cada um.\n"
            "   - O ponto verde (Cal) se alinhará perfeitamente ao centro (0, 0).\n"
            "3. AUTO-RANGE: Clique em 'Auto-Range' e gire o analógico em círculos completos tocando as bordas por 3s.\n"
            "4. FILTRO ANTI-RUÍDO: Ajuste Anti-Ruído (10-15%) se o sinal trepidar.\n"
            "5. SALVE O PERFIL: Guarde suas calibrações em arquivo JSON.\n"
            "6. JOGAR: Clique em 'Ativar Controle Virtual' para os jogos receberem os analógicos perfeitos!\n"
            "7. DESLIGAR: Clique em '⏻ Desligar Controle' no topo para desligar o controle sem fio instantaneamente."
        ),
        "en": (
            "1. CONNECT CONTROLLER: Turn on your Xbox 360 wireless controller via the PC receiver.\n"
            "2. AUTO-CENTER: Leave both sticks untouched in rest position. Click 'Auto-Center' on each stick.\n"
            "   - The green dot (Cal) will snap cleanly to dead center (0, 0).\n"
            "3. AUTO-RANGE: Click 'Auto-Range' and rotate the stick in full circles against the edges for 3 seconds.\n"
            "4. NOISE FILTER: Tune Noise Filter (10-15%) and Anti-Jitter if the input wobbles.\n"
            "5. SAVE PROFILE: Save your configuration to a portable JSON file.\n"
            "6. PLAY: Click 'Activate Virtual Gamepad' so all PC games read calibrated inputs!\n"
            "7. TURN OFF: Click '⏻ Turn Off Controller' on top to power off the wireless gamepad immediately."
        ),
        "es": (
            "1. CONECTAR: Encienda el mando Xbox 360 con el receptor inalámbrico.\n"
            "2. AUTO-CENTRO: Suelte ambos sticks y pulse 'Auto-Centro' en cada uno.\n"
            "3. AUTO-RANGO: Pulse 'Auto-Rango' y gire en círculos completos durante 3 segundos.\n"
            "4. FILTRO DE RUIDO: Ajuste el filtro si el punto tiembla.\n"
            "5. GUARDAR: Guarde su perfil en JSON.\n"
            "6. JUGAR: Active el 'Mando Virtual' para enviar los datos corregidos a los juegos.\n"
            "7. APAGAR: Pulse '⏻ Apagar Mando' para apagarlo de inmediato."
        ),
        "fr": (
            "1. CONNECTER : Allumez la manette sans fil avec le récepteur PC.\n"
            "2. AUTO-CENTRE : Laissez les sticks au repos et cliquez sur 'Auto-Centre'.\n"
            "3. AUTO-PORTÉE : Cliquez sur 'Auto-Portée' et tournez en rond pendant 3s.\n"
            "4. FILTRE ANTI-BRUIT : Ajustez si le signal oscille.\n"
            "5. ENREGISTRER : Sauvegardez votre profil en JSON.\n"
            "6. JOUER : Activez la 'Manette Virtuelle' pour jouer sans dérive !\n"
            "7. ÉTEINDRE : Cliquez sur '⏻ Éteindre la Manette' pour couper l'alimentation."
        ),
        "de": (
            "1. VERBINDEN: Xbox 360 Wireless Controller einschalten.\n"
            "2. AUTO-ZENTRIERUNG: Sticks loslassen und 'Auto-Zentrierung' anklicken.\n"
            "3. AUTO-BEREICH: 'Auto-Bereich' anklicken und 3 Sekunden im Kreis drehen.\n"
            "4. RAUSCHFILTER: Filter bei Schwankungen anpassen.\n"
            "5. SPEICHERN: Profil als JSON sichern.\n"
            "6. SPIELEN: 'Virtuellen Controller aktivieren' anklicken.\n"
            "7. AUSSCHALTEN: '⏻ Controller ausschalten' schaltet das Gerät sofort ab."
        ),
        "it": (
            "1. CONNETTI: Accendi il controller wireless con il ricevitore PC.\n"
            "2. AUTO-CENTRO: Lascia le levette a riposo e premi 'Auto-Centro'.\n"
            "3. AUTO-RAGGIO: Premi 'Auto-Raggio' e ruota a cerchio per 3 secondi.\n"
            "4. FILTRO RUMORE: Regola se il cursore vibra.\n"
            "5. SALVA: Salva il profilo in formato JSON.\n"
            "6. GIOCA: Attiva il 'Controller Virtuale' per giocare con input perfetti.\n"
            "7. SPEGNI: Premi '⏻ Spegni Controller' per spegnerlo subito."
        ),
        "ja": (
            "1. 接続: Xbox 360 ワイヤレス受信機経由でコントローラーの電源を入れます。\n"
            "2. 自動中央補正: スティックに触れずに各側で「自動中央補正」をクリックします。\n"
            "3. 自動範囲補正: 「自動範囲補正」を押し、外周に沿って3秒間回転させます。\n"
            "4. ノイズ低減: 軸の微小なブレがある場合はノイズフィルタを調整します。\n"
            "5. 保存: 設定をJSONファイルに保存します。\n"
            "6. ゲーム開始: 「仮想ゲームパッド有効化」を押すとゲームに補正値が送られます。\n"
            "7. 電源オフ: 上部の「⏻ 電源オフ」をクリックすると即座に電源を切ることができます。"
        ),
        "zh": (
            "1. 连接手柄: 打开 Xbox 360 无线手柄并与 PC 接收器配对。\n"
            "2. 自动归中: 保持摇杆完全静止在中心，分别点击左右侧的“自动归中”。\n"
            "3. 自动范围: 点击“自动范围”，贴紧边缘画完整大圈旋转 3 秒。\n"
            "4. 抗噪滤波: 若静止时点位有轻微抖动，可适度调高平滑滤波。\n"
            "5. 保存配置: 点击“保存配置”存为便携式 JSON 文件。\n"
            "6. 畅玩游戏: 点击“启用虚拟手柄”，即可将校准信号完美传递给所有电脑游戏！\n"
            "7. 关机功能: 点击顶部的“⏻ 关闭手柄电源”按钮，可立即关闭无线手柄。"
        ),
        "ru": (
            "1. ПОДКЛЮЧИТЕ: Включите беспроводной геймпад через приемник.\n"
            "2. АВТО-ЦЕНТР: Не трогайте стики и нажмите 'Авто-центр' для каждого стика.\n"
            "3. АВТО-ДИАПАЗОН: Нажмите 'Авто-диапазон' и вращайте по кругу 3 секунды.\n"
            "4. ФИЛЬТР ШУМА: Настройте подавление шума при микроколебаниях.\n"
            "5. СОХРАНИТЬ: Сохраните профиль в JSON.\n"
            "6. ИГРАТЬ: Нажмите 'Включить виртуальный геймпад'.\n"
            "7. ВЫКЛЮЧИТЬ: Кнопка '⏻ Выключить геймпад' сверху моментально отключит питание."
        ),
        "ko": (
            "1. 연결: PC 무선 수신기를 통해 Xbox 360 컨트롤러 전원을 켭니다.\n"
            "2. 자동 중앙 정렬: 스틱을 중립에 두고 '자동 중앙 정렬'을 누릅니다.\n"
            "3. 자동 범위 감지: '자동 범위 감지'를 누르고 테두리를 따라 3초간 원을 그리세요.\n"
            "4. 노이즈 필터: 떨림이 있는 경우 안티 지터 및 필터를 조절합니다.\n"
            "5. 프로필 저장: 설정을 JSON 파일로 저장합니다.\n"
            "6. 게임 플레이: '가상 게임패드 활성화'를 눌러 게임에 완벽한 신호를 전달하세요!\n"
            "7. 전원 끄기: 상단의 '⏻ 컨트롤러 끄기' 버튼을 누르면 즉시 무선 전원이 차단됩니다."
        ),
    },

    # ---- Help tab: Hall Effect ---------------------------------------------
    "help_hall_title": {
        "pt": "🧲 DIAGNÓSTICO: HALL EFFECT vs. POTENCIÔMETRO NO XBOX 360",
        "en": "🧲 DIAGNOSIS: HALL EFFECT vs. POTENTIOMETER ON XBOX 360",
        "es": "🧲 DIAGNÓSTICO: HALL EFFECT vs. POTENCIÓMETRO EN XBOX 360",
        "fr": "🧲 DIAGNOSTIC : EFFET HALL vs. POTENTIOMÈTRE SUR XBOX 360",
        "de": "🧲 DIAGNOSE: HALL-EFFEKT vs. POTENTIOMETER BEI XBOX 360",
        "it": "🧲 DIAGNOSI: EFFETTO HALL vs. POTENZIOMETRO SU XBOX 360",
        "ja": "🧲 診断解説: Xbox 360 におけるホール効果とポテンショメータ",
        "zh": "🧲 深度诊断: Xbox 360 上霍尔电磁摇杆与电位器对比",
        "ru": "🧲 ДИАГНОСТИКА: ДАТЧИКИ ХОЛЛА И ПОТЕНЦИОМЕТРЫ ДЛЯ XBOX 360",
        "ko": "🧲 진단 분석: Xbox 360에서 홀 센서와 가변저항의 차이",
    },
    "help_hall_body": {
        "pt": (
            "O circuito ADC do Xbox 360 foi desenhado para POTENCIÔMETROS RESISTIVOS de 10kΩ.\n\n"
            "• POTENCIÔMETROS TRADICIONAIS (OEM):\n"
            "  Solução plug & play perfeita. Qualquer desvio mecânico de solda é corrigido pelo Auto-Center!\n\n"
            "• SENSORES HALL EFFECT RETROFIT (Por que o eixo Y costuma travar em 32767?):\n"
            "  O Xbox 360 não possui firmware adaptativo para curva Hall. Se a rotação do ímã estiver fora da\n"
            "  janela linear de 3.3V, o ADC satura no valor máximo (32767). Se ocorrer isso, teste 'Inverter Eixo Y'\n"
            "  ou substitua por potenciômetros analógicos de boa qualidade."
        ),
        "en": (
            "The Xbox 360 ADC hardware was specifically designed for 10kΩ RESISTIVE POTENTIOMETERS.\n\n"
            "• TRADITIONAL POTENTIOMETERS (OEM):\n"
            "  100% plug & play. Any minor mechanical solder offset is completely resolved by this tool's Auto-Center!\n\n"
            "• HALL EFFECT RETROFIT (Why the Y axis often locks at 32767):\n"
            "  The Xbox 360 lacks active firmware calibration for magnetic non-linearity. If the magnet is rotated\n"
            "  beyond its linear 3.3V window, the ADC saturates at raw 32767. Try toggling 'Invert Y Axis' or swap\n"
            "  to standard high-grade analog potentiometers."
        ),
        "es": (
            "El ADC de Xbox 360 fue diseñado para potenciómetros resistivos de 10kΩ.\n"
            "Los potenciómetros tradicionales son plug & play y cualquier desviación la corrige el Auto-Centro.\n"
            "En sensores Hall Effect, el eje Y puede saturar en 32767 si el imán no está perfectamente alineado."
        ),
        "fr": (
            "Le circuit de la Xbox 360 est conçu pour des potentiomètres résistifs de 10kΩ.\n"
            "Les potentiomètres classiques sont plug & play et corrigés par l'Auto-Centre.\n"
            "Avec l'Effet Hall, l'axe Y peut saturer à 32767 si l'aimant est mal aligné."
        ),
        "de": (
            "Die Xbox 360 Schaltung ist für 10kΩ Potentiometer ausgelegt.\n"
            "Klassische Potentiometer sind Plug & Play und werden durch Auto-Zentrierung perfekt korrigiert.\n"
            "Hall-Sensoren können bei Fehlstellung die 3,3V ADC-Sättigung bei 32767 auslösen."
        ),
        "it": (
            "Il circuito Xbox 360 è progettato per potenziometri resistivi da 10kΩ.\n"
            "I potenziometri tradizionali sono plug & play e corretti dall'Auto-Centro.\n"
            "Con sensori a Effetto Hall, l'asse Y può saturare a 32767 se il magnete è ruotato."
        ),
        "ja": (
            "Xbox 360 の回路は 10kΩ 抵抗式ポテンショメータ専用に設計されています。\n"
            "標準ポテンショメータは完全なプラグ＆プレイで、ハンダのズレも「自動中央補正」で解決します。\n"
            "ホール効果モジュールでは、磁石の角度ズレにより ADC が 3.3V で飽和し 32767 で固着することがあります。"
        ),
        "zh": (
            "Xbox 360 的硬件转换电路专为 10kΩ 传统碳膜电位器设计。\n"
            "传统电位器即插即用，焊接产生的轻微机械偏差可通过本工具的“自动归中”彻底解决。\n"
            "若改装霍尔摇杆，因缺少机内校准，微小磁极偏移极易导致 3.3V 电压满量程饱和，使 Y 轴死锁在 32767。"
        ),
        "ru": (
            "Схема Xbox 360 рассчитана на резистивные потенциометры 10 кОм.\n"
            "Обычные потенциометры подключаются без проблем, а погрешности пайки устраняет Авто-центр.\n"
            "Датчики Холла при малейшем перекосе магнита вызывают насыщение АЦП 3.3В и зависание оси Y на 32767."
        ),
        "ko": (
            "Xbox 360 하드웨어는 10kΩ 가변저항에 맞춰 설계되었습니다.\n"
            "일반 가변저항은 즉시 호환되며 미세한 오차는 자동 중앙 정렬로 완벽히 해결됩니다.\n"
            "홀 효과 센서는 미세한 각도 오차로 인해 3.3V 포화가 발생하여 Y축이 32767에 고정될 수 있습니다."
        ),
    },

    # ---- Help tab: Curves --------------------------------------------------
    "help_curves_title": {
        "pt": "📈 GUIA DE CURVAS DE RESPOSTA E DEADZONE SUAVE",
        "en": "📈 RESPONSE CURVES & SMOOTH DEADZONE GUIDE",
        "es": "📈 GUÍA DE CURVAS DE RESPUESTA",
        "fr": "📈 GUIDE DES COURBES DE RÉPONSE",
        "de": "📈 REAKTIONSKURVEN-LEITFADEN",
        "it": "📈 GUIDA ALLE CURVE DI RISPOSTA",
        "ja": "📈 応答曲線とスムーズデッドゾーン解説",
        "zh": "📈 响应曲线与平滑死区技术说明",
        "ru": "📈 РУКОВОДСТВО ПО КРИВЫМ ОТКЛИКА",
        "ko": "📈 응답 곡선 및 스무스 데드존 가이드",
    },
    "help_curves_body": {
        "pt": (
            "• Deadzone Radial Suave: Transição cúbica Hermite que evita pulos na saída do centro.\n"
            "• Linear (1:1): Mapeamento direto.\n"
            "• Suave (FPS): Mais estabilidade perto do centro para mira de precisão.\n"
            "• Agressivo: Reação rápida para jogos de corrida e arcade.\n"
            "• Extra Suave: Modo sniper de alta precisão."
        ),
        "en": (
            "• Smooth Radial Deadzone: Hermite cubic interpolation prevents jarring steps leaving deadzone.\n"
            "• Linear (1:1): Pure 1:1 proportional response.\n"
            "• Smooth (FPS): Extra control near center for accurate shooter aim.\n"
            "• Aggressive: Fast response for racing and arcade fighting.\n"
            "• Extra Smooth: Fine control for high-zoom snipers."
        ),
        "es": (
            "• Zona Muerta Suave: Interpolación cúbica Hermite sin saltos bruscos.\n"
            "• Lineal (1:1): Respuesta directa.\n"
            "• Suave (FPS): Mayor precisión en el centro para apuntar.\n"
            "• Agresivo: Respuesta rápida para carreras.\n"
            "• Extra Suave: Modo francotirador."
        ),
        "fr": (
            "• Zone morte radiale fluide avec interpolation Hermite.\n"
            "• Linéaire : Réponse directe 1:1.\n"
            "• Fluide (FPS) : Précision accrue au centre pour la visée.\n"
            "• Agressif : Rapide pour les jeux de course.\n"
            "• Ultra Fluide : Idéal pour les snipers."
        ),
        "de": (
            "• Sanfte radiale Totzone: Hermite-Kubik-Interpolation verhindert Ruckler.\n"
            "• Linear (1:1): Direkte Umsetzung.\n"
            "• Sanft (FPS): Hohe Präzision im Zentrum.\n"
            "• Aggressiv: Schnelle Reaktion für Rennspiele.\n"
            "• Extra Sanft: Für Scharfschützen."
        ),
        "it": (
            "• Zona morta radiale morbida con interpolazione Hermite.\n"
            "• Lineare (1:1): Risposta diretta.\n"
            "• Morbida (FPS): Maggiore precisione al centro per mirare.\n"
            "• Aggressiva: Reazione rapida per corse.\n"
            "• Ultra Morbida: Modalità cecchino."
        ),
        "ja": (
            "• スムーズ円形デッドゾーン: エルミート3次補間によりデッドゾーン境界での段差を解消。\n"
            "• リニア (1:1): 等倍の直接入力。\n"
            "• スムーズ (FPS): 中心付近を緩やかにし照準の微調整を容易にします。\n"
            "• アグレッシブ: レースゲーム等での素早い入力向け。\n"
            "• 超スムーズ: スナイパー向けの高倍率微小操作用。"
        ),
        "zh": (
            "• 径向平滑死区: 采用 Hermite 三次样条插值，完全消除跨出死区瞬间的顿挫跃冲感。\n"
            "• 线性 (1:1): 物理位置与输出成正比。\n"
            "• 平滑 (FPS): 中心区域灵敏度平缓，极度适合射击游戏微调压枪瞄准。\n"
            "• 激进: 摇杆轻推即获大幅度转向，适合赛车与格斗游戏。\n"
            "• 极度平滑: 狙击专享超细腻微调。"
        ),
        "ru": (
            "• Плавная мертвая зона: Кубическая интерполяция Эрмита устраняет рывки при выходе из центра.\n"
            "• Линейная (1:1): Прямой отклик.\n"
            "• Плавная (FPS): Мягкая зона у центра для точного прицеливания.\n"
            "• Агрессивная: Быстрый отклик для гонок.\n"
            "• Сверхплавная: Снайперский режим."
        ),
        "ko": (
            "• 스무스 반경 데드존: 에르미트 3차 보간으로 데드존 이탈 시 튀는 현상을 방지합니다.\n"
            "• 선형 (1:1): 직접적인 1:1 입력.\n"
            "• 부드러움 (FPS): 정밀 조준을 위해 중앙 민감도를 완만하게 합니다.\n"
            "• 민첩: 레이싱 게임에 적합한 빠른 응답.\n"
            "• 초정밀: 원거리 저격 조준용 모드."
        ),
    },

    # ---- Help tab: Virtual & HidHide ---------------------------------------
    "help_virtual_title": {
        "pt": "🎮 CONTROLE VIRTUAL & DICA HIDHIDE (EVITAR CONTROLE DUPLO)",
        "en": "🎮 VIRTUAL CONTROLLER & HIDHIDE TIP (PREVENT DOUBLE INPUT)",
        "es": "🎮 MANDO VIRTUAL Y CONSEJO HIDHIDE",
        "fr": "🎮 MANETTE VIRTUELLE & CONSEIL HIDHIDE",
        "de": "🎮 VIRTUELLER CONTROLLER & HIDHIDE TIPP",
        "it": "🎮 CONTROLLER VIRTUALE & GUIDA HIDHIDE",
        "ja": "🎮 仮想ゲームパッドと HidHide 解説 (2重認識防止)",
        "zh": "🎮 虚拟手柄与 HidHide 防双重识别教程",
        "ru": "🎮 ВИРТУАЛЬНЫЙ ГЕЙМПАД И HIDHIDE",
        "ko": "🎮 가상 게임패드 및 HidHide 팁 (이중 입력 방지)",
    },
    "help_virtual_body": {
        "pt": (
            "COMO FUNCIONA O CONTROLE VIRTUAL:\n"
            "  O driver ViGEmBus cria um Xbox 360 virtual perfeito no Windows que repassa valores calibrados.\n\n"
            "DICA DE OURO — EVITAR DOIS CONTROLES DETECTADOS NOS JOGOS:\n"
            "  Se algum jogo detectar o controle físico (Player 1) e o virtual (Player 2) ao mesmo tempo:\n"
            "  1. Baixe a ferramenta gratuita HidHide (da Nefarius): https://github.com/nefarius/HidHide/releases\n"
            "  2. Adicione o Python na lista de permissões ('Applications').\n"
            "  3. Na aba 'Devices', marque para ocultar o controle físico Xbox 360 dos jogos."
        ),
        "en": (
            "HOW VIRTUAL GAMEPAD WORKS:\n"
            "  ViGEmBus creates a clean virtual Xbox 360 controller in Windows forwarding calibrated axes.\n\n"
            "PRO TIP — PREVENTING DOUBLE CONTROLLER CONFLICT:\n"
            "  If a game detects both physical (Player 1) and virtual (Player 2) controllers:\n"
            "  1. Download free HidHide utility: https://github.com/nefarius/HidHide/releases\n"
            "  2. Add Python to the 'Applications' whitelist.\n"
            "  3. In 'Devices', check the box to hide the physical Xbox 360 controller from other apps."
        ),
        "es": (
            "ViGEmBus emula un mando Xbox 360 virtual con los datos corregidos.\n"
            "Para evitar que los juegos detecten 2 mandos simultáneos, instale HidHide:\n"
            "https://github.com/nefarius/HidHide/releases y oculte el mando físico."
        ),
        "fr": (
            "ViGEmBus émule une manette virtuelle avec vos valeurs étalonnées.\n"
            "Pour éviter qu'un jeu détecte deux manettes (Joueur 1 & Joueur 2), utilisez HidHide :\n"
            "https://github.com/nefarius/HidHide/releases pour masquer la manette physique."
        ),
        "de": (
            "ViGEmBus erstellt einen virtuellen Xbox 360 Controller für Spiele.\n"
            "Falls Spiele zwei Controller (Spieler 1 & 2) erkennen, nutzen Sie HidHide:\n"
            "https://github.com/nefarius/HidHide/releases zum Ausblenden des physischen Geräts."
        ),
        "it": (
            "ViGEmBus emula un controller Xbox 360 virtuale per i giochi.\n"
            "Per evitare doppio controller nei giochi, scarica HidHide:\n"
            "https://github.com/nefarius/HidHide/releases e nascondi il controller fisico."
        ),
        "ja": (
            "ViGEmBus が補正後の信号を出力する仮想 Xbox 360 コントローラーを作成します。\n"
            "ゲームで物理コントローラーと仮想コントローラーが二重認識される場合は、HidHide を使用してください:\n"
            "https://github.com/nefarius/HidHide/releases (物理コントローラーを非表示に設定)。"
        ),
        "zh": (
            "ViGEmBus 驱动在 Windows 中生成一个完美的虚拟 Xbox 360 控制器并向游戏输出校准信号。\n"
            "防双重手柄识别技巧 (解决部分游戏将物理与虚拟手柄识别为 1P 和 2P 的冲突):\n"
            "1. 前往下载免费的 HidHide 驱动工具: https://github.com/nefarius/HidHide/releases\n"
            "2. 将 Python 添加到白名单，并在设备列表中勾选隐藏物理 Xbox 360 手柄即可。"
        ),
        "ru": (
            "ViGEmBus создает виртуальный геймпад для игр с калиброванными стиками.\n"
            "Если игра видит два контроллера одновременно, используйте утилиту HidHide:\n"
            "https://github.com/nefarius/HidHide/releases для скрытия физического устройства."
        ),
        "ko": (
            "ViGEmBus는 보정된 값을 게임에 전달하는 가상 Xbox 360 컨트롤러를 생성합니다.\n"
            "게임에서 물리 컨트롤러와 가상 컨트롤러가 동시에 인식되는 경우 HidHide를 사용하세요:\n"
            "https://github.com/nefarius/HidHide/releases (물리 장치 숨김 설정)."
        ),
    },
}


def T(key: str, **kwargs: object) -> str:
    """Translate *key* to the current language."""
    entry = STRINGS.get(key)
    if entry is None:
        return f"[{key}]"
    text = entry.get(_current_lang, entry.get("en", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text


def set_language(lang: str) -> None:
    """Set active language code."""
    global _current_lang
    valid_codes = [c for c, _ in LANGUAGES]
    if lang in valid_codes:
        _current_lang = lang


def get_language() -> str:
    """Return active language code."""
    return _current_lang


def get_languages() -> list[tuple[str, str]]:
    """Return list of supported (code, display_name) tuples."""
    return LANGUAGES


def toggle_language() -> str:
    """Cycle to the next language in LANGUAGES list."""
    global _current_lang
    codes = [c for c, _ in LANGUAGES]
    try:
        idx = codes.index(_current_lang)
        _current_lang = codes[(idx + 1) % len(codes)]
    except ValueError:
        _current_lang = "pt"
    return _current_lang


CURVE_KEYS = ["linear", "smooth", "aggressive", "extra_smooth"]


def get_curve_labels() -> list[str]:
    """Return response curve labels in the current language."""
    return [T(f"curve_{key}") for key in CURVE_KEYS]


def curve_label_to_key(label: str) -> str:
    """Map a translated curve label back to its internal key."""
    for key in CURVE_KEYS:
        lbl_key = f"curve_{key}"
        entry = STRINGS.get(lbl_key, {})
        for lang_code, translated in entry.items():
            if translated == label:
                return key
    return "linear"


def curve_key_to_label(key: str) -> str:
    """Map an internal curve key to a translated label."""
    return T(f"curve_{key}")
