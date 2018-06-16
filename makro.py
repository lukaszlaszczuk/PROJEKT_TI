from datetime import datetime
from xlwings import Book
import matplotlib.pyplot as plt



def clear_data():
 
    # Nazwa arkusza źródłowego
    sheet_name = "Klient"
    # Nazwa arkusza na wyniki
    output = "KlientC"
    # Inicjujemy aktywny skoroszyt, aby inne funkcje wiedziały skąd brać dane
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Book.caller
    wb = Book.caller()
    # Próbujemy usunąć arkusz, ignorujemy błąd, jeśli nie istniał
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Book.sheets
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Sheet.delete
    try:
        wb.sheets[output].delete()
    except:
        pass
    # Tworzymy nowy arkusz o zadanej nazwie
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.main.Sheets.add
    wb.sheets.add(output, after=sheet_name)
    # Wybiera aktywny arkusz (właśnie utworzony)
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.main.Sheets.active
    sheet = wb.sheets.active
    # Wyciągnięcie największego obiektu `Range` zawierającego `A1` ale nie zawierającego pustych pól
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.current_region
    table = wb.sheets[sheet_name].range('A1').current_region
    # wyciągnięcie wartości (dane osobowe z kolumny A, daty z B i numery klienta z C)
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.options
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.value
    [names, dates, ids] = table.options(transpose=True).value
    # wyrzucamy stare nagłówki tabeli
    names = names[1:]
    dates = dates[1:]
    ids = ids[1:]
    # inicjalizacja zmiennych na podzielone dane
    firstnames = []
    surnames = []
    # przechodzimy po wszystkich osobach
    for data in names:
        # dzielimy napisy na spacjach, wyrzucamy puste, powiększamy 1. literę
        parts = [part.capitalize() for part in data.split(" ") if part]
        # zapamiętanie danych
        firstnames.append(" ".join(parts[:-1]))
        surnames.append(parts[-1])
    # zmiana formatu dat na obiekt `datetime`
    dates = [datetime.strptime(data, '%d-%m-%Y') for data in dates]

    #dodajemy wiek
    starosc = []
    for data in dates:
        starosc.append( datetime.today().year - data.year ) #append dodaje do listy nowy wiek

    # Nagłówek tabeli
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.color
    sheet.range('A1:E1').value = ["Imię", "Nazwisko", "Data", "Numer", "Wiek"]
    sheet.range('A1:E1').color = (150, 150, 150)
    # Wpisanie danych do tabeli
    sheet.range('A2').options(transpose=True).value = firstnames
    sheet.range('B2').options(transpose=True).value = surnames
    sheet.range('C2').options(transpose=True).value = dates
    sheet.range('D2').options(transpose=True).value = ids
    sheet.range('E2').options(transpose=True).value = starosc

#################################################

    wiekklientow = []
    for i in range(len(starosc)):
        wiekklientow.append(starosc[i])

