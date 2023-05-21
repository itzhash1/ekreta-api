import requests, hashlib, base64, hmac

headers = {
    'User-Agent': 'hu.ekreta.student/3.0.4/7.1.2/25'
}

class KRETAEncoder():
    def __init__(self) -> None:
        self.KeyProd = 'baSsxOwlU1jM'.encode('utf-8')
    def encodeRefreshToken(self, refreshToken):
        return self.encodeKey(refreshToken)
    def createLoginKey(self, userName, instituteCode, nonce):
        loginKeyPayload = instituteCode.upper() + nonce + userName.upper()
        return self.encodeKey(loginKeyPayload)
    def encodeKey(self, payload : str):
        return base64.b64encode(hmac.new(self.KeyProd, payload.encode('utf-8'), digestmod=hashlib.sha512).digest()).decode('utf-8')

class IdpApiV1:
    def __init__(self, kretaEncoder : KRETAEncoder, proxies : dict = None) -> None:
        self.kretaEncoder = kretaEncoder
        self.proxies = proxies
    def extendToken(self, refresh_token : str, institute_code : str, nonce : str):
        try:
            refresh_token_data = {
                'refresh_token': refresh_token,
                'institute_code': institute_code,
                'grant_type': 'refresh_token',
                'client_id': 'kreta-ellenorzo-mobile-android',
                'refresh_user_data': False
            }

            refreshTokenHeaders = headers.copy()
            refreshTokenHeaders.update({
                'X-AuthorizationPolicy-Key': self.kretaEncoder.encodeRefreshToken(refresh_token),
                'X-AuthorizationPolicy-Version': 'v2'
            })

            return requests.post("https://idp.e-kreta.hu/connect/token", data=refresh_token_data, headers=refreshTokenHeaders, proxies=self.proxies).json()
        except:
            pass
    def getNonce(self) -> str or None:
        try:
            return requests.get("https://idp.e-kreta.hu/nonce", headers=headers, proxies=self.proxies).text
        except Exception as e:
            print(e)
            print('Ha ez történik nagy valószínűséggel az ip címed tiltva lett.')
    def login(self, userName : str, password : str, institute_code : str, nonce : str):
        try:
            login_data = {
                'userName': userName,
                'password': password,
                'institute_code': institute_code,
                'grant_type': 'password',
                'client_id': 'kreta-ellenorzo-mobile-android',
            }

            loginHeaders = headers.copy()
            loginHeaders.update({
                'X-AuthorizationPolicy-Nonce': nonce,
                'X-AuthorizationPolicy-Key': self.kretaEncoder.createLoginKey(userName, institute_code, nonce),
                'X-AuthorizationPolicy-Version': 'v2'
            })

            return requests.post("https://idp.e-kreta.hu/connect/token", data=login_data, headers=loginHeaders, proxies=self.proxies).json()
        except:
            pass
    def revokeRefreshToken(self, refresh_token : str):
        try:
            revokeRefreshTokenData = {
                'token': refresh_token,
                'client_id': 'kreta-ellenorzo-mobile-android',
                'token_type': 'refresh token'
            }

            return requests.post("https//idp.e-kreta.hu/connect/revocation", data=revokeRefreshTokenData, headers=headers, proxies=self.proxies).text
        except:
            pass

