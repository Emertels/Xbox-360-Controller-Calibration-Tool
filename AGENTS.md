# AGENTS.md — Guia de Arquitetura e Engenharia para IAs e Desenvolvedores

Este documento é o guia canônico para agentes autônomos de IA, LLMs e desenvolvedores que precisem manter, depurar, testar ou estender a ferramenta **Xbox 360 Controller Calibration Tool**.

---

## 📌 Visão Geral do Sistema

- **Nome do Projeto:** Xbox 360 Controller Calibration Tool
- **Versão:** 1.0.0 (Release Oficial de Lançamento)
- **Linguagem:** Python 3.10+ (desenvolvido e testado em Python 3.12 64-bit no Windows 11)
- **Framework de UI:** `tkinter` + `ttk` nativo do Python (sem frameworks pesados como PyQt/Electron)
- **Interface com Hardware:** Windows XInput API direta via `ctypes` (`xinput1_4.dll` ➔ `xinput1_3.dll` ➔ `xinput9_1_0.dll`), com suporte a desligamento por ordinal 103
- **Emulação Virtual:** `vgamepad` sobre o driver kernel `ViGEmBus`
- **Persistência:** Arquivos de perfil em JSON versionado na pasta local `profiles/`
- **Localização:** Internacionalização nativa em `i18n.py` com 10 idiomas (pt, en, es, fr, de, it, ja, zh, ru, ko) com seleção via Combobox
- **Hardware Suportado:** Controles de Xbox 360 sem fio (via Receptor Wireless USB para PC com ou sem cabo Play & Charge USB do AliExpress) e controles com fio USB nativos (originais ou paralelos/clones).

---

## ⚠️ Natureza Experimental & Limitações Físicas

Esta ferramenta é um utilitário comunitário de calibração via software:
1. **Não é 100% perfeita:** O software compensa centro, ruído e alcance calculando offsets matemáticos em tempo real. Dependendo do jogo e da resposta de polling, podem ocorrer pequenas divergências de precisão.
2. **Não substitui reparos físicos:** Caso o gimbal do analógico esteja quebrado mecanicamente, sem tensão de retorno ou com as pistas de carbono do potenciômetro rompidas, a peça precisará de troca física (solda de novos potenciômetros 10kΩ).

---

## 🎯 Por que a ferramenta foi concebida desta forma?

1. **Protocolo XInput do Xbox 360 é Read-Only:** A API XInput da Microsoft expõe apenas funções de leitura (`XInputGetState`) e vibração (`XInputSetState`). Não existe comando no protocolo para regravar zonas mortas ou offsets de calibração na memória flash interna do microcontrolador (MCU) do controle original.
2. **Receptor Wireless masca USB direto:** Ferramentas WebUSB/WebHID (ex: DriftGuard) dependem de descritores de endpoint USB de controle com fio nativo. Quando o controle é wireless, o chip do receptor sem fio oficial gerencia a comunicação de rádio e bloqueia comandos de baixo nível de firmware.
3. **Cabo Play & Charge só transporta energia:** Os pinos de dados (D+ e D-) não são conectados ao microcontrolador na porta superior do controle sem fio; apenas os pinos de alimentação 5V estão ligados ao circuito de recarga de bateria. Portanto, o cabo USB (como os kits acessíveis do AliExpress/Shopee) fornece energia contínua, enquanto o receptor wireless recebe os comandos.
4. **Solução por Injeção Virtual:** Esta ferramenta roda um loop de leitura ultra-rápido (~16ms por frame / ~60-120fps), aplica matemática de calibração em ponto flutuante e envia o estado corrigido para um controle Xbox 360 virtual emulado via ViGEmBus.

---

## 🏗️ Topologia da Arquitetura de Módulos

```
C:\Projetos\Calibration_Controle_Xbox_360\
│
├── INICIAR_SEM_CMD.vbs         # Launcher silencioso via WScript (0 CMD)
├── INICIAR.bat                 # Launcher batch com busca inteligente de Python (pythonw)
├── INSTALAR_DEPENDENCIAS.bat   # Script portátil de instalação de pacotes via pip
├── main.py                     # Entry point, GUI Tkinter, loop de renderização a 60fps
├── i18n.py                     # Motor de internacionalização (10 idiomas nativos)
├── xinput_reader.py            # Binding ctypes com as DLLs XInput (zero dependência externa)
├── calibration.py              # Pipeline matemático: filtros EMA, Hermite step, curvas e range
├── virtual_gamepad.py          # Wrapper seguro sobre vgamepad / ViGEmBus (graceful degradation)
├── profiles.py                 # Serialização e deserialização atômica de arquivos JSON
├── requirements.txt            # Dependência externa opcional: vgamepad>=0.1.0
├── README.md                   # Documentação completa em Português (PT-BR)
├── README.en.md                # Documentação completa em Inglês (EN)
├── AGENTS.md                   # Este arquivo (guia de engenharia em Português)
├── AGENTS.en.md                # Guia de engenharia em Inglês
└── profiles/                   # Pasta portátil onde os perfis JSON são armazenados
```

