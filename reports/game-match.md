# Game matching report

```json
{
 "vita3k_entries": 3865,
 "vita3k_distinct_ids": 3405,
 "vita3k_id_prefixes": {
  "PCSE": 1172,
  "PCSG": 1154,
  "PCSB": 855,
  "PCSH": 249,
  "PCSA": 153,
  "PCSF": 135,
  "PCSC": 93,
  "PCSD": 54
 },
 "psp_games": {
  "games": 751,
  "characters": 9261
 },
 "psp_with_vndb_disc_id": {
  "games": 543,
  "characters": 7885
 },
 "vita_games": {
  "games": 618,
  "characters": 9250
 },
 "vita_with_vndb_title_id": {
  "games": 271,
  "characters": 4169
 },
 "vita_with_vita3k_title_match": {
  "games": 340,
  "characters": 5342
 },
 "vita_with_either": {
  "games": 456,
  "characters": 7037
 },
 "vita_games_listed_in_vita3k": {
  "games": 455,
  "characters": 7026
 },
 "title_check_pairs": 325,
 "title_check_exact": 200,
 "title_check_with_suffixes": 200,
 "title_check_unique_game": 188,
 "enrichment_conflicts": 0,
 "ambiguous_vita_titles": 257,
 "clannad_v4": {
  "vndb_ids": [],
  "vita3k_ids": [
   "PCSG00415"
  ],
  "vita3k_names": [
   "CLANNAD"
  ]
 }
}
```

## Title misses (Vita3K name vs VNDB titles, normalized)

