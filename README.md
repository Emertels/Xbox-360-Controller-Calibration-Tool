# 🎮 Xbox 360 Controller Calibration Tool (v1.0.0)

[![Português](https://img.shields.io/badge/Idioma-Portugu%C3%AAs_(Brasil)-green.svg)](README.md)
[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.en.md)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Plataforma-Windows_10%2F11-0078D6?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/Licen%C3%A7a-MIT-22c55e)
![Version](https://img.shields.io/badge/Vers%C3%A3o-1.0.0_Oficial-blueviolet)

Ferramenta profissional, leve e de código aberto para calibração avançada de analógicos, gatilhos de pressão e botões de controles **Xbox 360** via software no Windows.

Projetada especialmente para resolver desvios de centro, drift e troca de componentes (analógicos substituídos, solda caseira, drift residual ou retrofit).

---

> [!WARNING]
> ### ⚠️ Aviso Importante: Ferramenta Experimental & Precisão
> Esta ferramenta é um projeto de software **experimental e de código aberto desenvolvido para a comunidade**.
> - **Não é 100% precisa:** Como opera através de emulação matemática em tempo real via software (Windows XInput e ViGEmBus), pequenas variações, comportamentos específicos de deadzone de alguns jogos ou arredondamentos podem ocorrer.
> - **Limitações Físicas:** A ferramenta compensa drift, ruído elétrico e desvios de centralização via software, mas **não faz milagres em componentes fisicamente danificados**. Se a mola mecânica estiver quebrada, o eixo estiver frouxo ou a trilha de carbono do potenciômetro estiver totalmente desgastada, ainda será necessária manutenção física.

> [!TIP]
> ### 🔌 Compatibilidade com Cabo USB & Kit Play & Charge (AliExpress / Shopee / Amazon)
> Você pode usar seu controle normalmente com aquele cabo USB acessível:
> - **Controle Sem Fio com Cabo Play & Charge:** Funciona perfeitamente alimentado pelo **cabo USB / Kit Play & Charge** (aquele kit barato encontrado facilmente no **AliExpress, Shopee, Mercado Livre ou Amazon**). O cabo fornece energia contínua de 5V para a bateria do controle, permitindo jogar direto no PC sem gastar pilhas. O sinal dos comandos de jogo é transmitido sem fio para o **Receptor Wireless USB** (original Microsoft ou clone compatível do AliExpress).
> - **Controles com Fio USB (Originais ou Paralelos do AliExpress):** Controles que já possuem fio nativo USB integrado (sejam originais da Microsoft ou réplicas/paralelos comprados no AliExpress) conectam-se diretamente e funcionam de imediato via driver padrão XInput.

---

## 📋 Sumário

1. [O Problema: Por que esta ferramenta existe?](#-o-problema-por-que-esta-ferramenta-existe)
2. [Arquitetura & Como Funciona](#-arquitetura--como-funciona)
3. [Principais Funcionalidades (v1.0.0)](#-principais-funcionalidades-v100)
4. [Diagnóstico Técnico: Hall Effect vs. Potenciômetros no Xbox 360](#-diagnóstico-técnico-hall-effect-vs-potenciômetros-no-xbox-360)
5. [Pré-requisitos & Instalação Rápida](#-pré-requisitos--instalação-rápida)
6. [Guia Passo a Passo de Uso](#-guia-passo-a-passo-de-uso)
7. [Dica de Ouro: Como Evitar Controle Duplo com HidHide](#-dica-de-ouro-como-evitar-controle-duplo-com-hidhide)
8. [Estrutura do Projeto](#-estrutura-do-projeto)
9. [Perguntas Frequentes (FAQ)](#-perguntas-frequentes-faq)
10. [Referências e Links Úteis](#-referências-e-links-úteis)
11. [Licença & Créditos](#-licença--créditos)

---

## 🧐 O Problema: Por que esta ferramenta existe?

O controle **Xbox 360** (especialmente o modelo sem fio com o receptor wireless para PC) é um dos joysticks mais populares da história, mas sofre com limitações sérias de software moderno:

- ❌ **Sem calibração nativa no Windows:** O aplicativo oficial *Xbox Accessories* da Microsoft suporta apenas controles Xbox One e Xbox Series. O Xbox 360 foi descontinuado sem qualquer suporte oficial de calibração de fábrica.
- ❌ **API XInput é somente leitura (Read-Only):** A API padrão do Windows permite ler os eixos e acionar a vibração, mas **não possui nenhum comando para gravar calibração na memória flash/MCU do controle físico**.
- ❌ **DriftGuard e ferramentas WebHID não suportam o Receptor Wireless:** Softwares modernos de navegador exigem comunicação WebUSB direta com o chip do controle. Quando conectado via receptor wireless, o chip do dongle mascara a comunicação de baixo nível.
- ❌ **O cabo Play & Charge do controle sem fio só conduz energia:** O cabo Play & Charge possui apenas os pinos de alimentação de 5V (para recarregar a bateria). A transmissão de comandos continua sendo por radiofrequência sem fio.

### A Solução: Calibração em Tempo Real por Camada de Software
Esta ferramenta atua como uma ponte transparente de altíssima velocidade: lê os dados brutos com precisão máxima via `ctypes` direto da DLL nativa do Windows (`xinput1_4.dll`), aplica um pipeline matemático completo de filtragem e calibração, e emite um controle virtual perfeito (através do driver ViGEmBus) reconhecido instantaneamente por todos os jogos de PC (Steam, Epic, Game Pass, emuladores, etc.).

---

## ⚙️ Arquitetura & Como Funciona

```
┌─────────────────────────────────┐
│  🎮 Controle Físico             │
│  Xbox 360 Wireless / USB        │
│  (Receptor ou Cabo AliExpress)  │
└───────────────┬─────────────────┘
                │ 1. Leitura bruta (~0.1ms via ctypes -> xinput1_4.dll)
                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  📊 Calibration Tool (Python 3.10+ + Tkinter / ~60-120 FPS)                 │
│                                                                             │
│  [Pipeline por Analógico]:                                                  │
│   Sinal Bruto ➔ Filtro Anti-Ruído (EMA) ➔ Filtro Anti-Jitter               │
│   ➔ Subtração de Centro (Mediana) ➔ Inversão de Eixos (X/Y)                │
│   ➔ Deadzone Radial Suave (Hermite) ➔ Curva de Resposta (Linear/Suave)      │
│   ➔ Escala de Alcance (Auto-Range) ➔ Clamping e Limitação segura           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ 2. Injeção de estado calibrado
                                       ▼
                         ┌───────────────────────────┐
                         │  🕹️ Controle Virtual     │
                         │  Xbox 360 (ViGEmBus)      │
                         └─────────────┬─────────────┘
                                       │ 3. Dispositivo de entrada limpo
                                       ▼
                         ┌───────────────────────────┐
                         │  🎯 Jogos no PC (Steam,   │
                         │  Epic, Game Pass, etc.)   │
                         │  Sinal 100% calibrado!    │
                         └───────────────────────────┘
```

---

## ✨ Principais Funcionalidades (v1.0.0)

| Recurso | Descrição |
|---|---|
| **🌐 10 Idiomas Nativos** | Seletor instantâneo com 10 idiomas completos: **Português (Brasil), English, Español, Français, Deutsch, Italiano, 日本語, 简体中文, Русский e 한국어**. |
| **🎮 Layout Físico Autêntico** | Painel central unificado reproduzindo a geometria real do controle: gatilhos e bumpers no topo (**LT/LB** e **RT/RB**), menu central (**Back**, **Xbox Guide**, **Start**), asa esquerda com stick (**LS**) e **D-Pad em cruz**, e asa direita com diamante **ABXY** e stick (**RS**). |
| **🎯 Gatilhos Analógicos 0-255** | Botões dedicados para **LT** e **RT** com barras analógicas independentes (esquerda e direita) com leitura contínua de 0 a 255 e porcentagem em tempo real. |
| **⏻ Botão Desligar Controle** | Desliga o controle sem fio do Xbox 360 instantaneamente pelo software via comando de rádio nativo XInput (ordinal 103), sem precisar tirar a bateria! |
| **⊕ Auto-Center por Mediana** | Calibração de centro em ~2 segundos que utiliza a mediana estatística (robusta contra picos espúrios de ruído). |
| **◎ Auto-Range (Calibração de Alcance)** | Gire o stick em círculos por 3 segundos para que a ferramenta calcule o diâmetro físico real, garantindo 100% de corrida/mira nos jogos. |
| **〰️ Deadzone Radial Suave (Hermite)** | Transição cúbica aveludada na saída da zona morta. Elimina o 'salto' brusco característico de deadzones axiais comuns. |
| **🛡️ Filtro Anti-Ruído & Anti-Jitter** | Média móvel exponencial (EMA) + corte de trepidação para estabilizar analógicos desgastados ou com ruído elétrico. |
| **📈 Curvas de Resposta Selecionáveis** | **Linear** (1:1), **Suave** (quadrática, ideal para mira/FPS), **Agressiva** (raiz quadrada, ideal para corrida) e **Extra Suave** (cúbica, modo sniper). |
| **🔄 Inversão de Eixos (Inv. X / Inv. Y)** | Inversão independente por analógico caso módulos de reposição tenham sido soldados com orientação invertida. |
| **⚡ Deadzone de Gatilhos (LT / RT)** | Ajuste de sensibilidade inicial nos gatilhos analógicos para evitar aceleração ou tiros acidentais. |
| **💾 Perfis Portáteis em JSON** | Salve e carregue configurações personalizadas para diferentes jogos ou controles na pasta `profiles/`. |
| **🎮 Controle Virtual ViGEmBus** | Integração com `vgamepad` para criar um controle virtual no Windows e repassar comandos aos jogos. |
| **🚀 Inicialização Silenciosa** | Launcher `INICIAR_SEM_CMD.vbs` que abre a ferramenta diretamente sem exibir janela preta de terminal. |

---

## 🧲 Diagnóstico Técnico: Hall Effect vs. Potenciômetros no Xbox 360

Se você substituiu os analógicos originais do seu controle Xbox 360, preste atenção neste guia técnico:

### 1. Potenciômetros Tradicionais (Alps RKJXV 10kΩ — Padrão OEM)
- **Como funcionam:** Divisores de tensão resistivos. O microcontrolador do Xbox 360 aplica 3.3V nas extremidades e lê a voltagem no terminal central (wiper).
- **Veredito para o Xbox 360:** **A melhor escolha (Plug & Play).**
- **Vantagem com esta ferramenta:** Não se preocupe se a sua solda ficou com um leve deslocamento mecânico (offset). O botão **Auto-Center** desta ferramenta centraliza o stick perfeitamente em 0, eliminando a necessidade de soldar *trim pots* físicos.

### 2. Módulos com Sensor Hall Effect (Magnéticos Retrofit)
- **Por que o eixo Y costuma travar em 32767 no Xbox 360?**
  - Sensores Hall Effect geram voltagens a partir da proximidade de pequenos ímãs de neodímio.
  - O Xbox 360 **não possui rotina interna de calibração no MCU**. Em controles modernos (DualSense, Xbox Series), o firmware calibra a curva do Hall Effect via software.
  - No Xbox 360, sem calibração no MCU, uma rotação de poucos graus do ímã faz a voltagem atingir 3.3V (saturação do conversor analógico-digital) antes mesmo do stick atingir o limite mecânico da carcaça, travando o valor em **32.767**.
- **O que fazer se o seu controle está com Hall Effect travando ou inconsistente:**
  1. Teste marcar a opção **Inverter Eixo Y** na ferramenta para ver se o valor passa a variar no sentido correto.
  2. Se o stick estiver duro ou travando mecanicamente, a carcaça do gimbal Hall Effect está desalinhada com a placa de circuito impresso.
  3. **Solução mais prática e duradoura:** Dessoldar o módulo Hall Effect problemático e soldar um conjunto de **potenciômetros tradicionais novos de 10kΩ**. Nossa ferramenta cuidará da centralização e do drift via software!

---

## 📦 Pré-requisitos & Instalação Rápida

> [!IMPORTANT]
> ### 🚨 Atenção aos 2 Passos Obrigatórios antes de usar:
> 1. **Você precisa ter o Python 3 instalado no Windows:** Ao instalar o Python, **é fundamental marcar a caixinha "Add python.exe to PATH"** na primeira tela do instalador.
> 2. **Execute o instalador de dependências:** Antes de abrir o programa pela primeira vez, dê um duplo clique em **`INSTALAR_DEPENDENCIAS.bat`** para instalar as bibliotecas necessárias automaticamente.

### Requisitos do Sistema:
- **Windows 10** ou **Windows 11** (64-bit)
- **Python 3.10 ou superior** instalado no computador ([Baixar do site oficial](https://www.python.org/downloads/) — **marque a opção *"Add python.exe to PATH"***)
- **Receptor Wireless para PC** (para controle sem fio) ou **Cabo USB / Play & Charge**
- **ViGEmBus Driver** (necessário para gerar o controle virtual calibrado nos jogos)

### Instalação Passo a Passo (Menos de 2 minutos):

1. **Baixar o Projeto:**
   - Baixe o arquivo `Xbox360_Calibration_Tool_v1.0.0.zip` na aba [Releases](https://github.com/Emertels/Xbox-360-Controller-Calibration-Tool/releases) e extraia em qualquer pasta do seu PC.

2. **Instalar Dependências (Obrigatório na primeira vez):**
   - Dê um duplo clique no arquivo:
     ```cmd
     INSTALAR_DEPENDENCIAS.bat
     ```
   - Uma janela preta se abrirá, detectará o Python automaticamente e instalará o pacote `vgamepad`. Quando terminar, pressione qualquer tecla para fechar.

3. **Instalar o Driver ViGEmBus (Obrigatório para reconhecer o controle nos jogos):**
   - Baixe e execute o instalador oficial `.msi` do ViGEmBus:
     👉 [Baixar ViGEmBus Driver (Releases no GitHub)](https://github.com/nefarius/ViGEmBus/releases)
   - Instalação padrão: clique em *Next → Next → Install*.

4. **Iniciar a Ferramenta:**
   - **Sem janela preta de console (Recomendado):** Dê duplo clique em **`INICIAR_SEM_CMD.vbs`**.
   - **Via script convencional:** Dê duplo clique em **`INICIAR.bat`**.

---

## 🕹️ Guia Passo a Passo de Uso

```
1. Ligar o Controle ➔ 2. Auto-Center ➔ 3. Auto-Range ➔ 4. Salvar Perfil ➔ 5. Ativar Virtual
```

1. **Ligue o controle:** Pressione o botão central Xbox Guide ou plugue o cabo USB. O status no topo mudará para `✅ Controle conectado — Jogador 1`.
2. **Auto-Center (Centralização Automática):**
   - **Solte completamente os analógicos** (deixe-os em repouso na posição neutra).
   - Clique em **⊕ Auto-Center** no painel do Analógico Esquerdo. Aguarde 2 segundos sem encostar no controle.
   - Repita o mesmo no Analógico Direito.
   - O ponto verde (**Cal**) ficará perfeitamente fixado no centro exato (0, 0).
3. **Auto-Range (Calibração de Alcance):**
   - Clique em **◎ Auto-Range** e gire o analógico em círculos completos tocando as extremidades plásticas por 3 segundos.
   - O alcance será ajustado automaticamente para que você atinja 100% de corrida em qualquer direção.
4. **Ajuste Fino de Deadzone e Anti-Ruído:**
   - Se o ponto verde tremer levemente, aumente o **Filtro Anti-Ruído** (ex: 15%) e o **Anti-Jitter** (ex: 80).
   - Se houver drift mecânico remanescente, suba a **Deadzone** para 5% a 8%.
5. **Salvar Perfil:**
   - Clique em **💾 Salvar Perfil** para guardar suas calibrações em um arquivo `.json` portátil.
6. **Jogar:**
   - Clique em **▶ Ativar Controle Virtual**.
   - O driver criará um controle Xbox 360 virtual que repassa aos jogos os valores 100% calibrados!

---

## 💡 Dica de Ouro: Como Evitar Controle Duplo com HidHide

Alguns jogos no PC (como jogos de corrida, simuladores ou emuladores) detectam simultaneamente o controle físico do Xbox 360 (Player 1) e o controle virtual gerado pelo ViGEmBus (Player 2), causando comandos duplicados.

Para resolver isso de forma 100% limpa e profissional:

1. Baixe o **HidHide** (ferramenta gratuita e oficial mantida pela equipe da Nefarius):
   👉 [Baixar HidHide Installer](https://github.com/nefarius/HidHide/releases)
2. Abra o configurador do HidHide:
   - Na aba **Applications**, adicione o executável do Python (`python.exe` e `pythonw.exe`) como permitidos (*whitelist*).
   - Na aba **Devices**, marque a caixa ao lado do seu **controle físico Xbox 360 Wireless Receiver / Controller** para ocultá-lo dos demais aplicativos.
3. Ative a opção **Enable device hiding**.
4. **Resultado:** Todos os seus jogos verão exclusivamente o controle virtual calibrado, sem qualquer conflito de dois controles!

---

## 📁 Estrutura do Repositório

```
Xbox-360-Controller-Calibration-Tool/
│
├── INICIAR_SEM_CMD.vbs         # Launcher silencioso (100% sem janela preta)
├── INICIAR.bat                 # Script batch portátil com busca inteligente de Python
├── INSTALAR_DEPENDENCIAS.bat   # Script automático para instalar dependências via pip
├── main.py                     # Interface gráfica principal (Tkinter, ~60-120fps)
├── i18n.py                     # Módulo de internacionalização (10 idiomas nativos)
├── xinput_reader.py            # Wrapper ctypes de alto desempenho sobre xinput1_4.dll
├── calibration.py              # Motor matemático: deadzone Hermite, EMA, curvas, range
├── virtual_gamepad.py          # Emulador de controle virtual via ViGEmBus (vgamepad)
├── profiles.py                 # Gerenciador de perfis de calibração em JSON
├── requirements.txt            # Dependências Python (vgamepad)
├── README.md                   # Documentação em Português (PT-BR)
├── README.en.md                # Documentation in English (EN)
├── AGENTS.md                   # Documentação técnica e arquitetural em Português
├── AGENTS.en.md                # System Architecture & Technical Guide in English
└── profiles/                   # Pasta portátil onde os perfis JSON são armazenados
```

---

## ❓ Perguntas Frequentes (FAQ)

#### A ferramenta precisa ficar aberta enquanto eu jogo?
Sim! Como o microcontrolador do Xbox 360 não permite salvar dados de calibração no seu hardware, a ferramenta atua como um tradutor em tempo real em segundo plano com uso desprezível de CPU (< 0.5%).

#### O que é a Curva de Resposta e qual devo escolher?
- **Linear (1:1):** Mapeamento direto padrão.
- **Suave (Quadrática):** Reduz a sensibilidade perto do centro para precisão cirúrgica de mira e acelera nas bordas. Altamente recomendada para jogos de tiro / FPS (Halo, Call of Duty, Battlefield).
- **Agressiva (Raiz Quadrada):** Reação instantânea a pequenos toques. Excelente para jogos de corrida (Forza, Need for Speed, F1) e luta.
- **Extra Suave (Cúbica):** Modo sniper com extrema estabilidade no centro.

#### Meu analógico esquerdo tem o Y travado em 32767. A ferramenta conserta isso?
Se o valor está travado em 32.767 mesmo movendo o stick em todas as direções, o sensor não está emitindo variação de voltagem (comum em sensores Hall Effect desalinhados no 360). Veja a seção [Diagnóstico Técnico: Hall Effect vs. Potenciômetros](#-diagnóstico-técnico-hall-effect-vs-potenciômetros-no-xbox-360) para entender o motivo e a solução recomendada.

---

## 🔗 Referências e Links Úteis

- **ViGEmBus (Virtual Gamepad Emulation Framework):** https://github.com/nefarius/ViGEmBus
- **HidHide (Driver de Ocultação de Dispositivos de Entrada):** https://github.com/nefarius/HidHide
- **vgamepad (Python Bindings para ViGEm):** https://pypi.org/project/vgamepad/
- **Microsoft XInput API Documentation:** https://learn.microsoft.com/en-us/windows/win32/xinput/getting-started-with-xinput
- **Gamepad Tester Online:** https://hardwaretester.com/gamepad

---

## 📄 Licença & Créditos

Distribuído sob a licença **MIT**. Você é livre para usar, estudar, modificar e distribuir este projeto conforme desejar.

Desenvolvido por **Emerson Teles** ([@Emertels](https://github.com/Emertels)) com auxílio do **Google Antigravity**.

---

## 👨‍💻 Sobre o Autor

Desenvolvido e mantido por **Emerson Teles** (conhecido na comunidade como **Emertels**).

Entusiasta de tecnologia, informática, jogos, manutenção de sistemas e tradução/localização de softwares para Português do Brasil (PT-BR). Desenvolvedor focado em utilitários práticos, ferramentas de produtividade, automação inteligente em PowerShell e soluções completas de localização técnica que aproximam ferramentas modernas do público brasileiro.

### 🛠️ Projetos & Contribuições

- [AI-Chat-Vault](https://github.com/Emertels/AI-Chat-Vault) — Backup portátil e recuperação de conversas locais de 20+ ferramentas e assistentes de IA.
- [Antigravity — Tradução PT-BR](https://github.com/Emertels/Antigravity-Traducao-PTBR) — Localização completa do Google Antigravity Desktop para Português do Brasil.
- [Codex Router — Tradução PT-BR](https://github.com/Emertels/CodexRouter-Traducao-PTBR) — Pacote de tradução e localização do Codex Router Control Center em PT-BR.
- [Cursor AI — Tradução PT-BR](https://github.com/Emertels/Cursor-Traducao-PTBR) — Localização completa e profunda do Cursor AI para Português do Brasil.
- [Devin AI — Tradução PT-BR](https://github.com/Emertels/Devin-Traducao-PTBR) — Tradução e localização completa do Devin Desktop para Português do Brasil.
- [GPU Tweak III — Tradução PT-BR](https://github.com/Emertels/GPU-Tweak-III-Traducao-PTBR) — Tradução em português brasileiro e instalador automatizado para ASUS GPU Tweak III.
- [Microsoft Photos Fix](https://github.com/Emertels/Microsoft-Photos-Fix) — Solução definitiva em PowerShell e C# para rota de inicialização rápida e visualização no app Fotos do Windows.
- [PSBBN-Translator](https://github.com/Emertels/PSBBN-Translator) — Suíte corporativa de tradução e localização para o PSBBN Definitive Project (PlayStation 2) em 40 idiomas.
- [Silent Hill: Homecoming — Tradução PT-BR](https://github.com/Emertels/Silent-Hill-Homecoming-Traducao-PTBR) — Tradução e revisão completa do jogo para PC em português brasileiro.
- [Suite-Emuladores](https://github.com/Emertels/Suite-Emuladores) — Suíte inteligente em PowerShell para download e atualização autônoma de 56 emuladores e frontends no Windows.
- [Xbox 360 Controller Calibration Tool](https://github.com/Emertels/Xbox-360-Controller-Calibration-Tool) — Ferramenta profissional para calibração avançada de analógicos, gatilhos e botões de controles Xbox 360 no Windows.
- [ZCode — Tradução PT-BR](https://github.com/Emertels/ZCode-Traducao-PTBR) — Tradução e localização completa do ZCode Desktop para Português do Brasil.

### 🌐 Conecte-se comigo & Comunidades Oficiais

<div align="left">

[![GitHub](https://img.shields.io/badge/GitHub-Emertels-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/emertels)
[![Website](https://img.shields.io/badge/Website-Emerson_Teles-0070F3?style=for-the-badge&logo=googlechrome&logoColor=white)](https://emertels.github.io)
[![Discord](https://img.shields.io/badge/Discord-Emertels%20Server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://emertels.github.io/discord)
[![X / Twitter](https://img.shields.io/badge/X_Twitter-@emertels-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/emertels)
[![YouTube](https://img.shields.io/badge/YouTube-Emerson_Teles-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@emersonteles2379)
[![Telegram](https://img.shields.io/badge/Telegram-Aplicativos%20Mods-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/apksmodsandroid)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Apoiar%20Projeto-FF5E5B?style=for-the-badge&logo=kofi&logoColor=white)](https://ko-fi.com/emertels)

</div>