---

## 🔄 Fluxo de Dados por Frame (`App._tick` a cada ~16ms)

```
[Hardware XInput]
       │
       ▼
XInputReader.get_state(idx)
       │
       ├─► ControllerState (dataclass com eixos brutos e bitmask de botões)
       │
       ▼
NoiseFilter.apply(raw_x, raw_y, strength, anti_jitter)
       │
       ├─► (filt_x, filt_y) [Sinal atenuado via Exponential Moving Average]
       │
       ▼
apply_stick_calibration(filt_x, filt_y, stick_settings)
       │
       ├─ 1. Subtrai offset de centro (mediana calculada no Auto-Center)
       ├─ 2. Aplica inversão de polaridade (invert_x, invert_y se ativo)
       ├─ 3. Calcula magnitude polar: r = sqrt(dx² + dy²)
       ├─ 4. Aplica Deadzone Radial Suave:
       │     Se r <= deadzone: retorna (0, 0)
       │     Se r < deadzone + transition: interpola via Hermite cúbico: t = t*t*(3 - 2t)
       ├─ 5. Aplica Curva de Resposta selecionada:
       │     Linear: y = x
       │     Suave: y = x² (quadrática)
       │     Agressivo: y = sqrt(x)
       │     Extra Suave: y = x³ (cúbica)
       ├─ 6. Escala pelo fator Auto-Range e clampa em [-32768, 32767]
       │
       ▼
apply_trigger_deadzone(raw_trigger, deadzone)
       │
       ▼
StickCanvas.update() / TriggerUnit.update() / ControllerPanel.update()  [Renderização na tela]
       │
       ▼
VirtualGamepad.update(...)  [Injeção de pacotes no driver ViGEmBus para os jogos]
```

---

## 📦 Detalhes de Cada Componente

### 1. `xinput_reader.py`
- **Objetivo:** Ler estado dos controles físicos sem depender de pacotes de terceiros.
- **Implementação:** Usa `ctypes.WinDLL`. Tenta carregar em cascata:
  1. `xinput1_4.dll` (Windows 8 / 10 / 11 nativa)
  2. `xinput1_3.dll` (DirectX June 2010 redist)
  3. `xinput9_1_0.dll` (Legado Windows 7/Vista)
- **Estruturas C:**
  - `XINPUT_GAMEPAD`: espelha os tipos C (`wButtons` ushort, triggers ubyte, eixos short).
  - `XINPUT_STATE`: empacota `dwPacketNumber` e a struct do gamepad.
- **Métodos Chave:**
  - `find_connected_controller() -> int | None`: varre os slots 0 a 3 procurando controle conectado.
  - `get_state(player_index: int) -> ControllerState`: consulta com overhead de ~0.05ms.
  - `power_off(controller_index: int) -> bool`: envia comando não-documentado XInput via ordinal 103 para desligar controles sem fio sem desconectar bateria.

### 2. `calibration.py`
- **Objetivo:** Conter toda a matemática pura de calibração sem acoplamento à interface gráfica.
- **Classes:**
  - `StickCalibration`: dataclass com `center_x`, `center_y`, `deadzone`, `range_scale`, `invert_x`, `invert_y`, `response_curve`, `noise_filter`, `anti_jitter`.
  - `CalibrationSettings`: agrupa `left_stick`, `right_stick` e deadzones dos gatilhos (`left_trigger_deadzone`, `right_trigger_deadzone`).
  - `NoiseFilter`: filtro EMA com corte de anti-jitter. Se a diferença delta for menor que o limiar `anti_jitter`, ignora flutuações de ruído estático.
- **Funções Chave:**
  - `apply_stick_calibration(raw_x, raw_y, cal) -> tuple[int, int]`: pipeline com deadzone radial com transição Hermite contínua, prevenindo solavancos na borda.
  - `apply_trigger_deadzone(raw, deadzone) -> int`: remapeia de `[deadzone, 255]` para `[0, 255]`.

