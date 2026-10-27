' Launcher silencioso para Xbox 360 Calibration Tool v1.0.0
' Executa a ferramenta sem abrir janela preta de console (CMD)
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
mainScript = scriptDir & "\main.py"

localAppData = WshShell.ExpandEnvironmentStrings("%LOCALAPPDATA%")
programFiles = WshShell.ExpandEnvironmentStrings("%ProgramFiles%")

Dim pythonwCandidates(6)
pythonwCandidates(0) = localAppData & "\Programs\Python\Python312\pythonw.exe"
pythonwCandidates(1) = localAppData & "\Programs\Python\Python313\pythonw.exe"
pythonwCandidates(2) = localAppData & "\Programs\Python\Python311\pythonw.exe"
pythonwCandidates(3) = localAppData & "\Programs\Python\Python310\pythonw.exe"
pythonwCandidates(4) = programFiles & "\PyManager\pythonw.exe"
pythonwCandidates(5) = "C:\Users\Emerson Teles\AppData\Local\Programs\Python\Python312\pythonw.exe"
pythonwCandidates(6) = "pythonw.exe"

Dim chosenPython, i
chosenPython = ""

For i = 0 To 5
    If fso.FileExists(pythonwCandidates(i)) Then
        chosenPython = pythonwCandidates(i)
        Exit For
    End If
Next

If chosenPython = "" Then
    chosenPython = "pythonw.exe"
End If

WshShell.CurrentDirectory = scriptDir
On Error Resume Next
WshShell.Run """" & chosenPython & """ """ & mainScript & """", 0, False

If Err.Number <> 0 Then
    Err.Clear
    WshShell.Run "pyw -3 """ & mainScript & """", 0, False
    If Err.Number <> 0 Then
        MsgBox "Nao foi possivel localizar o Python 3 instalado no sistema!" & vbCrLf & _
               "Por favor, instale o Python 3 marcando 'Add python.exe to PATH':" & vbCrLf & _
               "https://www.python.org/downloads/", vbCritical, "Xbox 360 Calibration Tool"
    End If
End If

Set WshShell = Nothing
Set fso = Nothing
