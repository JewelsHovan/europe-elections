S = {}
S["STATUS"] = "Le Pen leads; second place open"
S["DATES"] = "First round April 2027, runoff two weeks later"
S["PRESETS"] = """          <button type="button" data-preset="phil:57">Harris 57</button>
          <button type="button" data-preset="phil:55">OpinionWay 55</button>
          <button type="button" data-preset="phil:50">57 minus 2022 poll gap</button>
          <button type="button" data-preset="mel:69">vs Mélenchon, Harris 69</button>
          <button type="button" data-preset="mel:67">vs Mélenchon, OpinionWay 67</button>"""

S["LEAD"] = """    <p class="lead" id="state">Six months before the first round, Marine Le Pen (RN) polls 31–35% and wins every tested runoff: 55–57% against Édouard Philippe and 67–69% against Jean-Luc Mélenchon. The open question is who joins her in the runoff. Ifop's poll of 25–29 September put Philippe (16%) ahead of Mélenchon (15%), reversing the September trend. Geographically, the RN leads almost everywhere outside Paris, the big western and southern cities and Brittany. Its opponents' votes are concentrated, so the national score decides the result, not the number of departments won.</p>
    <ul>
      <li><strong>RN vote:</strong> its base is the Northeast, the Mediterranean rim and small-town France. Its fastest growth from 2022 to 2024 came in the formerly left rural Southwest: Ariège +10 points, Aude +8, Tarn +7.</li>
      <li><strong>Firewall against the RN:</strong> Paris and its inner suburbs, Lyon (Rhône), Nantes and Rennes, Brittany and the Catholic-centrist West. Under the model, these departments hold against Le Pen until she passes about 56% nationally.</li>
      <li><strong>Battlegrounds:</strong> 17 departments with about 9 million voters flip when Le Pen's national share is between 50% and 56%. Examples include Gironde, Haute-Garonne, Isère, Haute-Savoie, Calvados, Puy-de-Dôme, Vendée, Morbihan and Pyrénées-Atlantiques.</li>
      <li><strong>Mood:</strong> 18% call Macron a good president (Odoxa, 29 Sept, his lowest ever) and 74% expect the country to get worse. Purchasing power is the top concern at 54%, well ahead of immigration at 31%.</li>
    </ul>"""

