import threading

def my_function(obj):
    # Simuliere lange Berechnung
    for i in range(10):
        print(f"Berechne... Schritt {i+1}")
        time.sleep(1)  # Simuliert eine lange Berechnung
    print("Funktion erfolgreich abgeschlossen.")
    return "Ergebnis"

def run_with_timeout(func, args, timeout):
    # Um das Ergebnis des Threads zu speichern
    result = [None]

    # Wrapper-Funktion, um das Ergebnis zu speichern
    def wrapper():
        result[0] = func(*args)

    # Erstellen eines Threads, der die Funktion ausführt
    thread = threading.Thread(target=wrapper)

    # Starten des Threads
    thread.start()

    # Warte auf den Thread für die Timeout-Dauer
    thread.join(timeout=timeout)

    if thread.is_alive():
        # Wenn der Thread immer noch läuft, wird der Timeout gemeldet
        print(f"Timeout nach {timeout} Sekunden erreicht, Funktion wird abgebrochen.")
        return None
    else:
        # Wenn der Thread abgeschlossen ist, gibt das Ergebnis zurück
        return result[0]

# Beispiel für die Verwendung:
import time

# Objekte, die übergeben werden sollen
my_object = "Beispiel"

# Timeout auf 5 Sekunden setzen
result = run_with_timeout(my_function, (my_object,), timeout=5)

print("Ergebnis:", result)