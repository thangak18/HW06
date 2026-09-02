# capture_screenshots.ps1 — chup man hinh cho tung ma loi (yeu cau muc 6 de bai)
#
# Day la script da tao ra 24 anh trong bugs/screenshots/. Luu trong repo de
# nguoi cham tai lap duoc, va de quy trinh minh bach.
#
# CACH HOAT DONG
#   1. Mo mot cua so Windows Terminal moi, hien thi noi dung that cua
#      bugs/evidence/per_bug/<MA-LOI>.txt — von cat ra tu output cua lan chay
#      that `bash bugs/reproduce_bugs.sh` tren SUT.
#   2. Dua cua so len tren cung bang SetWindowPos(HWND_TOPMOST).
#   3. Chup TOAN BO man hinh bang Graphics.CopyFromScreen — doc pixel truc tiep
#      tu man hinh, dung co che ma Snipping Tool dung. Day la anh chup that,
#      khong phai anh ve lai bang thu vien do hoa.
#
# HAI CACH DA THU VA THAT BAI (ghi lai de khoi thu lai)
#   - SetForegroundWindow: tien trinh nen khong co quyen foreground nen goi
#     khong an, ket qua la chup nham cua so dang nam tren.
#   - PrintWindow(PW_RENDERFULLCONTENT): Windows Terminal ve bang GPU/DirectX
#     nen tra ve anh den kit.
#
# Usage:
#   powershell -File bugs/capture_screenshots.ps1 -Bug BUG-A1-01 `
#       -SrcFile bugs/evidence/per_bug/chunks/BUG-A1-01.part1.txt `
#       -OutFile bugs/screenshots/BUG-A1-01.png

param(
    [Parameter(Mandatory = $true)][string]$SrcFile,   # file van ban can hien thi
    [Parameter(Mandatory = $true)][string]$OutFile,   # duong dan anh PNG ghi ra
    [string]$Name = ""                                # nhan hien tren tab terminal
)

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