S["BATTLE"] = """    <p>France elects its president by national popular vote, so no department carries weight of its own. The map shows where votes have to move. Under the model, Le Pen carries 72 of 101 departments even when she gets only 50% nationally. A centre-right opponent therefore wins by running up large margins in a few dense areas and holding the West, not by winning many departments. The <strong>Flip point</strong> layer shows the national Le Pen share at which each department tips to her.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Flip point (Le Pen national share)</th><th class="num">Depts</th><th class="num">Voters</th><th>Departments</th></tr></thead>
      <tbody>
        <tr><td><span class="sw" style="background:#1c2868"></span>Under 45: RN even in a clear defeat</td><td class="num">44</td><td class="num">18.1M</td><td class="small">Northeast, Hauts-de-France, Mediterranean rim, Garonne valley, all 5 overseas departments</td></tr>
        <tr><td><span class="sw" style="background:#5a6bbd"></span>45–50</td><td class="num">28</td><td class="num">9.5M</td><td class="small">Seine-Maritime, Bas-Rhin, Loiret, Seine-et-Marne, Charente-Maritime, Côte-d'Or, Savoie, Doubs, Landes, Haute-Vienne and others</td></tr>
        <tr><td><span class="sw" style="background:#8e5fc0"></span>50–53: battleground</td><td class="num">9</td><td class="num">5.1M</td><td class="small">Isère, Manche, Aveyron, Vienne, Calvados, Gironde, Puy-de-Dôme, Haute-Savoie, Vendée</td></tr>
        <tr><td><span class="sw" style="background:#c3a2e3"></span>53–56: battleground</td><td class="num">8</td><td class="num">3.7M</td><td class="small">Deux-Sèvres, Indre-et-Loire, Morbihan, Lot, Côtes-d'Armor, Haute-Garonne, Mayenne, Pyrénées-Atlantiques</td></tr>
        <tr><td><span class="sw" style="background:#e3b25a"></span>56–60: falls only in a landslide</td><td class="num">5</td><td class="num">4.1M</td><td class="small">Maine-et-Loire, Val-d'Oise, Essonne, Finistère, Rhône</td></tr>
        <tr><td><span class="sw" style="background:#9a5a0c"></span>60+: firewall</td><td class="num">7</td><td class="num">6.8M</td><td class="small">Loire-Atlantique, Ille-et-Vilaine, Yvelines, Val-de-Marne, Seine-Saint-Denis, Hauts-de-Seine, Paris</td></tr>
      </tbody></table></div>
    <h3>Three zones to watch</h3>
    <ul>
      <li><strong>The West (Brittany, Pays de la Loire, Normandy coast).</strong> These are Christian-democrat departments that never gave the far right a majority. They voted for Macron's camp or the left in 2024: Mayenne, Maine-et-Loire, Vendée and Côtes-d'Armor were among the 7 departments where Macron's camp led. If Philippe is the opponent, these voters are his natural base, and Vendée, Manche and Calvados are the first of them to tip. A Le Pen breakthrough here would signal a national win.</li>
      <li><strong>Big-metro departments outside Paris.</strong> Gironde (Bordeaux), Haute-Garonne (Toulouse), Isère (Grenoble), Puy-de-Dôme (Clermont) and Haute-Savoie (Annecy). The cities vote left or centre (Bordeaux and Annecy went centrist in the March 2026 municipals), while the surrounding suburbs lean RN. Turnout in the city core decides these.</li>
      <li><strong>Île-de-France outer ring.</strong> Essonne, Val-d'Oise and Seine-et-Marne. Their dense, left-leaning inner suburbs sit next to RN-trending outer areas. In a Le Pen vs Philippe runoff, the swing depends on whether LFI voters in these departments vote Philippe, cast a blank ballot or stay home.</li>
    </ul>
    <h3>What a Mélenchon runoff changes</h3>
    <p>Switch the scenario to Le Pen vs Mélenchon. The map then follows the left vote, not the centre. The Catholic West, Yvelines, the wealthy west of Paris and the Alps move toward Le Pen or toward abstention. Only Paris, the inner suburbs, Brittany's cities and the left Southwest resist. At the polled 67–69%, Le Pen carries all but a handful of departments.</p>
    <h3>Local power from the March 2026 municipals</h3>
    <p>The RN held Perpignan and RN or allied lists won 55 towns above 3,500 residents, including Carcassonne, Castres, Menton and Liévin. Its ally Éric Ciotti took Nice. The RN did not win Toulon, Nîmes or Marseille. The left held Paris, Marseille, Lyon, Nantes, Lille and Rennes, the centre won Bordeaux and Annecy, and LFI won Saint-Denis and Roubaix. In the 27 September Senate election, chosen by local councillors, the RN–UDR reached 15 seats and formed its first Senate group.</p>"""