###################################################3
    indeksyklientow =[]
    for i in range(len(firstnames)):
        indeksyklientow.append(ids[i])

    imionaklientow = []
    for i in range(len(firstnames)):
        imionaklientow.append(firstnames[i])

    nazwiskaklientow = []
    for i in range(len(surnames)):
        nazwiskaklientow.append(surnames[i])
    # Ustawienie rozmiaru
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.autofit
    sheet.range('A1').current_region.autofit()


    # Nazwa arkusza źródłowego
    sheet_name = "Zakupy"
    # Nazwa arkusza na wyniki
    output = "ZakupyC"
    # Inicjujemy aktywny skoroszyt, aby inne funkcje wiedziały skąd brać dane
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Book.caller
    wb = Book.caller()
    # Próbujemy usunąć arkusz, ignorujemy błąd, jeśli nie istniał
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Book.sheets
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Sheet.delete
    try:
        wb.sheets[output].delete()
    except:
        pass
    # Tworzymy nowy arkusz o zadanej nazwie
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.main.Sheets.add
    wb.sheets.add(output, after=sheet_name)
    # Wybiera aktywny arkusz (właśnie utworzony)
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.main.Sheets.active
    sheet = wb.sheets.active
    # Wyciągnięcie największego obiektu `Range` zawierającego `A1` ale nie zawierającego pustych pól
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.current_region
    table = wb.sheets[sheet_name].range('A1').current_region
    # wyciągnięcie wartości (dane osobowe z kolumny A, daty z B i numery klienta z C)
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.options
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.value
    [idshopping, dates, sizes, costs] = table.options(transpose=True).value
    # wyrzucamy stare nagłówki tabeli
    idshopping = idshopping[1:]
    dates = dates[1:]
    sizes = sizes[1:]
    costs = costs[1:]
    # zmiana formatu dat na obiekt `datetime`
    dates = [datetime.strptime(data, '%d.%m.%Y') for data in dates]
    ostatni_data=datetime.strptime(str(max(dates))[:10], "%Y-%m-%d")#data ostatnich zakupow
    ostatni_data=ostatni_data.strftime('%Y-%m-%d')#konwertuję ją do porządanego formatu
    # zmiana formatu liczb w costs na pieniądze, jest to super kod excela, który zmienia format na "walutowe", można zmienić rozszerzenie pliku .xlsx na .zip
    # i otworzyć winrarem, rozpakować i wtedy w pliku "xl" mamy "style" i tam są formatowania komórek.
    format_kasa = '''# ##0,00 zł'''
    # "_-* #,##0.00\ [$zł-415]_-;\-* #,##0.00\ [$zł-415]_-;_-* "-"??\ [$zł-415]_-;_-@_-"  #<- księgowe zł
    # Nagłówek tabeli
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.color
    sheet.range('A1:D1').value = ["Numer", "Data zakupu", "Rozmiar koszyka", "Koszt koszyka"]
    sheet.range('A1:D1').color = (150, 150, 150)
    # Wpisanie danych do tabeli
    sheet.range('A2').options(transpose=True).value = idshopping
    sheet.range('B2').options(transpose=True).value = dates
    sheet.range('C2').options(transpose=True).value = sizes
    sheet.range('D2').options(transpose=True).value = costs
    #zmiana formatu dla kosztu koszyka na pieniądze
    n = len(costs)
    sheet.range((2,4), (n+1, 4)).number_format = format_kasa
    # Ustawienie rozmiaru
    #  http://docs.xlwings.org/en/stable/api.html#xlwings.Range.autofit
    sheet.range('A1').current_region.autofit()

    #wyciągamy ceny zakupów
    cenyposzczegolnychzakupow = []
    for i in range(len(costs)):
        cenyposzczegolnychzakupow.append(costs[i])
    #oraz numery klientów przy danych zakupach (używamy tego do wrzucenia danych)
    indeksyzakupow = []#na stronę internetową
    for i in range(len(idshopping)):
        indeksyzakupow.append(idshopping[i])
    #dodajemy ostatnie zakupy, kolumna przerwy aby currentregion przy wczytywaniu w następnym makrach pomijał te wartości
    sheet.range('F1').value = "Ostatnie zakupy w sklepie"
    sheet.range('F1').color = (150, 150, 150)
    sheet.range('F2').value = max(dates)
    sheet.range('F1').current_region.autofit()