- v6618 PCSG00146: `Steins;Gate: My Darling's Embrace(比翼恋理のだーりん` vs `mingyunshizhimenbiyilianlideairen`, `steinsgatedarlingoflovingvows`, `steinsgatedoublepack`, `steinsgatedoublepackfirstpresslimitededitionset`, `steinsgatedoublepackregularedition`, `steinsgatehiyokurenrinodarling`
- v5127 PCSG00274: `Chou no Doku Hana no Kusari Taishou Tsuyakoi Ibun` vs `butterflyspoisonbloodchains`, `choudoku`, `chounodokuhananokusari`, `chounodokuhananokusaritaishoutsuyakoiibundownloadedition`, `chounodokuhananokusaritaishoutsuyakoiibunpackageedition`, `diezhiduhuazhisuo`
- v16493 PCSG00249: `White Album 2: Shiawase no Mukougawa` vs `baisexiangbu2miniafterstory`, `wa2mas`, `whitealbum2miniafterstory`, `whitealbum2shiawasenomukougawaaquaprice2800`, `whitealbum2shiawasenomukougawaasedition`, `whitealbum2shiawasenomukougawaaslimitededition`
- v1715 PCSG00811: `Hakuoki: Edo Blossoms` vs `bagaenggwibaramuijang`, `bagaenggwikkochuijang`, `baoyingguizhengaifengzhizhang`, `baoyingguizhengaihuazhizhang`, `boyingguizhengaifenghuazhuan`, `hakuokidemonofthefleetingblossom`
- v7803 PCSG00203: `AMNESIA V Edition` vs `amnesia`, `amnesiamemories`, `amnesiamemoriesdownloadedition`, `amnesiashiyizheng`, `amnesiaveditiondownloadedition`, `amnesiaveditionpackageedition`
- v9846 PCSG00272: `Diabolik Lovers Limited` vs `diablo`, `diaboliklovers`, `diaboliklovershaunteddarkbridal`, `diabolikloverslimitedvedition`, `diabolikloverslimitedveditiondownloadedition`, `diabolikloverslimitedveditionlimitededition`
- v9846 PCSG00272: `Diabolik Lovers Limited` vs `diablo`, `diaboliklovers`, `diaboliklovershaunteddarkbridal`, `diabolikloverslimitedvedition`, `diabolikloverslimitedveditiondownloadedition`, `diabolikloverslimitedveditionlimitededition`
- v14415 PCSG00429: `NORN9 LAST ERA` vs `mingyunjiuchongzoulastera`, `norn9nornnonettelastera`, `norn9nornnonettelasteradl版`, `norn9nornnonettelasteradownloadedition`, `norn9nornnonettelasteralimitededition`, `norn9nornnonettelasteraregularedition`
- v3272 PCSG00247: `Motto Nee, Chanto Shouyo! +Plus` vs `mottoneechantoshiyouyo`, `mottoneechantoshiyouyoplusdownloadedition`, `mottoneechantoshiyouyoplusregularedition`, `mottoneechantoshiyouyoplusspeciallimitededition`, `mottoneeshiyo`, `もっと姉しよ`
- v14919 PCSG00405: `Lend fleur` vs `huazhinuwang`, `queenofflowers`, `reinedesfleurs`, `reinedesfleursdemopatch`, `reinedesfleursdownloadedition`, `reinedesfleurslimiteddxpackedition`
- v15253 PCSG00410: `Nekketsu Inou Bukatsu: Trigger Kiss` vs `nekketsuinoubukatsutantriggerkiss`, `nekketsuinoubukatsutantriggerkissdownloadedition`, `nekketsuinoubukatsutantriggerkisslimitededition`, `nekketsuinoubukatsutantriggerkissregularedition`, `熱血異能部活譚triggerkiss`, `熱血異能部活譚triggerkissダウンロード版`
- v853 PCSG00481: `Shinsouban Crimson Empire ~Circumstances to Serve a Noble~` vs `crimsonempirecircumstancestoserveanoble`, `feihongdiguo`, `shinsoubancrimsonempirecircumstancestoserveanobledeluxeedition`, `shinsoubancrimsonempirecircumstancestoserveanobledownloadedition`, `shinsoubancrimsonempirecircumstancestoserveanobleregularedition`, `クリムゾンエンパイアcircumstancestoserveanoble`
- v8591 PCSG00403: `AMNESIA LATER×CROWD V Edition` vs `amnesialater`, `amnesialatercrowdveditionダウンロード版`, `amnesialatercrowdveditionパッケージ版`, `amnesialaterxcrowdveditiondownloadedition`, `amnesialaterxcrowdveditionpackageedition`, `shiyizhengamnesialater`
- v11186 PCSG00403: `AMNESIA LATER×CROWD V Edition` vs `amnesiacrowd`, `amnesialatercrowdveditionダウンロード版`, `amnesialatercrowdveditionパッケージ版`, `amnesialaterxcrowdveditiondownloadedition`, `amnesialaterxcrowdveditionpackageedition`, `shiyizhengamnesiacrowd`
- v6714 PCSG00426: `Ren’ai 0 Kilometer V` vs `lianai0gongli`, `renai0kilometer`, `renai0kilometervdownloadedition`, `renai0kilometervpackageedition`, `renzero`, `zerokiro`
- v11472 PCSG00553: `Ken Ga Kimi For V` vs `jianweijunwu`, `kengakimi`, `kengakimiforvdownloadedition`, `kengakimiforvlimitededition`, `kengakimiforvregularedition`, `kengakimimomoyotsuzuritwinpack`
- v12751 PCSG00602: `Incognito, Falling in Love ― Snow Moon Flower Love Emaki ―` vs `lianairenfatie`, `ninkoi`, `shinobikoiutsutsu`, `shinobikoiutsutsukanmitsuhanaemakitwinpack`, `shinobikoiutsutsusetsugekkakoiemakidownloadedition`, `shinobikoiutsutsusetsugekkakoiemakilimitededition`
- v15771 PCSB01177: `Crashes) Psychedelica of the black butterfly` vs `geomeunnabiuipsychedelica`, `geomeunnabiuisaikidellika`, `heidiehuanjing`, `kokuchounopsychedelica`, `kokuchounopsychedelicadownloadedition`, `kokuchounopsychedelicalimitededition`
- v7634 PCSG00470: `Hanayaka Nari, Wa ga Ichizoku: Modern Nostalgie` vs `hanayakanariwagaichizoku`, `hanayakanariwagaichizokumodernnostalgiedownloadedition`, `hanayakanariwagaichizokumodernnostalgieregularedition`, `huacaihuanghuangwuzhiyizu`, `華ヤカ哉我ガ一族`, `華ヤカ哉我ガ一族モダンノスタルジィダウンロード版`
- v6723 PCSG00469: `Clock Zero ~Shuuen no Ichibyou~ ExTime` vs `clockzeroshuuennoichibyou`, `clockzeroshuuennoichibyoudevote`, `clockzeroshuuennoichibyouextimedownloadedition`, `clockzeroshuuennoichibyouextimelimitededition`, `clockzeroshuuennoichibyouextimeregularedition`, `clockzerozhongyanzhiyimiao`
- v1803 PCSG00485: `Hakuouki's Memoirs Omokagegehana` vs `hakuokistoriesoftheshinsengumi`, `hakuokizuisouroku`, `hakuoukizuisouroku`, `hakuoukizuisourokuomokagebanadownloadedition`, `hakuoukizuisourokuomokagebanalimitededition`, `hakuoukizuisourokuomokagebanaregularedition`
- v15062 PCSE00707: `AR Nosurge Plus: Ode to an Unborn Star` vs `arnosurgeodetoanunbornstar`, `arnosurgepluscielnosurgeofflinesurgeconsertoagenttwinpack`, `arnosurgeplusodetoanunbornstaraudownloadedition`, `arnosurgeplusodetoanunbornstareudownloadedition`, `arnosurgeplusodetoanunbornstarnadownloadedition`, `arnosurgeplusodetoanunbornstarnalimitedpackageedition`
- v15062 PCSB00798: `Ar nosurge Plus: Ode to an Unborn Star` vs `arnosurgeodetoanunbornstar`, `arnosurgepluscielnosurgeofflinesurgeconsertoagenttwinpack`, `arnosurgeplusodetoanunbornstaraudownloadedition`, `arnosurgeplusodetoanunbornstareudownloadedition`, `arnosurgeplusodetoanunbornstarnadownloadedition`, `arnosurgeplusodetoanunbornstarnalimitedpackageedition`
- v11300 PCSG00506: `Hitotsu Tobashi Ren’ai V` vs `hitoren`, `hitotsutobashirenai`, `hitotsutobashirenaivdownloadedition`, `hitotsutobashirenaivlimitededition`, `hitotsutobashirenaivregularedition`, `jianjiezhilian`
- v7833 PCSG00496: `OZMAFIA!! -vivace` vs `ozmafia`, `ozmafiavivacedownloadedition`, `ozmafiavivacelimitededition`, `ozmafiavivaceregularedition`, `ozmafiavivacetrialedition`, `ozmafiavivaceダウンロード版`
- v4671 PCSG00526: `Shinsouban Okashi na Shima no Peter Pan ~Sweet Never Land~` vs `okashinashimanopeterpansweetneverland`, `peterpanofthesweetisland`, `shinsoubanokashinashimanopeterpansweetneverlanddeluxeedition`, `shinsoubanokashinashimanopeterpansweetneverlanddownloadedition`, `shinsoubanokashinashimanopeterpansweetneverlandregularedition`, `お菓子な島のピーターパンsweetneverland`
- v1316 PCSG00580: `Shinsou-ban Mahou-tsukai to Goshujin-sama` vs `mahoutsukaitogoshujinsamawizardandthemaster`, `shinsoubanmahoutsukaitogoshujinsamadeluxeedition`, `shinsoubanmahoutsukaitogoshujinsamadownloadedition`, `shinsoubanmahoutsukaitogoshujinsamaregularedition`, `新装版魔法使いとご主人様ダウンロード版`, `新装版魔法使いとご主人様豪華版`
- v16295 PCSG00640: `SA7 - Silent Ability Seven` vs `sa7`, `sa7downloadedition`, `sa7limitededition`, `sa7regularedition`, `sa7ダウンロード版`, `sa7通常版`
- v12260 PCSG00540: `ChuSingura46+1 -忠臣蔵46+1- V` vs `chushingura461忠臣蔵461vダウンロード版`, `chushingura461忠臣蔵461vパッケージ版`, `chusingura461`, `chusingura461vdownloadedition`, `chusingura461vpackageedition`, `chuushingura461`
- v10950 PCSG00574: `School Wars ~Zenkan Pack Honpen & Sotsugyou Sensen~` vs `schoolwars`, `schoolwarszenkanpackhonpensotsugyousensendeluxeedition`, `schoolwarszenkanpackhonpensotsugyousensendownloadedition`, `schoolwarszenkanpackhonpensotsugyousensenregularedition`, `スクールウォーズ`, `スクールウォーズ全巻パック本編卒業戦線ダウンロード版`
- v12019 PCSG00574: `School Wars ~Zenkan Pack Honpen & Sotsugyou Sensen~` vs `schoolwarsgraduationwarfront`, `schoolwarssotsugyousensen`, `schoolwarszenkanpackhonpensotsugyousensendeluxeedition`, `schoolwarszenkanpackhonpensotsugyousensendownloadedition`, `schoolwarszenkanpackhonpensotsugyousensenregularedition`, `スクールウォーズ全巻パック本編卒業戦線ダウンロード版`
- v8043 PCSG00561: `12 Ji no Kane to Cinderella ～Cinderella Series Triple Zenkan Pack～` vs `12jinokanetocinderellacinderellaseriestriplezenkanpackdeluxeedition`, `12jinokanetocinderellacinderellaseriestriplezenkanpackdownloadedition`, `12jinokanetocinderellacinderellaseriestriplezenkanpackregularedition`, `12jinokanetocinderellahalloweenwedding`, `12時の鐘とシンデレラhalloweenwedding`, `12時の鐘とシンデレラシンデレラシリーズトリプル全巻パックダウンロード版`
- v10105 PCSG00561: `12 Ji no Kane to Cinderella ～Cinderella Series Triple Zenkan Pack～` vs `12jinokanetocinderellacinderellaseriestriplezenkanpackdeluxeedition`, `12jinokanetocinderellacinderellaseriestriplezenkanpackdownloadedition`, `12jinokanetocinderellacinderellaseriestriplezenkanpackregularedition`, `12時の鐘とシンデレラシンデレラシリーズトリプル全巻パックダウンロード版`, `12時の鐘とシンデレラシンデレラシリーズトリプル全巻パック豪華版`, `12時の鐘とシンデレラシンデレラシリーズトリプル全巻パック通常版`
- v11879 PCSG00561: `12 Ji no Kane to Cinderella ～Cinderella Series Triple Zenkan Pack～` vs `0jinokanetocinderellahalloweenwedding`, `0時の鐘とシンデレラhalloweenwedding`, `12jinokanetocinderellacinderellaseriestriplezenkanpackdeluxeedition`, `12jinokanetocinderellacinderellaseriestriplezenkanpackdownloadedition`, `12jinokanetocinderellacinderellaseriestriplezenkanpackregularedition`, `12時の鐘とシンデレラシンデレラシリーズトリプル全巻パックダウンロード版`
- v9915 PCSG00576: `Hanayaka Nari, Wa ga Ichizoku: Gentou Nostalgie` vs `hanayakanariwagaichizokugentounostalgiedownloadedition`, `hanayakanariwagaichizokugentounostalgieregularedition`, `hanayakanariwagaichizokukinemamosaic`, `huacaihuanghuangwuzhiyizudengyingwanhuajing`, `華ヤカ哉我ガ一族キネマモザイク`, `華ヤカ哉我ガ一族幻燈ノスタルジィダウンロード版`
- v12188 PCSG00576: `Hanayaka Nari, Wa ga Ichizoku: Gentou Nostalgie` vs `hanayakanariwagaichizokugentounostalgiedownloadedition`, `hanayakanariwagaichizokugentounostalgieregularedition`, `hanayakanariwagaichizokutasogarepolarstar`, `huacaihuanghuangwuzhiyizuhuanghunbeijixing`, `華ヤカ哉我ガ一族幻燈ノスタルジィダウンロード版`, `華ヤカ哉我ガ一族幻燈ノスタルジィ通常版`
- v4540 PCSG00604: `Beast Tamer and Prince ～Flower ＆ Snow～` vs `beastmasterandprince`, `beastmasterandprinces`, `moujuutsukaitooujisama`, `moujuutsukaitooujisamaflowersnowdownloadedition`, `moujuutsukaitooujisamaflowersnowpackageedition`, `猛獣使いと王子様`
- v4540 PCSG00244: `Beast Tamer and Prince` vs `beastmasterandprince`, `beastmasterandprinces`, `moujuutsukaitooujisama`, `moujuutsukaitooujisamaflowersnowdownloadedition`, `moujuutsukaitooujisamaflowersnowpackageedition`, `猛獣使いと王子様`
- v7815 PCSG00604: `Beast Tamer and Prince ～Flower ＆ Snow～` vs `beastmasterandprincessnowbride`, `moujuutsukaitooujisamaflowersnowdownloadedition`, `moujuutsukaitooujisamaflowersnowpackageedition`, `moujuutsukaitooujisamasnowbride`, `猛獣使いと王子様flowersnowダウンロード版`, `猛獣使いと王子様flowersnowパッケージ版`
- v14759 PCSG00666: `Ayakashi Gohan: Oomori!` vs `ayakashigohan`, `ayakashigohanoomoridownloadedition`, `ayakashigohanoomorifirstpresslimitededition`, `ayakashigohanoomoriregularedition`, `yaoguaifan`, `yaoguaimifan`
- v12282 PCSG00618: `Romeo VS Juliet Zenkan Pack` vs `romeovsjuliet`, `romeovsjulietallseriespackdeluxeedition`, `romeovsjulietallseriespackdownloadedition`, `romeovsjulietallseriespackregularedition`, `ロミオvsジュリエット`, `ロミオvsジュリエット全巻パックダウンロード版`
- v13911 PCSG00618: `Romeo VS Juliet Zenkan Pack` vs `romeojuliet`, `romeovsjulietallseriespackdeluxeedition`, `romeovsjulietallseriespackdownloadedition`, `romeovsjulietallseriespackregularedition`, `ロミオvsジュリエット全巻パックダウンロード版`, `ロミオvsジュリエット全巻パック豪華版`
- v17287 PCSG00713: `Hyakka Hyakurou ~Sengoku Ninpoucho~` vs `baihuabailangsengokurenfatie`, `hyakkahyakurousengokuninpouchou`, `hyakkahyakurousengokuninpouchoudownloadedition`, `hyakkahyakurousengokuninpouchoupackageedition`, `nightshade`, `百花百狼战国忍法帖`
- v17345 PCSG00826: `diabolik lovers[] can display start sceen image but crashes while click the start button` vs `diabolikloverslunaticparade`, `diabolikloverslunaticparadedl版`, `diabolikloverslunaticparadedownloadedition`, `diabolikloverslunaticparadelimitededition`, `diabolikloverslunaticparaderegularedition`, `diabolikloverslunaticparade通常版`
- v17608 PCSG00667: `LOVE:QUIZ - Koisuru Shoujo no Final Answer` vs `lovequizkoisuruotomenofinalanswer`, `lovequizkoisuruotomenofinalanswerdeluxeedition`, `lovequizkoisuruotomenofinalanswerdownloadedition`, `lovequizkoisuruotomenofinalanswerregularedition`, `lovequiz恋する乙女のファイナルアンサー`, `lovequiz恋する乙女のファイナルアンサーdl版`
- v13090 PCSG00654: `Gakuen K -Wonderful School Days- V Edition` vs `gakuenkwonderfulschooldays`, `gakuenkwonderfulschooldaysveditiondownloadedition`, `gakuenkwonderfulschooldaysveditionlimitededition`, `gakuenkwonderfulschooldaysveditionregularedition`, `keineweiteregeschichte`, `kproject`
- v13090 PCSG00654: `Gakuen K - Wonderful School Days V Edition` vs `gakuenkwonderfulschooldays`, `gakuenkwonderfulschooldaysveditiondownloadedition`, `gakuenkwonderfulschooldaysveditionlimitededition`, `gakuenkwonderfulschooldaysveditionregularedition`, `keineweiteregeschichte`, `kproject`
- v10289 PCSG00635: `Jyuzaengi: Engetsu Sangokuden 1+2` vs `juuzaengiengetsusangokuden`, `juuzaengiengetsusangokuden12downloadedition`, `juuzaengiengetsusangokuden12packageedition`, `shisanzhiyanyiyanyuesanguozhuan`, `十三支演义偃月三国传`, `十三支演義偃月三国伝`
- v12714 PCSG00635: `Jyuzaengi: Engetsu Sangokuden 1+2` vs `juuzaengiengetsusangokuden12downloadedition`, `juuzaengiengetsusangokuden12packageedition`, `juuzaengiengetsusangokuden2`, `jyuzaengiengetsusangokuden2`, `shisanzhiyanyiyanyuesanguozhuan2`, `十三支演義偃月三国伝12dl版`
- v17640 PCSG00853: `Period Cube ~Shackle of Amadeus~` vs `periodcubeshacklesofamadeus`, `periodcubeshacklesofamadeusdownloadedition`, `periodcubeshacklesofamadeuspackageedition`, `periodcubetorikagonoamadeus`, `periodcubetorikagonoamadeusdownloadedition`, `periodcubetorikagonoamadeuslimitededition`
- v17750 PCSG00829: `Kenka Bancho Otome` vs `kbo`, `kenkabanchouotome`, `kenkabanchouotomedownloadedition`, `kenkabanchouotomeregularedition`, `xuanhuafanzhangyinu`, `喧嘩番長乙女`
- v17750 PCSG00829: `Kenka Bancho Otome` vs `kbo`, `kenkabanchouotome`, `kenkabanchouotomedownloadedition`, `kenkabanchouotomeregularedition`, `xuanhuafanzhangyinu`, `喧嘩番長乙女`
- v13325 PCSG00716: `Clover Day's ～Making for Happiness.～` vs `cld`, `cloverdays`, `cloverdaysmakingforhappinessdownloadedition`, `cloverdaysmakingforhappinessfirstpresslimitededition`, `cloverdaysmakingforhappinessregularedition`, `cloverdaysmakingforhappinessダウンロード版`
- v8203 PCSG00751: `Arcana Famiglia -La storia della Arcana Famiglia- Ancora` vs `arcanafamiglia`, `arcanafamiglialastoriadellaarcanafamigliaancoradownloadedition`, `arcanafamiglialastoriadellaarcanafamigliaancorapackageedition`, `lastoriadellaarcanafamiglia`, `shenglingjiazu`, `アルカナファミリア`
- v18159 PCSG00787: `Snow White in the Mirror Realm` vs `kyoukainoshirayuki`, `kyoukainoshirayukidownloadedition`, `kyoukainoshirayukilimitededition`, `kyoukainoshirayukiregularedition`, `namlichshirayukisnowwhiteinthemirrorrealm`, `鏡界の白雪`
- v18160 PCSE01011: `Collar x Malice [] gameplay issue` vs `collarmalicedl版`, `collarmaliceツインパック`, `collarmalice通常版`, `collarmalice限定版`, `collarxmalice`, `collarxmalicedownloadedition`
- v18160 PCSE01011: `Collar x Malice - USA - Game ID` vs `collarmalicedl版`, `collarmaliceツインパック`, `collarmalice通常版`, `collarmalice限定版`, `collarxmalice`, `collarxmalicedownloadedition`
- v18161 PCSG00948: `Suran digit` vs `suurandigit`, `suurandigitdownloadedition`, `suurandigitlimitededition`, `suurandigitregularedition`, `数乱digit`, `数乱digitdl版`
- v18163 PCSG00766: `Nil Admirari's Balance Teito Illusion Kitan` vs `lengranzhitianchengdiduhuanhuoqitan`, `libraofniladmirari`, `niladmirarinotenbinteitogenwakukitan`, `niladmirarinotenbinteitogenwakukitandownloadedition`, `niladmirarinotenbinteitogenwakukitanlimitededition`, `niladmirarinotenbinteitogenwakukitanregularedition`
- v18164 PCSG00708: `Truth Hidden Under The Rose` vs `baranikakusareshiverite`, `baranikakusareshiveritedownloadedition`, `baranikakusareshiveritelimitededition`, `baranikakusareshiveriteregularedition`, `leboucemissairedelareine`, `薔薇に隠されしヴェリテ`

## Conflicts

