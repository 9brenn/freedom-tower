# Freedom Tower — GTA V Legacy RC1

Konwersja dostarczonego zasobu Robbbs3D do add-on DLC, przygotowana do testu
w grze. Zawiera budynek, plac i dziewięć wnętrz, bez systemu wind.

[Pobierz paczkę GTA V Legacy RC1 — ZIP, 42 MB](https://github.com/9brenn/freedom-tower/raw/refs/heads/main/output/Freedom_Tower_GTA_V_Legacy_RC1.zip)

[Instrukcja instalacji po polsku](docs/INSTALACJA_PL.txt) · [Raport kontroli](docs/RAPORT.txt) · [SHA-256](output/Freedom_Tower_GTA_V_Legacy_RC1.zip.sha256)

Wymagane MP Maps w Story Mode oraz oryginalne zasoby DLC gry, w tym
mpsecurity (Legacy build 2545+). Opcjonalny helper wymaga Script Hook V
i ScriptHookVDotNet v3.7.0-nightly.198 lub zgodnej nowszej wersji API v3.

Nie wykonano testu w GTA V. Brakującego w źródle `gtxd.meta` nie odtworzono
przez zgadywanie. Nie instalowano wadliwego globalnego manifestu scenariuszy
1604 ani jego trzech regionów NPC. To pozostaje do weryfikacji w grze.

Narzędzia w `tools/` dokumentują lokalny proces przygotowania i budowy RPF.
Obecnie korzystają z wejścia/XML i narzędzi CodeWalker zachowanych pod
`/workspace/conversion` oraz `/workspace/tools/CodeWalker` w tym środowisku;
nie są samodzielnym konwerterem dowolnych zasobów FiveM.
Oryginalne pliki źródłowe pozostały niezmienione poza repozytorium.
