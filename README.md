# Animacija-vektorskih-polj

Projekt pri predmetu Matematika z računalnikom na FMF je narejen po vzoru na [Vector field](https://anvaka.github.io/fieldplay/).

Animacija vektorskih polj je interaktivno orodje za vizualizacijo vektorskih pol in dinamičnih sistemov s pomočjo animiranih delcev.

# Kaj počne?

Vsaki toči v ravnini priredi vektor hitrosti, ki je definiran kot vektorsko polje. Tiste točke predstavimo z delci, ki se začnejo gibati, ko se dotaknejo vektorskega polja. Smer in hitrost delca sta določeni z vektorskim poljem. Na ta način lahko vizualiziramo geometrijo in dinamiko polja. To nam lahko pomaga razumeti stabilnost, privlačnost in druge lastnosti sistema. Zelo pogosto pa dobimo lepe in zanimive vzorce gibanja.

# Zanimivi primeri

Vizualno zanimivi primeri vektorskih polj se nahajajo v *pendulum.py*, *chaos.py* in *lorenz.py* ter *lorenz_rot.py*. Vsaka vizualizacija prikazuje delce, ki se premikajo po definiranem vektorskem polju. Ostale kode so uporabljene za raziskavo obnašanja delcev.

Vizualizacija temelji na:
- numeričnih integracijah s pomočjo Eulerjeve metode in Runge-Kutta
- projekciji 2D ali 3D gibanja na zaslon
- barvnih kodah, ki dajejo estetski in interpretacijski pomen
- sprotnem gibanju množice delcev

# Ideje za nadgradnjo

Temu projektu bi lahko dodala še
- **Uporabniški vmesnik** - na ta način bi lahko uporabniki vnašali enačbe vektorskih polj in bi lahko spreminjali polja v realnem času;
- **Eksport grafičnih prikazov** v GIF ali video formatu;
- **Animacije za različne matematične modele**.

# Zahvala
Navdih za vizualizacijski pristop je prišel iz projekta *Field Play*, ki je raziskovalno orodje za vektorska polja in vizualno interakcijo s polji preko delcev (ta repozitorij uporablja GLSL/WebGL ter deluje v brskalniku).