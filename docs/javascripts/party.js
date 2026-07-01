const BOX_KEY = 'rp_nuzlocke_box';

const POKEMON = {
  "Bulbasaur":"001","Ivysaur":"002","Venusaur":"003","Charmander":"004","Charmeleon":"005",
  "Charizard":"006","Squirtle":"007","Wartortle":"008","Blastoise":"009","Caterpie":"010",
  "Metapod":"011","Butterfree":"012","Weedle":"013","Kakuna":"014","Beedrill":"015",
  "Pidgey":"016","Pidgeotto":"017","Pidgeot":"018","Rattata":"019","Raticate":"020",
  "Spearow":"021","Fearow":"022","Ekans":"023","Arbok":"024","Pikachu":"025",
  "Raichu":"026","Sandshrew":"027","Sandslash":"028","Nidoran♀":"029","Nidorina":"030",
  "Nidoqueen":"031","Nidoran♂":"032","Nidorino":"033","Nidoking":"034","Clefairy":"035",
  "Clefable":"036","Vulpix":"037","Ninetales":"038","Jigglypuff":"039","Wigglytuff":"040",
  "Zubat":"041","Golbat":"042","Oddish":"043","Gloom":"044","Vileplume":"045",
  "Paras":"046","Parasect":"047","Venonat":"048","Venomoth":"049","Diglett":"050",
  "Dugtrio":"051","Meowth":"052","Persian":"053","Psyduck":"054","Golduck":"055",
  "Mankey":"056","Primeape":"057","Growlithe":"058","Arcanine":"059","Poliwag":"060",
  "Poliwhirl":"061","Poliwrath":"062","Abra":"063","Kadabra":"064","Alakazam":"065",
  "Machop":"066","Machoke":"067","Machamp":"068","Bellsprout":"069","Weepinbell":"070",
  "Victreebel":"071","Tentacool":"072","Tentacruel":"073","Geodude":"074","Graveler":"075",
  "Golem":"076","Ponyta":"077","Rapidash":"078","Slowpoke":"079","Slowbro":"080",
  "Magnemite":"081","Magneton":"082","Farfetch'd":"083","Doduo":"084","Dodrio":"085",
  "Seel":"086","Dewgong":"087","Grimer":"088","Muk":"089","Shellder":"090",
  "Cloyster":"091","Gastly":"092","Haunter":"093","Gengar":"094","Onix":"095",
  "Drowzee":"096","Hypno":"097","Krabby":"098","Kingler":"099","Voltorb":"100",
  "Electrode":"101","Exeggcute":"102","Exeggutor":"103","Cubone":"104","Marowak":"105",
  "Hitmonlee":"106","Hitmonchan":"107","Lickitung":"108","Koffing":"109","Weezing":"110",
  "Rhyhorn":"111","Rhydon":"112","Chansey":"113","Tangela":"114","Kangaskhan":"115",
  "Horsea":"116","Seadra":"117","Goldeen":"118","Seaking":"119","Staryu":"120",
  "Starmie":"121","Mr. Mime":"122","Scyther":"123","Jynx":"124","Electabuzz":"125",
  "Magmar":"126","Pinsir":"127","Tauros":"128","Magikarp":"129","Gyarados":"130",
  "Lapras":"131","Ditto":"132","Eevee":"133","Vaporeon":"134","Jolteon":"135",
  "Flareon":"136","Porygon":"137","Omanyte":"138","Omastar":"139","Kabuto":"140",
  "Kabutops":"141","Aerodactyl":"142","Snorlax":"143","Articuno":"144","Zapdos":"145",
  "Moltres":"146","Dratini":"147","Dragonair":"148","Dragonite":"149","Mewtwo":"150",
  "Mew":"151","Chikorita":"152","Bayleef":"153","Meganium":"154","Cyndaquil":"155",
  "Quilava":"156","Typhlosion":"157","Totodile":"158","Croconaw":"159","Feraligatr":"160",
  "Sentret":"161","Furret":"162","Hoothoot":"163","Noctowl":"164","Ledyba":"165",
  "Ledian":"166","Spinarak":"167","Ariados":"168","Crobat":"169","Chinchou":"170",
  "Lanturn":"171","Pichu":"172","Cleffa":"173","Igglybuff":"174","Togepi":"175",
  "Togetic":"176","Natu":"177","Xatu":"178","Mareep":"179","Flaaffy":"180",
  "Ampharos":"181","Bellossom":"182","Marill":"183","Azumarill":"184","Sudowoodo":"185",
  "Politoed":"186","Hoppip":"187","Skiploom":"188","Jumpluff":"189","Aipom":"190",
  "Sunkern":"191","Sunflora":"192","Yanma":"193","Wooper":"194","Quagsire":"195",
  "Espeon":"196","Umbreon":"197","Murkrow":"198","Slowking":"199","Misdreavus":"200",
  "Unown":"201","Wobbuffet":"202","Girafarig":"203","Pineco":"204","Forretress":"205",
  "Dunsparce":"206","Gligar":"207","Steelix":"208","Snubbull":"209","Granbull":"210",
  "Qwilfish":"211","Scizor":"212","Shuckle":"213","Heracross":"214","Sneasel":"215",
  "Teddiursa":"216","Ursaring":"217","Slugma":"218","Magcargo":"219","Swinub":"220",
  "Piloswine":"221","Corsola":"222","Remoraid":"223","Octillery":"224","Delibird":"225",
  "Mantine":"226","Skarmory":"227","Houndour":"228","Houndoom":"229","Kingdra":"230",
  "Phanpy":"231","Donphan":"232","Porygon2":"233","Stantler":"234","Smeargle":"235",
  "Tyrogue":"236","Hitmontop":"237","Smoochum":"238","Elekid":"239","Magby":"240",
  "Miltank":"241","Blissey":"242","Raikou":"243","Entei":"244","Suicune":"245",
  "Larvitar":"246","Pupitar":"247","Tyranitar":"248","Lugia":"249","Ho-Oh":"250",
  "Celebi":"251","Treecko":"252","Grovyle":"253","Sceptile":"254","Torchic":"255",
  "Combusken":"256","Blaziken":"257","Mudkip":"258","Marshtomp":"259","Swampert":"260",
  "Poochyena":"261","Mightyena":"262","Zigzagoon":"263","Linoone":"264","Wurmple":"265",
  "Silcoon":"266","Beautifly":"267","Cascoon":"268","Dustox":"269","Lotad":"270",
  "Lombre":"271","Ludicolo":"272","Seedot":"273","Nuzleaf":"274","Shiftry":"275",
  "Taillow":"276","Swellow":"277","Wingull":"278","Pelipper":"279","Ralts":"280",
  "Kirlia":"281","Gardevoir":"282","Surskit":"283","Masquerain":"284","Shroomish":"285",
  "Breloom":"286","Slakoth":"287","Vigoroth":"288","Slaking":"289","Nincada":"290",
  "Ninjask":"291","Shedinja":"292","Whismur":"293","Loudred":"294","Exploud":"295",
  "Makuhita":"296","Hariyama":"297","Azurill":"298","Nosepass":"299","Skitty":"300",
  "Delcatty":"301","Sableye":"302","Mawile":"303","Aron":"304","Lairon":"305",
  "Aggron":"306","Meditite":"307","Medicham":"308","Electrike":"309","Manectric":"310",
  "Plusle":"311","Minun":"312","Volbeat":"313","Illumise":"314","Roselia":"315",
  "Gulpin":"316","Swalot":"317","Carvanha":"318","Sharpedo":"319","Wailmer":"320",
  "Wailord":"321","Numel":"322","Camerupt":"323","Torkoal":"324","Spoink":"325",
  "Grumpig":"326","Spinda":"327","Trapinch":"328","Vibrava":"329","Flygon":"330",
  "Cacnea":"331","Cacturne":"332","Swablu":"333","Altaria":"334","Zangoose":"335",
  "Seviper":"336","Lunatone":"337","Solrock":"338","Barboach":"339","Whiscash":"340",
  "Corphish":"341","Crawdaunt":"342","Baltoy":"343","Claydol":"344","Lileep":"345",
  "Cradily":"346","Anorith":"347","Armaldo":"348","Feebas":"349","Milotic":"350",
  "Castform":"351","Kecleon":"352","Shuppet":"353","Banette":"354","Duskull":"355",
  "Dusclops":"356","Tropius":"357","Chimecho":"358","Absol":"359","Wynaut":"360",
  "Snorunt":"361","Glalie":"362","Spheal":"363","Sealeo":"364","Walrein":"365",
  "Clamperl":"366","Huntail":"367","Gorebyss":"368","Relicanth":"369","Luvdisc":"370",
  "Bagon":"371","Shelgon":"372","Salamence":"373","Beldum":"374","Metang":"375",
  "Metagross":"376","Regirock":"377","Regice":"378","Registeel":"379","Latias":"380",
  "Latios":"381","Kyogre":"382","Groudon":"383","Rayquaza":"384","Jirachi":"385",
  "Deoxys":"386","Turtwig":"387","Grotle":"388","Torterra":"389","Chimchar":"390",
  "Monferno":"391","Infernape":"392","Piplup":"393","Prinplup":"394","Empoleon":"395",
  "Starly":"396","Staravia":"397","Staraptor":"398","Bidoof":"399","Bibarel":"400",
  "Kricketot":"401","Kricketune":"402","Shinx":"403","Luxio":"404","Luxray":"405",
  "Budew":"406","Roserade":"407","Cranidos":"408","Rampardos":"409","Shieldon":"410",
  "Bastiodon":"411","Burmy":"412","Wormadam":"413","Mothim":"414","Combee":"415",
  "Vespiquen":"416","Pachirisu":"417","Buizel":"418","Floatzel":"419","Cherubi":"420",
  "Cherrim":"421","Shellos":"422","Gastrodon":"423","Ambipom":"424","Drifloon":"425",
  "Drifblim":"426","Buneary":"427","Lopunny":"428","Mismagius":"429","Honchkrow":"430",
  "Glameow":"431","Purugly":"432","Chingling":"433","Stunky":"434","Skuntank":"435",
  "Bronzor":"436","Bronzong":"437","Bonsly":"438","Mime Jr.":"439","Happiny":"440",
  "Chatot":"441","Spiritomb":"442","Gible":"443","Gabite":"444","Garchomp":"445",
  "Munchlax":"446","Riolu":"447","Lucario":"448","Hippopotas":"449","Hippowdon":"450",
  "Skorupi":"451","Drapion":"452","Croagunk":"453","Toxicroak":"454","Carnivine":"455",
  "Finneon":"456","Lumineon":"457","Mantyke":"458","Snover":"459","Abomasnow":"460",
  "Weavile":"461","Magnezone":"462","Lickilicky":"463","Rhyperior":"464","Tangrowth":"465",
  "Electivire":"466","Magmortar":"467","Togekiss":"468","Yanmega":"469","Leafeon":"470",
  "Glaceon":"471","Gliscor":"472","Mamoswine":"473","Porygon-Z":"474","Gallade":"475",
  "Probopass":"476","Dusknoir":"477","Froslass":"478","Rotom":"479","Uxie":"480",
  "Mesprit":"481","Azelf":"482","Dialga":"483","Palkia":"484","Heatran":"485",
  "Regigigas":"486","Giratina":"487","Cresselia":"488","Phione":"489","Manaphy":"490",
  "Darkrai":"491","Shaymin":"492","Arceus":"493"
};

