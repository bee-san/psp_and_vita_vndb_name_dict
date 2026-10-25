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
  "games": 391,
  "characters": 6203
 },
 "vita_with_either": {
  "games": 476,
  "characters": 7412
 },
 "vita_games_listed_in_vita3k": {
  "games": 475,
  "characters": 7401
 },
 "title_check_pairs": 325,
 "title_check_exact": 200,
 "title_check_with_suffixes": 258,
 "title_check_unique_game": 222,
 "enrichment_conflicts": 0,
 "ambiguous_vita_titles": 308,
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
- v1715 PCSG00811: `Hakuoki: Edo Blossoms` vs `bagaenggwibaramuijang`, `bagaenggwikkochuijang`, `baoyingguizhengaifengzhizhang`, `baoyingguizhengaihuazhizhang`, `boyingguizhengaifenghuazhuan`, `hakuokidemonofthefleetingblossom`
- v9846 PCSG00272: `Diabolik Lovers Limited` vs `diablo`, `diaboliklovers`, `diaboliklovershaunteddarkbridal`, `diabolikloverslimitedvedition`, `diabolikloverslimitedveditiondownloadedition`, `diabolikloverslimitedveditionlimitededition`
- v9846 PCSG00272: `Diabolik Lovers Limited` vs `diablo`, `diaboliklovers`, `diaboliklovershaunteddarkbridal`, `diabolikloverslimitedvedition`, `diabolikloverslimitedveditiondownloadedition`, `diabolikloverslimitedveditionlimitededition`
- v14415 PCSG00429: `NORN9 LAST ERA` vs `mingyunjiuchongzoulastera`, `norn9nornnonettelastera`, `norn9nornnonettelasteradl版`, `norn9nornnonettelasteradownloadedition`, `norn9nornnonettelasteralimitededition`, `norn9nornnonettelasteraregularedition`
- v3272 PCSG00247: `Motto Nee, Chanto Shouyo! +Plus` vs `mottoneechantoshiyouyo`, `mottoneechantoshiyouyoplusdownloadedition`, `mottoneechantoshiyouyoplusregularedition`, `mottoneechantoshiyouyoplusspeciallimitededition`, `mottoneeshiyo`, `もっと姉しよ`
- v14919 PCSG00405: `Lend fleur` vs `huazhinuwang`, `queenofflowers`, `reinedesfleurs`, `reinedesfleursdemopatch`, `reinedesfleursdownloadedition`, `reinedesfleurslimiteddxpackedition`
- v15253 PCSG00410: `Nekketsu Inou Bukatsu: Trigger Kiss` vs `nekketsuinoubukatsutantriggerkiss`, `nekketsuinoubukatsutantriggerkissdownloadedition`, `nekketsuinoubukatsutantriggerkisslimitededition`, `nekketsuinoubukatsutantriggerkissregularedition`, `熱血異能部活譚triggerkiss`, `熱血異能部活譚triggerkissダウンロード版`
- v12751 PCSG00602: `Incognito, Falling in Love ― Snow Moon Flower Love Emaki ―` vs `lianairenfatie`, `ninkoi`, `shinobikoiutsutsu`, `shinobikoiutsutsukanmitsuhanaemakitwinpack`, `shinobikoiutsutsusetsugekkakoiemakidownloadedition`, `shinobikoiutsutsusetsugekkakoiemakilimitededition`
- v15771 PCSB01177: `Crashes) Psychedelica of the black butterfly` vs `geomeunnabiuipsychedelica`, `geomeunnabiuisaikidellika`, `heidiehuanjing`, `kokuchounopsychedelica`, `kokuchounopsychedelicadownloadedition`, `kokuchounopsychedelicalimitededition`
- v1803 PCSG00485: `Hakuouki's Memoirs Omokagegehana` vs `hakuokistoriesoftheshinsengumi`, `hakuokizuisouroku`, `hakuoukizuisouroku`, `hakuoukizuisourokuomokagebanadownloadedition`, `hakuoukizuisourokuomokagebanalimitededition`, `hakuoukizuisourokuomokagebanaregularedition`
- v15062 PCSE00707: `AR Nosurge Plus: Ode to an Unborn Star` vs `arnosurgeodetoanunbornstar`, `arnosurgepluscielnosurgeofflinesurgeconsertoagenttwinpack`, `arnosurgeplusodetoanunbornstaraudownloadedition`, `arnosurgeplusodetoanunbornstareudownloadedition`, `arnosurgeplusodetoanunbornstarnadownloadedition`, `arnosurgeplusodetoanunbornstarnalimitedpackageedition`
- v15062 PCSB00798: `Ar nosurge Plus: Ode to an Unborn Star` vs `arnosurgeodetoanunbornstar`, `arnosurgepluscielnosurgeofflinesurgeconsertoagenttwinpack`, `arnosurgeplusodetoanunbornstaraudownloadedition`, `arnosurgeplusodetoanunbornstareudownloadedition`, `arnosurgeplusodetoanunbornstarnadownloadedition`, `arnosurgeplusodetoanunbornstarnalimitedpackageedition`
- v16295 PCSG00640: `SA7 - Silent Ability Seven` vs `sa7`, `sa7downloadedition`, `sa7limitededition`, `sa7regularedition`, `sa7ダウンロード版`, `sa7通常版`
- v12260 PCSG00540: `ChuSingura46+1 -忠臣蔵46+1- V` vs `chushingura461忠臣蔵461vダウンロード版`, `chushingura461忠臣蔵461vパッケージ版`, `chusingura461`, `chusingura461vdownloadedition`, `chusingura461vpackageedition`, `chuushingura461`
- v4540 PCSG00604: `Beast Tamer and Prince ～Flower ＆ Snow～` vs `beastmasterandprince`, `beastmasterandprinces`, `moujuutsukaitooujisama`, `moujuutsukaitooujisamaflowersnowdownloadedition`, `moujuutsukaitooujisamaflowersnowpackageedition`, `猛獣使いと王子様`
- v4540 PCSG00244: `Beast Tamer and Prince` vs `beastmasterandprince`, `beastmasterandprinces`, `moujuutsukaitooujisama`, `moujuutsukaitooujisamaflowersnowdownloadedition`, `moujuutsukaitooujisamaflowersnowpackageedition`, `猛獣使いと王子様`
- v7815 PCSG00604: `Beast Tamer and Prince ～Flower ＆ Snow～` vs `beastmasterandprincessnowbride`, `moujuutsukaitooujisamaflowersnowdownloadedition`, `moujuutsukaitooujisamaflowersnowpackageedition`, `moujuutsukaitooujisamasnowbride`, `猛獣使いと王子様flowersnowダウンロード版`, `猛獣使いと王子様flowersnowパッケージ版`
- v12282 PCSG00618: `Romeo VS Juliet Zenkan Pack` vs `romeovsjuliet`, `romeovsjulietallseriespackdeluxeedition`, `romeovsjulietallseriespackdownloadedition`, `romeovsjulietallseriespackregularedition`, `ロミオvsジュリエット`, `ロミオvsジュリエット全巻パックダウンロード版`
- v13911 PCSG00618: `Romeo VS Juliet Zenkan Pack` vs `romeojuliet`, `romeovsjulietallseriespackdeluxeedition`, `romeovsjulietallseriespackdownloadedition`, `romeovsjulietallseriespackregularedition`, `ロミオvsジュリエット全巻パックダウンロード版`, `ロミオvsジュリエット全巻パック豪華版`
- v17287 PCSG00713: `Hyakka Hyakurou ~Sengoku Ninpoucho~` vs `baihuabailangsengokurenfatie`, `hyakkahyakurousengokuninpouchou`, `hyakkahyakurousengokuninpouchoudownloadedition`, `hyakkahyakurousengokuninpouchoupackageedition`, `nightshade`, `百花百狼战国忍法帖`
- v17345 PCSG00826: `diabolik lovers[] can display start sceen image but crashes while click the start button` vs `diabolikloverslunaticparade`, `diabolikloverslunaticparadedl版`, `diabolikloverslunaticparadedownloadedition`, `diabolikloverslunaticparadelimitededition`, `diabolikloverslunaticparaderegularedition`, `diabolikloverslunaticparade通常版`
- v17608 PCSG00667: `LOVE:QUIZ - Koisuru Shoujo no Final Answer` vs `lovequizkoisuruotomenofinalanswer`, `lovequizkoisuruotomenofinalanswerdeluxeedition`, `lovequizkoisuruotomenofinalanswerdownloadedition`, `lovequizkoisuruotomenofinalanswerregularedition`, `lovequiz恋する乙女のファイナルアンサー`, `lovequiz恋する乙女のファイナルアンサーdl版`
- v10289 PCSG00635: `Jyuzaengi: Engetsu Sangokuden 1+2` vs `juuzaengiengetsusangokuden`, `juuzaengiengetsusangokuden12downloadedition`, `juuzaengiengetsusangokuden12packageedition`, `shisanzhiyanyiyanyuesanguozhuan`, `十三支演义偃月三国传`, `十三支演義偃月三国伝`
- v12714 PCSG00635: `Jyuzaengi: Engetsu Sangokuden 1+2` vs `juuzaengiengetsusangokuden12downloadedition`, `juuzaengiengetsusangokuden12packageedition`, `juuzaengiengetsusangokuden2`, `jyuzaengiengetsusangokuden2`, `shisanzhiyanyiyanyuesanguozhuan2`, `十三支演義偃月三国伝12dl版`
- v17640 PCSG00853: `Period Cube ~Shackle of Amadeus~` vs `periodcubeshacklesofamadeus`, `periodcubeshacklesofamadeusdownloadedition`, `periodcubeshacklesofamadeuspackageedition`, `periodcubetorikagonoamadeus`, `periodcubetorikagonoamadeusdownloadedition`, `periodcubetorikagonoamadeuslimitededition`
- v17750 PCSG00829: `Kenka Bancho Otome` vs `kbo`, `kenkabanchouotome`, `kenkabanchouotomedownloadedition`, `kenkabanchouotomeregularedition`, `xuanhuafanzhangyinu`, `喧嘩番長乙女`
- v17750 PCSG00829: `Kenka Bancho Otome` vs `kbo`, `kenkabanchouotome`, `kenkabanchouotomedownloadedition`, `kenkabanchouotomeregularedition`, `xuanhuafanzhangyinu`, `喧嘩番長乙女`
- v18159 PCSG00787: `Snow White in the Mirror Realm` vs `kyoukainoshirayuki`, `kyoukainoshirayukidownloadedition`, `kyoukainoshirayukilimitededition`, `kyoukainoshirayukiregularedition`, `namlichshirayukisnowwhiteinthemirrorrealm`, `鏡界の白雪`
- v18160 PCSE01011: `Collar x Malice [] gameplay issue` vs `collarmalicedl版`, `collarmaliceツインパック`, `collarmalice通常版`, `collarmalice限定版`, `collarxmalice`, `collarxmalicedownloadedition`
- v18160 PCSE01011: `Collar x Malice - USA - Game ID` vs `collarmalicedl版`, `collarmaliceツインパック`, `collarmalice通常版`, `collarmalice限定版`, `collarxmalice`, `collarxmalicedownloadedition`
- v18161 PCSG00948: `Suran digit` vs `suurandigit`, `suurandigitdownloadedition`, `suurandigitlimitededition`, `suurandigitregularedition`, `数乱digit`, `数乱digitdl版`
- v18163 PCSG00766: `Nil Admirari's Balance Teito Illusion Kitan` vs `lengranzhitianchengdiduhuanhuoqitan`, `libraofniladmirari`, `niladmirarinotenbinteitogenwakukitan`, `niladmirarinotenbinteitogenwakukitandownloadedition`, `niladmirarinotenbinteitogenwakukitanlimitededition`, `niladmirarinotenbinteitogenwakukitanregularedition`
- v18164 PCSG00708: `Truth Hidden Under The Rose` vs `baranikakusareshiverite`, `baranikakusareshiveritedownloadedition`, `baranikakusareshiveritelimitededition`, `baranikakusareshiveriteregularedition`, `leboucemissairedelareine`, `薔薇に隠されしヴェリテ`
- v18164 PCSG00708: `Truth Hidden Under The Rose` vs `baranikakusareshiverite`, `baranikakusareshiveritedownloadedition`, `baranikakusareshiveritelimitededition`, `baranikakusareshiveriteregularedition`, `leboucemissairedelareine`, `薔薇に隠されしヴェリテ`
- v13833 PCSG00768: `Walpurgis no Uta` vs `shengnvzhishi`, `walpurgisnoutawalpurgisgedichte`, `walpurgisnoutawalpurgisgedichtedownloadedition`, `walpurgisnoutawalpurgisgedichtepackageedition`, `ヴァルプルガの詩`, `ヴァルプルガの詩ダウンロード版`
- v18303 PCSG00833: `NORN9 ACT TUNE` vs `norn9nornnonetteacttune`, `norn9nornnonetteacttunedownloadedition`, `norn9nornnonetteacttunelimitededition`, `norn9nornnonetteacttuneregularedition`, `ノルンノネットアクトチューン`, `ノルンノネットアクトチューンdl版`
- v12438 PCSG00785: `Sangoku Rensenki: Otome no Heihou! Omoide Gaeshi - CS Edition` vs `sangokurensenkiomoidegaeshicseditiondownloadedition`, `sangokurensenkiomoidegaeshicseditionpackageedition`, `sangokurensenkiotomenoheihouomoidegaeshi`, `sanguolianzhanjishaonudebingfazhuiyihuixiang`, `三国恋战记少女的兵法追忆回想`, `三国恋戦記オトメの兵法思いでがえし`
- v18642 PCSG00152: `Tsukiei Academy -kou` vs `getsueigakuenkou`, `getsueigakuenkoulimitedbox`, `月英学園kou`, `月英学園koulimitedbox`
- v18644 PCSG01238: `Root Letter Last Answer` vs `letter`, `letterfanggenshujian`, `letterlastanswerdownloadedition`, `letterlastanswerregularedition`, `letterrootletter`, `letterrootletterdownloadedition`
- v10051 PCSG00850: `Chou Ezaru wa Akai Hana: Koi wa Tsuki ni Shirube Kareru` vs `benibana`, `bukeyuyuedehonghua`, `koezaruwaakaihana`, `koezaruwaakaihanakoiwatsukinimichibikareru`, `koezaruwaakaihanakoiwatsukinimichibikarerudownloadedition`, `koezaruwaakaihanakoiwatsukinimichibikarerutrialedition`
- v18838 PCSG00852: `Maji-Kyun! Renaissance` vs `magickyunrenaissance`, `magickyunrenaissancedownloadedition`, `magickyunrenaissancefirstpresslimitededitionkyunkyunbox`, `magickyunrenaissanceregularedition`, `マジきゅんっルネッサンス`, `マジきゅんっルネッサンスdl版`
- v19119 PCSB01030: `Fate/Extella: The Umbral Star` vs `fateextella`, `fateextellabestcollection`, `fateextelladl`, `fateextelladownloadedition`, `fateextellaregaliabox`, `fateextellaregularedition`
- v12159 PCSG00896: `Meiji Toukyou Renka: Full Moon` vs `meijitokyorenka`, `meijitokyorenkafullmoondownloadedition`, `meijitokyorenkafullmoonfirstpresslimitedakatsukinorokumeikanbox`, `meijitokyorenkafullmoonregularedition`, `meikoi`, `mingzhidongjinglianyu`
- v19298 PCSG00909: `Yunohana SpRING! ～Cherising Time～` vs `yunohanaspringcherishingtime`, `yunohanaspringcherishingtimedownloadedition`, `yunohanaspringcherishingtimelimitededition`, `yunohanaspringcherishingtimeregularedition`, `ゆのはなspringcherishingtime`, `ゆのはなspringcherishingtimedl版`
- v4542 PCSG00938: `Wand of Fortune R2` vs `wandoffortune2jikuunishizumumokushiroku`, `wandoffortuner2jikuunishizumumokushirokudownloadedition`, `wandoffortuner2jikuunishizumumokushirokulimitededition`, `wandoffortuner2jikuunishizumumokushirokuregularedition`, `wof2`, `xingyunzhizhang2yanmoyushikongzhongdemoshilu`
- v17291 PCSG00930: `Hakuouki Yugiroku The Great Banquet of the Members` vs `hakuoukiyuugiroku`, `hakuoukiyuugirokutaishitachinodaienkaidownloadedition`, `hakuoukiyuugirokutaishitachinodaienkailimitededition`, `hakuoukiyuugirokutaishitachinodaienkairegularedition`, `薄桜鬼遊戯録`, `薄桜鬼遊戯録隊士達の大宴会dl版`
- v19756 PCSG00930: `Hakuouki Yugiroku The Great Banquet of the Members` vs `hakuoukiyuugiroku2`, `hakuoukiyuugirokunimatsuribayashitotaishitachi`, `hakuoukiyuugirokutaishitachinodaienkaidownloadedition`, `hakuoukiyuugirokutaishitachinodaienkailimitededition`, `hakuoukiyuugirokutaishitachinodaienkairegularedition`, `薄桜鬼遊戯録弐祭囃子と隊士達`
- v12928 PCSG00991: `Getsuei no Kusari: Kouran Moratorium` vs `chainsofmoonlightmadnessmoratorium`, `getsueinokusarikyouranmoratorium`, `getsueinokusarikyouranmoratoriumdownloadedition`, `getsueinokusarikyouranmoratoriumfirstpresslimitededition`, `getsueinokusarikyouranmoratoriumregularedition`, `月影の鎖狂爛モラトリアム`
- v18397 PCSE01305: `The House in Fata Morgana` vs `fatamorgananoyakataanotherepisodes`, `fatamorgananoyakatacollectededition`, `fatamorgananoyakatagaiden`, `fatamorgananoyakataremaster`, `haishishenlouzhiguanchunzhenwange`, `thehouseinfatamorganaanotherepisodes`
- v18990 PCSE01305: `The House in Fata Morgana` vs `fatamorgananoyakatacollectededition`, `fatamorganashortstories`, `jibuhuibeishushuoyibuhuibeizhumuciweizhujianhuimiedegushi`, `tadahoro`, `talesaffordednottheirmomentinthelimelightlefttowasteawayinobscurity`, `thehouseinfatamorganadreamsoftherevenantscollectorsedition`
- v28264 PCSE01305: `The House in Fata Morgana` vs `fatamorgananoyakatacollectededition`, `fatamorgananoyakatagendaihen`, `haishishenlouzhiguanlunhuizhuanshi`, `thehouseinfatamorganadreamsoftherevenantscollectorsedition`, `thehouseinfatamorganadreamsoftherevenantsedition`, `thehouseinfatamorganadreamsoftherevenantsnadownloadedition`
- v20226 PCSG01042: `Kenka Bancho Otome : Kanzenmuketsu no My Honey` vs `kbomyperfecthoney`, `kenkabanchouotomekanzenmuketsunomyhoney`, `kenkabanchouotomekanzenmuketsunomyhoneydownloadedition`, `kenkabanchouotomekanzenmuketsunomyhoneypackageedition`, `xuanhuafanzhangyinuwodewanmeitianxin`, `喧嘩番長乙女完全無欠のマイハニー`
- v20249 PCSG01070: `Song of Heiligenstadt` vs `heiligenstadlerlied`, `heiligenstadtnouta`, `heiligenstadtnoutadownloadedition`, `heiligenstadtnoutalimitededition`, `heiligenstadtnoutaregularedition`, `ハイリゲンシュタットの歌`
- v151 PCSG00959: `DESIRE remaster ver.` vs `desire`, `desirehaitokunorasen`, `desireremasterversiondownloadedition`, `desireremasterversionfirstpresslimitededition`, `desireremasterversionregularedition`, `desire背徳の螺旋`
- v20326 PCSG01011: `空蝉之廻` vs `utsuseminomeguri`, `utsuseminomeguridownloadedition`, `utsuseminomeguripackageedition`, `空蝉の廻`, `空蝉の廻ダウンロード版`, `空蝉の廻パッケージ版`
- v21112 PCSG01096: `Beast and Princess ～in blossom～` vs `moujuutachitoohimesamainblossom`, `moujuutachitoohimesamainblossomdownloadedition`, `moujuutachitoohimesamainblossomlimitededition`, `moujuutachitoohimesamainblossomregularedition`, `猛獣たちとお姫様inblossom`, `猛獣たちとお姫様inblossomdl版`
- v1629 PCSG01036: `Scarlet Fragments ~Omoiiro no Memories~` vs `feisedesuipian`, `hiironokakera`, `hiironokakeraomoiironokioku`, `hiironokakeraomoiironokiokudownloadedition`, `hiironokakeraomoiironokiokulimitededition`, `scarletfragment`
- v1713 PCSG01036: `Scarlet Fragments ~Omoiiro no Memories~` vs `feisedesuipianzainapiantiankongxia`, `hiironokakeraanosoranoshitade`, `hiironokakeraomoiironokioku`, `hiironokakeraomoiironokiokudownloadedition`, `hiironokakeraomoiironokiokulimitededition`, `緋色の欠片あの空の下で`
- v21782 PCSG01139: `Evening Bell of Piofiore` vs `piofiorefatedmemories`, `piofiorenobanshou`, `piofiorenobanshoudownloadedition`, `piofiorenobanshoulimitededition`, `piofiorenobanshouregularedition`, `qianchengzhihuadewanzhong`