# ostatnie zakupy dla każdego klienta
    sheet_name = "ZakupyC"
    output = "OstatnieZakupy"
    wb = Book.caller()
    try:
        wb.sheets[output].delete()
    except:
        pass
    wb.sheets.add(output, after=sheet_name)
    #wyciągamy dane z ZakupyC
    sheet = wb.sheets.active
    table = wb.sheets[sheet_name].range('A1').current_region
    #masowo wczytujemy dane
    dane = table.value[1:]
    lasts = {} #będziemy tu trzymać informacje o każdym numerze (czyli kliencie)
    for id, date, size, cost in dane:
        if id not in lasts: #jeśli takiego numeru id, jeszcze nie sprawdzaliśmy to go dodajemy
            lasts[id] = (id, date, size, cost)
        else: #jeśli taki id już był, to sprawdzamy która data jest wcześniejsza
            poprzednie = lasts[id]
            if date > poprzednie[1]:
                lasts[id] = (id, date, size, cost)


    #wpisujemy dane do skoroszytu
    sheet.range('A1').value = ["Numer", "Ostatnia data", "Ostatni koszyk", "Ostatnia cena"]
    sheet.range('A1:D1').color = (150, 150, 150)
    sheet.range('A2').value = sorted(lasts.values()) #posortowane wg numerów: ids, dates, sizes, costs

    sheet.range('A1').current_region.autofit()

 #łączymy dane

    # przygotowanie arkusza
    output = "DaneRazem"
    wb = Book.caller()
    try:
        wb.sheets[output].delete()
    except:
        pass
    wb.sheets.add(output, after="OstatnieZakupy")
    sheet = wb.sheets.active

    #wczytujemy masowo dane
    klient = wb.sheets["KlientC"].range('A1').current_region
    zakupy = wb.sheets["ZakupyC"].range('A1').current_region
    ostatnie_zakupy = wb.sheets["OstatnieZakupy"].range('A1').current_region

    ile_kupil = {}
    zakup = zakupy.value[1:]
    for ids, dates, sizes, costs in zakup:
        if ids not in ile_kupil:
            ile_kupil[ids] = sizes #jeśli nowy numer to dodajemy, jeśli stary to zwiększamy mu stan licznika

        else:
            ile_kupil[ids] += sizes #+= zwiększa istniejącą wartość o nową

    #Chcemy dowiedzieć się "kiedy ostatni raz kupował" każdy z klientów. Znowu dictionary
    kiedy_kupil = {}
    ostatni_zakup = ostatnie_zakupy.value[1:] # w ostatnim zakupie mamy te informacje, wystarczy je zebrać
    for ids, dates, sizes, costs in ostatni_zakup:
        if ids not in kiedy_kupil:
            kiedy_kupil[ids] = (dates, sizes)


    #zbieramy wyniki w kupę, w formie listy
    wyniki = []
    klienci = klient.value[1:]
    ostatnie_zakupy = ostatnie_zakupy.value[1:]


    listawszystkichzakupow=[]

    for firstnames, surnames, dates, ids, wiek in klienci:
        numer, imie, nazwisko =  ids, firstnames, surnames
        #ile kto kupił:
        if ids not in ile_kupil: #bo może ktoś nie miał zakupów
            ile = 0
            listawszystkichzakupow.append(0)
        else:
            ile = ile_kupil[ids]
            listawszystkichzakupow.append(ile_kupil[ids])

        #kiedy kto kupił i ile ostatnim razem :
        if ids not in kiedy_kupil: #jeśli nie miał zakupów, no to daty też nie ma, wsadzamy None
            kiedy = (None, 0)
        else:
            kiedy = kiedy_kupil[ids]

        #wynik
        wyniki.append( (numer, imie, nazwisko, ile)+kiedy )

    sheet.range('A1').value = ["Numer", "Imię", "Nazwisko", "All koszyki" , "Ostatnie zakupy", "Ostatni koszyk"]
    sheet.range('A1:F1').color = (150, 150, 150)
    sheet.range('A2').value = wyniki
    sheet.range('A1').current_region.autofit()




    licznikzakupow = [0] * len(imionaklientow)#tworzymy listę z zerem dla kazdego klienta, ktore bedziemy zmieniac, jesli byly zakupy
    zostawionepieniadze = [0]*len(imionaklientow)#tak samo dla sumy pozostawionych pieniędzy
    for i in range(len(imionaklientow)):
        for j in range(len(indeksyzakupow)):
            if indeksyklientow[i]==indeksyzakupow[j]:
                licznikzakupow[i] = licznikzakupow[i]+1
                zostawionepieniadze[i] = zostawionepieniadze[i]+cenyposzczegolnychzakupow[j]
    calkowity_obrot=sum(zostawionepieniadze)