### 3. `i18n.py`
- **Objetivo:** Suporte a 10 idiomas completos e centralizados (`pt`, `en`, `es`, `fr`, `de`, `it`, `ja`, `zh`, `ru`, `ko`).
- **Funções:**
  - `T(key: str, **kwargs) -> str`: busca tradução com suporte a interpolação via `.format()`.
  - `set_language(lang: str) -> None`: altera o idioma ativo.
  - `get_languages() -> list[tuple[str, str]]`: lista de códigos e nomes amigáveis com bandeiras.
  - `get_curve_labels()`, `curve_label_to_key()`, `curve_key_to_label()`: mapeamento seguro entre nomes amigáveis traduzidos para a UI e os identificadores internos do motor de cálculo.

### 4. `virtual_gamepad.py`
- **Objetivo:** Fornecer camada de saída virtual via driver kernel ViGEmBus.
- **Degradação Suave (Graceful Degradation):**
  - Se `vgamepad` não estiver instalado, a flag booleana `VGAMEPAD_AVAILABLE` é definida como `False`.
  - A ferramenta abre normalmente em **modo diagnóstico/visualizador**, sem crashar.
  - O botão de controle virtual na UI mostra aviso e orienta o usuário a rodar o script de instalação.
- **Tratamento de Exceções:**
  - Se o pacote Python `vgamepad` estiver presente mas o driver `.msi` do ViGEmBus não estiver instalado no Windows, intercepta `RuntimeError` e instrui o usuário com link direto da release oficial do GitHub.

### 5. `profiles.py`
- **Objetivo:** Salvar configurações de calibração em arquivos `.json` humanos e versionados.
- **Localização:** Subpasta `profiles/` dentro da pasta raiz do projeto (caminho portátil).
- **Esquema JSON:**
  ```json
  {
    "version": 1,
    "timestamp": "2026-10-27T14:00:00Z",
    "calibration": {
      "left_stick": { ... },
      "right_stick": { ... },
      "left_trigger_deadzone": 0,
      "right_trigger_deadzone": 0
    }
  }
  ```

### 6. `main.py`
- **Objetivo:** GUI em Tkinter com alta responsividade, layout escuro e controles visuais.
- **Widgets Customizados:**
  - `StickCanvas`: radar polar com círculos de 25%, 50%, 75%, 100%, vetor vermelho (raw) e vetor verde (calibrado).
  - `TriggerUnit` / `TriggerBar`: barras analógicas de pressão (0-255 e %) com botões dedicados de gatilho (`[ LT ]` na esquerda e `[ RT ]` na direita) que acendem e afundam com a pressão física.
  - `ControllerPanel`: painel central unificado reproduzindo a geometria física oficial do Xbox 360: gatilhos e bumpers no topo (`LT/LB` e `RT/RB`), menu central (`Back`, `⨂ Xbox`, `Start`), asa esquerda com stick (`LS`) e D-Pad em cruz (`▲`, `◀`, `▶`, `▼`), e asa direita com diamante `ABXY` (`Y` amarelo, `X` azul, `B` vermelho, `A` verde) e stick (`RS`).
  - `StickCalibrationPanel`: painel com Auto-Center por mediana, Auto-Range por círculos contínuos, sliders e seleção de curva de resposta.
  - `TriggersTab`: aba dedicada a deadzones de gatilhos e explicação técnica de curvas.
  - `HelpTab`: guia de calibração e diagnóstico de sensores Hall Effect vs. Potenciômetros.
  - `VirtualGuideTab`: guia de uso do controle virtual nos jogos e tutorial do utilitário HidHide.

---

## 🛠️ Convenções de Código e Extensões

1. **Idiomas:**
   - Variáveis, classes, métodos e comentários de código: **Inglês**.
   - Textos exibidos ao usuário na UI: **Centralizados em `i18n.py`**, sempre obtidos através de `T("chave")`.
2. **Ranges de Entrada e Saída:**
   - Analógicos: signed 16-bit inteiro (`-32768` a `32767`). O centro nominal é `0`.
   - Gatilhos: unsigned 8-bit inteiro (`0` a `255`).
3. **Deadzone:**
   - **Sempre radial (polar)**, nunca axial quadrada. Deadzone axial causa deformação em movimentos diagonais em jogos modernos.

---

## 🚀 Como Empacotar como Executável Único (`.exe`)

Para gerar um binário `.exe` portátil sem exigir Python instalado:

1. Instale o PyInstaller no ambiente:
   ```powershell
   py -3 -m pip install pyinstaller
   ```
2. Compile na pasta do projeto:
   ```powershell
   py -3 -m PyInstaller --onefile --noconsole --name "Xbox360_Calibration_Tool" main.py
   ```
3. O executável standalone será gerado em `dist\Xbox360_Calibration_Tool.exe`.
