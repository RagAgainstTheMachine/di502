---
doc_id: Doc07
title: TÜBİTAK Yapay Zekâ Politikası
source_pdf: doc07_tubitak_yapay_zeka_politikasi.pdf
source_pdf_sha256: 928085bab9a9df26512a6f2139d1889861da5ad314e52d4cdd4be7f0b8050d39
source_pdf_pages: 8
tool: PyMuPDF 1.28.2 (MuPDF 1.28.2), Python 3.10.12
extractor: src/extraction/extract.py (sha256 377ed8abb1aff0b3…)
extraction_date: '2026-11-02'
part_used_inventory: All, 8 pp.
pages_used: PDF pages 1–8
selection_rule: All 8 pages. Page number (bottom 85 pt) moved into the marker; the ruled table on p. 5 is read cell by cell.
page_marker_format: '<!-- page: pdf N | printed M -->  (printed = number printed on the page, or none)'
verbatim: text-layer only; line breaks become spaces; a line-end hyphen is removed only when the joined word occurs elsewhere
  in the same PDF (see report)
status: reviewed_against_pdf
review_date: '2026-11-10'
source_markdown_sha256: 14d644c9e4a5ddd32d49f5632c11130635a0a29baa7f1c43c9ddbf6b0c557a85
review_scope: 8 PDF sayfasının tamamı; kapak ve kaynakça dahil.
review_tools: pypdfium2; pypdf; sekiz kaynak sayfanın görüntüsü
review_notes: Metin aktarımı doğrulandı. Başlık seviyeleri, giriş paragrafları, dört liste maddesi, üç sayfa geçişi, beş satırlı
  politika tablosu ve dört kaynak kaydı düzenlendi. Kaynağın ifadeleri değiştirilmedi.
retrieval_preprocessing:
  policy_version: 1
  reviewed_markdown_file: doc07_tubitak_yapay_zeka_politikasi.md
  reviewed_markdown_sha256: 2585c8d492ceaee5b8491b700455f95fed6b4759aac1899290f5f9baea90dcb7
  excluded_pdf_pages:
  - 1
  - 8
  retained_pdf_pages:
  - 2
  - 3
  - 4
  - 5
  - 6
  - 7
  citation_callouts_removed: 13
  bibliography_records_archived: 4
  numbered_policy_sections_retained_in_section_metadata: true
---

# TÜBİTAK Yapay Zekâ Politikası



<!-- page: pdf 1 | printed none -->

<!-- page: pdf 2 | printed 1 -->



## Giriş

Türkiye Bilimsel ve Teknolojik Araştırma Kurumu’nun (TÜBİTAK) kurumsal süreçlerinde yapay zekâ (YZ) teknolojilerinden üst düzeyde faydalanarak veriye dayalı karar alma kültürünü yerleştirmek, operasyonel verimliliği artırmak ve bilimsel araştırma kapasitesini güçlendirmek için temel çerçeveyi belirlemek amacıyla bu politika belgesi hazırlanmıştır. Politikanın nihai hedefi, TÜBİTAK'ı YZ'yi içselleştiren, bu teknolojiyle verimli bir şekilde kullanabilen ve Ar-Ge ve yenilik süreçlerinde YZ'den etkin bir araç olarak faydalanabilen öncü bir kuruma dönüştürmektir.

Bu politika belgesi, TÜBİTAK Başkanlık, merkez ve enstitülerinin proje yönetimi, idari operasyonları, mali süreçleri, insan kaynakları yönetimi ve Ar-Ge ve yenilik faaliyetleri dâhil olmak üzere tüm fonksiyonlarını kapsar.

Türkiye’nin aşağıda özetlenen ulusal hedefleri ve strateji belgeleriyle uyum içinde tasarlanmış olan bu politika belgesi, kurumsal YZ politikasını bir tercihten ziyade, bir zorunluluk olarak konumlandırmaktadır. Bu sayede, kurum içinde kaynak tahsisi ve değişim yönetimi süreçlerinde politikanın uygulanabilirliği artırılmaktadır.

