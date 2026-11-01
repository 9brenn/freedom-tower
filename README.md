# Freedom Tower — GTA V Legacy RC3 MAP

**RC1 i RC2 zamykały Story Mode w zgłoszonej instalacji Legacy 1.0.3889.0.**
RC3 przebudowuje sposób rejestracji dodatku według układu map Single Player.
Nie ma jeszcze potwierdzenia uruchomienia RC3 w grze.

[Pobierz RC3 MAP — ZIP 42 MB](https://github.com/9brenn/freedom-tower/raw/refs/heads/main/output/Freedom_Tower_GTA_V_Legacy_RC3_MAP.zip)

[Instalacja i próba uruchomienia](docs/INSTALACJA_PL.txt) · [Zmiany RC3 i wyniki](docs/RC3_ZMIANY.txt) · [Podstawa techniczna](docs/RUNTIME_REFERENCES.md)

RC3 używa `EXTRACONTENT_LEVEL_PACK`, `GROUP_UPDATE_STREAMING` i osobnego
archiwum `CONTENTS_DLC_MAP_DATA`. Usunięto wymuszone żądania YTYP przy starcie,
które występowały równocześnie z żądaniami manifestu. Kod FiveM uzgadnia te dwa
mechanizmy; zwykły Single Player nie zapewnia tych napraw. Nie oznacza to
jeszcze ustalenia dokładnej przyczyny crasha z instalacji użytkownika.

Zachowano wszystkie modele i rozmieszczenie 9 wnętrz: hol, garaż,
4 apartamenty i 3 biura. W dwóch definicjach wyczyszczono sześć odwołań do
nieistniejących własnych physicsDictionary; kolizje wieżowca i wnętrz zachowano.
Biuro Agency korzysta z oryginalnego mpsecurity gry.

Zamknij grę i podmień **cały** plik `mods/update/x64/dlcpacks/freedomtower/dlc.rpf`.
Zachowaj jeden wpis `<Item>dlcpacks:/freedomtower/</Item>` w aktywnym dlclist.xml.
Sprawdź ASI Loader i OpenIV.asi w ASI Manager. Pierwszą próbę uruchomienia
wykonaj bez opcjonalnego loadera DLL i bez zmieniania innych modów/gameconfig.

Do właściwego widoku budynku po wczytaniu Story Mode wymagane jest MP Maps,
włączone trainerem lub opcjonalnym loaderem. Wymagane oryginalne zasoby DLC
Legacy 2545+ (m.in. mpapartment, mpexecutive, mpsecurity). Brak skryptu wind;
do oględzin wyższych pięter można użyć noclip. Szczegóły są w instrukcji.

Jeśli nadal występuje awaria, do rozróżnienia instalacji/ASI od pełnych zasobów
potrzebny jest wynik małej paczki bez budynku:

[Pobierz TEST_LADOWANIA — około 2 KB](https://github.com/9brenn/freedom-tower/raw/refs/heads/main/output/Freedom_Tower_TEST_LADOWANIA.zip)

Instrukcja podmiany i przywrócenia pełnego dodatku znajduje się w tym ZIP.
Nie instaluj jej obok pełnej paczki. Dotychczasowe RC1/RC2 pozostają w
`output/` wyłącznie jako materiał porównawczy, z potwierdzonym zgłoszeniem awarii.

Kontrole RC3: ponowny odczyt RPF i zasobów, niezależny dekoder układu,
porównanie wszystkich plików z RC2 oraz kontrola danych geometrii i zależności.
Nie wykonano testu w GTA V. Nie potwierdzono stabilności, wyglądu, ruchu NPC ani
zgodności z innymi modami. Brakuje źródłowego `gtxd.meta`; nie zgadywano jego
zawartości. Wadliwy manifest scenariuszy 1604 i trzy regiony NPC są poza paczką.

Narzędzia w `tools/` korzystają z wejścia/XML i CodeWalker zachowanych pod
`/workspace/conversion` oraz `/workspace/tools/CodeWalker` w tym środowisku.
Domyślny katalog wyników to `/workspace/conversion/rc3`, zmieniany przez
`FREEDOM_TOWER_BUILD_DIR`. Oryginalne pliki wejściowe pozostają niezmienione.
`verify_rc2.py` i dokumenty oznaczone RC2 są historycznym porównaniem RC1–RC2.
