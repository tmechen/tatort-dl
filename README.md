# tatort-dl
Archivierung von Tatort Folgen aus der Mediathek

Mit diesem Script können die aktuell verfügbaren Tatort Folgen (alle Seiten von https://www.daserste.de/unterhaltung/krimi/tatort/videos/index.html) gesichert werden. Zusätzlich zum Download der Folgen werden sie, sofern möglich, mittels der API von TVDB benannt. Mit entsprechenden Änderungen im Script an den Pfaden kann das Tool natürlich auch für jede andere Serie verwendet werden. Dafür müssen GANZE_FOLGEN_URL sowie TVDB_SERIES_ID entsprechend angepasst werden.

### Disclaimer
Hierbei handelt es sich keinesfalls um ein 100% stabiles Archivierungstool, die Fehlerbehandlung ist minimal, die Anpassung auf die ARD Mediathek nur sehr eingeschränkt und nicht abgesichert gegen große Änderungen an der Website.


### .env File
Zur Ausführung wird ein .env File im gleichen Verzeichnis benötigt.
In diesem .env File werden relevante Variablen hinterlegt:
```
TVDB_USER_NAME=""
TVDB_USER_KEY=""
TVDB_API_KEY=""
SAVE_PATH=""
ARCHIV_FILE=""
```


### Benennung mittels TVDB API
benötigt wird ein API Zugang zu TVDB (siehe https://thetvdb.com/api-information) zur Zuordnung.
Egebnis der Benennung ist dann zb `s2018e02_Odenthal-66-Kopper` zur 
* Identifikation der Folge  **02**
* aus dem Jahr  **2018** 
* mit Kommisarin  **Odenthal**
* der  **66**te Folge mit ihr als Kommisarin 
* mit Titel **Kopper**

Gespeichert werden die Dateien in Ordnern gemäß der Season im konfigurierbaren `SAFE_PATH`.
Das Beispiel erzeugt `$SAVE_PATH/Season2018/s2018e02_Odenthal-66-Kopper.mp4`.


### Archiv File
damit das Script zb per cron periodisch ausgeführt werden kann und dabei nicht jede Folge mehrfach heruntergeladen wird, werden die Folgen die bereits vollständig heruntergeladen wurden, in einem Archiv File gelistet. Dieses File kann beliebig angegeben werden mittels `ARCHIV_FILE` im .env File.