- **Milli Teknoloji Hamlesi Vizyonu:** Politika, Türkiye'nin teknolojik bağımsızlık ve küresel rekabetçilik hedeflerine hizmet eden Milli Teknoloji Hamlesi vizyonunun kurumsal düzeydeki bir yansımasıdır. TÜBİTAK'ın YZ'yi kendi süreçlerine entegre etmesi, "Türkiye'nin milli teknoloji hamlesine liderlik eden kurum olma" vizyonunun bir gereğidir.

- **Ulusal Yapay Zekâ Stratejisi (UYZS) 2021-2025:** Politika belgesi UYZS'nin "Kaliteli Veriye ve Teknik Altyapıya Erişim İmkânlarını Genişletmek" ve "YZ Uzmanlarını Yetiştirmek ve Alanda İstihdamı Artırmak" gibi stratejik önceliklerinin, TÜBİTAK bünyesinde somut adımlarla hayata geçirilmesi için kurumsal bir politika çerçevesi sunar.

- **On İkinci Kalkınma Planı ve 2030 Sanayi ve Teknoloji Stratejisi:** Üst politika belgelerinde vurgulanan dijital dönüşüm, yüksek katma değerli üretim, verimlilik artışı ve inovasyon odaklı ekosistem hedefleri, bu belgenin temel dayanaklarını oluşturur.

- **TÜBİTAK 2024-2028 Stratejik Planı:** Politika, doğrudan TÜBİTAK Stratejik Planı'nın "Amaç 4: Sürdürülebilir yönetişim modeli ve operasyonel verimlilik ile kurumsal kapasiteyi güçlendirmek" başlığı altında yer alan "Hedef 4.1: Süreç bazlı iyileştirmeler doğrultusunda yalınlaştırma, ortaklaştırma ve dijitalleşme ile operasyonel verimlilik artırılacaktır" maddesine de hizmet etmek üzere tasarlanmıştır. Makro hedeflerle mikro uygulamalar arasında bir köprü görevi görerek TÜBİTAK'ın YZ dönüşümünü stratejik bir çerçeveye 

<!-- page: pdf 3 | printed 2 -->

 oturtması amaçlanmaktadır.

## 1. Temel İlkeler

TÜBİTAK'ın YZ'ye yaklaşımının etik ve stratejik çerçevesini oluşturan ve aşağıda detayları sunulan bu ilkeler, Kurum içinde geliştirilecek veya kullanılacak tüm YZ uygulamaları için bağlayıcıdır.

### 1.1. İnsan Odaklılık ve Etik Değerlere Bağlılık

Yapay zekâ sistemleri, insan zekâsını ve yeteneklerini ikame etmek için değil, onları desteklemek ve güçlendirmek için bir araç olarak görülmektedir. Tüm uygulamalar; şeffaflık, açıklanabilirlik, adalet, ayrımcılık yapmama ve hesap verebilirlik gibi evrensel etik ilkelere bağlıdır. Karar süreçlerinde insan denetimi ve nihai onayı esastır.

### 1.2. Stratejik Özerklik ve Verimlilik Dengesi

YZ çözümlerinin geliştirilmesi ve tedarikinde yerli ve milli yetkinliklerin geliştirilmesi esastır. Ancak, hızlı sonuç alınması gereken alanlarda, küresel çapta kabul görmüş en iyi uygulamalardan ve hazır çözümlerden faydalanılarak verimlilik sağlanabilir. Türkiye'nin teknolojik bağımsızlığına katkı sağlama misyonu, bir yanda kritik YZ alanlarında (örneğin, milli güvenlikle ilgili projeler, Türkçe dil modelleri) yerli yetkinlik geliştirme yaklaşımını gerektirirken; diğer yanda, bir kamu kurumu olarak kaynakları verimli kullanma zorunluluğu, standart idari süreçlerde (örneğin, doküman yönetimi, talep takibi) kanıtlanmış ve uygun maliyetli çözümleri benimseme yaklaşımını gerektirir.

### 1.3. Veriye Dayalı Yönetim ve Gelişim Kültürü