const STAT_BIAS = {
  "001":"spec","002":"spec","003":"spec","004":"spec","005":"spec","006":"spec","007":"spec",
  "008":"spec","009":"spec","010":"phys","011":"spec","012":"spec","013":"phys","014":"balanced",
  "015":"phys","016":"spec","017":"spec","018":"spec","019":"phys","020":"phys","021":"phys",
  "022":"phys","023":"phys","024":"phys","025":"phys","026":"balanced","027":"phys","028":"phys",
  "029":"phys","030":"phys","031":"phys","032":"phys","033":"phys","034":"phys","035":"spec",
  "036":"spec","037":"spec","038":"spec","039":"balanced","040":"spec","041":"phys","042":"phys",
  "043":"spec","044":"spec","045":"spec","046":"phys","047":"phys","048":"phys","049":"spec",
  "050":"phys","051":"phys","052":"phys","053":"balanced","054":"spec","055":"spec","056":"phys",
  "057":"phys","058":"balanced","059":"phys","060":"phys","061":"phys","062":"phys","063":"spec",
  "064":"spec","065":"spec","066":"phys","067":"phys","068":"phys","069":"phys","070":"phys",
  "071":"phys","072":"spec","073":"spec","074":"phys","075":"phys","076":"phys","077":"phys",
  "078":"phys","079":"phys","080":"spec","081":"spec","082":"spec","083":"phys","084":"phys",
  "085":"phys","086":"balanced","087":"balanced","088":"phys","089":"phys","090":"phys",
  "091":"phys","092":"spec","093":"spec","094":"spec","095":"phys","096":"phys","097":"balanced",
  "098":"phys","099":"phys","100":"spec","101":"spec","102":"spec","103":"spec","104":"phys",
  "105":"phys","106":"phys","107":"phys","108":"spec","109":"phys","110":"phys","111":"phys",
  "112":"phys","113":"spec","114":"spec","115":"phys","116":"spec","117":"spec","118":"phys",
  "119":"phys","120":"spec","121":"spec","122":"spec","123":"phys","124":"spec","125":"spec",
  "126":"spec","127":"phys","128":"phys","129":"spec","130":"phys","131":"balanced","132":"balanced",
  "133":"phys","134":"spec","135":"spec","136":"phys","137":"spec","138":"spec","139":"spec",
  "140":"phys","141":"phys","142":"phys","143":"phys","144":"spec","145":"spec","146":"spec",
  "147":"phys","148":"phys","149":"phys","150":"spec","151":"balanced","152":"balanced","153":"spec",
  "154":"spec","155":"spec","156":"spec","157":"spec","158":"phys","159":"phys","160":"phys",
  "161":"phys","162":"phys","163":"spec","164":"spec","165":"phys","166":"phys","167":"phys",
  "168":"phys","169":"phys","170":"spec","171":"spec","172":"phys","173":"spec","174":"spec",
  "175":"spec","176":"spec","177":"spec","178":"spec","179":"spec","180":"spec","181":"spec",
  "182":"spec","183":"spec","184":"spec","185":"phys","186":"spec","187":"spec","188":"spec",
  "189":"spec","190":"phys","191":"balanced","192":"spec","193":"spec","194":"phys","195":"phys",
  "196":"spec","197":"phys","198":"balanced","199":"spec","200":"spec","201":"balanced",
  "202":"balanced","203":"spec","204":"phys","205":"phys","206":"phys","207":"phys","208":"phys",
  "209":"phys","210":"phys","211":"phys","212":"phys","213":"balanced","214":"phys","215":"phys",
  "216":"phys","217":"phys","218":"spec","219":"spec","220":"phys","221":"phys","222":"spec",
  "223":"balanced","224":"balanced","225":"spec","226":"spec","227":"phys","228":"spec",
  "229":"spec","230":"balanced","231":"phys","232":"phys","233":"spec","234":"phys","235":"balanced",
  "236":"balanced","237":"phys","238":"spec","239":"spec","240":"phys","241":"phys","242":"spec",
  "243":"spec","244":"phys","245":"spec","246":"phys","247":"phys","248":"phys","249":"balanced",
  "250":"phys","251":"balanced","252":"spec","253":"spec","254":"spec","255":"spec","256":"balanced",
  "257":"phys","258":"phys","259":"phys","260":"phys","261":"phys","262":"phys","263":"phys",
  "264":"phys","265":"phys","266":"phys","267":"spec","268":"phys","269":"spec","270":"spec",
  "271":"spec","272":"spec","273":"phys","274":"phys","275":"phys","276":"phys","277":"phys",
  "278":"spec","279":"spec","280":"spec","281":"spec","282":"spec","283":"spec","284":"spec",
  "285":"balanced","286":"phys","287":"phys","288":"phys","289":"phys","290":"phys","291":"phys",
  "292":"phys","293":"balanced","294":"balanced","295":"balanced","296":"phys","297":"phys",
  "298":"spec","299":"spec","300":"phys","301":"phys","302":"balanced","303":"phys","304":"phys",
  "305":"phys","306":"phys","307":"spec","308":"spec","309":"spec","310":"spec","311":"spec",
  "312":"spec","313":"spec","314":"spec","315":"spec","316":"balanced","317":"balanced","318":"phys",
  "319":"phys","320":"balanced","321":"balanced","322":"spec","323":"spec","324":"balanced",
  "325":"spec","326":"spec","327":"balanced","328":"phys","329":"spec","330":"spec","331":"balanced",
  "332":"balanced","333":"balanced","334":"balanced","335":"phys","336":"phys","337":"spec",
  "338":"phys","339":"phys","340":"phys","341":"phys","342":"phys","343":"balanced","344":"balanced",
  "345":"spec","346":"balanced","347":"phys","348":"phys","349":"phys","350":"spec","351":"spec",
  "352":"phys","353":"phys","354":"phys","355":"phys","356":"phys","357":"balanced","358":"spec",
  "359":"phys","360":"balanced","361":"balanced","362":"phys","363":"spec","364":"spec","365":"spec",
  "366":"spec","367":"phys","368":"spec","369":"phys","370":"spec","371":"phys","372":"phys",
  "373":"phys","374":"phys","375":"phys","376":"phys","377":"phys","378":"spec","379":"balanced",
  "380":"spec","381":"spec","382":"spec","383":"phys","384":"balanced","385":"balanced","386":"balanced",
  "387":"phys","388":"phys","389":"phys","390":"balanced","391":"balanced","392":"balanced",
  "393":"spec","394":"spec","395":"spec","396":"phys","397":"phys","398":"phys","399":"phys",
  "400":"phys","401":"balanced","402":"phys","403":"phys","404":"phys","405":"phys","406":"spec",
  "407":"spec","408":"phys","409":"phys","410":"phys","411":"phys","412":"spec","413":"spec",
  "414":"spec","415":"balanced","416":"balanced","417":"spec","418":"phys","419":"phys","420":"spec",
  "421":"spec","422":"spec","423":"spec","424":"phys","425":"spec","426":"spec","427":"phys",
  "428":"phys","429":"spec","430":"phys","431":"phys","432":"phys","433":"spec","434":"phys",
  "435":"phys","436":"balanced","437":"phys","438":"phys","439":"spec","440":"spec","441":"spec",
  "442":"balanced","443":"phys","444":"phys","445":"phys","446":"phys","447":"phys","448":"spec",
  "449":"phys","450":"phys","451":"phys","452":"phys","453":"balanced","454":"phys","455":"phys",
  "456":"spec","457":"spec","458":"spec","459":"balanced","460":"balanced","461":"phys","462":"spec",
  "463":"phys","464":"phys","465":"spec","466":"phys","467":"spec","468":"spec","469":"spec",
  "470":"phys","471":"spec","472":"phys","473":"phys","474":"spec","475":"phys","476":"spec",
  "477":"phys","478":"spec","479":"spec","480":"balanced","481":"balanced","482":"balanced",
  "483":"spec","484":"spec","485":"spec","486":"phys","487":"balanced","488":"spec","489":"balanced",
  "490":"balanced","491":"spec","492":"balanced","493":"balanced"
};