S["POLLS"] = """    <p>The rows below test different line-ups, so they are not an average. "—" means the candidate was not included.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Pollster, fieldwork</th><th class="num">Le Pen</th><th class="num">Mélenchon</th><th class="num">Philippe</th><th class="num">Attal</th><th class="num">Glucksmann</th><th class="num">Retailleau</th><th class="num">Zemmour</th><th class="num">Tondelier</th></tr></thead>
      <tbody>
        <tr><td><a href="https://www.tf1info.fr/politique/elections/presidentielle/sondage-lci-presidentielle-2027-ce-que-revelent-les-resultats-de-notre-derniere-enquete-2467226.html">Ifop</a>, 25–29 Sep</td><td class="num">32</td><td class="num">15</td><td class="num"><strong>16</strong></td><td class="num">8</td><td class="num">11</td><td class="num">7</td><td class="num">4</td><td class="num">3</td></tr>
        <tr><td><a href="https://tolunacorporate.com/fr/intentions-de-vote-a-lelection-presidentielle-2027-septembre-2026-2/">Toluna-Harris</a>, 22–24 Sep</td><td class="num">35</td><td class="num"><strong>17</strong></td><td class="num">13</td><td class="num">5</td><td class="num">10</td><td class="num">7</td><td class="num">5</td><td class="num">3</td></tr>
        <tr><td><a href="https://cluster17.com/presidentielle-2027-le-pen-largement-en-tete-melenchon-et-philippe-au-coude-a-coude/">Cluster17</a>, 15–16 Sep</td><td class="num">31</td><td class="num">19</td><td class="num">19</td><td class="num">—</td><td class="num">12</td><td class="num">7.5</td><td class="num">3.5</td><td class="num">2.5</td></tr>
        <tr><td><a href="https://www.commission-des-sondages.fr/notices/files/notices/2026/septembre/10260-pres-iv-opinionway-cnews-11-septembre.pdf">OpinionWay</a>, 9–10 Sep</td><td class="num">34</td><td class="num"><strong>17</strong></td><td class="num">15</td><td class="num">7</td><td class="num">9</td><td class="num">7</td><td class="num">2</td><td class="num">3</td></tr>
        <tr><td><a href="https://www.ipsos.com/fr-fr/presidentielle-2027-le-point-7-mois-du-scrutin">Ipsos-BVA</a>, 3–9 Sep</td><td class="num">33</td><td class="num"><strong>15.5</strong></td><td class="num">14</td><td class="num">6</td><td class="num">11.5</td><td class="num">7</td><td class="num">4</td><td class="num">4</td></tr>
        <tr><td><a href="https://elabe.fr/fichier-pdf/13224-les-francais-et-lelection-presidentielle-2027/">Elabe</a>, 26–28 Aug</td><td class="num">34</td><td class="num">14</td><td class="num"><strong>17</strong></td><td class="num">—</td><td class="num">11.5</td><td class="num">6.5</td><td class="num">4</td><td class="num">3.5</td></tr>
      </tbody></table></div>
    <p>In Ifop's line-up with Philippe as the only centre candidate and Glucksmann for the left, the figures are Philippe 21 and Mélenchon 16. That gap is why the Philippe–Attal decision on a single candidate, due by early 2027, matters more than any other event before the vote.</p>
    <h3>Runoff tests</h3>
    <div class="bars">
      <span>Le Pen vs Philippe, Harris 22–24 Sep</span><span class="track"><span class="fill" style="width:57%;background:#3d4fa1"></span></span><span class="num">57–43</span>
      <span>Le Pen vs Philippe, OpinionWay 9–10 Sep</span><span class="track"><span class="fill" style="width:55%;background:#3d4fa1"></span></span><span class="num">55–45</span>
      <span>Le Pen vs Mélenchon, Harris 22–24 Sep</span><span class="track"><span class="fill" style="width:69%;background:#3d4fa1"></span></span><span class="num">69–31</span>
      <span>Le Pen vs Mélenchon, OpinionWay 9–10 Sep</span><span class="track"><span class="fill" style="width:67%;background:#3d4fa1"></span></span><span class="num">67–33</span>
    </div>
    <div class="warning"><strong>Polling error</strong>Early runoff polls have overstated Le Pen before. In early 2017 they had her near 40–45% and she got 33.9%. Through 2022 they had her at 47–49% and she got 41.5%. The "57 minus 2022 poll gap" preset applies the same 7-point gap to today's best Harris number, which gives a 50–50 race.</div>"""

