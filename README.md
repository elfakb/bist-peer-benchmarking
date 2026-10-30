# BIST Food Retail Peer Benchmarking

Financial statement analysis and peer benchmarking of three Borsa Istanbul food retailers: BIM, Migros and Sok Marketler.

## Objective

Evaluate the three companies on profitability, leverage, liquidity, growth and cash generation together, rather than ranking them by revenue alone.

## Data

- Source: Yahoo Finance (`yfinance`), annual consolidated statements.
- Companies: BIMAS.IS, MGROS.IS, SOKM.IS.
- Period: [START]–[END]. All amounts in TRY million.
- The raw extract is stored with its fetch date for reproducibility.
- Validation: [state which figures you checked against KAP, or remove this line].

## Methodology

1. `fetch_data.py` downloads income statement, balance sheet and cash flow data.
2. `clean_data.py` maps Yahoo line items to a standard schema, converts units, derives missing gross profit where possible and writes a data quality log.
3. `calculate_ratios.py` computes all ratios and the peer comparison table.
4. `quality_checks.py` flags balance sheet inconsistencies and unusual values.
5. `load_to_sqlite.py` loads the tables into SQLite, where `ratio_views.sql` reproduces the ratios in SQL.

### Key definitions

- ROA and ROE use year-end balances, not averages.
- Debt-to-equity = total liabilities / equity.
- Net debt / EBITDA is reported with and without lease liabilities (IFRS 16). Without leases = (total debt - lease liabilities - cash) / EBITDA.
- Free cash flow = operating cash flow - capital expenditure. Lease payments are not deducted.
- Cash conversion = operating cash flow / net income.
- Growth is year-over-year. The 2022-2023 transition is excluded (see Limitations).

## Results

### Latest fiscal year

| Metric | BIM | Migros | Sok |
|---|---|---|---|
| Gross margin (%) | 19.34 | 24.31 | 20.54 |
| Operating margin (%) | 2.48 | 2.81 | -1.62 |
| Net margin (%) | 2.58 | 1.57 | -0.69 |
| ROA (%) | 5.51 | 3.09 | -1.82 |
| ROE (%) | 11.25 | 8.18 | -5.44 |
| Current ratio | 1.03 | 0.79 | 0.86 |
| Quick ratio | 0.53 | 0.36 | 0.22 |
| Debt-to-equity | 1.03 | 1.64 | 1.98 |
| Net debt / EBITDA, incl. leases | 0.75 | 0.09 | 0.28 |
| Net debt / EBITDA, excl. leases | -0.04 | -0.49 | -0.52 |
| Revenue growth (%) | 6.03 | 7.34 | 5.36 |
| Operating profit growth (%) | 118.39 | 57.96 | 58.32 |
| Net income growth (%) | -23.41 | -22.07 | n/m |
| Operating cash flow (TRY mn) | 40,903 | 28,655 | 22,287 |
| Free cash flow (TRY mn) | 19,620 | 14,842 | 17,125 |
| Cash conversion (x) | 2.20 | 4.43 | n/m |

### Multi-year averages

| Metric | BIM | Migros | Sok |
|---|---|---|---|
| Gross margin (%) | 16.90 | 21.19 | 19.68 |
| Operating margin (%) | 1.83 | 0.61 | -1.56 |
| Net margin (%) | 4.20 | 3.77 | 2.18 |
| ROA (%) | 9.24 | 7.02 | 4.09 |
| ROE (%) | 19.53 | 19.27 | 11.29 |
| Current ratio | 1.00 | 0.81 | 0.91 |
| Debt-to-equity | 1.08 | 1.69 | 1.78 |
| Operating cash flow (TRY mn) | 32,176 | 25,089 | 18,658 |
| Free cash flow (TRY mn) | 14,936 | 15,056 | 13,938 |

n/m: not meaningful (net income near zero or sign change). Average growth figures are omitted for the same reason.

## Key findings