function loadBox() {
  try { return JSON.parse(localStorage.getItem(BOX_KEY)) || []; }
  catch { return []; }
}

function saveBox(box) {
  localStorage.setItem(BOX_KEY, JSON.stringify(box));
  renderBoxPage();
}

const LEVEL_CAPS = [
  { name: 'Roark',              gym: 'Oreburgh Gym',    cap: 16 },
  { name: 'Gardenia',           gym: 'Eterna Gym',      cap: 26 },
  { name: 'Fantina',            gym: 'Hearthome Gym',   cap: 33 },
  { name: 'Maylene',            gym: 'Veilstone Gym',   cap: 39 },
  { name: 'Wake',               gym: 'Pastoria Gym',    cap: 44 },
  { name: 'Byron',              gym: 'Canalave Gym',    cap: 53 },
  { name: 'Candice',            gym: 'Snowpoint Gym',   cap: 56 },
  { name: 'Volkner',            gym: 'Sunyshore Gym',   cap: 62 },
  { name: 'Champion Cynthia',   gym: 'Pokémon League',  cap: 78 },
  { name: 'Champion Cynthia ★', gym: 'Pokémon League',  cap: 89 },
];

const CAP_KEY = 'rp_nuzlocke_cap';

function loadCapIndex() {
  const v = parseInt(localStorage.getItem(CAP_KEY), 10);
  return isNaN(v) ? 0 : Math.min(Math.max(0, v), LEVEL_CAPS.length - 1);
}