Veri, Kurumun en değerli stratejik varlıklarından biri olarak kabul edilir. Karar alma süreçleri, politika geliştirme, kaynak tahsisi ve performans ölçümü; doğrulanmış ve kaliteli veriye dayalı analitik modellerle desteklenir. Kurumun her seviyesinde veri kalitesinin geliştirilmesi ile birlikte, veriye dayalı karar verme, düşünme ve yönetme kültürü teşvik edilir.

### 1.4. Güvenilirlik, Güvenlik ve Mahremiyet

Kurum içinde geliştirilen veya kullanılan tüm YZ sistemlerinin güvenli, dayanıklı, sürdürülebilir 

<!-- page: pdf 4 | printed 3 -->

 ve gerekli siber güvenlik standartlarına uygun olması hedeflenir. Veri mahremiyeti ile ilgili tüm mevzuata tam uyum ve kurumsal bilgilerin gizliliğinin korunması önceliktir. Kişisel verilerin etik ve yasal çerçeve içinde toplanması, saklanması ve işlenmesi temel bir hassasiyet olarak değerlendirilir.

### 1.5. Çevik ve Sonuç Odaklı Yaklaşım

YZ teknolojilerinin hızla geliştiği göz önünde bulundurularak, politika ve uygulamalar dinamik bir yaklaşımla yönetilir. Bu sayede pilot projelerle denemeler yapılması, hızlı öğrenme süreçlerinin ve başarılı modellerin Kurum geneline hızla uyarlanması teşvik edilir.

### 1.6. Mevzuat ve Uyum

Kurum bünyesinde geliştirilen, tedarik edilen veya kullanılan tüm yapay zekâ sistem ve uygulamaları, yürürlükteki ulusal ve uluslararası mevzuata, düzenlemelere ve standartlara uyum sağlamak zorundadır. Bu çerçevede, başta Anayasa ve 6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) olmak üzere veri mahremiyetine ilişkin tüm yasal yükümlülüklere titizlikle riayet edilir, kişisel verilerin işlendiği tüm YZ süreçleri bu düzenlemelere uygun olarak tasarlanır ve denetlenir. Aynı zamanda, YZ sistemlerinin sorumlu bir şekilde yönetilmesi, risklerinin değerlendirilmesi ve hesap verebilirliğinin sağlanması amacıyla ISO/IEC 42001 (Yapay Zekâ Yönetim Sistemi) standardı referans alınır. Bu sistemlerin dayandığı bilgi varlıklarının güvenliğini ve bütünlüğünü temin etmek için ise ISO/IEC 27001 (Bilgi Güvenliği Yönetim Sistemi) standardının gereklilikleri esas alınır. Böylece TÜBİTAK'ın YZ alanındaki faaliyetlerinin yalnızca teknolojik olarak değil, aynı zamanda hukuki ve etik açıdan da sağlam bir zeminde yürütülmesi güvence altına alınır.



<!-- page: pdf 5 | printed 4 -->



## 2. Politika Alanları

Bu bölümde, temel ilkelerin Kurumun hangi fonksiyonel alanlarında ve nasıl hayata geçirileceği tanımlanmıştır. Aşağıdaki tablo, her politika alanının stratejik çerçevesini özetlemektedir.

| Politika Alanı | Amaç | Dayanak |
| --- | --- | --- |
| Veri Yönetişimi ve Stratejik Varlık Olarak Verinin Yönetimi | YZ uygulamaları için sağlam, kaliteli ve erişilebilir bir veri temeli oluşturmak. | UYZS: Kaliteli Veriye Erişim |
| Operasyonel Süreçlerin YZ ile Optimizasyonu | İdari ve destek süreçlerinde verimliliği artırmak, maliyetleri düşürmek ve personeli katma değerli işlere yönlendirmek. | TÜBİTAK SP 2024-2028: Hedef 4.1 (Operasyonel Verimlilik), OECD Governing with Artificial Intelligence |
| Ar-Ge ve Yenilik Süreçlerinin Hızlandırılması | YZ'yi kolaylaştırıcı bir araç olarak kullanarak inovasyon döngüsünü kısaltmak ve bilimsel etkiyi artırmak. | 2030 Sanayi ve Teknoloji Stratejisi: Yüksek Teknoloji |
| Kurumsal Yetkinlik ve Yetenek Yönetimi | Kurumun YZ'yi etkin kullanacak ve geliştirecek insan kaynağı kapasitesini oluşturmak ve sürdürülebilirliğini sağlamak. | UYZS: YZ Uzmanlarını Yetiştirmek |
| Teknoloji Altyapısı | Modern YZ uygulamaları için gerekli olan hesaplama ve depolama altyapısını sağlamak. | UYZS: Teknik Altyapı |