1. **BIM has the strongest overall profile.** It leads on ROA, ROE, net margin, current ratio and operating cash flow, and has the lowest debt-to-equity.
2. **Migros combines the highest gross margin with the weakest liquidity.** It has the best gross margin (24.31%) and fastest latest revenue growth (7.34%), but its current ratio is 0.79 and debt-to-equity is 1.64.
3. **Sok is the riskiest profile.** It reports an operating loss, a net loss, negative ROE and the highest debt-to-equity (1.98). Yet its operating cash flow (22,287) and free cash flow (17,125) are strongly positive, so profit and cash tell different stories.

Other observations:

- Operating profit grew in the latest year for all three while net income fell. This suggests that items below operating profit, such as financing costs, tax or inflation accounting effects, absorbed the gain. This is a hypothesis and needs verification in the notes to the statements.
- Low quick ratios are typical of grocery retail, where inventory turns quickly and suppliers finance working capital. They should not be read in isolation as distress.
- On an excl.-lease basis all three show negative net debt, meaning cash exceeds non-lease borrowings. Including leases, net debt / EBITDA is below 1x for all three.

## Limitations

- **TMS 29 (inflation accounting).** Statements from 2023 onward are expressed in year-end purchasing power, earlier years are nominal. Growth for the transition year is excluded, and multi-year averages mix nominal and restated figures.
- **Data source.** Yahoo Finance is not an official filing source. Line item definitions can differ from KAP and may change over time. Some items (lease liabilities, capex) may be incomplete.
- **Free cash flow overstates cash available**, because principal lease payments are classified as financing and not deducted. For retailers this is material.
- **Year-end ratios.** ROA and ROE are distorted when balance sheets change quickly.
- **Sample size.** Three companies and a short period do not support statistical conclusions.
- **Ratios near zero** (net income growth, cash conversion) are unstable and are flagged as not meaningful.

## Topics for further analysis

- Reconcile figures with KAP filings and notes to the statements.
- Decompose the gap between operating profit and net income (finance costs, monetary gain/loss, tax).
- Compute free cash flow after lease payments.
- Add market multiples using price data.

## Repository structure

```
bist-peer-benchmarking/
├── data/raw, data/processed
├── sql/create_tables.sql, ratio_views.sql
├── python/config.py, fetch_data.py, clean_data.py,
│          calculate_ratios.py, quality_checks.py, load_to_sqlite.py
├── powerbi/
├── reports/
└── docs/
```

## How to run

```
pip install -r requirements.txt
cd python
python fetch_data.py
python clean_data.py
python calculate_ratios.py
python quality_checks.py
python load_to_sqlite.py
```

## Power BI (optional)

An optional dashboard built on `fact_ratios.csv`, `dim_company.csv` and `dim_period.csv`, with company and year filters. [Add screenshots here, or remove this section.]

## Tools

Python (pandas, yfinance), SQL (SQLite), Power BI.



# BIST Gıda Perakende Sektörü Emsal Karşılaştırması

Borsa İstanbul'da işlem gören üç gıda perakendecisinin (BIM, Migros, Şok Marketler) finansal tablo analizi ve emsal karşılaştırması.

## Amaç

Üç şirketi yalnızca gelire göre sıralamak yerine kârlılık, borçluluk, likidite, büyüme ve nakit üretimi açısından birlikte değerlendirmek.

## Veri

