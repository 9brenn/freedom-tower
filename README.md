# Freedom Tower — GTA V Legacy RC2

**RC1 ma zgłoszony crash podczas ładowania Story Mode w Legacy 1.0.3889.0.**
RC2 usuwa zbędną kopię stockowych definicji biura Agency oraz ich ponowną
rejestrację. Przyczyna awarii i skuteczność tej zmiany wymagają testu w grze.

[Pobierz RC2 — kandydat poprawki zgodności, ZIP 42 MB](https://github.com/9brenn/freedom-tower/raw/refs/heads/main/output/Freedom_Tower_GTA_V_Legacy_RC2.zip)

[Instrukcja instalacji i testu](docs/INSTALACJA_PL.txt) · [Zmiany RC2](docs/RC2_ZMIANY.txt) · [Raport kontroli](docs/RAPORT.txt)

Najpierw sprawdź wczytanie Story Mode bez wpisu `freedomtower` w `dlclist.xml`.
Następnie zamknij grę, podmień cały `dlc.rpf` na RC2, przywróć jeden wpis i
wykonaj próbę **bez loadera DLL i bez aktywowania MP Maps**.
Jeśli gra się wczyta, dopiero potem sprawdź właściwy wygląd z MP Maps.
Jeśli pełne RC2 nadal zamyka grę, można sprawdzić samą aktywację dodatku:

[Mała paczka diagnostyczna — bez budynku](https://github.com/9brenn/freedom-tower/raw/refs/heads/main/output/Freedom_Tower_TEST_LADOWANIA.zip)

Instrukcja próby i przywrócenia pełnego DLC jest w `TEST_PL.txt` tej paczki.
Nie instaluj obydwu paczek jednocześnie; podmieniają ten sam `dlc.rpf`.
RC1 pozostaje w `output/` wyłącznie do porównania z wcześniejszą wersją.

Konwersja dostarczonego zasobu Robbbs3D do add-on DLC zachowuje budynek, plac
oraz 9 rozmieszczeń wnętrz, bez systemu wind. Własne modele i mapy rozmieszczeń
nie zmieniły się między RC1 a RC2. Biuro Agency korzysta z oryginalnego mpsecurity.

Do właściwego wyglądu wymagane są MP Maps w Story Mode i oryginalne DLC gry,
w tym mpsecurity (Legacy build 2545+). Opcjonalny helper wymaga Script Hook V
i ScriptHookVDotNet v3.7.0-nightly.198 lub zgodnej nowszej wersji API v3.
Na czas diagnozy ładowania pozostaw helper wyłączony.

Nie wykonano testu w uruchomionym GTA V. Brakuje źródłowego `gtxd.meta`;
nie odtwarzano go przez zgadywanie. Nie instalowano wadliwego globalnego
manifestu scenariuszy 1604 ani jego trzech regionów NPC.

Narzędzia w `tools/` dokumentują lokalny proces przygotowania i budowy RPF.
Korzystają z wejścia/XML i narzędzi CodeWalker zachowanych pod
`/workspace/conversion` oraz `/workspace/tools/CodeWalker` w tym środowisku.
Domyślny katalog wyników to `/workspace/conversion/rc2`, zmieniany przez
`FREEDOM_TOWER_BUILD_DIR`. Nie jest to samodzielny konwerter dowolnych zasobów.
Oryginalne pliki źródłowe pozostały niezmienione poza repozytorium.