function saveCapIndex(i) {
  localStorage.setItem(CAP_KEY, String(i));
  renderBoxPage();
}

function siteRoot() {
  const css = document.querySelector('link[href*="/assets/"]');
  return css ? css.href.replace(/\/assets\/.*$/, '') : window.location.origin;
}

function spriteUrl(id) {
  return siteRoot() + '/img/pokemon/' + String(id).padStart(3, '0') + '.png';
}

// ── My Box page ──

function renderBoxPage() {
  const root = document.getElementById('rp-box-root');
  if (!root) return;

  const box = loadBox();
  const alive = box.filter(p => !p.fainted);
  const fainted = box.filter(p => p.fainted);

  const capIdx = loadCapIndex();
  const cap = LEVEL_CAPS[capIdx];

  root.innerHTML = `
    <div class="rp-page-toolbar">
      <span class="rp-page-count">${alive.length} alive · ${fainted.length} fainted</span>
      <button class="rp-btn-primary rp-page-add-btn" id="rp-page-add">+ Add Pokémon</button>
    </div>
    <div class="rp-cap-bar">
      <button class="rp-cap-nav" id="rp-cap-prev" ${capIdx === 0 ? 'disabled' : ''}>‹</button>
      <div class="rp-cap-info">
        <span class="rp-cap-name">${cap.name} · ${cap.gym}</span>
        <span class="rp-cap-level">Lv. ${cap.cap}</span>
      </div>
      <button class="rp-cap-nav" id="rp-cap-next" ${capIdx === LEVEL_CAPS.length - 1 ? 'disabled' : ''}>›</button>
    </div>
    ${alive.length === 0 && fainted.length === 0
      ? '<p class="rp-empty">No Pokémon yet.</p>'
      : `<div class="rp-box-grid-page">
          ${alive.map(p => slotHTML(p, box.indexOf(p), cap.cap)).join('')}
          ${fainted.length && alive.length ? '<div class="rp-fainted-divider">Fainted</div>' : ''}
          ${fainted.length ? '<div class="rp-clear-box-row"><button class="rp-clear-box-btn" id="rp-page-clear">Clear Box</button></div>' : ''}
          ${fainted.map(p => slotHTML(p, box.indexOf(p), cap.cap)).join('')}
        </div>`
    }
  `;

  root.querySelector('#rp-page-add').addEventListener('click', () => openAddModal(null, null));
  root.querySelector('#rp-page-clear')?.addEventListener('click', clearBox);
  root.querySelector('#rp-cap-prev')?.addEventListener('click', () => saveCapIndex(capIdx - 1));
  root.querySelector('#rp-cap-next')?.addEventListener('click', () => saveCapIndex(capIdx + 1));
  root.querySelectorAll('.rp-slot[data-index]').forEach(slot => {
    slot.addEventListener('click', () => openDetailModal(parseInt(slot.dataset.index, 10)));
  });
  root.querySelectorAll('.rp-lvl-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const index = parseInt(btn.dataset.index, 10);
      const box = loadBox();
      if (!box[index]) return;
      if (btn.dataset.dir === 'inc') {
        box[index].level = Math.min(100, (box[index].level ?? 0) + 1);
      } else if (box[index].level) {
        box[index].level = Math.max(1, box[index].level - 1);
      }
      saveBox(box);
    });
  });
}