### 2.1. Veri Yönetişimi ve Stratejik Varlık Olarak Verinin Yönetimi

YZ girişimlerinin başarılı olması için kaliteli, erişilebilir ve standartlaştırılmış veri önem taşımaktadır. TÜBİTAK bünyesindeki tüm verinin (destek programları, idari ve mali süreçler, Ar-Ge ve yenilik süreçleri, insan kaynakları süreçleri vb.) standartlaştırılmış, merkezi bir yönetişim çerçevesine tabi olması hedeflenir. Veri silolarının ortadan kaldırılması, veri kalitesinin sürekli olarak izlenmesi ve iyileştirilmesi gözetilir.

### 2.2. Operasyonel Süreçlerin YZ ile Optimizasyonu

İdari, mali, insan kaynakları, satın alma ve destek hizmetleri gibi tekrara dayalı ve kural tabanlı tüm kurumsal süreçlerde verimliliği artırmak, insan hatasını azaltmak ve kaynak kullanımını optimize etmek amacıyla YZ tabanlı otomasyon ve karar destek sistemleri benimsenir. Böylece TÜBİTAK Stratejik Planı'ndaki verimlilik hedefine doğru ilerlenmesi planlanmaktadır. Amaç çalışanları rutin ve tekrarlı görevlerden daha stratejik ve katma değerli görevlere yönlendirmektir.



<!-- page: pdf 6 | printed 5 -->



### 2.3. Ar-Ge ve Yenilik Süreçlerinin YZ ile Hızlandırılması

YZ, TÜBİTAK nezdinde yürütülen Ar-Ge ve yenilik faaliyetlerinde bilimsel ve teknolojik geliştirme süreçlerini hızlandıracak bir katalizör olarak konumlandırılır. Büyük veri analizi, karmaşık sistem modellemesi, hipotez geliştirme, deney tasarımı ve sonuçların yorumlanması gibi süreçlerde YZ araçlarının kullanımı teşvik edilir ve desteklenir. Bu yaklaşım YZ'yi bir bilişim teknolojisi aracı olmaktan çıkarıp, temel bir bilimsel enstrümana dönüştürür ve TÜBİTAK’ın ana misyonlarından birisi olan bilgi ve teknoloji üretimine doğrudan olumlu şekilde etki eder.

### 2.4. Kurumsal Yetkinlik ve Yetenek Yönetimi

Teknoloji tek başına yeterli değildir; onu kullanacak ve geliştirecek insan kaynağı kritik öneme sahiptir. Bu doğrultuda, tüm TÜBİTAK personelinin temel YZ okuryazarlığı seviyesine ulaşması, araştırmacılar ve teknik personelin ise ileri düzey YZ yetkinlikleri kazanabileceği programların oluşturulması hedeflenir. YZ alanında istihdamın nitelik ve niceliğini artırmaya, YZ alanında uzman yeteneklerin Kuruma kazandırılmasına yönelik çalışmalar yapılır. Ayrıca, başarılı uygulamalar için deneyim paylaşımına yönelik etkinliklerin gerçekleştirilmesi teşvik edilir.

### 2.5. Teknoloji Altyapısı ve Ekosistem Yönetimi

Büyük ölçekli YZ modellerinin eğitimi ve kullanımı, yüksek miktarda hesaplama gücü gerektirmektedir. Bu ihtiyacı karşılamak üzere, TÜBİTAK'ın operasyonel ihtiyaçlarını karşılayacak, ölçeklenebilir ve güvenli bir Yüksek Başarımlı Hesaplama (YBH) ve veri depolama altyapısına erişimin artırılması için çalışmalar yapılır. Ayrıca, kaynak israfını önlemek ve Kurum içinde bilgi birikiminin yayılmasını sağlamak amacıyla, ortak YZ platformları, araç setleri, modeller ve gerekli uyarıların paylaşıldığı bir iç ekosistemin oluşturulması teşvik edilir.

