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

function loadBox() {
  try { return JSON.parse(localStorage.getItem(BOX_KEY)) || []; }
  catch { return []; }
}

function saveBox(box) {
  localStorage.setItem(BOX_KEY, JSON.stringify(box));
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
  const ordered = [...alive, ...fainted];

  root.innerHTML = `
    <div class="rp-page-toolbar">
      <span class="rp-page-count">${alive.length} alive · ${fainted.length} fainted</span>
      <button class="rp-btn-primary rp-page-add-btn" id="rp-page-add">+ Add Pokémon</button>
    </div>
    ${ordered.length === 0
      ? '<p class="rp-empty">No Pokémon yet.</p>'
      : `<div class="rp-box-grid-page">${ordered.map(p => slotHTML(p, box.indexOf(p))).join('')}</div>`
    }
  `;

  root.querySelector('#rp-page-add').addEventListener('click', () => openAddModal(null, null));
  root.querySelectorAll('.rp-slot[data-index]').forEach(slot => {
    slot.addEventListener('click', () => openDetailModal(parseInt(slot.dataset.index, 10)));
  });
}

function slotHTML(pokemon, index) {
  const label = pokemon.nickname || pokemon.speciesName;
  const tooltip = [
    label,
    pokemon.level ? 'Lv.' + pokemon.level : null,
    pokemon.caughtAt || null,
    pokemon.fainted ? '(fainted)' : null,
    pokemon.evolutionDelayed ? 'Evo delayed' : null,
  ].filter(Boolean).join(' · ');

  return `<div class="rp-slot${pokemon.fainted ? ' rp-fainted' : ''}" data-index="${index}" title="${tooltip}">
    <img src="${spriteUrl(pokemon.id)}" alt="${pokemon.speciesName}">
    ${pokemon.evolutionDelayed ? '<div class="rp-evo-badge" title="Evolution delayed">E</div>' : ''}
    <div class="rp-slot-name">${label}</div>
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

  const label = p.nickname ? `${p.nickname} (${p.speciesName})` : p.speciesName;

  const modal = document.createElement('div');
  modal.id = 'rp-modal';
  modal.innerHTML = `
    <div class="rp-modal-backdrop"></div>
    <div class="rp-modal-box">
      <div class="rp-modal-species">
        <img src="${spriteUrl(p.id)}" alt="${p.speciesName}"${p.fainted ? ' style="filter:grayscale(100%) opacity(.45)"' : ''}>
        <span>${label}</span>
      </div>
      <div class="rp-detail-info">
        ${p.level ? `<div>Level: ${p.level}</div>` : ''}
        ${p.caughtAt ? `<div>Caught at: ${p.caughtAt}</div>` : ''}
        ${p.fainted ? `<div class="rp-warning" style="margin-top:8px">This Pokémon has fainted.</div>` : ''}
        ${p.evolutionDelayed ? `<div class="rp-evo-note">Evolution delayed</div>` : ''}
      </div>
      <div class="rp-modal-actions">
        <button class="rp-btn-primary" data-action="info" data-index="${index}">Access Info</button>
        ${!p.fainted
          ? `<button class="rp-btn-secondary" data-action="faint" data-index="${index}">Mark as fainted</button>`
          : `<button class="rp-btn-secondary" data-action="revive" data-index="${index}">Restore to box</button>`
        }
        <button class="rp-btn-secondary" data-action="evo-delay" data-index="${index}">${p.evolutionDelayed ? 'Remove evo delay' : 'Delay evolution'}</button>
        <button class="rp-btn-danger" data-action="remove" data-index="${index}">Remove</button>
        <button class="rp-btn-secondary" data-action="close">Close</button>
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
      if (box[index]) { box[index].evolutionDelayed = !box[index].evolutionDelayed; saveBox(box); }
      closeModal();
      break;
    case 'close':
      closeModal();
      break;
  }
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