function nextLearnedMove(pokemonId, level) {
  const moves = (typeof LEVEL_UP_MOVES !== 'undefined') && LEVEL_UP_MOVES[pokemonId];
  if (!moves || !level) return null;
  const next = moves.find(([ml]) => ml > level);
  return next ? `Lv.${next[0]} ${next[1]}` : null;
}

function slotHTML(pokemon, index, capLevel) {
  const label = pokemon.nickname || pokemon.speciesName;
  const bias = STAT_BIAS[pokemon.id];
  const biasLabel = bias === 'phys' ? 'Atk' : bias === 'spec' ? 'SpAtk' : 'Balanced';
  const next = nextLearnedMove(pokemon.id, pokemon.level);
  const atCap = capLevel && pokemon.level != null && pokemon.level >= capLevel;
  const tooltip = [
    label,
    pokemon.level ? 'Lv.' + pokemon.level : null,
    pokemon.caughtAt || null,
    pokemon.fainted ? '(fainted)' : null,
    pokemon.evolutionDelayed ? (pokemon.evoDelayLevel ? `Evo delayed until Lv.${pokemon.evoDelayLevel}` : 'Evo delayed') : null,
  ].filter(Boolean).join(' · ');

  return `<div class="rp-slot${pokemon.fainted ? ' rp-fainted' : ''}${atCap ? ' rp-at-cap' : ''}" data-index="${index}" title="${tooltip}">
    <img src="${spriteUrl(pokemon.id)}" alt="${pokemon.speciesName}">
    ${pokemon.evolutionDelayed ? `<div class="rp-evo-badge" title="Evolution delayed">${pokemon.evoDelayLevel ? 'E→' + pokemon.evoDelayLevel : 'E'}</div>` : ''}
    <div class="rp-slot-name">${label}</div>
    ${bias ? `<div class="rp-slot-bias rp-slot-bias--${bias}">${biasLabel}</div>` : ''}
    <div class="rp-slot-level">
      <button class="rp-lvl-btn" data-dir="dec" data-index="${index}">−</button>
      <span>${pokemon.level ? 'Lv.' + pokemon.level : '?'}</span>
      <button class="rp-lvl-btn" data-dir="inc" data-index="${index}">+</button>
    </div>
    ${next ? `<div class="rp-slot-next-move" title="Next move to learn">${next}</div>` : ''}
  </div>`;
}