## Vita games with no title ID (most characters first)

- v13636 Sengoku Hime 5 ~Senka Tatsu Haou no Keifu~ (91 characters): `sengokuhime5senkatatsuhaounokeifu`, `戦極姫5戦渦断つ覇王の系譜`, `戦極姫5戦禍断つ覇王の系譜`, `戦極姫5戦禍断つ覇王の系譜豪華`
- v23492 Moe Moe Niji Taisen (Ryaku) 3 (63 characters): `mengmeng2cidazhanlue3`, `moemoenijitaisenryaku3`, `moemoeworldwarii3`, `moeniji3`, `萌え萌え2次大戦略3`
- v5922 Kara no Shoujo - The Second Episode (48 characters): `karanoshojothesecondepisode`, `karanoshoujo2`, `karanoshoujothesecondepisode`, `kns2`, `uronoshoujo`
- v2153 Umineko no Naku Koro ni Chiru (43 characters): `haimaomingqizhishisan`, `kogdaplachutchajkikrah`, `uminekononakukoronichiru`, `uminekononakukoronipsvitaport`, `uminekowhentheycryanswerarcs`
- v5919 Moe Moe Daisensou☆Gendaibaan (43 characters): `moemoedaisensougendaibaan`, `moemoedaisensougendaiban`, `萌え萌え大戦争げんだいばん`, `萌え萌え大戦争げんだいばーん`, `萌え萌え大戦争げんだいばーんプレミアムエディション版`
- v31157 Higurashi no Naku Koro ni: Console Arcs (37 characters): `higurashinonakukoroniconsolearcs`, `higurashinonakukoronisui`, `higurashiproject`, `higurashiwhentheycryconsolearcs`, `ひぐらしのなく頃にconsolearcs`
- v1141 Ore-tachi ni Tsubasa wa Nai (36 characters): `oretachinitsubasawanai`, `oretsuba`, `wedonthavewings`, `wewithoutwings`, `womenmeiyouchibang`
- v810 Kara no Shoujo (30 characters): `girlintheshell`, `karanoshojo`, `karanoshoujo`, `karanoshoujothefirstepisode`, `kezhishaonu`
- v7724 Grisaia no Rakuen -LE EDEN DE LA GRISAIA- (30 characters): `grisaianorakuenleedendelagrisaia`, `huisedeleyuan`, `ledendelagrisaia`, `theedenofgrisaia`, `グリザイアの楽園leedendelagrisaia`
- v19848 Nil Admirari no Tenbin: Kuroyuri En'youtan (29 characters): `niladmirarinotenbin2`, `niladmirarinotenbinkuroyurienyoutan`, `niladmirarinotenbintwinpack`, `ニルアドミラリの天秤クロユリ炎陽譚`, `ニルアドミラリの天秤ツインパック`
- v7602 Fate/EXTRA (28 characters): `fateextra`, `fateextrapsndownload`, `フェイトエクストラ`
- v842 Ore-tachi ni Tsubasa wa Nai ~Prelude~ (27 characters): `oretachinitsubasawanai`, `oretachinitsubasawanaiprelude`, `oretsuba`, `俺たちに翼はない`, `俺たちに翼はないprelude`
- v20431 Sakura no Toki -Sakura no Mori no Shita o Ayumu- (27 characters): `sakuranotokisakuranomorinoshitaoayumu`, `sakutoki`, `yingzhikemanbuyuyinghuazhisenxia`, `サクラノ刻櫻の森の下を歩む`, `樱之刻漫步于樱花之森下`
- v19100 Cross Ange - Tenshi to Ryuu no Rondo tr. (24 characters): `crossangerondoofangelsanddragons`, `crossangetenshitoryuunorondotr`, `クロスアンジュ天使と竜の輪舞tr`
- v68 Higurashi no Naku Koro ni Kai (22 characters): `hanchanmingqizhishijie`, `higu2`, `higurashinonakukoronikai`, `higurashinonakukoronisui`, `higurashiproject`
- v16212 Tokeijikake no Ley Line -Asagiri ni Chiru Hana- (22 characters): `aclockworkleylineflowersfallinginthemorningmist`, `finalepisodeofleyline`, `shizhongjiguandeleylinezhaowuzhongpiaolingzhihua`, `tokeijikakenoleyline3`, `tokeijikakenoleylineasagirinichiruhana`
- v29345 Class of '09 (22 characters): `classof09`, `itsnotadatingsimitsarejectionsim`, `theantivisualnovel`
- v20903 Hatsukoi Valentine (21 characters): `hatsukoivalentine`, `初恋ばれんたいん`
- v20951 Hatsukoi Valentine SPECIAL (21 characters): `hatsukoivalentinespecial`, `初恋ばれんたいんspecial`
- v12849 Ao no Kanata no Four Rhythm (20 characters): `4rhythm`, `aokana`, `aokanafourrhythmsacrosstheblue`, `aonokanatanofourrhythm`, `beyondtheskyintothefirmament`
- v20616 Gensou no Artemis (20 characters): `actressschoolmysteryadventure`, `artemisofillusion`, `gensounoartemis`, `幻想のアルテミス`
- v24 Umineko no Naku Koro ni (19 characters): `haimaomingqizhishi`, `kogdaplachutchajki`, `uminekononakukoroni`, `uminekononakukoronipsvitaport`, `uminekowhentheycryquestionarcs`
- v47 Kagetsu Tooya (19 characters): `geyueshiye`, `kagetsutohya`, `kagetsutooya`, `歌月十夜`
- v10028 Irotoridori no Hikari (19 characters): `colorfullight`, `hyeonghyeongsaeksaeguibit`, `irohika`, `irotoridorinohikari`, `irotoridorinosekaiworldsendrebirth`
- v11093 Tokeijikake no Ley Line -Zan'ei no Yoru ga Akeru Toki- (19 characters): `aclockworkleylinedaybreakofremnantsshadow`, `aclockworkleylinedaybreakofremnantsshadows`, `shizhongjiguandeleylinecanyingzhiyejiangmingshi`, `tokeijikakenoleyline2`, `tokeijikakenoleylinekagerounisamayoumajo`
- v14062 Majo Koi Nikki (19 characters): `majokoinikki`, `majokoinikkidragoncaravan`, `majonikki`, `monulianairiji`, `thewitchslovediary`
- v16842 Date A Live: Twin Edition Rio Reincarnation (19 characters): `datealiverioreincarnation`, `datealivetwineditionrioreincarnation`, `randevuczhizhnjureinkarnatsijario`, `yuehuidazuozhanlinxulunhui`, `yuehuidazuozhantwineditionriolunhui`
- v18157 Echo (19 characters): `echo`
- v25725 SHUFFLE! Episode 2 ~Kami ni mo Akuma ni mo Nerawareteiru Otoko~ (19 characters): `shuffleepisode2beishenyumotongshidingshangdenanren`, `shuffleepisode2kaminimoakumanimonerawareteiruotoko`, `shuffleepisode2被神与魔同时盯上的男人`, `shuffleepisode2被神與魔同時盯上的男人`, `shuffleエピソード2神にも悪魔にも狙われている男`
- v18777 Ikemen Bakumatsu ◆ Unmei no Koi (18 characters): `destinedtoloveikemensamurairomances`, `dtl`, `ikemenbakumatsuunmeinokoi`, `ikemenbakumatsuunmeinokoihananomiyakotokoinoran`, `イケメン幕末運命の恋`
- v47507 Favorite Dear (18 characters): `favoritedear`, `favoritedearenkannomonogatari`, `フェィバリットディア円環の物語`, `フェイバリットディア`
- v5390 Tokimeki Memorial 2 (17 characters): `tokimekimemorial2`, `tokimemo2`, `ときめきメモリアル2`, `ときメモ2`
- v10588 Roommates (17 characters): `roommates`
- v12480 Daitoshokan no Hitsujikai -Dreaming Sheep- (17 characters): `agoodlibrarianlikeagoodshepherdfandiscafterandanotherstory`, `daitoshokannohitsujikaidreamingsheep`, `daitoshokannohitsujikailibraryparty`, `datushuguandemuyangrendreamingsheep`, `大図書館の羊飼いdreamingsheep`
- v14706 Date A Live: Arusu Install (17 characters): `datealivearsinstall`, `datealivearusuinstall`, `datealiveii`, `datealivetwineditionrioreincarnation`, `yuehuidazuozhan`
- v17731 Yahari Game demo Ore no Seishun Love Come wa Machigatteiru. Zoku (17 characters): `guoranyouxiliwodeqingchunlianaiwuyuyeyouwentixu`, `guoranyouxizhongwodeqingchunlianaiwuyuyeyouwentixu`, `oregairu2`, `yaharigamedemoorenoseishunlovecomewamachigatteiruzoku`, `やはりゲームでも俺の青春ラブコメはまちがっている続`
- v31383 Circadia (17 characters): `circadia`, `サーカディア`
- v19 Tokimeki Memorial (16 characters): `chunaishouzha`, `heartthrobmemorial`, `tokimekimemorial`, `tokimekimemorialforeverwithyou`, `tokimemo`
- v1185 Stellar ☆ Theater (16 characters): `stellartheater`, `stellartheaterportable`, `ステラシアター`, `ステラシアターポータブル`
- v1377 Kono Yo no Hate de Koi o Utau Shoujo YU-NO (16 characters): `isesangkkeuteseosarangeulnoraehaneunsonyeoyuno`, `koihate`, `konoyonohatedekoioutaushoujoyuno`, `yuno`, `yunoagirlthatchantsloveattheboundofthisworldpc98dlc`
- v1940 Beniiro Tenjou Ayakashi Kitan (16 characters): `beniirotenjouayakashikitan`, `beniirotenjouayakashikitanfutaai`, `beniten`, `紅天`, `紅色天井艶妖綺譚`
- v10979 Kono Oozora ni, Tsubasa o Hirogete: FLIGHT DIARY (16 characters): `ifmyhearthadwingsflightdiary`, `imhfd`, `konooozoranitsubasaohirogetecruisesign`, `konooozoranitsubasaohirogeteflightdiary`, `konosorafd`
- v945 Katawa Shoujo (15 characters): `disabilitygirls`, `jangaesonyeo`, `katawashoujo`, `katawashoujor7`, `khimkhuytthiun`
- v1949 Memories Off 6: Next Relation (15 characters): `memoriesoff6completedownloadeditionpsvitaedition`, `memoriesoff6completepsvitaedition`, `memoriesoff6nextrelation`, `mo6nr`, `twavesecondchapter`
- v8158 Daitoshokan no Hitsujikai (15 characters): `agoodlibrarianlikeagoodshepherd`, `daitoshokannohitsujikai`, `daitoshokannohitsujikailibraryparty`, `datushuguandemuyangren`, `大図書館の羊飼い`
- v12630 Yahari Game demo Ore no Seishun Love Come wa Machigatteiru. (15 characters): `guoranyouxiliwodeqingchunlianaiwuyuyeyouwenti`, `guoranyouxizhongwodeqingchunlianaiwuyuyeyouwenti`, `hamachi`, `myyouthromanticcomedyingameiswrongasiexpected`, `oregairu`
- v22791 Grisaia: Phantom Trigger Vol. 3 (15 characters): `grisaiaphantomtrigger0304`, `grisaiaphantomtriggervol3`, `huisehuanyingbanjidi3juan`, `pt3`, `グリザイアファントムトリガー0304`
- v28806 Tsui no Sora Remake (15 characters): `endskyremake`, `tnsr`, `tsuinosoraremake`, `tsuire`, `zhongzhikongremake`
- v776 Rui wa Tomo o Yobu (14 characters): `ruicallstomo`, `ruitomo`, `ruiwatomooyobu`, `zhiyileiju`, `るいは智を呼ぶ`
- v1646 Memories Off 6 ~T-Wave~ (14 characters): `memoff6`, `memooff6`, `memoriesoff6completedownloadeditionpsvitaedition`, `memoriesoff6completepsvitaedition`, `memoriesoff6twave`
- v10016 Tokeijikake no Ley Line -Tasogaredoki no Kyoukaisen- (14 characters): `aclockworkleyline`, `aclockworkleylinetheborderlineofdusk`, `shizhongjiguandeleylinehuanghunshidejingjiexian`, `tokeijikakenoleylinekagerounisamayoumajo`, `tokeijikakenoleylinekagerounisamayoumajotrialedition`
- v11038 Dream Club Zero (14 characters): `dreamcclubzero`, `dreamclubzero`, `dreamclubzeroportable`, `ドリームクラブzero`, `ドリームクラブzeroportable`
- v16497 Élan (14 characters): `elan`, `elanpluspsnedition`, `elanpsnedition`, `エラン`, `エランプラス`
- v22790 Grisaia: Phantom Trigger Vol. 2 (14 characters): `grisaiaphantomtrigger0102`, `grisaiaphantomtriggervol2`, `huisehuanyingbanjidi2juan`, `huisehuanyingbanjivol2`, `pt2`
- v22792 Grisaia: Phantom Trigger Vol. 4 (14 characters): `grisaiaphantomtrigger0304`, `grisaiaphantomtriggervol4`, `huisehuanyingbanjidi4juan`, `pt4`, `グリザイアファントムトリガー0304`
- v33 Kanon (13 characters): `kanon`
- v67 Higurashi no Naku Koro ni (13 characters): `gdyzapłaczacykady`, `hanchanmingqizhishichutipian`, `higurashinonakukoroni`, `higurashinonakukoronisui`, `higurashiproject`
- v3246 Tsui no Sora (13 characters): `endsky`, `tns`, `tsuinosora`, `tsuinosorarenpyport`, `zhongzhikong`
- v3941 Rui wa Tomo o Yobu Fan Disc -Asu no Mukou ni Mieru Kaze- (13 characters): `ruiwatomooyobu`, `ruiwatomooyobufandiscasunomukounimierukaze`, `zhiyileijufdchuixiangmingribiandekeshizhifeng`, `るいは智を呼ぶ`, `るいは智を呼ぶfd`
- v8202 Memories Off: Yubikiri no Kioku - Futari no Fuuryuuan (13 characters): `memoriesoffyubikirinokiokufutarinofuuryuuan`, `memoriesoffyubikirinokiokufutarinofuuryuuanplus`, `memoriesoffyubikirinokiokupsvitaedition`, `ゆびきりの記憶ふたりの風流庵ぷらす`, `メモリーズオフゆびきりの記憶psvita版`

## Conflicts