S["SENTIMENT"] = """    <div class="table-wrap"><table>
      <thead><tr><th>Measure</th><th class="num">Value</th><th>Source, date</th></tr></thead>
      <tbody>
        <tr><td>Macron is a "good president"</td><td class="num">18%</td><td class="small"><a href="https://www.bfmtv.com/politique/elysee/avec-seulement-18-d-opinion-positive-la-popularite-d-emmanuel-macron-atteint-son-plus-bas-historique_AD-202609290112.html">Odoxa-Mascaret</a>, 29 Sep (his lowest)</td></tr>
        <tr><td>Lecornu is a "good PM"</td><td class="num">24%</td><td class="small">Odoxa-Mascaret, 29 Sep</td></tr>
        <tr><td>Expect France to deteriorate</td><td class="num">74%</td><td class="small"><a href="https://www.jean-jaures.org/publication/enquete-electorale-2026-les-enseignements-de-la-vague-de-septembre/">Ipsos/Cevipof electoral survey</a>, Sep</td></tr>
        <tr><td>Certain to vote in 2027</td><td class="num">67%</td><td class="small">Same survey (intention, not projected turnout)</td></tr>
        <tr><td>Trust politics</td><td class="num">22%</td><td class="small"><a href="https://www.sciencespo.fr/cevipof/fr/actualites/barometre-de-la-confiance-politique-cevipof-2026-la-confiance-s-effondre-en-politique-la-proximite-fait-figure-de-refuge/">Cevipof trust barometer</a>, Feb 2026</td></tr>
        <tr><td>RN is a danger to democracy</td><td class="num">41%</td><td class="small"><a href="https://www.veriangroup.com/hubfs/4011%20-%20Barom%C3%A8tre%20dimage%20du%20RN%202026%20-%20VF%2009012026.pdf">Verian</a>, Jan 2026 (Ipsos, Oct 2025, different wording: 49%)</td></tr>
        <tr><td>At least 50% likely to vote RN some day</td><td class="num">45%</td><td class="small"><a href="https://www.jean-jaures.org/publication/les-quatre-familles-qui-votent-rn-la-france-oubliee-les-liberaux-identitaires-la-france-glissante-la-droite-radicale-opportuniste/">Ipsos via Fondation Jean-Jaurès</a>, Apr 2026 (potential, not intention)</td></tr>
      </tbody></table></div>
    <h3>Top concerns (Ipsos-BVA, 9–10 Sep)</h3>
    <div class="bars">
      <span>Purchasing power</span><span class="track"><span class="fill" style="width:54%"></span></span><span class="num">54%</span>
      <span>Social protection system</span><span class="track"><span class="fill" style="width:40%"></span></span><span class="num">40%</span>
      <span>Immigration</span><span class="track"><span class="fill" style="width:31%"></span></span><span class="num">31%</span>
      <span>Debt and deficits</span><span class="track"><span class="fill" style="width:30%"></span></span><span class="num">30%</span>
      <span>Crime</span><span class="track"><span class="fill" style="width:26%"></span></span><span class="num">26%</span>
    </div>
    <p>The September strikes show the same pressures. On 29 September, public-service unions marched over pay and service funding: 206,000 demonstrators according to the Interior Ministry, 300,000 according to the CGT. The 2027 budget presented on 1 October asks for about €54 billion in savings and new revenue.</p>"""

S["NEWS"] = """    <ul>
      <li><strong>Bardella affair (28 Sep onward).</strong> Mediapart published 2013 messages it attributes to Jordan Bardella that contain antisemitic claims. Bardella calls them forgeries and filed a defamation complaint, and Le Pen backed him. On 30 September Macron called the reported remarks "gravissimes" and asked the RN to clarify its position. No poll has yet measured an effect, because Ifop's fieldwork mostly ended before publication. (<a href="https://fr.euronews.com/2026/09/29/accusations-dantisemitisme-jordan-bardella-porte-plainte-contre-mediapart-pour-diffamation">Euronews</a>, <a href="https://www.rtl.fr/actu/politique/ecrits-antisemites-attribues-a-jordan-bardella-emmanuel-macron-juge-les-propos-rapportes-par-medipart-gravissimes-et-inacceptables-et-appelle-le-rn-a-clarifier-7900679142">RTL</a>)</li>
      <li><strong>Ifop poll (30 Sep).</strong> Philippe moves ahead of Mélenchon for second place. (<a href="https://www.tf1info.fr/politique/elections/presidentielle/sondage-lci-presidentielle-2027-ce-que-revelent-les-resultats-de-notre-derniere-enquete-2467226.html">TF1</a>)</li>
      <li><strong>Budget (1 Oct).</strong> PM Sébastien Lecornu presents the 2027 state and social-security budgets. The Assembly debate is expected from 13 October. The Socialists threaten a censure motion unless the draft changes, and the RN has reserved judgment. (<a href="https://www.rtl.fr/actu/politique/recessif-imparfait-le-budget-de-redressement-de-sebastien-lecornu-a-l-epreuve-de-l-assemblee-et-de-la-censure-7900679179">RTL</a>)</li>
      <li><strong>Senate (1 Oct).</strong> The vote for Senate president is at 15:00 today; Gérard Larcher is the incumbent. The new 15-member RN–UDR group sits for the first time. (<a href="https://www.france24.com/fr/info-en-continu/20260930-s%C3%A9nat-g%C3%A9rard-larcher-l-insubmersible-homme-du-contre-pouvoir-%C3%A0-l-%C3%A9preuve-du-rn">AFP/France 24</a>)</li>
      <li><strong>Campaign positions (30 Sep).</strong> Attal attacked Philippe's proposed pension age of 65. Retailleau proposed placing EU law below the French constitution. No agreement between Philippe and Attal on a single candidate has been reported. (<a href="https://www.letelegramme.fr/france/gabriel-attal-critique-la-reforme-des-retraites-dedouard-philippe-qui-reprend-la-reforme-macron-de-2022-7128568.php">Le Télégramme</a>)</li>
      <li><strong>Le Pen's appeal.</strong> Her lawyers must file their arguments with the Cour de cassation by 1 or 15 October. The court aims to rule by early April 2027, which leaves a ruling before the first round possible. (<a href="https://www.franceinfo.fr/politique/front-national/affaire-des-assistants-fn-au-parlement-europeen/les-avocats-de-marine-le-pen-ont-jusqu-au-15-octobre-pour-justifier-le-pourvoi-dans-l-affaire-des-assistants-d-eurodeputes-fn_8177831.html">franceinfo</a>)</li>
    </ul>
    <div class="note"><strong>Corrections to the 28 Sep brief</strong>The PS–Place publique primary has five candidates, not six. Its votes are 9–10 and 16–17 October, and voting requires membership or a €10–15 contribution. The separate 11 October "united left" vote between Tondelier and Ruffin could not be confirmed as still scheduled. The brief said Mélenchon makes the runoff in every scenario; Ifop's latest poll contradicts that. The brief also called a pre-election court ruling on Le Pen unlikely, which was too confident.</div>"""