// ── Add modal ──

function pokemonDatalist() {
  return '<datalist id="rp-pokemon-list">' +
    Object.keys(POKEMON).map(n => `<option value="${n}">`).join('') +
    '</datalist>';
}

function openAddModal(id, name) {
  closeModal();
  const box = loadBox();
  const duplicate = id && box.some(p => p.id === id && !p.fainted);

  const modal = document.createElement('div');
  modal.id = 'rp-modal';
  modal.innerHTML = `
    <div class="rp-modal-backdrop"></div>
    <div class="rp-modal-box">
      <h3>Add to My Box</h3>
      ${duplicate ? `<div class="rp-warning">You already have a ${name} in your box.</div>` : ''}
      ${id
        ? `<div class="rp-modal-species">
             <img src="${spriteUrl(id)}" alt="${name}">
             <span>${name}</span>
           </div>`
        : `<div class="rp-form-row">
             <label>Pokémon name</label>
             <input id="rp-in-species" type="text" list="rp-pokemon-list" placeholder="e.g. Charizard" autocomplete="off">
             ${pokemonDatalist()}
           </div>
           <div id="rp-preview" class="rp-modal-species" style="display:none">
             <img id="rp-preview-img" src="" alt="">
             <span id="rp-preview-name"></span>
           </div>`
      }
      <div class="rp-form-row">
        <label>Nickname <small>(optional)</small></label>
        <input id="rp-in-nickname" type="text" placeholder="">
      </div>
      <div class="rp-form-row">
        <label>Level <small>(optional)</small></label>
        <input id="rp-in-level" type="number" min="1" max="100" placeholder="">
      </div>
      <div class="rp-form-row">
        <label>Caught at <small>(optional)</small></label>
        <input id="rp-in-location" type="text" placeholder="Route 210">
      </div>
      <div class="rp-modal-actions">
        <button class="rp-btn-primary" id="rp-btn-confirm" data-id="${id || ''}" data-name="${name || ''}">Add</button>
        <button class="rp-btn-secondary" id="rp-btn-cancel">Cancel</button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.querySelector('.rp-modal-backdrop').addEventListener('click', closeModal);
  modal.querySelector('#rp-btn-cancel').addEventListener('click', closeModal);
  modal.querySelector('#rp-btn-confirm').addEventListener('click', confirmAdd);

  const speciesInput = modal.querySelector('#rp-in-species');
  if (speciesInput) {
    speciesInput.focus();
    speciesInput.addEventListener('input', () => {
      const val = speciesInput.value.trim();
      const lookupId = POKEMON[val];
      const preview = modal.querySelector('#rp-preview');
      if (lookupId) {
        preview.style.display = 'flex';
        modal.querySelector('#rp-preview-img').src = spriteUrl(lookupId);
        modal.querySelector('#rp-preview-img').alt = val;
        modal.querySelector('#rp-preview-name').textContent = val;
      } else {
        preview.style.display = 'none';
      }
    });
  } else {
    modal.querySelector('input')?.focus();
  }
}

function confirmAdd(e) {
  let id = e.currentTarget.dataset.id;
  let name = e.currentTarget.dataset.name;

  if (!id) {
    name = document.getElementById('rp-in-species')?.value.trim() || '';
    id = POKEMON[name];
    if (!name || !id) return;
  }

  const nickname = document.getElementById('rp-in-nickname')?.value.trim() || null;
  const levelStr = document.getElementById('rp-in-level')?.value;
  const level = levelStr ? parseInt(levelStr, 10) : null;
  const caughtAt = document.getElementById('rp-in-location')?.value.trim() || null;

  const box = loadBox();
  box.push({ id, speciesName: name, nickname, level, caughtAt, fainted: false, evolutionDelayed: false });
  saveBox(box);
  closeModal();
}

// ── Detail modal ──

function openDetailModal(index) {
  closeModal();
  const box = loadBox();
  const p = box[index];
  if (!p) return;

  const next = nextLearnedMove(p.id, p.level);

  const modal = document.createElement('div');
  modal.id = 'rp-modal';
  modal.innerHTML = `
    <div class="rp-modal-backdrop"></div>
    <div class="rp-modal-box rp-modal-box--detail">
      <button class="rp-modal-close" data-action="close" aria-label="Close">✕</button>
      <div class="rp-detail-header${p.fainted ? ' rp-detail-header--fainted' : ''}">
        <img src="${spriteUrl(p.id)}" alt="${p.speciesName}" class="rp-detail-sprite${p.fainted ? ' rp-detail-sprite--fainted' : ''}">
        <div class="rp-detail-header-text">
          <div class="rp-detail-name">${p.nickname || p.speciesName}</div>
          ${p.nickname ? `<div class="rp-detail-species">${p.speciesName}</div>` : ''}
        </div>
      </div>
      <div class="rp-modal-body">
        <div class="rp-detail-meta">
          ${(p.level || p.caughtAt) ? `<div class="rp-detail-meta-row">
            ${p.level ? `<span class="rp-detail-meta-pill">Lv. ${p.level}</span>` : ''}
            ${p.caughtAt ? `<span class="rp-detail-meta-pill">${p.caughtAt}</span>` : ''}
          </div>` : ''}
          ${next ? `<div class="rp-detail-next-move">Next: ${next}</div>` : ''}
          ${p.fainted ? `<div class="rp-detail-status rp-detail-status--fainted">This Pokémon has fainted</div>` : ''}
          ${p.evolutionDelayed ? `<div class="rp-detail-status rp-detail-status--evo">Evolution delayed${p.evoDelayLevel ? ' until Lv. ' + p.evoDelayLevel : ''}</div>` : ''}
        </div>
        ${!p.evolutionDelayed ? `
        <div class="rp-form-row">
          <label>Delay evolution until level <small>(optional)</small></label>
          <input id="rp-evo-level" type="number" min="1" max="100" placeholder="">
        </div>` : ''}
        <div class="rp-detail-actions">
          <button class="rp-detail-btn rp-detail-btn--primary" data-action="info" data-index="${index}">View Pokémon page</button>
          <div class="rp-detail-btn-pair">
            ${!p.fainted
              ? `<button class="rp-detail-btn rp-detail-btn--secondary" data-action="faint" data-index="${index}">Mark fainted</button>`
              : `<button class="rp-detail-btn rp-detail-btn--secondary" data-action="revive" data-index="${index}">Restore to box</button>`
            }
            <button class="rp-detail-btn rp-detail-btn--secondary" data-action="evo-delay" data-index="${index}">${p.evolutionDelayed ? 'Clear evo delay' : 'Delay evolution'}</button>
          </div>
          <button class="rp-detail-btn rp-detail-btn--remove" data-action="remove" data-index="${index}">Remove from box</button>
        </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.querySelector('.rp-modal-backdrop').addEventListener('click', closeModal);
  modal.addEventListener('click', onDetailAction);
}

