# qsim - Polski Przewodnik

<div align="center">

# qsim

Wysokowydajny symulator obwodów kwantowych dla C++ i Python.

[English README](README.md) | [Polski README](README_PL.md)

</div>

_qsim_ jest symulatorem wektora stanu dla obwodów kwantowych. Reprezentuje stan kwantowy jako wektor amplitud o wartościach zespolonych i stosuje mnożenie macierz-wektor do symulacji transformacji, które ewoluują stan w czasie.

## Funkcje

qsim jest _pełnym_ symulatorem wektora stanu, co oznacza, że oblicza wszystkie _2<sup>n</sup>_ amplitudy wektora stanu, gdzie _n_ jest liczbą kubitów.

*   Aby przyspieszyć symulację, qsim używa fuzji bramek, arytmetyki pojedynczej precyzji, instrukcji AVX/FMA do wektoryzacji oraz OpenMP do wielowątkowości.

*   qsim jest wysoce zoptymalizowany, aby wykorzystać zestawy instrukcji arytmetycznych wektorowych i wielowątkowość na komputerach, które je zapewniają, a także GPU, gdy są dostępne.

*   qsim zawiera interfejs [Cirq](https://quantumai.google/cirq) (`qsimcirq`) i może być używany do symulacji obwodów kwantowych napisanych w Cirq.

## Instalacja

### Instalacja Python

Interfejs Python qsim-Cirq nazywa się `qsimcirq` i jest dostępny jako pakiet PyPI dla użytkowników Linux, MacOS i Windows:

```shell
pip install qsimcirq
```

### Wymagania

qsimcirq wymaga Python 3.10 lub nowszego. Wszystkie wymagane zależności zostaną automatycznie zainstalowane podczas instalacji.

## Szybki Start

### Twój Pierwszy Obwód Kwantowy

Oto prosty przykład, który pomoże Ci zacząć:

```python
import cirq
import qsimcirq

# Utwórz prosty obwód kwantowy z 2 kubitami
q0, q1 = cirq.LineQubit.range(2)

# Zbuduj obwód
circuit = cirq.Circuit(
    cirq.H(q0),           # Bramka Hadamarda na kubicie 0
    cirq.CNOT(q0, q1),    # Bramka CNOT
    cirq.measure(q0, q1, key='wynik')  # Zmierz oba kubity
)

print("Obwód:")
print(circuit)

# Utwórz symulator qsim
simulator = qsimcirq.QSimSimulator()

# Uruchom symulację
result = simulator.run(circuit, repetitions=10)

print("\nWyniki:")
print(result)
```

## Przykłady

Katalog `examples/` zawiera przyjazne dla początkujących przykłady:

### 1. basic_circuit.py - Podstawowy Obwód
Prosty wprowadzenie do obwodów kwantowych pokazujące:
- Jak tworzyć kubity
- Jak stosować podstawowe bramki kwantowe
- Jak symulować i mierzyć wyniki

**Uruchom**: `python3 examples/basic_circuit.py`

### 2. bell_state.py - Stan Bella
Tworzenie i weryfikacja stanu Bella (maksymalnie splątany stan kwantowy):
- Splątanie kwantowe
- Bramki Hadamarda i CNOT
- Korelacje pomiarów

**Uruchom**: `python3 examples/bell_state.py`

### 3. quantum_teleportation.py - Teleportacja Kwantowa
Implementacja protokołu teleportacji kwantowej:
- Zaawansowane protokoły kwantowe
- Operacje wielokubitowe
- Komunikacja klasyczna z operacjami kwantowymi

**Uruchom**: `python3 examples/quantum_teleportation.py`

## Dokumentacja

### Przewodniki dla Początkujących
- **QUICKSTART.md**: Przewodnik szybkiego startu (po angielsku)
- **examples/**: Przykładowe skrypty z komentarzami
- **docs/tutorials/**: Interaktywne notebooki Jupyter

### Szczegółowa Dokumentacja
- **docs/usage.md**: Szczegółowe instrukcje użytkowania
- **docs/cirq_interface.md**: Praca z Cirq
- **docs/install_qsimcirq.md**: Szczegóły instalacji
- **Strona dokumentacji**: https://quantumai.google/qsim

## Zaawansowane Użycie

### Przyspieszenie GPU
Jeśli masz GPU zgodne z CUDA, qsim automatycznie je wykryje i użyje dla lepszej wydajności.

### Symulacja Większych Obwodów
Dla obwodów z wieloma kubitami możesz dostosować parametry symulacji:

```python
simulator = qsimcirq.QSimSimulator(
    qsim_options=qsimcirq.QSimOptions(
        max_fused_gate_size=4,  # Kontrola fuzji bramek
        cpu_threads=8           # Liczba wątków CPU
    )
)
```

### Użycie C++
Kod jest zaprojektowany jako biblioteka, która może być włączona do aplikacji użytkowników. Przykładowe aplikacje znajdują się w katalogu [apps](https://github.com/quantumlib/qsim/tree/main/apps).

## Testowanie

Aby zbudować i uruchomić wszystkie testy:

```shell
make run-tests
```

Aby uruchomić tylko testy C++ lub Python:
```shell
make run-cxx-tests  # Tylko testy C++
make run-py-tests   # Tylko testy Python
```

## Typowe Problemy

### Błąd Importu
Jeśli otrzymujesz błąd importu, upewnij się, że qsimcirq jest zainstalowany:
```bash
pip3 install --upgrade qsimcirq
```

### Problemy z Wydajnością
Dla dużych obwodów rozważ:
- Użycie przyspieszenia GPU (jeśli dostępne)
- Dostosowanie liczby wątków CPU
- Użycie symulatora qsimh (hybrydowego) dla bardzo dużych obwodów

## Pomoc

- **Dokumentacja**: https://quantumai.google/qsim
- **Problemy**: Zgłoś błędy lub zadaj pytania na GitHub
- **Email**: quantum-oss-maintainers@google.com

## Cytowanie qsim

Podczas publikowania artykułów lub pisania o qsim, proszę cytować używaną wersję qsim. Używamy Zenodo do przechowywania wydań. Odwiedź [stronę qsim na Zenodo](https://doi.org/10.5281/zenodo.4023103) aby uzyskać rekordy bibliograficzne.

## Kontakt

W przypadku pytań lub wątpliwości, które nie zostały tutaj omówione, wyślij email na adres quantum-oss-maintainers@google.com.

## Zastrzeżenie

To nie jest oficjalnie wspierany produkt Google. Ten projekt nie kwalifikuje się do [Google Open Source Software Vulnerability Rewards Program](https://bughunters.google.com/open-source-security).

Copyright 2019 Google LLC.

---

**Dziękujemy za używanie qsim! Miłego programowania kwantowego! 🎯**