S["CALENDAR"] = """    <div class="table-wrap"><table>
      <thead><tr><th>Date</th><th>Event</th></tr></thead>
      <tbody>
        <tr><td>1 Oct</td><td>Budget presented; Senate presidency vote</td></tr>
        <tr><td>9–10 Oct, 16–17 Oct</td><td>PS–Place publique primary, rounds 1 and 2 (Glucksmann favoured)</td></tr>
        <tr><td>From 13 Oct</td><td>Assembly budget debate; possible censure motion against Lecornu</td></tr>
        <tr><td>15 Oct</td><td>Latest deadline for Le Pen's Cour de cassation filing</td></tr>
        <tr><td>Early 2027</td><td>Philippe–Attal decision on a single centre candidate</td></tr>
        <tr><td>By early April 2027</td><td>Target date for the Cour de cassation ruling</td></tr>
        <tr><td>April 2027</td><td>First round, runoff two weeks later; legislative elections expected in June</td></tr>
      </tbody></table></div>"""

S["METHOD"] = """    <p><strong>Results data.</strong> Official department-level results from the Interior Ministry on data.gouv.fr: 2022 presidential, rounds 1 and 2; 2024 legislative, round 1; 2024 European. The blocs for 2024 legislative results are: RN + allies = RN, UXD (Ciotti), REC, EXD; Left = UG (NFP), DVG, ECO, EXG and others; Macron camp = ENS, DVC, HOR, UDI; LR + right = LR, DVD. Department boundaries come from <a href="https://github.com/gregoiredavid/france-geojson">france-geojson</a>, simplified.</p>
    <p><strong>Projection model.</strong> Each department gets a lean: the average of its logit difference from the national figure in two elections, the 2022 Le Pen runoff share and the 2024 far-right first-round share. The projected Le Pen share is logistic(logit(national share) + lean). For the Mélenchon scenario, the lean is the department's 2024 left-bloc share relative to the national left share, so the map follows the geography of the left vote. Overseas departments use the 2022 runoff only, because the RN stood in few overseas races in 2024. Corsica's 2024 vote went largely to regionalist lists, which belong to no bloc, so its Mélenchon-scenario figure is exaggerated. The flip point is the national share at which the projected share reaches 50%. Roll-ups weight departments by registered voters and ignore turnout differences.</p>
    <p><strong>Limits.</strong> This is a uniform-swing model on a logit scale. It assumes every department moves together and cannot capture realignments: a stronger RN surge in the West, a collapse of the "republican front" in left suburbs, or differential abstention. The 2022 overseas Le Pen vote was largely an anti-Macron protest and may not repeat. Treat department figures as relative positions, not forecasts.</p>
    <p><strong>News, polls and sentiment.</strong> Sources are linked inline. All polls are registered with the Commission des sondages. Fieldwork for the 30 September Ifop poll mostly predates the Bardella story.</p>"""

b = open("body.html").read()
for k, v in S.items():
    b = b.replace("%%" + k + "%%", v)
open("body.filled.html", "w").write(b)
import re; print(re.findall(r"%%[A-Z]+%%", b))
