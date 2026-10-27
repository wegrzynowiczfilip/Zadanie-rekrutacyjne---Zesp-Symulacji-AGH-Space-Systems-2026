#Rekrutacja AGH Space Systems 2026 - Zespół Symulacji
Projekt rekrutacyjny: symulacja lotu rakiety na paliwo ciekłe w kategorii Liquid 9k na zawody EuRoC. Rakieta bazuje na konstrukcji Turbulencja.

1. rekrutacjav1.ork - projekt rakiety w OpenRocket (wymiary, waga, kształt)
2. zawisza_9k.eng - plik silnika ciekłego Zawisza 9k (krzywa ciągu, 11 sekund pracy)
3. drag_curve.csv - surowe dane oporu powietrza wyciągnięte z OpenRocket
4. clean_drag.py - skrypt w Pythonie usuwający błędy i powtórzenia z danych oporu
5. drag_curve_clean.csv - oczyszczony plik oporu gotowy dla RocketPy
6. sim_6dof.py - główny skrypt symulacji 6-DOF w RocketPy (liczy lot i spadochrony)
7. sensitivity_analysis.py - skrypt sprawdzający wpływ wiatru i kąta pochylenia wyrzutni
8. sim_6dof_results.png - wykres 3D trajektorii lotu rakiety
9. sensitivity_results.png - wykresy pokazujące wpływ wiatru oraz kąta szyny

Wyniki symulacji:
- Prędkość zejścia z szyny: 40,7 m/s (wymóg regulaminu: minimum 30 m/s)
- Wysokość apogeum: 9261 m (cel: 9000 m, naddatek 261m)
- Prędkość maksymalna: Mach 1,48 (482,8 m/s)
- Otwarcie spadochronu głównego: 450m nad ziemią
- Prędkość lądowania: 7,98 m/s (wymóg regulaminu: poniżej 9 m/s)