if (-not ([System.Management.Automation.PSTypeName]'Win32Api').Type) {
    Add-Type @"
using System;
using System.Runtime.InteropServices;
public struct RECT { public int Left, Top, Right, Bottom; }
public class Win32Api {
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
    // PrintWindow chup dung noi dung cua MOT cua so, ke ca khi no bi cua so
    // khac che. CopyFromScreen doc pixel dang hien tren man hinh nen se chup
    // nham cua so dang nam tren.
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
    // SetWindowPos voi HWND_TOPMOST dua cua so len tren cung ma KHONG can quyen
    // foreground — thu ma SetForegroundWindow doi hoi va tien trinh nen khong co.
    [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
}
"@
}

$src = $SrcFile
if (-not (Test-Path $src)) { throw "Khong thay $src" }
if (-not $Name) { $Name = [IO.Path]::GetFileNameWithoutExtension($OutFile) }

# nhan duy nhat de tim lai dung cua so vua mo
$marker = "BANGCHUNG-$Name"
$slug   = ($Name -replace '[^A-Za-z0-9]', '_')
# Dem so dong SAU khi xuong dong o 80 cot, de chieu cao cua so vua khit noi dung
$lineCount = 0
foreach ($l in (Get-Content -LiteralPath $src -Encoding UTF8)) {
    $lineCount += [Math]::Max(1, [Math]::Ceiling($l.Length / 80.0))
}
$rows = [Math]::Min(24, [Math]::Max(10, $lineCount + 2))

# Script chay ben trong cua so console moi
$inner = Join-Path $env:TEMP "shoot_inner_$slug.ps1"
@"
chcp 65001 > `$null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
`$Host.UI.RawUI.WindowTitle = '$marker'
try {
    `$b = `$Host.UI.RawUI.BufferSize; `$b.Width = 116; `$b.Height = 400
    `$Host.UI.RawUI.BufferSize = `$b
    `$w = `$Host.UI.RawUI.WindowSize; `$w.Width = 116; `$w.Height = $rows
    `$Host.UI.RawUI.WindowSize = `$w
} catch { }
Clear-Host
# Tu xuong dong o 80 cot: cua so terminal hep hon buffer nen dong dai se bi
# cat mat ben phai neu de terminal tu cuon ngang.
Get-Content -LiteralPath '$src' -Encoding UTF8 | ForEach-Object {
    `$l = `$_
    while (`$l.Length -gt 80) { `$l.Substring(0, 80); `$l = '  ' + `$l.Substring(80) }
    `$l
}
Start-Sleep -Seconds 120
"@ | Out-File -FilePath $inner -Encoding utf8 -Force

cmd /c start "" powershell.exe -NoProfile -NoLogo -ExecutionPolicy Bypass -File "$inner"

# Tim cua so mang dung tieu de da dat
$hwnd = [IntPtr]::Zero
for ($i = 0; $i -lt 80; $i++) {
    Start-Sleep -Milliseconds 250
    $win = Get-Process -ErrorAction SilentlyContinue |
           Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -like "*$marker*" } |
           Select-Object -First 1
    if ($win) { $hwnd = $win.MainWindowHandle; $winProc = $win; break }
}
if ($hwnd -eq [IntPtr]::Zero) {
    Remove-Item $inner -Force -ErrorAction SilentlyContinue
    throw "Khong tim thay cua so mang tieu de $marker"
}

[void][Win32Api]::ShowWindow($hwnd, 5)
[void][Win32Api]::SetForegroundWindow($hwnd)

# Do kich thuoc that roi dua cua so len tren cung tai goc trai man hinh,
# de khong co cua so nao che mat luc chup.
$r = New-Object RECT
[void][Win32Api]::GetWindowRect($hwnd, [ref]$r)
$w = $r.Right - $r.Left
$h = $r.Bottom - $r.Top
if ($w -le 0 -or $h -le 0) { throw "Kich thuoc cua so khong hop le: ${w}x${h}" }

# Windows Terminal bo qua $Host.UI.RawUI.WindowSize nen phai dat kich thuoc
# bang PIXEL. Cac hang so do tu anh chup thu: chrome tab ~62px, moi dong ~28px.
# Chieu cao tinh vua khit noi dung va KHONG che thanh tac vu, de dong ho he
# thong con nam trong anh lam moc thoi gian doi chung.
$winW = 1180
$winH = 62 + 25 + ($rows * 28) + 15

$HWND_TOPMOST = [IntPtr](-1)
$SWP_SHOWWINDOW = 0x0040
[void][Win32Api]::SetWindowPos($hwnd, $HWND_TOPMOST, 50, 20, $winW, $winH, $SWP_SHOWWINDOW)
Start-Sleep -Milliseconds 1500          # doi terminal ve xong noi dung

# Chup TOAN BO man hinh, khong cat rieng cua so terminal: anh giu lai ca ngu
# canh lam viec that (thanh tac vu, dong ho he thong, cac cua so khac) nen
# nguoi cham doi chieu duoc moc thoi gian, giong anh chup Postman Console.
# Windows Terminal ve bang GPU nen PrintWindow tra ve anh den; phai doc pixel
# that tu man hinh. Cua so da duoc dat TOPMOST nen chac chan khong bi che.
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$w = $screen.Width
$h = $screen.Height

$bmp = New-Object System.Drawing.Bitmap($w, $h)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($screen.X, $screen.Y, 0, 0, (New-Object System.Drawing.Size($w, $h)))
$g.Dispose()

$outDir = Split-Path -Parent $OutFile
if ($outDir -and -not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
$out = $OutFile
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()

# Dong cua so va don file tam
Stop-Process -Id $winProc.Id -Force -ErrorAction SilentlyContinue
Get-Process powershell -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*shoot_inner_$slug*" } |
    Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 200
Remove-Item $inner -Force -ErrorAction SilentlyContinue

"{0}  {1}x{2}" -f $Name, $w, $h