class MobileApiV3:
    def __init__(self, authorizationToken : str, institute_code : str, proxies : dict = None) -> None:
        self.apiUrl = f'https://{institute_code}.e-kreta.hu/ellenorzo/v3'
        self.headers = headers.copy()
        self.headers.update({
            'Authorization': f'Bearer {authorizationToken}',
            'apiKey': '21ff6c25-d1da-4a68-a811-c881a6057463'
        })

        self.proxies = proxies
    def deleteBankAccountNumber(self):
        try:
            return requests.delete(f'{self.apiUrl}/sajat/Bankszamla', headers=self.headers, proxies=self.proxies).text
        except:
            pass
    def deleteReservation(self, uid : str):
        try:
            return requests.delete(f'{self.apiUrl}/sajat/Fogadoorak/Idopontok/Jelentkezesek/{uid}', headers=self.headers, proxies=self.proxies).text
        except:
            pass
    def downloadAttachment(self, uid : str):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Csatolmany/{uid}', headers=self.headers, proxies=self.proxies).text
        except:
            pass
    def getAnnouncedTests(self, Uids : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/BejelentettSzamonkeresek', params={
                'Uids': Uids
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getAnnouncedTests(self, datumTol : str = None, datumIg : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/BejelentettSzamonkeresek', params={
                'datumTol': datumTol,
                'datumIg': datumIg
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getClassAverage(self, oktatasiNevelesiFeladatUid : str, tantargyUid : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Ertekelesek/Atlagok/OsztalyAtlagok', params={
                'oktatasiNevelesiFeladatUid': oktatasiNevelesiFeladatUid,
                'tantargyUid': tantargyUid
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getClassMaster(self, Uids : str):
        try:
            return requests.get(f'{self.apiUrl}/felhasznalok/Alkalmazottak/Tanarok/Osztalyfonokok', params={
                'Uids': Uids
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getConsultingHour(self, uid : str):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Fogadoorak/{uid}', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getConsultingHours(self, datumTol : str = None, datumIg : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Fogadoorak', params={
                'datumTol': datumTol,
                'datumIg': datumIg
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getDeviceGivenState(self) -> bool or None:
        try:
            return bool(requests.get(f'{self.apiUrl}/TargyiEszkoz/IsEszkozKiosztva', headers=self.headers, proxies=self.proxies).text)
        except:
            pass
    def getEvaluations(self):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Ertekelesek', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getGroups(self):
        try:
            return requests.get(f'{self.apiUrl}/sajat/OsztalyCsoportok', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getGuardian4T(self):
        try:
            return requests.get(f'{self.apiUrl}/sajat/GondviseloAdatlap', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getHomework(self, id : str):
        try:
            return requests.get(f'{self.apiUrl}/sajat/HaziFeladatok/{id}', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getHomeworks(self, datumTol : str = None, datumIg : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/HaziFeladatok', params={
                'datumTol': datumTol,
                'datumIg': datumIg
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getLEPEvents(self):
        try:
            return requests.get(f'{self.apiUrl}/Lep/Eloadasok', headers=self.headers).json()
        except:
            pass
    def getLesson(self, orarendElemUid : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/OrarendElem', params={
                'orarendElemUid': orarendElemUid
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getLessons(self, datumTol : str = None, datumIg : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/OrarendElemek', params={
                'datumTol': datumTol,
                'datumIg': datumIg
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getNotes(self, datumTol : str = None, datumIg : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Feljegyzesek', params={
                'datumTol': datumTol,
                'datumIg': datumIg
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getNoticeBoardItems(self):
        try:
            return requests.get(f'{self.apiUrl}/sajat/FaliujsagElemek', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getOmissions(self, datumTol : str = None, datumIg : str = None):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Mulasztasok', params={
                'datumTol': datumTol,
                'datumIg': datumIg
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getRegistrationState(self):
        try:
            return requests.get(f'{self.apiUrl}/TargyiEszkoz/IsRegisztralt', headers=self.headers, proxies=self.proxies).text
        except:
            pass
    def getSchoolYearCalendar(self):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Intezmenyek/TanevRendjeElemek', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getStudent(self):
        try:
            return requests.get(f'{self.apiUrl}/sajat/TanuloAdatlap', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getSubjectAverage(self, oktatasiNevelesiFeladatUid : str):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Ertekelesek/Atlagok/TantargyiAtlagok', params={
                'oktatasiNevelesiFeladatUid': oktatasiNevelesiFeladatUid
            }, headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def getTimeTableWeeks(self):
        try:
            return requests.get(f'{self.apiUrl}/sajat/Intezmenyek/Hetirendek/Orarendi', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
    def postBankAccountNumber(self, BankszamlaSzam : str, BankszamlaTulajdonosNeve : str, BankszamlaTulajdonosTipusId : str, SzamlavezetoBank : str):
        try:
            return requests.post(f'{self.apiUrl}/sajat/Bankszamla', data=f'BankAccountNumberPostDto(bankAccountNumber={BankszamlaSzam}, bankAccountOwnerType={BankszamlaTulajdonosTipusId}, bankAccountOwnerName={BankszamlaTulajdonosNeve}, bankName={SzamlavezetoBank})', headers=self.headers, proxies=self.proxies).text
        except:
            pass
    def postContact(self, email, telefonszam):
        try:
            return requests.post(f'{self.apiUrl}/sajat/Elerhetoseg', data={
                'email': email,
                'telefonszam': telefonszam
            }, headers=self.headers, proxies=self.proxies).text
        except:
            pass
    def postCovidForm(self):
        try:
            return requests.post(f'{self.apiUrl}/Bejelentes/Covid', headers=self.headers, proxies=self.proxies).text
        except:
            pass
    def postReservation(self, uid : str):
        try:
            return requests.post(f'{self.apiUrl}/sajat/Fogadoorak/Idopontok/Jelentkezesek/{uid}', headers=self.headers, proxies=self.proxies).text
        except:
            pass
    def updateLepEventPermission(self, EloadasId : str, Dontes : bool):
        try:
            return requests.post(f'{self.apiUrl}/Lep/Eloadasok/GondviseloEngedelyezes', data=f'LepEventGuardianPermissionPostDto(eventId={EloadasId}, isPermitted={str(Dontes)})', headers=self.headers, proxies=self.proxies).text
        except:
            pass

class GlobalApiV1:
    def __init__(self, proxies : dict = None) -> None:
        self.headers = headers.copy()
        self.headers.update({
            'api-version': 'v1'
        })

        self.proxies  = proxies
    def getInstitutes(self):
        try:
            return requests.get('https://kretaglobalapi.e-kreta.hu/intezmenyek/kreta/publikus', headers=self.headers, proxies=self.proxies).json()
        except:
            pass
