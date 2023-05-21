# ekreta-api
E-Kréta API 2023/05

https://kretaglobalapi.e-kreta.hu/intezmenyek/kreta/publikus - Intézmények Lekérése Listaként

```
[
    {
        'id': String,
        'azonosito': String,
        'nev': String,
        'rovidNev': String,
        'omKod': String,
        'kretaLink': String,
        'telepules': String,
        'aktivTanevId': Integer,
        'aktivTanevGuid': String,
        'aktivTanevNev': String,
        'kornyezetId': Integer,
        'kornyezetNev': String,
        'kornyezetTeljesNev': String,
        'fenntartoAzonosito': String,
        'fenntartoNev': ''
    },
]
```

https://idp.e-kreta.hu/connect/token - Bejelentkezés

Response:
```
{
    'access_token': '',
    'expires_in': '',
    'expires_in': 1800,
    'id_token': '',
    'refresh_token': '',
    'token_type': ''
}
```

MobileApi - getAnnouncedTests
Response:
```
[
    {
        'TantargyNeve': String,
        'BejelentesDatuma': String,
        'OrarendiOraOraszama': Integer,
        'Datum': String,
        'OsztalyCsoport': {
            'Uid': String,
        },
        'Modja': {
            'Leiras': String,
            'Nev': String,
            'Uid': String
        },
        'Tantargy': {
            'Nev': String,
            'Kategoria': {
                'Leiras': String,
                'Nev': String,
                'Uid': String
            },
            'Uid': String
        },
        'RogzitoTanarNeve': String,
        'Temaja': String,
        'Uid': String,
    },
]
```

MobileApi - getClassAverage
Response:
```
[
    {
        'TanuloAtlag': Float,
        'OsztalyCsoportAtlag': Float,
        'OsztalyCsoportAtlagtolValoElteres': Float,
        'Tantargy': {
            'Nev': String,
            'Kategoria': {
                'Leiras': String,
                'Nev': String,
                'Uid': String
            },
            'Uid': String
        },
        'Uid': String
    }
]


```
