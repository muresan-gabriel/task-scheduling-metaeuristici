# Algoritmi metaeuristici și aplicații

## Task Scheduling (Alocare de Sarcini) cu Algoritm Genetic

Dancs Cătălina
Mureșan Gabriel

### 1. Introducere

Problema Alocării de Sarcini (Task Scheduling Problem) se referă la distribuirea unui set de sarcini către mai multe resurse (cum ar fi procesoare, oameni sau mașini), având ca scop optimizarea unui obiectiv specific. De exemplu, poate fi vorba despre reducerea timpului total necesar pentru finalizarea tuturor sarcinilor, folosirea cât mai eficientă a resurselor sau scăderea costurilor. Fiind o problemă complexă (NP-hard), găsirea celei mai bune soluții devine foarte dificilă pe măsură ce crește numărul de sarcini și resurse implicate.

Aici intră în joc Algoritmii Genetici (GA), o metodă inspirată din natura, care imită procesul de evoluție. În acest context, soluțiile posibile sunt tratate ca indivizi dintr-o populație, care "evoluează" prin selecție, combinare (crossover) și mutație. În cazul problemei de alocare de sarcini, soluțiile reprezintă diferite moduri în care sarcinile pot fi distribuite resurselor, iar aceste operații genetice sunt adaptate astfel încât să respecte toate regulile problemei.

Algoritmii genetici sunt o alegere grozavă pentru alocarea de sarcini, deoarece pot explora rapid un spațiu mare de soluții și găsesc variante bune chiar și atunci când problema devine complicată. În acest proiect, o să implementăm un Algoritm Genetic în Python pentru această problemă, analizând cum diferiți parametri ai algoritmului influențează rezultatele și performanța acestuia.

### 2. Problema de rezolvat

Problema Alocării de Sarcini (Task Scheduling) poate fi abordată eficient folosind Algoritmi Genetici (GA), iar Python oferă toate instrumentele necesare pentru implementare. GA este ideal pentru astfel de probleme deoarece poate găsi soluții de calitate într-un timp rezonabil, chiar și pentru cazuri complexe cu multe sarcini și resurse.

**Despre Algoritmul Genetic pentru Task Scheduling**

Scopul algoritmului reprezintă distribuirea unui set de sarcini pe mai multe resurse (ex. mașini virtuale) astfel încât să se minimizeze penalizările pentru utilizarea excesivă a resurselor sau sarcinile nealocate.

Pași principali:

1. Inițializare: Generăm o populație de soluții inițiale, fiecare fiind o alocare aleatorie de sarcini pe resurse.
2. Evaluarea Fitness-ului: Calculăm penalizările fiecărei soluții (ex. depășirea resurselor).
3. Selecție: Alegem soluțiile bune pentru reproducere.
4. Încrucișare (Crossover): Generăm soluții noi combinând părinți selectați.
5. Mutație: Introducem mici modificări pentru a crește diversitatea populației.
6. Iterație: Repetăm pașii până ajungem la o soluție acceptabilă sau se atinge numărul maxim de generații.
7. Codul Python pentru Task Scheduling cu GA
8. Codul de mai sus este un exemplu complet de implementare a unui algoritm genetic pentru alocarea de sarcini. Iată principalele componente ale algoritmului:

### **Formularea matematică a problemei de Alocare de Sarcini**

**Problema de Alocare de Sarcini** poate fi formalizată astfel:

Fie:
- \( M = \{m_1, m_2, \dots, m_k\} \): un set de **resurse** (mașini sau procesoare), fiecare cu o capacitate limitată de:
  - RAM: \( \text{RAM}(m_i) \)
  - CPU: \( \text{CPU}(m_i) \)
  - Stocare: \( \text{Storage}(m_i) \)
- \( T = \{t_1, t_2, \dots, t_n\} \): un set de **sarcini**, fiecare cu un set de cerințe:
  - RAM necesar: \( \text{RAM}(t_j) \)
  - CPU necesar: \( \text{CPU}(t_j) \)
  - Stocare necesară: \( \text{Storage}(t_j) \)

**Decizie:**  
Fiecare sarcină \( t_j \) trebuie atribuită unei resurse \( m_i \), notată ca \( x_{ij} \), unde:
\[
x_{ij} =
\begin{cases}
1, & \text{dacă sarcina } t_j \text{ este atribuită resursei } m_i \\
0, & \text{altfel.}
\end{cases}
\]

**Constrângeri:**
1. Fiecare sarcină este atribuită exact unei resurse:
\[
\sum_{i=1}^{k} x_{ij} = 1, \quad \forall j \in \{1, 2, \dots, n\}.
\]
2. Cerințele totale ale sarcinilor atribuite unei resurse nu trebuie să depășească capacitățile resursei:
\[
\sum_{j=1}^{n} x_{ij} \cdot \text{RAM}(t_j) \leq \text{RAM}(m_i), \quad \forall i \in \{1, 2, \dots, k\},
\]
\[
\sum_{j=1}^{n} x_{ij} \cdot \text{CPU}(t_j) \leq \text{CPU}(m_i), \quad \forall i \in \{1, 2, \dots, k\},
\]
\[
\sum_{j=1}^{n} x_{ij} \cdot \text{Storage}(t_j) \leq \text{Storage}(m_i), \quad \forall i \in \{1, 2, \dots, k\}.
\]

**Funcția de optimizare:**  
Scopul este minimizarea penalităților pentru:
1. Depășirea resurselor.
2. Sarcinile care rămân nealocate.

Funcția de cost poate fi definită astfel:
\[
\text{Cost} = \sum_{i=1}^{k} \left( \max\left(0, \sum_{j=1}^{n} x_{ij} \cdot \text{RAM}(t_j) - \text{RAM}(m_i) \right) + \max\left(0, \sum_{j=1}^{n} x_{ij} \cdot \text{CPU}(t_j) - \text{CPU}(m_i) \right) + \max\left(0, \sum_{j=1}^{n} x_{ij} \cdot \text{Storage}(t_j) - \text{Storage}(m_i) \right) \right) + P_{\text{nealocate}}.
\]

Aici, \( P_{\text{nealocate}} \) este penalitatea pentru sarcinile care nu au fost atribuite niciunei resurse.

**Reprezentare în Algoritmul Genetic:**  
- **Cromozom:** O listă \( [x_1, x_2, \dots, x_n] \), unde fiecare \( x_j \) reprezintă resursa \( m_i \) la care este alocată sarcina \( t_j \).
- **Fitness:** Inversul funcției de cost:
\[
\text{Fitness} = \frac{1}{1 + \text{Cost}}.
\]

**Operatori genetici:**
1. **Selecție:** Soluțiile cu fitness mai mare au șanse mai mari să fie selectate.
2. **Încrucișare:** Două soluții (părinți) generează descendenți prin schimbarea unor secțiuni din cromozomi.
3. **Mutație:** O parte din sarcini sunt reasignate aleatoriu altor resurse pentru a explora noi soluții.


**2.1. Utilizarea Python pentru rezolvarea problemei**

****

### 3. Metoda de rezolvare


### 4. Rezultate

### 5. Concluzii