## 3. Uygulama, İzleme ve Yönetişim

Bu politikanın etkin bir şekilde hayata geçirilmesi, Kurum içindeki YZ faaliyetlerinin koordine edilmesi ve stratejik önceliklerin belirlenmesinden sorumlu bir Yapay Zekâ Koordinasyon Grubu kurulmuştur. Bu Grup, Kurumun tüm birimlerini ilgilendiren stratejik bir ekip olarak görev yapar. Söz konusu Grup, Ar-Ge'den insan kaynaklarına, finanstan hukuka kadar tüm paydaşları aynı masada toplayarak Kurum genelinde bir sahiplenme ve eşgüdüm sağlayarak, kaynakların önceliklendirilmesi, standartların belirlenmesi ve ortaya çıkan sorunların hızla çözülmesi ve 

<!-- page: pdf 7 | printed 6 -->

 politikanın etkin bir şekilde uygulanması için çalışmalar yürütür. Grup, kurumsal politika alanlarındaki ilerlemeyi (model yaşam döngüleri, yapay zekâ etki değerlendirmesi, başarı ölçütleri ve denetimlere ilişkin başarı metrikleri, IS0 42001 iç denetim periyotları vb. yöntemlerle) izleyerek dokümante eder. Ek olarak, ilgili birimlerden temsilcilerin oluşturduğu Birim Temsilcileri Grubu aracılığı ile birimler arası koordinasyon ve sürekli iletişimi sağlar.

## 4. Sonuç

İşbu politika belgesi, TÜBİTAK’ın yapay zekâ teknolojilerini tüm kurumsal süreçlerine entegre ederek operasyonel verimliliği artırmasını ve bilimsel araştırma kapasitesini güçlendirmesini sağlayan temel stratejik çerçeveyi çizmektedir. Milli Teknoloji Hamlesi vizyonu ve Ulusal Yapay Zekâ Stratejisi hedefleriyle tam uyum içinde hazırlanan metin, dijital dönüşümü kurumsal bir tercihten ziyade bir zorunluluk olarak konumlandırmaktadır. Kurum, yapay zekâ uygulamalarında insan odaklılığı, etik değerlere bağlılığı ve şeffaflığı esas alarak, teknolojiyi insan zekâsını ikame eden değil onu güçlendiren bir araç olarak tanımlamaktadır. Stratejik özerklik ilkesi doğrultusunda kritik alanlarda yerli yetkinliklerin geliştirilmesi hedeflenirken, standart süreçlerde küresel çözümlerden faydalanılarak kaynak verimliliği dengesi gözetilmiştir. Verinin en değerli varlık olduğu bilinciyle yönetim süreçlerinin analitik temellere dayandırıldığı merkezi bir veri yönetişim kültürü oluşturulması amaçlanmaktadır. Operasyonel süreçlerin yapay zekâ destekli otomasyonu sayesinde, idari yüklerin hafifletilmesi ve insan kaynağının daha stratejik, katma değerli bilimsel faaliyetlere odaklanması sağlanabilir. Ar-Ge ve yenilik faaliyetlerinde yapay zekânın bir hızlandırıcı olarak kullanılmasıyla, hipotez geliştirme ve veri analizi gibi aşamaların kısaltılması ve bilimsel çıktıların etkisinin artırılması planlanmaktadır. Bu dönüşümün başarısı için personel yetkinliklerinin artırılmasına ve ölçeklenebilir, güvenli bir yüksek başarımlı hesaplama altyapısının kurulmasına yönelik yatırımlar önceliklendirilmektedir. Tüm süreçlerin ilgili yasa ve standartlara uygun, güvenli, mahremiyete saygılı ve hesap verebilir bir yapıda yürütülmesi, kurumsal güvenilirlik açısından teminat altına alınmaktadır. Nihai olarak bu politika TÜBİTAK’ı, teknolojiyi sadece kullanan değil, ona yön veren öncü bir kurum olarak konumlandırmaktadır.



<!-- page: pdf 8 | printed 7 -->