function onDetailAction(e) {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  const index = parseInt(btn.dataset.index, 10);
  const box = loadBox();

  switch (btn.dataset.action) {
    case 'info':
      if (box[index]) window.location.href = siteRoot() + '/pokemons/' + box[index].id + '/';
      break;
    case 'faint':
      if (box[index]) { box[index].fainted = true; saveBox(box); }
      closeModal();
      break;
    case 'revive':
      if (box[index]) { box[index].fainted = false; saveBox(box); }
      closeModal();
      break;
    case 'remove':
      box.splice(index, 1);
      saveBox(box);
      closeModal();
      break;
    case 'evo-delay':
      if (box[index]) {
        if (box[index].evolutionDelayed) {
          box[index].evolutionDelayed = false;
          box[index].evoDelayLevel = null;
        } else {
          const levelInput = document.getElementById('rp-evo-level');
          const level = levelInput?.value ? parseInt(levelInput.value, 10) : null;
          box[index].evolutionDelayed = true;
          box[index].evoDelayLevel = level;
        }
        saveBox(box);
      }
      closeModal();
      break;
    case 'close':
      closeModal();
      break;
  }
}

function clearBox() {
  if (!confirm('Remove all Pokémon from your box? This cannot be undone.')) return;
  saveBox([]);
}

function closeModal() {
  document.getElementById('rp-modal')?.remove();
}

// ── Add to Box button on Pokémon pages ──

function injectAddButton() {
  const match = window.location.pathname.match(/\/pokemons\/(\d{3})\//);
  if (!match) return;

  const id = match[1];
  const h1 = document.querySelector('.md-content h1');
  if (!h1 || document.getElementById('rp-add-btn')) return;
  const name = h1.textContent.trim();

  const btn = document.createElement('button');
  btn.id = 'rp-add-btn';
  btn.className = 'rp-add-btn';
  btn.textContent = '+ Add to My Box';
  btn.addEventListener('click', () => openAddModal(id, name));
  h1.insertAdjacentElement('afterend', btn);
}

// ── Init ──

document$.subscribe(() => {
  renderBoxPage();
  injectAddButton();
});
