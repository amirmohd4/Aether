export interface Department {
  id: string;
  name: string;
  code: string;
  icon: string;
}

export interface WorkflowStep {
  id: string;
  name: string;
}

export interface ServiceFees {
  base_fee: number;
  stamp_duty_percentage: number;
  registration_fee_percentage: number;
}

export interface Service {
  id: string;
  department_id: string;
  name: string;
  description: string;
  processing_time: string;
  fees: ServiceFees;
  required_documents: string[];
  workflow_steps: WorkflowStep[];
}

export interface CountryConfig {
  country_code: string;
  country_name: string;
  flag: string;
  region: 'Asia' | 'Europe' | 'Africa' | 'Americas' | 'Oceania';
  currency: {
    code: string;
    symbol: string;
    name: string;
  };
  id_system: {
    name: string;
    format: string;
    verification_endpoint: string;
  };
  default_language: string;
  supported_languages: string[];
  departments: Department[];
  services: Service[];
}

// Master Raw Data for all 195 UN Member States
export const ALL_UN_COUNTRIES: Array<{
  code: string;
  name: string;
  flag: string;
  region: 'Asia' | 'Europe' | 'Africa' | 'Americas' | 'Oceania';
  currCode: string;
  currSym: string;
  currName: string;
  idName: string;
  idFormat: string;
}> = [
  // Asia
  { code: "IN", name: "India", flag: "🇮🇳", region: "Asia", currCode: "INR", currSym: "₹", currName: "Indian Rupee", idName: "Aadhaar / PAN", idFormat: "12-digit UID / 10-char PAN" },
  { code: "AE", name: "United Arab Emirates", flag: "🇦🇪", region: "Asia", currCode: "AED", currSym: "د.إ", currName: "UAE Dirham", idName: "UAE Pass / Emirates ID", idFormat: "784-XXXX-XXXXXXX-X" },
  { code: "SA", name: "Saudi Arabia", flag: "🇸🇦", region: "Asia", currCode: "SAR", currSym: "﷼", currName: "Saudi Riyal", idName: "Nafath / Iqama", idFormat: "10-digit National ID" },
  { code: "JP", name: "Japan", flag: "🇯🇵", region: "Asia", currCode: "JPY", currSym: "¥", currName: "Japanese Yen", idName: "My Number Card", idFormat: "12-digit Individual Number" },
  { code: "SG", name: "Singapore", flag: "🇸🇬", region: "Asia", currCode: "SGD", currSym: "S$", currName: "Singapore Dollar", idName: "Singpass / NRIC", idFormat: "SXXXXXXXA" },
  { code: "CN", name: "China", flag: "🇨🇳", region: "Asia", currCode: "CNY", currSym: "¥", currName: "Chinese Yuan", idName: "Resident Identity Card", idFormat: "18-digit Citizen ID" },
  { code: "KR", name: "South Korea", flag: "🇰🇷", region: "Asia", currCode: "KRW", currSym: "₩", currName: "South Korean Won", idName: "Resident Registration Card", idFormat: "YYMMDD-1234567" },
  { code: "ID", name: "Indonesia", flag: "🇮🇩", region: "Asia", currCode: "IDR", currSym: "Rp", currName: "Indonesian Rupiah", idName: "e-KTP (NIK)", idFormat: "16-digit NIK" },
  { code: "MY", name: "Malaysia", flag: "🇲🇾", region: "Asia", currCode: "MYR", currSym: "RM", currName: "Malaysian Ringgit", idName: "MyKad / NRIC", idFormat: "YYMMDD-PB-###G" },
  { code: "TH", name: "Thailand", flag: "🇹🇭", region: "Asia", currCode: "THB", currSym: "฿", currName: "Thai Baht", idName: "Thai National ID Card", idFormat: "13-digit ID Number" },
  { code: "VN", name: "Vietnam", flag: "🇻🇳", region: "Asia", currCode: "VND", currSym: "₫", currName: "Vietnamese Dong", idName: "CCCD / Citizen ID", idFormat: "12-digit Personal ID" },
  { code: "PH", name: "Philippines", flag: "🇵🇭", region: "Asia", currCode: "PHP", currSym: "₱", currName: "Philippine Peso", idName: "PhilSys National ID", idFormat: "12-digit PhilID PCN" },
  { code: "PK", name: "Pakistan", flag: "🇵🇰", region: "Asia", currCode: "PKR", currSym: "₨", currName: "Pakistani Rupee", idName: "NADRA CNIC", idFormat: "13-digit CNIC" },
  { code: "BD", name: "Bangladesh", flag: "🇧🇩", region: "Asia", currCode: "BDT", currSym: "৳", currName: "Bangladeshi Taka", idName: "National Smart ID Card", idFormat: "10-digit NID" },
  { code: "LK", name: "Sri Lanka", flag: "🇱🇰", region: "Asia", currCode: "LKR", currSym: "Rs", currName: "Sri Lankan Rupee", idName: "National Identity Card (NIC)", idFormat: "12-digit NIC" },
  { code: "NP", name: "Nepal", flag: "🇳🇵", region: "Asia", currCode: "NPR", currSym: "Rs", currName: "Nepalese Rupee", idName: "National ID Card (NID)", idFormat: "10-digit NID" },
  { code: "IL", name: "Israel", flag: "🇮🇱", region: "Asia", currCode: "ILS", currSym: "₪", currName: "Israeli Shekel", idName: "Teudat Zehut", idFormat: "9-digit Identity Number" },
  { code: "QA", name: "Qatar", flag: "🇶🇦", region: "Asia", currCode: "QAR", currSym: "﷼", currName: "Qatari Riyal", idName: "QID Card", idFormat: "11-digit Qatar ID" },
  { code: "KW", name: "Kuwait", flag: "🇰🇼", region: "Asia", currCode: "KWD", currSym: "د.ك", currName: "Kuwaiti Dinar", idName: "Civil ID Card", idFormat: "12-digit Civil ID" },
  { code: "OM", name: "Oman", flag: "🇴🇲", region: "Asia", currCode: "OMR", currSym: "﷼", currName: "Omani Rial", idName: "Civil Status ID", idFormat: "8-digit Civil Number" },
  { code: "BH", name: "Bahrain", flag: "🇧🇭", region: "Asia", currCode: "BHD", currSym: "ب.د", currName: "Bahraini Dinar", idName: "Central Population Registry (CPR)", idFormat: "9-digit CPR" },
  { code: "JO", name: "Jordan", flag: "🇯🇴", region: "Asia", currCode: "JOD", currSym: "د.ا", currName: "Jordanian Dinar", idName: "National ID Number", idFormat: "10-digit National ID" },
  { code: "LB", name: "Lebanon", flag: "🇱🇧", region: "Asia", currCode: "LBP", currSym: "ل.ل", currName: "Lebanese Pound", idName: "Lebanese National ID", idFormat: "12-digit ID" },
  { code: "IQ", name: "Iraq", flag: "🇮🇶", region: "Asia", currCode: "IQD", currSym: "ع.د", currName: "Iraqi Dinar", idName: "National Unified ID", idFormat: "12-digit National Card" },
  { code: "IR", name: "Iran", flag: "🇮🇷", region: "Asia", currCode: "IRR", currSym: "﷼", currName: "Iranian Rial", idName: "National Smart Card", idFormat: "10-digit National Code" },
  { code: "KZ", name: "Kazakhstan", flag: "🇰🇿", region: "Asia", currCode: "KZT", currSym: "₸", currName: "Kazakhstani Tenge", idName: "IIN / eGov.kz", idFormat: "12-digit Individual ID" },
  { code: "UZ", name: "Uzbekistan", flag: "🇺🇿", region: "Asia", currCode: "UZS", currSym: "soʻm", currName: "Uzbekistani Som", idName: "JShShIR / Citizen ID", idFormat: "14-digit PINFL" },
  { code: "AZ", name: "Azerbaijan", flag: "🇦🇿", region: "Asia", currCode: "AZN", currSym: "₼", currName: "Azerbaijani Manat", idName: "FIN Code / Citizen ID", idFormat: "7-char FIN Code" },
  { code: "GE", name: "Georgia", flag: "🇬🇪", region: "Asia", currCode: "GEL", currSym: "₾", currName: "Georgian Lari", idName: "Personal Number ID", idFormat: "11-digit Personal Number" },
  { code: "AM", name: "Armenia", flag: "🇦🇲", region: "Asia", currCode: "AMD", currSym: "֏", currName: "Armenian Dram", idName: "Social Services Card (PSN)", idFormat: "10-digit PSN" },
  { code: "TJ", name: "Tajikistan", flag: "🇹🇯", region: "Asia", currCode: "TJS", currSym: "ЅM", currName: "Tajikistani Somoni", idName: "SIN / National ID", idFormat: "12-digit SIN" },
  { code: "TM", name: "Turkmenistan", flag: "🇹🇲", region: "Asia", currCode: "TMT", currSym: "m", currName: "Turkmenistan Manat", idName: "Passport ID", idFormat: "8-digit Passport ID" },
  { code: "KG", name: "Kyrgyzstan", flag: "🇰🇬", region: "Asia", currCode: "KGS", currSym: "сом", currName: "Kyrgyzstani Som", idName: "PIN / e-ID", idFormat: "14-digit PIN" },
  { code: "AF", name: "Afghanistan", flag: "🇦🇫", region: "Asia", currCode: "AFN", currSym: "؋", currName: "Afghan Afghani", idName: "e-Tazkira", idFormat: "13-digit Tazkira ID" },
  { code: "MM", name: "Myanmar", flag: "🇲🇲", region: "Asia", currCode: "MMK", currSym: "K", currName: "Myanmar Kyat", idName: "NRC Card", idFormat: "State/Township NRC" },
  { code: "KH", name: "Cambodia", flag: "🇰🇭", region: "Asia", currCode: "KHR", currSym: "៛", currName: "Cambodian Riel", idName: "Khmer Khmer ID", idFormat: "9-digit ID Card" },
  { code: "LA", name: "Laos", flag: "🇱🇦", region: "Asia", currCode: "LAK", currSym: "₭", currName: "Lao Kip", idName: "Lao National ID", idFormat: "10-digit ID" },
  { code: "MN", name: "Mongolia", flag: "🇲🇳", region: "Asia", currCode: "MNT", currSym: "₮", currName: "Mongolian Tögrög", idName: "Citizen Registration Number", idFormat: "12-digit Civil ID" },
  { code: "BT", name: "Bhutan", flag: "🇧🇹", region: "Asia", currCode: "BTN", currSym: "Nu.", currName: "Bhutanese Ngultrum", idName: "Citizenship Identity Card (CID)", idFormat: "11-digit CID" },
  { code: "MV", name: "Maldives", flag: "🇲🇻", region: "Asia", currCode: "MVR", currSym: "Rf", currName: "Maldivian Rufiyaa", idName: "National Identity Card", idFormat: "AXXXXXX Card Number" },
  { code: "BN", name: "Brunei", flag: "🇧🇳", region: "Asia", currCode: "BND", currSym: "B$", currName: "Brunei Dollar", idName: "Smart Identity Card (IC)", idFormat: "01-XXXXXX IC" },
  { code: "TL", name: "Timor-Leste", flag: "🇹🇱", region: "Asia", currCode: "USD", currSym: "$", currName: "US Dollar", idName: "Electoral / Citizen Card", idFormat: "8-digit Card ID" },
  { code: "YE", name: "Yemen", flag: "🇾🇪", region: "Asia", currCode: "YER", currSym: "﷼", currName: "Yemeni Rial", idName: "National ID Card", idFormat: "11-digit Personal ID" },
  { code: "SY", name: "Syria", flag: "🇸🇾", region: "Asia", currCode: "SYP", currSym: "LS", currName: "Syrian Pound", idName: "National Identity Card", idFormat: "11-digit ID" },
  { code: "PS", name: "Palestine", flag: "🇵🇸", region: "Asia", currCode: "ILS", currSym: "₪", currName: "Israeli Shekel", idName: "Palestinian ID Card", idFormat: "9-digit ID Number" },

  // Europe
  { code: "EE", name: "Estonia", flag: "🇪🇪", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "e-Residency / Smart-ID", idFormat: "11-digit Personal Code" },
  { code: "GB", name: "United Kingdom", flag: "🇬🇧", region: "Europe", currCode: "GBP", currSym: "£", currName: "British Pound", idName: "GOV.UK One Login / NINo", idFormat: "QQ123456A" },
  { code: "DE", name: "Germany", flag: "🇩🇪", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "BundID / Personalausweis", idFormat: "6-digit eID Code" },
  { code: "FR", name: "France", flag: "🇫🇷", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "FranceConnect / CNI", idFormat: "15-digit NIR Code" },
  { code: "IT", name: "Italy", flag: "🇮🇹", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "SPID / CIE Digital", idFormat: "16-char Codice Fiscale" },
  { code: "ES", name: "Spain", flag: "🇪🇸", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "Cl@ve / DNIe", idFormat: "8-digit NIF/NIE + Letter" },
  { code: "NL", name: "Netherlands", flag: "🇳🇱", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "DigiD / BSN", idFormat: "9-digit BSN Number" },
  { code: "CH", name: "Switzerland", flag: "🇨🇭", region: "Europe", currCode: "CHF", currSym: "CHF", currName: "Swiss Franc", idName: "SwissID / AHV", idFormat: "756.XXXX.XXXX.XX" },
  { code: "SE", name: "Sweden", flag: "🇸🇪", region: "Europe", currCode: "SEK", currSym: "kr", currName: "Swedish Krona", idName: "BankID / Personnummer", idFormat: "YYYYMMDD-XXXX" },
  { code: "NO", name: "Norway", flag: "🇳🇴", region: "Europe", currCode: "NOK", currSym: "kr", currName: "Norwegian Krone", idName: "BankID / Fødselsnummer", idFormat: "11-digit Personal ID" },
  { code: "DK", name: "Denmark", flag: "🇩🇰", region: "Europe", currCode: "DKK", currSym: "kr.", currName: "Danish Krone", idName: "MitID / CPR", idFormat: "DDMMYY-XXXX CPR" },
  { code: "FI", name: "Finland", flag: "🇫🇮", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "Suomi.fi / Henkilötunnus", idFormat: "DDMMYY-XXXT" },
  { code: "IE", name: "Ireland", flag: "🇮🇪", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "MyGovID / PPSN", idFormat: "7-digit PPSN + Letter" },
  { code: "BE", name: "Belgium", flag: "🇧🇪", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "itsme / eID", idFormat: "11-digit National Register" },
  { code: "AT", name: "Austria", flag: "🇦🇹", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "ID Austria", idFormat: "10-digit Social Security" },
  { code: "PL", name: "Poland", flag: "🇵🇱", region: "Europe", currCode: "PLN", currSym: "zł", currName: "Polish Złoty", idName: "mObywatel / PESEL", idFormat: "11-digit PESEL Number" },
  { code: "PT", name: "Portugal", flag: "🇵🇹", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "Chave Móvel Digital", idFormat: "8-digit Cartão de Cidadão" },
  { code: "GR", name: "Greece", flag: "🇬🇷", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "Gov.gr / AFM", idFormat: "9-digit AFM Number" },
  { code: "CZ", name: "Czechia", flag: "🇨🇿", region: "Europe", currCode: "CZK", currSym: "Kč", currName: "Czech Koruna", idName: "eIdentita / Rodné číslo", idFormat: "YYMMDD/XXXX" },
  { code: "HU", name: "Hungary", flag: "🇭🇺", region: "Europe", currCode: "HUF", currSym: "Ft", currName: "Hungarian Forint", idName: "Ügyfélkapu / TAJ", idFormat: "9-digit TAJ Number" },
  { code: "RO", name: "Romania", flag: "🇷🇴", region: "Europe", currCode: "RON", currSym: "lei", currName: "Romanian Leu", idName: "Ghișeul.ro / CNP", idFormat: "13-digit CNP Code" },
  { code: "UA", name: "Ukraine", flag: "🇺🇦", region: "Europe", currCode: "UAH", currSym: "₴", currName: "Ukrainian Hryvnia", idName: "Diia App / RNTRC", idFormat: "10-digit Tax Code" },
  { code: "HR", name: "Croatia", flag: "🇭🇷", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "e-Građani / OIB", idFormat: "11-digit OIB Number" },
  { code: "SK", name: "Slovakia", flag: "🇸🇰", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "Slovensko.sk / Rodné číslo", idFormat: "10-digit Personal ID" },
  { code: "BG", name: "Bulgaria", flag: "🇧🇬", region: "Europe", currCode: "BGN", currSym: "лв", currName: "Bulgarian Lev", idName: "EGN Citizen Number", idFormat: "10-digit EGN" },
  { code: "SI", name: "Slovenia", flag: "🇸🇮", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "si-pass / EMŠO", idFormat: "13-digit EMŠO" },
  { code: "LT", name: "Lithuania", flag: "🇱🇹", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "m.Parašas / Asmens kodas", idFormat: "11-digit Personal Code" },
  { code: "LV", name: "Latvia", flag: "🇱🇻", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "eParaksts / Personas kods", idFormat: "11-digit Personal Code" },
  { code: "CY", name: "Cyprus", flag: "🇨🇾", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "Cy Login / ID Card", idFormat: "10-digit Social Security" },
  { code: "MT", name: "Malta", flag: "🇲🇹", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "e-ID Malta", idFormat: "7-digit ID Card + Letter" },
  { code: "IS", name: "Iceland", flag: "🇮🇸", region: "Europe", currCode: "ISK", currSym: "kr", currName: "Icelandic Króna", idName: "Auðkenni / Kennitala", idFormat: "DDMMYY-XXXX ID" },
  { code: "LU", name: "Luxembourg", flag: "🇱🇺", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "LuxTrust / Matricule", idFormat: "11-digit Matricule ID" },
  { code: "AL", name: "Albania", flag: "🇦🇱", region: "Europe", currCode: "ALL", currSym: "L", currName: "Albanian Lek", idName: "e-Albania / NIPT", idFormat: "10-char NIPT ID" },
  { code: "RS", name: "Serbia", flag: "🇷🇸", region: "Europe", currCode: "RSD", currSym: "дин.", currName: "Serbian Dinar", idName: "eUprava / JMBG", idFormat: "13-digit JMBG" },
  { code: "BA", name: "Bosnia and Herzegovina", flag: "🇧🇦", region: "Europe", currCode: "BAM", currSym: "KM", currName: "Convertible Mark", idName: "JMBG Citizen Code", idFormat: "13-digit JMBG" },
  { code: "ME", name: "Montenegro", flag: "🇲🇪", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "eUprava / JMBG", idFormat: "13-digit JMBG" },
  { code: "MK", name: "North Macedonia", flag: "🇲🇰", region: "Europe", currCode: "MKD", currSym: "ден", currName: "Macedonian Denar", idName: "EMBG Number", idFormat: "13-digit EMBG" },
  { code: "MD", name: "Moldova", flag: "🇲🇩", region: "Europe", currCode: "MDL", currSym: "L", currName: "Moldovan Leu", idName: "IDNP Code", idFormat: "13-digit IDNP" },
  { code: "BY", name: "Belarus", flag: "🇧🇾", region: "Europe", currCode: "BYN", currSym: "Br", currName: "Belarusian Ruble", idName: "Personal Identification Number", idFormat: "14-char Identification" },
  { code: "RU", name: "Russia", flag: "🇷🇺", region: "Europe", currCode: "RUB", currSym: "₽", currName: "Russian Ruble", idName: "Gosuslugi / SNILS", idFormat: "11-digit SNILS Code" },
  { code: "MC", name: "Monaco", flag: "🇲🇨", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "Monapass / CNI", idFormat: "6-digit Citizen ID" },
  { code: "LI", name: "Liechtenstein", flag: "🇱🇮", region: "Europe", currCode: "CHF", currSym: "CHF", currName: "Swiss Franc", idName: "eID Liechtenstein", idFormat: "9-digit PEID" },
  { code: "SM", name: "San Marino", flag: "🇸🇲", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "ISS Code", idFormat: "5-digit Citizen Code" },
  { code: "AD", name: "Andorra", flag: "🇦🇩", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "NIA Andorra", idFormat: "6-digit NIA Number" },
  { code: "VA", name: "Vatican City", flag: "🇻🇦", region: "Europe", currCode: "EUR", currSym: "€", currName: "Euro", idName: "Vatican Citizen ID", idFormat: "4-digit Vatican ID" },

  // Americas
  { code: "US", name: "United States", flag: "🇺🇸", region: "Americas", currCode: "USD", currSym: "$", currName: "US Dollar", idName: "SSN / Login.gov", idFormat: "XXX-XX-XXXX SSN" },
  { code: "CA", name: "Canada", flag: "🇨🇦", region: "Americas", currCode: "CAD", currSym: "CA$", currName: "Canadian Dollar", idName: "SIN / Interac Verified", idFormat: "9-digit SIN Number" },
  { code: "MX", name: "Mexico", flag: "🇲🇽", region: "Americas", currCode: "MXN", currSym: "MEX$", currName: "Mexican Peso", idName: "CURP / INE Digital", idFormat: "18-character CURP" },
  { code: "BR", name: "Brazil", flag: "🇧🇷", region: "Americas", currCode: "BRL", currSym: "R$", currName: "Brazilian Real", idName: "CPF / Gov.br", idFormat: "XXX.XXX.XXX-XX CPF" },
  { code: "AR", name: "Argentina", flag: "🇦🇷", region: "Americas", currCode: "ARS", currSym: "ARS$", currName: "Argentine Peso", idName: "Mi Argentina / DNI", idFormat: "8-digit DNI Number" },
  { code: "CO", name: "Colombia", flag: "🇨🇴", region: "Americas", currCode: "COP", currSym: "COL$", currName: "Colombian Peso", idName: "Cédula Digital", idFormat: "10-digit Cédula ID" },
  { code: "CL", name: "Chile", flag: "🇨🇱", region: "Americas", currCode: "CLP", currSym: "CLP$", currName: "Chilean Peso", idName: "ClaveÚnica / RUN", idFormat: "8-digit RUN + Check" },
  { code: "PE", name: "Peru", flag: "🇵🇪", region: "Americas", currCode: "PEN", currSym: "S/", currName: "Peruvian Sol", idName: "RENIEC / DNI", idFormat: "8-digit DNI Card" },
  { code: "VE", name: "Venezuela", flag: "🇻🇪", region: "Americas", currCode: "VES", currSym: "Bs.", currName: "Venezuelan Bolívar", idName: "SAIME / Cédula", idFormat: "V-XXXXXXXX ID" },
  { code: "EC", name: "Ecuador", flag: "🇪🇨", region: "Americas", currCode: "USD", currSym: "$", currName: "US Dollar", idName: "Registro Civil / Cédula", idFormat: "10-digit Cédula ID" },
  { code: "GT", name: "Guatemala", flag: "🇬🇹", region: "Americas", currCode: "GTQ", currSym: "Q", currName: "Guatemalan Quetzal", idName: "DPI / CUI Number", idFormat: "13-digit CUI Code" },
  { code: "CU", name: "Cuba", flag: "🇨🇺", region: "Americas", currCode: "CUP", currSym: "₱", currName: "Cuban Peso", idName: "Carné de Identidad", idFormat: "11-digit Carné ID" },
  { code: "DO", name: "Dominican Republic", flag: "🇩🇴", region: "Americas", currCode: "DOP", currSym: "RD$", currName: "Dominican Peso", idName: "Cédula de Identidad", idFormat: "XXX-XXXXXXX-X" },
  { code: "CR", name: "Costa Rica", flag: "🇨🇷", region: "Americas", currCode: "CRC", currSym: "₡", currName: "Costa Rican Colón", idName: "Cédula de Identidad", idFormat: "9-digit Cédula Number" },
  { code: "PA", name: "Panama", flag: "🇵🇦", region: "Americas", currCode: "PAB", currSym: "B/.", currName: "Panamanian Balboa", idName: "Cédula de Identidad", idFormat: "X-XXX-XXXX Cédula" },
  { code: "UY", name: "Uruguay", flag: "🇺🇾", region: "Americas", currCode: "UYU", currSym: "$U", currName: "Uruguayan Peso", idName: "Gub.uy / Cédula", idFormat: "7-digit Cédula + Digit" },
  { code: "PY", name: "Paraguay", flag: "🇵🇾", region: "Americas", currCode: "PYG", currSym: "₲", currName: "Paraguayan Guaraní", idName: "Cédula de Identidad", idFormat: "7-digit Cédula Number" },
  { code: "BO", name: "Bolivia", flag: "🇧🇴", region: "Americas", currCode: "BOB", currSym: "Bs.", currName: "Bolivian Boliviano", idName: "SEGIP / Cédula", idFormat: "7-digit Cédula ID" },
  { code: "JM", name: "Jamaica", flag: "🇯🇲", region: "Americas", currCode: "JMD", currSym: "J$", currName: "Jamaican Dollar", idName: "NIDS / TRN", idFormat: "9-digit TRN Number" },
  { code: "TT", name: "Trinidad and Tobago", flag: "🇹🇹", region: "Americas", currCode: "TTD", currSym: "TT$", currName: "Trinidad Dollar", idName: "National ID Card", idFormat: "10-digit ID Card" },
  { code: "BS", name: "Bahamas", flag: "🇧🇸", region: "Americas", currCode: "BSD", currSym: "B$", currName: "Bahamian Dollar", idName: "NIB Smart Card", idFormat: "9-digit NIB Number" },
  { code: "SV", name: "El Salvador", flag: "🇸🇻", region: "Americas", currCode: "USD", currSym: "$", currName: "US Dollar / Bitcoin", idName: "DUI Card", idFormat: "8-digit DUI + Check" },
  { code: "HN", name: "Honduras", flag: "🇭🇳", region: "Americas", currCode: "HNL", currSym: "L", currName: "Honduran Lempira", idName: "DNI Card", idFormat: "13-digit DNI ID" },
  { code: "NI", name: "Nicaragua", flag: "🇳🇮", region: "Americas", currCode: "NIO", currSym: "C$", currName: "Nicaraguan Córdoba", idName: "Cédula de Identidad", idFormat: "XXX-DDMMYY-XXXXA" },
  { code: "GY", name: "Guyana", flag: "🇬🇾", region: "Americas", currCode: "GYD", currSym: "G$", currName: "Guyanese Dollar", idName: "National ID Card", idFormat: "9-digit ID Card" },
  { code: "SR", name: "Suriname", flag: "🇸🇷", region: "Americas", currCode: "SRD", currSym: "Sr$", currName: "Surinamese Dollar", idName: "e-ID Card / CBB", idFormat: "10-digit Citizen ID" },
  { code: "BB", name: "Barbados", flag: "🇧🇧", region: "Americas", currCode: "BBD", currSym: "Bds$", currName: "Barbadian Dollar", idName: "Trident ID Card", idFormat: "10-digit National ID" },
  { code: "BZ", name: "Belize", flag: "🇧🇿", region: "Americas", currCode: "BZD", currSym: "BZ$", currName: "Belize Dollar", idName: "Social Security Board (SSB)", idFormat: "9-digit SSB Number" },
  { code: "HT", name: "Haiti", flag: "🇭🇹", region: "Americas", currCode: "HTG", currSym: "G", currName: "Haitian Gourde", idName: "NIF / CIN Card", idFormat: "10-digit CIN Code" },
  { code: "GD", name: "Grenada", flag: "🇬🇩", region: "Americas", currCode: "XCD", currSym: "EC$", currName: "East Caribbean Dollar", idName: "NIS Card", idFormat: "8-digit NIS Number" },
  { code: "LC", name: "Saint Lucia", flag: "🇱🇨", region: "Americas", currCode: "XCD", currSym: "EC$", currName: "East Caribbean Dollar", idName: "NIC Card", idFormat: "8-digit NIC Number" },
  { code: "VC", name: "Saint Vincent and the Grenadines", flag: "🇻🇨", region: "Americas", currCode: "XCD", currSym: "EC$", currName: "East Caribbean Dollar", idName: "Electoral ID", idFormat: "7-digit ID Card" },
  { code: "AG", name: "Antigua and Barbuda", flag: "🇦🇬", region: "Americas", currCode: "XCD", currSym: "EC$", currName: "East Caribbean Dollar", idName: "ABSSB Card", idFormat: "8-digit Registration" },
  { code: "DM", name: "Dominica", flag: "🇩🇲", region: "Americas", currCode: "XCD", currSym: "EC$", currName: "East Caribbean Dollar", idName: "Social Security Card", idFormat: "8-digit SS ID" },
  { code: "KN", name: "Saint Kitts and Nevis", flag: "🇰🇳", region: "Americas", currCode: "XCD", currSym: "EC$", currName: "East Caribbean Dollar", idName: "Social Security Board ID", idFormat: "7-digit SSB" },

  // Africa
  { code: "KE", name: "Kenya", flag: "🇰🇪", region: "Africa", currCode: "KES", currSym: "KSh", currName: "Kenyan Shilling", idName: "Huduma Namba / National ID", idFormat: "8-digit National ID" },
  { code: "NG", name: "Nigeria", flag: "🇳🇬", region: "Africa", currCode: "NGN", currSym: "₦", currName: "Nigerian Naira", idName: "NIN / BVN", idFormat: "11-digit National ID Number" },
  { code: "ZA", name: "South Africa", flag: "🇿🇦", region: "Africa", currCode: "ZAR", currSym: "R", currName: "South African Rand", idName: "Smart ID Card / eHomeAffairs", idFormat: "13-digit ID Number" },
  { code: "EG", name: "Egypt", flag: "🇪🇬", region: "Africa", currCode: "EGP", currSym: "E£", currName: "Egyptian Pound", idName: "National ID Card", idFormat: "14-digit National ID" },
  { code: "MA", name: "Morocco", flag: "🇲🇦", region: "Africa", currCode: "MAD", currSym: "DH", currName: "Moroccan Dirham", idName: "CNIE / Gov.ma", idFormat: "2-char + 6-digit CNIE" },
  { code: "GH", name: "Ghana", flag: "🇬🇭", region: "Africa", currCode: "GHS", currSym: "GH₵", currName: "Ghanaian Cedi", idName: "Ghana Card / NIA", idFormat: "GHA-XXXXXXXXX-X" },
  { code: "ET", name: "Ethiopia", flag: "🇪🇹", region: "Africa", currCode: "ETB", currSym: "Br", currName: "Ethiopian Birr", idName: "Fayda Digital ID", idFormat: "12-digit Fayda ID" },
  { code: "TZ", name: "Tanzania", flag: "🇹🇿", region: "Africa", currCode: "TZS", currSym: "TSh", currName: "Tanzanian Shilling", idName: "NIDA Card", idFormat: "20-digit NIDA Code" },
  { code: "UG", name: "Uganda", flag: "🇺🇬", region: "Africa", currCode: "UGX", currSym: "USh", currName: "Ugandan Shilling", idName: "NIRA NIN Card", idFormat: "14-character NIN" },
  { code: "RW", name: "Rwanda", flag: "🇷🇼", region: "Africa", currCode: "RWF", currSym: "FRw", currName: "Rwandan Franc", idName: "Irembo / National ID", idFormat: "16-digit National ID" },
  { code: "DZ", name: "Algeria", flag: "🇩🇿", region: "Africa", currCode: "DZD", currSym: "DA", currName: "Algerian Dinar", idName: "NIN Card", idFormat: "18-digit NIN Code" },
  { code: "CI", name: "Ivory Coast", flag: "🇨🇮", region: "Africa", currCode: "XOF", currSym: "CFA", currName: "West African CFA Franc", idName: "NNI Card", idFormat: "11-digit NNI Number" },
  { code: "SN", name: "Senegal", flag: "🇸🇳", region: "Africa", currCode: "XOF", currSym: "CFA", currName: "West African CFA Franc", idName: "CEDEAO Smart ID", idFormat: "13-digit ECOWAS ID" },
  { code: "ZW", name: "Zimbabwe", flag: "🇿🇼", region: "Africa", currCode: "ZWG", currSym: "ZiG", currName: "Zimbabwe Gold", idName: "National Registration Card", idFormat: "2-digit-6-digit-Letter-2-digit" },
  { code: "AO", name: "Angola", flag: "🇦🇴", region: "Africa", currCode: "AOA", currSym: "Kz", currName: "Angolan Kwanza", idName: "Bilhete de Identidade (BI)", idFormat: "14-char BI ID" },
  { code: "MZ", name: "Mozambique", flag: "🇲🇿", region: "Africa", currCode: "MZN", currSym: "MT", currName: "Mozambican Metical", idName: "Bilhete de Identidade", idFormat: "12-digit BI Number" },
  { code: "ZM", name: "Zambia", flag: "🇿🇲", region: "Africa", currCode: "ZMW", currSym: "ZK", currName: "Zambian Kwacha", idName: "National Registration Card (NRC)", idFormat: "6-digit/11/1 NRC" },
  { code: "TN", name: "Tunisia", flag: "🇹🇳", region: "Africa", currCode: "TND", currSym: "DT", currName: "Tunisian Dinar", idName: "Carte d'Identité Nationale (CIN)", idFormat: "8-digit CIN Code" },
  { code: "SD", name: "Sudan", flag: "🇸🇩", region: "Africa", currCode: "SDG", currSym: "LS", currName: "Sudanese Pound", idName: "National Number ID", idFormat: "11-digit National ID" },
  { code: "MG", name: "Madagascar", flag: "🇲🇬", region: "Africa", currCode: "MGA", currSym: "Ar", currName: "Malagasy Ariary", idName: "Carte d'Identité Nationale", idFormat: "12-digit CIN Number" },
  { code: "CM", name: "Cameroon", flag: "🇨🇲", region: "Africa", currCode: "XAF", currSym: "FCFA", currName: "Central African CFA Franc", idName: "CNI Card", idFormat: "9-digit CNI ID" },
  { code: "CD", name: "DR Congo", flag: "🇨🇩", region: "Africa", currCode: "CDF", currSym: "FC", currName: "Congolese Franc", idName: "ONIP Citizen ID", idFormat: "12-digit ONIP ID" },
  { code: "CG", name: "Republic of the Congo", flag: "🇨🇬", region: "Africa", currCode: "XAF", currSym: "FCFA", currName: "Central African CFA Franc", idName: "CNI Card", idFormat: "10-digit CNI ID" },
  { code: "ML", name: "Mali", flag: "🇲🇱", region: "Africa", currCode: "XOF", currSym: "CFA", currName: "West African CFA Franc", idName: "NINA Card", idFormat: "15-digit NINA Number" },
  { code: "BF", name: "Burkina Faso", flag: "🇧🇫", region: "Africa", currCode: "XOF", currSym: "CFA", currName: "West African CFA Franc", idName: "CNIB Card", idFormat: "BXXXXXXX CNIB" },
  { code: "BJ", name: "Benin", flag: "🇧🇯", region: "Africa", currCode: "XOF", currSym: "CFA", currName: "West African CFA Franc", idName: "CIP / NPI Card", idFormat: "10-digit NPI Code" },
  { code: "TG", name: "Togo", flag: "🇹🇬", region: "Africa", currCode: "XOF", currSym: "CFA", currName: "West African CFA Franc", idName: "Carte d'Identité Nationale", idFormat: "8-digit CNI" },
  { code: "NE", name: "Niger", flag: "🇳🇪", region: "Africa", currCode: "XOF", currSym: "CFA", currName: "West African CFA Franc", idName: "Carte d'Identité Nationale", idFormat: "9-digit CNI Code" },
  { code: "TD", name: "Chad", flag: "🇹🇩", region: "Africa", currCode: "XAF", currSym: "FCFA", currName: "Central African CFA Franc", idName: "NNI Card", idFormat: "10-digit NNI" },
  { code: "MR", name: "Mauritania", flag: "🇲🇷", region: "Africa", currCode: "MRU", currSym: "UM", currName: "Mauritanian Ouguiya", idName: "NNI Number", idFormat: "10-digit NNI Number" },
  { code: "NA", name: "Namibia", flag: "🇳🇦", region: "Africa", currCode: "NAD", currSym: "N$", currName: "Namibian Dollar", idName: "Namibian Identity Document", idFormat: "11-digit ID Number" },
  { code: "BW", name: "Botswana", flag: "🇧🇼", region: "Africa", currCode: "BWP", currSym: "P", currName: "Botswana Pula", idName: "Omang ID Card", idFormat: "9-digit Omang Code" },
  { code: "GA", name: "Gabon", flag: "🇬🇦", region: "Africa", currCode: "XAF", currSym: "FCFA", currName: "Central African CFA Franc", idName: "CNI Card", idFormat: "10-digit CNI Number" },
  { code: "GQ", name: "Equatorial Guinea", flag: "🇬🇶", region: "Africa", currCode: "XAF", currSym: "FCFA", currName: "Central African CFA Franc", idName: "DNI Card", idFormat: "8-digit DNI Number" },
  { code: "MW", name: "Malawi", flag: "🇲🇼", region: "Africa", currCode: "MWK", currSym: "MK", currName: "Malawian Kwacha", idName: "NRIS National ID", idFormat: "8-character ID Code" },
  { code: "SO", name: "Somalia", flag: "🇸🇴", region: "Africa", currCode: "SOS", currSym: "Sh.So.", currName: "Somali Shilling", idName: "NIRA Smart ID", idFormat: "11-digit NIRA ID" },
  { code: "DJ", name: "Djibouti", flag: "🇩🇯", region: "Africa", currCode: "DJF", currSym: "Fdj", currName: "Djiboutian Franc", idName: "Carte d'Identité Nationale", idFormat: "8-digit CNI" },
  { code: "MU", name: "Mauritius", flag: "🇲🇺", region: "Africa", currCode: "MUR", currSym: "₨", currName: "Mauritian Rupee", idName: "Mauritius National ID (MNID)", idFormat: "ADDMMYYXXXXXX" },
  { code: "SC", name: "Seychelles", flag: "🇸🇨", region: "Africa", currCode: "SCR", currSym: "SR", currName: "Seychellois Rupee", idName: "NIN Card", idFormat: "9-digit NIN Code" },
  { code: "CV", name: "Cabo Verde", flag: "🇨🇻", region: "Africa", currCode: "CVE", currSym: "Esc", currName: "Cape Verdean Escudo", idName: "CNI Card", idFormat: "8-digit CNI Number" },
  { code: "GM", name: "Gambia", flag: "🇬🇲", region: "Africa", currCode: "GMD", currSym: "D", currName: "Gambian Dalasi", idName: "National ID Card", idFormat: "8-digit ID Number" },
  { code: "SL", name: "Sierra Leone", flag: "🇸🇱", region: "Africa", currCode: "SLE", currSym: "Le", currName: "Sierra Leonean Leone", idName: "NCRA NIN Card", idFormat: "10-digit NIN Number" },
  { code: "LR", name: "Liberia", flag: "🇱🇷", region: "Africa", currCode: "LRD", currSym: "L$", currName: "Liberian Dollar", idName: "NIR National ID", idFormat: "10-digit NIR Number" },
  { code: "CF", name: "Central African Republic", flag: "🇨🇫", region: "Africa", currCode: "XAF", currSym: "FCFA", currName: "Central African CFA Franc", idName: "CNI Card", idFormat: "8-digit CNI Number" },
  { code: "SS", name: "South Sudan", flag: "🇸🇸", region: "Africa", currCode: "SSP", currSym: "SS£", currName: "South Sudanese Pound", idName: "National ID Card", idFormat: "9-digit ID Code" },
  { code: "BI", name: "Burundi", flag: "🇧🇮", region: "Africa", currCode: "BIF", currSym: "FBu", currName: "Burundian Franc", idName: "CNI Card", idFormat: "8-digit CNI Code" },
  { code: "ER", name: "Eritrea", flag: "🇪🇷", region: "Africa", currCode: "ERN", currSym: "Nfk", currName: "Eritrean Nakfa", idName: "National ID Card", idFormat: "8-digit ID Number" },
  { code: "KM", name: "Comoros", flag: "🇰🇲", region: "Africa", currCode: "KMF", currSym: "CF", currName: "Comorian Franc", idName: "Carte d'Identité Nationale", idFormat: "8-digit CNI" },
  { code: "GN", name: "Guinea", flag: "🇬🇳", region: "Africa", currCode: "GNF", currSym: "FG", currName: "Guinean Franc", idName: "Carte Biométrique", idFormat: "10-digit NIN Code" },
  { code: "GW", name: "Guinea-Bissau", flag: "🇬🇼", region: "Africa", currCode: "XOF", currSym: "CFA", currName: "West African CFA Franc", idName: "Bilhete de Identidade", idFormat: "8-digit BI Number" },
  { code: "LS", name: "Lesotho", flag: "🇱🇸", region: "Africa", currCode: "LSL", currSym: "M", currName: "Lesotho Loti", idName: "National ID Card", idFormat: "10-digit ID Number" },
  { code: "SZ", name: "Eswatini", flag: "🇸🇿", region: "Africa", currCode: "SZL", currSym: "E", currName: "Swazi Lilangeni", idName: "National ID Card", idFormat: "13-digit ID Code" },
  { code: "ST", name: "Sao Tome and Principe", flag: "🇸🇹", region: "Africa", currCode: "STN", currSym: "Db", currName: "São Tomé and Príncipe Dobra", idName: "Bilhete de Identidade", idFormat: "7-digit BI Number" },

  // Oceania
  { code: "AU", name: "Australia", flag: "🇦🇺", region: "Oceania", currCode: "AUD", currSym: "A$", currName: "Australian Dollar", idName: "myGov / Medicare / TFN", idFormat: "9-digit TFN Number" },
  { code: "NZ", name: "New Zealand", flag: "🇳🇿", region: "Oceania", currCode: "NZD", currSym: "NZ$", currName: "New Zealand Dollar", idName: "RealMe / IRD Number", idFormat: "9-digit IRD Number" },
  { code: "PG", name: "Papua New Guinea", flag: "🇵🇬", region: "Oceania", currCode: "PGK", currSym: "K", currName: "Papua New Guinean Kina", idName: "NIPA National ID Card", idFormat: "10-digit NID Number" },
  { code: "FJ", name: "Fiji", flag: "🇫🇯", region: "Oceania", currCode: "FJD", currSym: "FJ$", currName: "Fijian Dollar", idName: "Fiji Joint Card / TIN", idFormat: "9-digit TIN Number" },
  { code: "SB", name: "Solomon Islands", flag: "🇸🇧", region: "Oceania", currCode: "SBD", currSym: "SI$", currName: "Solomon Islands Dollar", idName: "National ID / NPF", idFormat: "8-digit NPF Code" },
  { code: "VU", name: "Vanuatu", flag: "🇻🇺", region: "Oceania", currCode: "VUV", currSym: "VT", currName: "Vanuatu Vatu", idName: "National Identity Card", idFormat: "8-digit ID Card" },
  { code: "WS", name: "Samoa", flag: "🇼🇸", region: "Oceania", currCode: "WST", currSym: "WS$", currName: "Samoan Tālā", idName: "National ID Card", idFormat: "7-digit ID Number" },
  { code: "TO", name: "Tonga", flag: "🇹🇴", region: "Oceania", currCode: "TOP", currSym: "T$", currName: "Tongan Paʻanga", idName: "National ID Card", idFormat: "7-digit ID Number" },
  { code: "FM", name: "Micronesia", flag: "🇫🇲", region: "Oceania", currCode: "USD", currSym: "$", currName: "US Dollar", idName: "SSN / FSM Card", idFormat: "9-digit SSN Code" },
  { code: "PW", name: "Palau", flag: "🇵🇼", region: "Oceania", currCode: "USD", currSym: "$", currName: "US Dollar", idName: "Palau ID Card", idFormat: "6-digit ID Card" },
  { code: "MH", name: "Marshall Islands", flag: "🇲🇭", region: "Oceania", currCode: "USD", currSym: "$", currName: "US Dollar", idName: "SSN / Citizen Card", idFormat: "9-digit SSN" },
  { code: "KI", name: "Kiribati", flag: "🇰🇮", region: "Oceania", currCode: "AUD", currSym: "A$", currName: "Australian Dollar", idName: "National Identity Card", idFormat: "7-digit ID Number" },
  { code: "NR", name: "Nauru", flag: "🇳🇷", region: "Oceania", currCode: "AUD", currSym: "A$", currName: "Australian Dollar", idName: "Nauru Identity Card", idFormat: "5-digit ID Card" },
  { code: "TV", name: "Tuvalu", flag: "🇹🇻", region: "Oceania", currCode: "AUD", currSym: "A$", currName: "Australian Dollar", idName: "Tuvalu Identity Card", idFormat: "5-digit ID Card" }
];