- Kaynak: Yahoo Finance (`yfinance`), yıllık konsolide tablolar.
- Şirketler: BIMAS.IS, MGROS.IS, SOKM.IS.
- Dönem: [BAŞLANGIÇ]–[BİTİŞ]. Tüm tutarlar milyon TL.
- Ham veri, tekrar üretilebilirlik için çekim tarihiyle saklanır.
- Doğrulama: [KAP'tan kontrol ettiğin kalemleri yaz veya bu satırı sil].

## Yöntem

1. `fetch_data.py` gelir tablosu, bilanço ve nakit akış verilerini indirir.
2. `clean_data.py` Yahoo kalemlerini standart şemaya eşler, birimleri dönüştürür, mümkünse eksik brüt kârı türetir ve veri kalite kaydı oluşturur.
3. `calculate_ratios.py` tüm oranları ve emsal karşılaştırma tablosunu hesaplar.
4. `quality_checks.py` bilanço tutarsızlıklarını ve olağandışı değerleri işaretler.
5. `load_to_sqlite.py` tabloları SQLite'a yükler, `ratio_views.sql` oranları SQL ile yeniden üretir.

### Temel tanımlar

- ROA ve ROE ortalama değil dönem sonu bakiyelerle hesaplanır.
- Borç / Öz kaynak = toplam yükümlülükler / öz kaynaklar.
- Net borç / FAVÖK, kiralama yükümlülükleri (TFRS 16) dahil ve hariç verilir. Kiralama hariç = (toplam borç - kiralama yükümlülüğü - nakit) / FAVÖK.
- Serbest nakit akışı = işletme nakit akışı - yatırım harcaması. Kiralama ödemeleri düşülmemiştir.
- Nakit dönüşümü = işletme nakit akışı / net kâr.
- Büyüme yıllık değişimdir. 2022-2023 geçiş dönemi hariç tutulur (Sınırlamalar bölümüne bakın).

## Sonuçlar

### Son mali yıl

| Metrik | BIM | Migros | Şok |
|---|---|---|---|
| Brüt marj (%) | 19.34 | 24.31 | 20.54 |
| Faaliyet marjı (%) | 2.48 | 2.81 | -1.62 |
| Net marj (%) | 2.58 | 1.57 | -0.69 |
| ROA (%) | 5.51 | 3.09 | -1.82 |
| ROE (%) | 11.25 | 8.18 | -5.44 |
| Cari oran | 1.03 | 0.79 | 0.86 |
| Asit-test oranı | 0.53 | 0.36 | 0.22 |
| Borç / Öz kaynak | 1.03 | 1.64 | 1.98 |
| Net borç / FAVÖK, kiralama dahil | 0.75 | 0.09 | 0.28 |
| Net borç / FAVÖK, kiralama hariç | -0.04 | -0.49 | -0.52 |
| Gelir büyümesi (%) | 6.03 | 7.34 | 5.36 |
| Faaliyet kârı büyümesi (%) | 118.39 | 57.96 | 58.32 |
| Net kâr büyümesi (%) | -23.41 | -22.07 | anlamsız |
| İşletme nakit akışı (mn TL) | 40,903 | 28,655 | 22,287 |
| Serbest nakit akışı (mn TL) | 19,620 | 14,842 | 17,125 |
| Nakit dönüşümü (x) | 2.20 | 4.43 | anlamsız |

### Çok yıllı ortalamalar

| Metrik | BIM | Migros | Şok |
|---|---|---|---|
| Brüt marj (%) | 16.90 | 21.19 | 19.68 |
| Faaliyet marjı (%) | 1.83 | 0.61 | -1.56 |
| Net marj (%) | 4.20 | 3.77 | 2.18 |
| ROA (%) | 9.24 | 7.02 | 4.09 |
| ROE (%) | 19.53 | 19.27 | 11.29 |
| Cari oran | 1.00 | 0.81 | 0.91 |
| Borç / Öz kaynak | 1.08 | 1.69 | 1.78 |
| İşletme nakit akışı (mn TL) | 32,176 | 25,089 | 18,658 |
| Serbest nakit akışı (mn TL) | 14,936 | 15,056 | 13,938 |

"Anlamsız": net kârın sıfıra yakın olması veya işaret değiştirmesi nedeniyle yorumlanamayan değer. Aynı nedenle ortalama büyüme değerleri verilmemiştir.

## Temel bulgular

1. **BIM en güçlü genel profile sahip.** ROA, ROE, net marj, cari oran ve işletme nakit akışında öndedir, borç / öz kaynak oranı en düşüktür.
2. **Migros en yüksek brüt marjı en zayıf likidite ile birleştiriyor.** Brüt marj (%24.31) ve son yıl gelir büyümesi (%7.34) en yüksektir, ancak cari oran 0.79 ve borç / öz kaynak 1.64'tür.
3. **Şok en riskli profil.** Faaliyet zararı, net zarar, negatif ROE ve en yüksek borç / öz kaynak (1.98) vardır. Buna rağmen işletme nakit akışı (22,287) ve serbest nakit akışı (17,125) güçlü pozitiftir, yani kâr ve nakit farklı hikâyeler anlatıyor.

Diğer gözlemler:

- Son yılda üç şirketin de faaliyet kârı artarken net kârı düşmüştür. Bu, faaliyet kârının altındaki kalemlerin (finansman gideri, vergi, enflasyon muhasebesi etkileri) kazancı eritmiş olabileceğini düşündürür. Bu bir hipotezdir, finansal tablo dipnotlarından doğrulanmalıdır.
- Düşük asit-test oranı gıda perakendesinde olağandır, çünkü stok hızlı döner ve işletme sermayesi tedarikçilerce finanse edilir. Tek başına sıkıntı göstergesi sayılmamalıdır.
- Kiralama hariç bazda üç şirketin de net borcu negatiftir, yani nakit, kiralama dışı borçlardan fazladır. Kiralama dahil bazda üçünde de net borç / FAVÖK 1x altındadır.

## Sınırlamalar

- **TMS 29 (enflasyon muhasebesi).** 2023 ve sonrası tablolar yıl sonu satın alma gücüyle, önceki yıllar nominal ifade edilir. Geçiş yılı büyümesi hariç tutulmuştur, çok yıllı ortalamalar nominal ve düzeltilmiş rakamları karıştırır.
- **Veri kaynağı.** Yahoo Finance resmî bildirim kaynağı değildir. Kalem tanımları KAP'tan farklı olabilir ve zamanla değişebilir. Bazı kalemler (kiralama yükümlülüğü, yatırım harcaması) eksik olabilir.
- **Serbest nakit akışı, kullanılabilir nakdi olduğundan yüksek gösterir.** Kiralama anapara ödemeleri finansman faaliyeti sayıldığı için düşülmemiştir. Perakendede bu fark önemlidir.
- **Dönem sonu oranlar.** Bilanço hızlı değiştiğinde ROA ve ROE çarpıtılır.
- **Örneklem.** Üç şirket ve kısa dönem istatistiksel sonuç çıkarmaya yetmez.
- **Sıfıra yakın paydalar** (net kâr büyümesi, nakit dönüşümü) kararsızdır ve anlamsız olarak işaretlenmiştir.

## Daha ayrıntılı incelenmesi gereken konular

- Rakamların KAP bildirimleri ve dipnotlarla mutabakatı.
- Faaliyet kârı ile net kâr arasındaki farkın ayrıştırılması (finansman gideri, parasal kazanç/kayıp, vergi).
- Kiralama ödemeleri sonrası serbest nakit akışı.
- Hisse fiyatı ile piyasa çarpanları.

## Klasör yapısı

```
bist-peer-benchmarking/
├── data/raw, data/processed
├── sql/create_tables.sql, ratio_views.sql
├── python/config.py, fetch_data.py, clean_data.py,
│          calculate_ratios.py, quality_checks.py, load_to_sqlite.py
├── powerbi/
├── reports/
└── docs/
```

## Çalıştırma

```
pip install -r requirements.txt
cd python
python fetch_data.py
python clean_data.py
python calculate_ratios.py
python quality_checks.py
python load_to_sqlite.py
```

## Power BI (isteğe bağlı)

`fact_ratios.csv`, `dim_company.csv` ve `dim_period.csv` üzerine kurulu, şirket ve yıl filtreli isteğe bağlı dashboard. [Ekran görüntüsü ekle veya bu bölümü sil.]

## Araçlar

Python (pandas, yfinance), SQL (SQLite), Power BI.