################################
    sredniakwota = [] #lista pomocnicza do zadania dodatkowego(tworzenie wykresu srednich wydatkow)
    for i in range(len(wiekklientow)):
        if licznikzakupow[i] == 0:
            sredniakwota.append(0)
        else:
            sredniakwota.append(zostawionepieniadze[i]/licznikzakupow[i])
####################################

    def get_path(name): #funkcja pozwalająca zapisać pliki html do folderu w którym znajduje się makro.py
        from os.path import realpath, dirname, join
        return join(dirname(realpath(__file__)), name)

################################
#tworzymy wykres  w matplotlibie
    plt.scatter(wiekklientow,sredniakwota,marker='o',s=25,c='g')
    plt.xlabel("Wiek klienta")
    plt.title("Wykres punktowy")
    plt.grid()
    plt.ylabel("Średnia kwota wydanych pieniędzy")
    plt.savefig(get_path("wykres.png"))



####################################


#### HTML :


    wb = Book.caller()
    def pisz(tekst): #funkcja do zapisywania kodu HTML przez Pythona
            tekst += "\n"
            f.write(tekst.encode("utf-8"))
    with open( get_path('stronaglowna.html'), "wb") as f:
        #docstringi ułatwiają zapis kodu strony internetowej i ich przejrzystosć
        pisz(("""
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="utf-8"/>\
    <title>Strona główna</title>
    <link href="https://fonts.googleapis.com/css?family=Josefin+Sans&amp;subset=latin-ext" rel="stylesheet">
    <link rel="shortcut icon" href="logo.png"/>
    <style>
        
        body{
            background-color: #ddd;
            font-family: 'Josefin Sans', sans-serif;
            font-size: 16px;
        }
        .naglowek{
            font-size:200%;
            text-align:center;
            color:blue;
            background-color:#ddd;
            padding:0.7em
        }
            
        .container{
            background-color: #9db7fe;
        }
        
        .glowny{
            background-color: #9db7fe;
            text-align: center;
        }
        p{
        display: inline-block;
        font-size: 100%;
        font-style: italic;
        text-align:center;
        
        }
        nav ul{
            margin: 5px;
            padding: 5px;
            text-align: center;
        }
        nav li {
            display: inline-block;
            width: 200px;
            border-width: 3px;
            margin: 15px;
            border-style: dotted;
            line-height:5em;
        }
        nav a {
            display: inline-block;
            color: #000;
            font-size: 150%;
            text-decoration: none;
        }
    </style>

</head>
<body>
    <div class="container">
    <div class="naglowek">
        <header>
            <h1>Strona główna</h1>
        </header>
    </div>
    <div class="glowny">
        <nav>
        <ul>
            <li>
                <a href="Podsumowanie.html">Podsumowanie</a>
            </li>
            <li>
                <a href="Tabela.html">Tabelka klientów</a>
            </li>
            <li>
                <a href="Wykres.html">Wykres</a>
            </li>
            <li>
                <a href="Autorzy.html">O autorach</a>
            </li>
        </ul>
        </nav>
        <picture>
            <source media="(min-width: 850px)" srcset="logo.png">
            <source media="(min-width: 650px)" srcset="w13.jpg">
            <img src="herb.jpg" alt="Herb Wrocławia" style= "width: auto;">
        </picture>
        <br>
        <br>
        <p>Strona przygotowana w ramach projektu z Technologii Informacyjnych</p>
    </div>
    </div>
</body>
</html>
"""))
            
            
    with open( get_path('Podsumowanie.html'), "wb") as f:
        pisz(("""
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="utf-8"/>
    <title>Podsumowanie</title>
    <link href="https://fonts.googleapis.com/css?family=Josefin+Sans&amp;subset=latin-ext" rel="stylesheet">
    <link rel="shortcut icon" href="logo.png"/>
<style>
    body{
            background-color: #9db7fe;
            font-family: 'Josefin Sans', sans-serif;
    }
    header{

            text-align:center;
    }
    table {

            border-collapse: collapse;
            width: 100%;
    }

    td, th {
            border: 1px solid #dddddd;
            
            text-align: left;
            padding: 8px;
    }

    tr:nth-child(even) {
            background-color: #dddddd;
    }
    .button {
        font-family: 'Josefin Sans', sans-serif;
        position:absolute;
        transition: .5s ease;
        left: 40%;
        display: block;

        margin-left: auto;
        margin-right: auto;
        background-color: #47d74d;
        border: none;
        color:black;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;

        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
</style>
</head>
<body>

        <header>
            <h1>Podsumowanie</h1>
        </header>
        <table>
            <tr>
            <th>Ilość klientów</th>
            """))
        pisz('<td>'+str(len(imionaklientow))+'</td>')
        pisz('</tr>')
        pisz('<tr>')
        pisz('<th>Całkowity obrót</th>')
        pisz('<td>'+str(calkowity_obrot)+' zł</td>')
        pisz('</tr>')
        pisz('<tr>')
        pisz('<th>Data ostatniej sprzedaży</th>')
        pisz('<td>'+str(ostatni_data)+'</td>')
        pisz('</tr>')
        pisz('</table>')
        pisz('<br>')
        pisz('<a href="stronaglowna.html" class="button">Powrót do strony głównej</a>')
        
        pisz('</body>')
        pisz('</html>')
    with open( get_path('Tabela.html'), "wb") as f:

        pisz(("""
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="utf-8"/>
    <title>Tabela</title>
    <link href="https://fonts.googleapis.com/css?family=Josefin+Sans&amp;subset=latin-ext" rel="stylesheet">
    <link rel="shortcut icon" href="logo.png"/>
<style>
    body{
    background-color: #dddddd
    }
    table {
       font-family: 'Josefin Sans', sans-serif;
       background-color: #dddddd;
       border-collapse: collapse;
       width: 100%;
       }

    td, th {
        border: 1px solid black; text-align: left;
        padding: 8px;
        }

    tr:nth-child(even) {
        background-color: #9db7fe;
        }
    
    
            
    
    .button {
        font-family: 'Josefin Sans', sans-serif;
        position:absolute;
        transition: .5s ease;
        left: 40%;
        display: block;

        margin-left: auto;
        margin-right: auto;
        background-color: #47d74d;
        border: none;
        color:black;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;

        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        
    }
</style>
</head>
<body>

    <table>
        <tr>
            <th>Imię</th>
            <th>Nazwisko</th>
            <th>Sumaryczna liczba produktów</th>
            <th>Liczba zakupów</th>
            <th>Suma pozostawionych pieniędzy</th>
        </tr>
"""))#tworzymy tabelkę
          #sciągamy dane z poprzednio utworzonych list  
        for i in range(len(imionaklientow)): #dla kazdego klienta
                pisz('<tr>')#tworzymy wiersz
                pisz('<td>'+str(imionaklientow[i])+'</td>')#dodajemy imię, sumę produktów i wydaną sumę
                pisz('<td>'+str(nazwiskaklientow[i])+'</td>')
                pisz('<td>'+str(int(listawszystkichzakupow[i]))+'</td>')
                pisz('<td>'+str(licznikzakupow[i])+'</td>')
                pisz('<td>'+str(round(zostawionepieniadze[i],2))+' zł</td>')
        pisz('</tr>')
        pisz('</table>')
        pisz('<br>')  #odnosnik do strony głównej
        pisz('<a href="stronaglowna.html" class="button">Powrót do strony głównej</a>')
        pisz('</body>')
        pisz('</html>')

    with open( get_path('Wykres.html'), "wb") as f:
        pisz(("""
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="utf-8"/>
    <title>Wykresik</title>
    <link href="https://fonts.googleapis.com/css?family=Josefin+Sans&amp;subset=latin-ext" rel="stylesheet">
    <link rel="shortcut icon" href="logo.png"/>
<style>
    body{
        background-color: #9db7fe;
        font-family: 'Josefin Sans', sans-serif;
        font-size: 16px;
    }
    h1{
        
        font-family: 'Josefin Sans', sans-serif;
        font-size: 200%;
        font-weight: bold;
        text-align: center;
    }
    .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
    }
    
            
    
    .button {
        position:absolute;
        transition: .5s ease;
        left: 40%;
        display: block;

        margin-left: auto;
        margin-right: auto;
        background-color: #47d74d;
        border: none;
        color:black;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;

        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        
    }
</style>
</head>
<body>
    <h1> Zadanie dodatkowe (wykres): </h1>
    <br>
    <img src="wykres.png" alt="Wykres" class="center">
    <br>
    <a href="stronaglowna.html" class="button">Powrót do strony głównej</a>
    
    
    
</body>
</html>
"""))
    with open( get_path('Autorzy.html'), "wb") as f:
        pisz(("""
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="utf-8"/>
    <title>Autorzy</title>
    <link href="https://fonts.googleapis.com/css?family=Josefin+Sans&amp;subset=latin-ext" rel="stylesheet">
    <link rel="shortcut icon" href="logo.png"/>
<style>
    body{
        background-color: #9db7fe;
        font-family: 'Josefin Sans', sans-serif;
        font-size: 16px;
        }
    .naglowek{
        font-size:200%;
        text-align:center;
        color:blue;
        background-color:#ddd;
        padding:0.7em
    }
    .inne{
        font-size:125%;
        background-color:#ddd;
    }
    h1{  color:blue;
          text-align:center;
          
    }
    h2{   color:blue;
          text-align:center;
          font-size:175%;}
    p{
      
      padding: 50px;
      font-size:125%;
      font-style: italic;
    }
    .column{
        box-sizing: border-box;
        float: left;
        width: 50%;
        padding: 10px;
    }
    .row::after{
        content:"";
        clear: both;
        display:table;
    }
    .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
    }
    .button {
        position:absolute;
        transition: .5s ease;
        left: 40%;
        display: block;

        margin-left: auto;
        margin-right: auto;
        background-color: #47d74d;
        border: none;
        color:black;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;

        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        
    }
</style>
</head>
<body>
    <div class="naglowek">
    <h1> Informacje o autorach:</h1>
    <br>
    </div>
    <div class="inne">
    <p>Projekt wykonali: Łukasz Łaszczuk oraz Dariusz Pałatyński. Żeby nie było tak nudno, to
    przygotowaliśmy kilka informacji o nas ;D.</p>
    <h2>Skład Darka ;)</h2>
    <img src="sklad.png" alt="Wykres" class="center">
    <br>
    <br>
    <h2>Nasza uczelnia i ulubiony sport:</h2>
    <br>
    
    <div class="row">
    <div class="column">
    
    <div id="map" style="width:430px;height:260px;;padding:10px;" class="center"></div>
    <script>
        function myMap() {
            var mapOptions = {
                center: new google.maps.LatLng(51.107226, 17.062014),
                zoom: 15,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            }
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);
        }
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?callback=myMap" class="center"> </script>
    
    
    </div>
    <div class="column">
    <iframe style="width:498px; height:276px"
    src="forest2.gif">
    </iframe> 
    </div>
    </div>
    <p style="text-align:center">P.S. Życzymy powodzenia w półmaratonie!</p>
    <a href="stronaglowna.html" class="button">Powrót do strony głównej</a>
    <br>
    <br>
    <br>
    <br>
    </div>
</body>
</html>
"""))