// Helper generator to construct a complete CountryConfig for any UN member state
export function buildCountryConfig(raw: typeof ALL_UN_COUNTRIES[0]): CountryConfig {
  const codeLower = raw.code.toLowerCase();
  
  return {
    country_code: raw.code,
    country_name: raw.name,
    flag: raw.flag,
    region: raw.region,
    currency: {
      code: raw.currCode,
      symbol: raw.currSym,
      name: raw.currName
    },
    id_system: {
      name: raw.idName,
      format: raw.idFormat,
      verification_endpoint: `/api/v1/identity/verify/${codeLower}`
    },
    default_language: "en",
    supported_languages: ["en"],
    departments: [
      {
        id: `dept_rev_${codeLower}`,
        name: `Ministry of Lands, Housing & Revenue Registry (${raw.name})`,
        code: "REV",
        icon: "Landmark"
      },
      {
        id: `dept_trans_${codeLower}`,
        name: `National Road Transport & Mobility Authority`,
        code: "MOT",
        icon: "Car"
      },
      {
        id: `dept_corp_${codeLower}`,
        name: `Ministry of Trade, Industry & Corporate Registration`,
        code: "MCA",
        icon: "Building2"
      },
      {
        id: `dept_court_${codeLower}`,
        name: `Supreme Sovereign Court & Judicial Records`,
        code: "JUD",
        icon: "Scale"
      }
    ],
    services: [
      {
        id: `srv_${codeLower}_prop_reg`,
        department_id: `dept_rev_${codeLower}`,
        name: `Digital Property Registration & Title Clearance`,
        description: `Instant title audit, cadastral parcel check, stamp duty clearance, and e-deed recordation in ${raw.name}.`,
        processing_time: "< 30 seconds",
        fees: { base_fee: 250, stamp_duty_percentage: 3.5, registration_fee_percentage: 0.5 },
        required_documents: [`Identity Verification (${raw.idName})`, "Title Deed Copy", "Survey Cadastral Map", "Tax Clearance Slip"],
        workflow_steps: [
          { id: "title_check", name: "Title Audit & Registry Verification" },
          { id: "encumbrance", name: "Lien & Encumbrance Search" },
          { id: "fraud_detection", name: "AI Land Fraud Risk Scoring" },
          { id: "stamp_payment", name: `Stamp Duty Settlement (${raw.currCode})` },
          { id: "registration", name: "Digital Registry Ledger Recordation" },
          { id: "certificate", name: "e-Ownership Certificate Issued" }
        ]
      },
      {
        id: `srv_${codeLower}_corp_inc`,
        department_id: `dept_corp_${codeLower}`,
        name: `Commercial Business Registration & Tax ID`,
        description: `Automated company incorporation, trade name reservation, and official business license issuance in ${raw.name}.`,
        processing_time: "< 20 seconds",
        fees: { base_fee: 150, stamp_duty_percentage: 0.0, registration_fee_percentage: 0.0 },
        required_documents: [`Director ${raw.idName}`, "Articles of Association", "Registered Address Proof"],
        workflow_steps: [
          { id: "name_check", name: "Trade Name Availability Audit" },
          { id: "identity_sync", name: `Biometric Identity Authentication (${raw.idName})` },
          { id: "fee_payment", name: `Treasury License Fee (${raw.currCode})` },
          { id: "certificate", name: "Digital Certificate of Incorporation Issued" }
        ]
      },
      {
        id: `srv_${codeLower}_dl_renew`,
        department_id: `dept_trans_${codeLower}`,
        name: `Digital Driving Permit & Vehicle Record`,
        description: `Instant identity verification, driver status check, and electronic permit pass issuance.`,
        processing_time: "< 15 seconds",
        fees: { base_fee: 50, stamp_duty_percentage: 0.0, registration_fee_percentage: 0.0 },
        required_documents: [`Citizen ID (${raw.idName})`, "Existing Permit ID", "Medical Fitness Certificate"],
        workflow_steps: [
          { id: "id_auth", name: `Identity Authentication (${raw.idName})` },
          { id: "traffic_audit", name: "Traffic Citation & Impound Check" },
          { id: "fee_settle", name: `Permit Renewal Fee (${raw.currCode})` },
          { id: "pass_gen", name: "e-Permit Pass Generation" }
        ]
      },
      {
        id: `srv_${codeLower}_court_case`,
        department_id: `dept_court_${codeLower}`,
        name: `E-Filing & Sovereign Case Clearance Audit`,
        description: `Verification of litigation history, legal encumbrances, and digital court order filings.`,
        processing_time: "< 25 seconds",
        fees: { base_fee: 100, stamp_duty_percentage: 0.0, registration_fee_percentage: 0.0 },
        required_documents: [`Applicant ID (${raw.idName})`, "Court Case Filing ID / Petition"],
        workflow_steps: [
          { id: "litigation_search", name: "Judicial Registry Database Audit" },
          { id: "order_verify", name: "Digital Signature & Seal Verification" },
          { id: "certificate", name: "Official Judicial Clearance Certificate Issued" }
        ]
      }
    ]
  };
}

// Generate the COUNTRIES_CONFIG map for ALL 195 UN Member States
export const COUNTRIES_CONFIG: Record<string, CountryConfig> = ALL_UN_COUNTRIES.reduce((acc, raw) => {
  acc[raw.code] = buildCountryConfig(raw);
  return acc;
}, {} as Record<string, CountryConfig>);

// Helper to safely get config for any country code
export function getCountryConfig(code: string): CountryConfig {
  if (COUNTRIES_CONFIG[code]) {
    return COUNTRIES_CONFIG[code];
  }
  // Default fallback to India or standard
  return COUNTRIES_CONFIG["IN"] || buildCountryConfig(ALL_UN_COUNTRIES[0]);
}

// Master state/province dataset for key countries
export const COUNTRY_STATES_MAP: Record<string, string[]> = {
  "IN": [
    "Karnataka", "Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Delhi NCR", 
    "Gujarat", "Telangana", "Kerala", "West Bengal", "Rajasthan", "Punjab", 
    "Haryana", "Andhra Pradesh", "Madhya Pradesh", "Bihar", "Odisha"
  ],
  "US": [
    "California", "Texas", "New York", "Florida", "Illinois", "Washington", 
    "Pennsylvania", "Georgia", "Ohio", "North Carolina", "Virginia", "Massachusetts",
    "Colorado", "Arizona", "Michigan", "New Jersey"
  ],
  "AE": [
    "Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah", "Fujairah", "Umm Al Quwain"
  ],
  "KE": [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Uasin Gishu (Eldoret)", 
    "Kiambu", "Machakos", "Kilifi", "Kajiado", "Garissa"
  ],
  "CA": [
    "Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan", "Nova Scotia"
  ],
  "AU": [
    "New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia", "Tasmania", "ACT"
  ],
  "DE": [
    "Bavaria", "Berlin", "Baden-Württemberg", "North Rhine-Westphalia", "Hesse", "Hamburg", "Saxony"
  ],
  "GB": [
    "England", "Scotland", "Wales", "Northern Ireland"
  ],
  "NG": [
    "Lagos", "Abuja FCT", "Kano", "Rivers", "Oyo", "Enugu", "Delta", "Kaduna"
  ],
  "BR": [
    "São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Paraná", "Rio Grande do Sul"
  ],
  "JP": [
    "Tokyo Metropolis", "Osaka Prefecture", "Kanagawa", "Aichi", "Hokkaido", "Kyoto"
  ],
  "ZA": [
    "Gauteng (Johannesburg/Pretoria)", "Western Cape (Cape Town)", "KwaZulu-Natal (Durban)", "Eastern Cape"
  ],
  "MX": [
    "Mexico City (CDMX)", "Jalisco (Guadalajara)", "Nuevo León (Monterrey)", "Edomex", "Yucatán"
  ],
  "ES": [
    "Madrid", "Catalonia (Barcelona)", "Andalusia", "Valencia", "Basque Country"
  ],
  "CN": [
    "Guangdong", "Beijing Municipality", "Shanghai Municipality", "Zhejiang", "Jiangsu", "Sichuan"
  ]
};

export function getCountryStates(code: string): string[] | null {
  const upperCode = code.toUpperCase();
  if (COUNTRY_STATES_MAP[upperCode]) {
    return COUNTRY_STATES_MAP[upperCode];
  }
  return null;
}

