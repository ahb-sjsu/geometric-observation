# The vacuity of "fresh": a survey of replication and consistency schemes through the consumer-relative witnessed certificate

**Status:** working survey (Observation Theory program). Companion to
`GOAL.md` (the thesis) and the sealed XPROTO-PG cell in
`network-governor` (the one measured cell so far). This document maps the
*full* replication/consistency design space — not the handful of schemes
one happens to recall — and asks, for each, where a **consumer-relative,
witnessed, calibrated** freshness certificate applies, what its form must
be, and whether the idea is already present as prior art.

Four verified research passes (consensus/strong-DB, leaderless/eventual/
CRDT, BFT/probabilistic/physical-time, edge/storage/hardware) underlie
§4; primary-source citations and uncertainty flags are preserved inline.

---

## 1. The question

Every replicated or cached system makes a freshness claim to its readers:
*caught up*, *committed*, *consistent*, *final*, *valid*, *in sync*. Each
such claim is issued by a **monitor** that infers a global property from
partial observation, and each can be **vacuous** — reporting fresh while
the specific consumer that trusts the report reads stale or wrong data.
The program's baseline result: for single-leader PostgreSQL streaming, the
standard global-replication-lag monitor is *two-sidedly* vacuous across
heterogeneous consumers (no threshold's worst-case error < ~0.50), while a
WAL-witnessed, per-footprint certificate holds every error ≤ 0.06. This
survey asks how far that finding generalizes.

We grade every scheme against a four-word grammar (from `GOAL.md`):

- **consumer-relative** — graded against the distortion the *actual*
  downstream reader feels over its footprint `tr(P_i·Σ)`, not a
  signal-blind global quantity;
- **witnessed** — measured against an independent ground-truth channel,
  not inferred from the monitor grading itself;
- **calibrated** — carrying a *measured* false-clear rate;
- **derivable** — margins predicted a priori from structure.

## 2. The organizing claim: certificate form follows order structure

The central synthesis of this survey is that the **form** a freshness
certificate can take is not a design choice — it is forced by two
properties of the replication scheme: its **order structure** (how updates
are ordered) and its **witness availability** (what independent
ground-truth metadata the system already carries). This yields four
certificate forms, and every scheme in the taxonomy is a special case:

| order structure | example schemes | certificate form | calibration output |
|---|---|---|---|
| **total** (single log / index) | PG WAL, Raft/Paxos log, Zab zxid, MongoDB oplog, Kafka offset+epoch, Galera seqno, Oracle SCN, chain replication | **scalar `≤`** on a log position: `max(chg-pos over footprint) ≤ replay-pos` | one false-clear number |
| **partial** (causal / version metadata) | EPaxos dep-DAG, Dynamo/Cassandra/Riak, CRDTs, causal stores, DHTs | **version-set dominance** `V(replica) ⊒ V(footprint)` in the partial order | a false-clear *surface* (per key / per session guarantee) |
| **probabilistic** (work/stake depth) | Nakamoto/Bitcoin, PoW chains | **calibrated depth/reversal bound** — already a consumer-chosen staleness margin | reversal probability vs depth (already published) |
| **physical-time-bounded** (clock/lease) | Spanner TrueTime, HLC/CockroachDB, DNS/CDN TTL, leases, HW cache coherence | **time/lease-bounded validity** — valid until bound, witnessed by origin/directory | staleness-vs-bound violation rate |

The corollary that makes the survey worth writing: **as order weakens from
total to partial to probabilistic, the certificate does not disappear — it
changes form, and its calibration changes from a number to a surface.**
The consumer-relative, witnessed *idea* survives every regime; what varies
is the witness cost (a scalar log position is cheap; per-key vector clocks
are not) and the shape of the calibrated output.

**A finding that recurred in all four passes:** the *witnessed* leg is
nearly universal — essentially every scheme already carries a monotone
ground-truth position independent of its ops monitor (LSN ≙ Raft index ≙
zxid ≙ oplog ts ≙ Kafka offset+epoch ≙ Galera seqno ≙ Oracle SCN ≙
vector clock ≙ CRDT lattice ≙ chain depth ≙ TrueTime interval ≙ coherence
directory). What is missing *everywhere* is a **measured false-clear
rate**, and what is *partially present* is the **consumer-relative knob**.
The program's delta is precisely the intersection nobody ships.

## 3. Three distinctions the survey holds throughout

Conflating these is where prior art gets mis-credited in both directions:

1. **consumer-blind vs consumer-relative.** Global lag, "quorum met,"
   "finalized," ISR count, TTL, `HEALTH_OK` — all consumer-blind. A
   certificate graded against *this* reader's footprint is
   consumer-relative. Most deployed monitors are blind.
2. **inferred vs witnessed.** The monitor grading itself (a lag gauge
   reading its own clock; "R replicas answered") vs an independent
   ground-truth channel (a log index, a version vector, a coherence
   directory, a lease, a beacon schedule).
3. **offered-by-construction vs measured.** Session guarantees, PNUTS
   per-record timeline, Cosmos DB's five levels, MongoDB causal sessions,
   Galera `wsrep_sync_wait`, Oracle `STANDBY_MAX_DATA_DELAY`, and hardware
   cache coherence *already* deliver consumer-relative or witnessed
   behavior — but **none publishes a measured false-clear rate.** The
   program's honest delta is the *measurement*, not the grammar.

## 4. The taxonomy

Six fields per scheme: **(1)** reader-facing claim · **(2)** deployed
consumer-blind monitor · **(3)** independent witness available ·
**(4)** order structure · **(5)** characteristic false-clear mode ·
**(6)** consumer-relative / prior-art status.

### 4.1 Consensus & strongly-consistent replication

The log layer (Paxos/Raft/Zab/VR/EPaxos) plus the strongly-consistent
databases built on it. **Total order is the norm** — so the certificate is
a scalar log-position comparison — with two structural outliers (EPaxos =
partial order; Spanner/CockroachDB = physical-time-bounded).

| System | (1) claim | (2) blind monitor | (3) witness | (4) order | (5) false-clear | (6) status |
|---|---|---|---|---|---|---|
| **Paxos / Multi-Paxos** (Lamport '98) | per-instance agreement, stable | "instance decided", leader liveness | instance # + ballot | total | learner has instance *i* but gaps below *i* → serves truncated committed state; **no read model at all** | reads delegated upward; no bound |
| **Fast / Flexible Paxos** (Lamport '06; Howard+ '16) | same safety, tuned quorums | as Multi-Paxos | instance/ballot; quorum sizes | total | FPaxos: a mis-sized read-quorum Q2 that stops intersecting the commit set → follower-read misses committed entries (*directly tunable* false-clear) | Q2 size is a deployment-relative dial, uncalibrated |
| **EPaxos** (Moraru+ SOSP'13) | interfering cmds ordered; others not | "command committed" | per-cmd **dependency set** + seq | **partial (DAG)** | committed-but-**unexecuted**: dep-graph not resolved → reader's key omits a committed conflicting write | deps are per-key ⇒ purest consumer-relative object in the tier; unmeasured |
| **Raft** (Ongaro '14) | linearizable SMR | commit/matchIndex, leader liveness | **log index + term** | total | (a) deposed leader serves stale read (→ ReadIndex/lease; lease is **clock-drift-vulnerable**); (b) follower read trails commit index | ReadIndex/follower-read per-request knobs; no published rate |
| **Zab / ZooKeeper** (Junqueira+ '11) | writes linearizable; **reads local & may be stale** | leader epoch, zxid quorum-ack | **zxid** (epoch,counter); `sync()` | total | read from lagging follower → stale znode while write globally committed (documented) | **`sync()` = consumer-relative witness knob**; local-vs-sync rate unmeasured — strong cell |
| **Viewstamped Repl.** (Oki/Liskov '88) | linearizable via primary + views | "op committed", view liveness | op# + view# + commit# | total | backup behind commit#, or stale primary mid-view-change | witness triple exists; reads uncalibrated |
| **Spanner / TrueTime** (Corbett+ OSDI'12) | **external consistency** (global linearizability) | TrueTime **ε** / commit-wait; replica health | TrueTime interval `[earliest,latest]`; per-group `t_safe` | **physical-time total** | snapshot read blocks past `t_safe`; but **ε underestimate** (clock fault) → commit-wait too short → silent external-consistency violation | bounded/exact-staleness reads are per-read + time-bounded (**closest to calibrated**); ε-fault false-clear rate unpublished |
| **CockroachDB** (Taft+ SIGMOD'20) | serializable; per-key linearizable on leaseholder | replication lag, **closed timestamp**, leaseholder health | **HLC** + per-range closed ts | physical-time total | **follower reads land ~4.2 s in the past by default**; consumer assuming fresh gets stale row while cluster "healthy" | `AS OF SYSTEM TIME`/`with_max_staleness()` per-query bounded — well-instrumented, rate unpublished |
| **Calvin** (Thomson+ '12) | deterministic serializable | sequencer epoch, apply progress | **global input log** (epoch #) | total | replica received-but-not-executed epoch → stale-but-eventually-identical read | *[FLAG: research system; ops inferred from design]* |
| **FoundationDB** (Zhou+ '21) | strict serializability | proxy/log health, read-version staleness | **GRV read version**; ~5 s MVCC window | total | **`causal_read_risky`** trades a GRV round-trip for a possibly-stale read version in a proxy-fault window (a named false-clear surface) | risky-read is per-txn; 5 s window is a *ceiling* not a rate — measurable |
| **MongoDB replica sets** | tunable: majority / linearizable / causal sessions | secondary **optime lag**, oplog window, majority-commit point | **oplog `ts`** + `afterClusterTime` cluster time | total (+ per-session causal) | `readPreference:secondary`+`readConcern:local` → stale or **rolled-back** data on failover | **causal sessions (`afterClusterTime`) = textbook per-session knob**; rate unpublished — **top structural twin of the PG cell** |
| **Kafka ISR / HW** | record ≤ high-watermark is committed & readable | **ISR size**, under-replicated=0, consumer lag | **offset + leader epoch** (KIP-101/320) | total per-partition | **ISR shrink** to leader-only w/o `min.insync.replicas` → "committed" records lost on failover; old HW truncation could diverge | consumers *opt into* epoch-truncation check; skip-rate unmeasured — strong cell |
| **etcd** | linearizable default; serializable opt-in | Raft commit index, slow-read metric | log index + term; **`revision`** | total | `--consistency=s` serves stale from follower while cluster healthy | serializable flag per-request; revision witness makes rate easy to measure |
| **Galera / MySQL Group Repl.** | certification-based "virtually synchronous"; **reads not sync by default** | **apply-queue depth** (`wsrep_local_recv_queue`), flow control | writeset **seqno** (GTID) | total | node "synced" but just-certified writeset unapplied in local queue → reader misses committed write | **`wsrep_sync_wait` = per-session witness knob**; off-vs-on rate measurable — strong cell |
| **Redis (async + WAIT)** | default async: **no failover guarantee**; WAIT = best-effort | **replication offset lag**, `master_link_status:up` | replication **offset** + repl-ID | total per-master (no consensus) | master ACKs write, dies before propagating → promoted replica lacks it; WAIT narrows but can't eliminate | WAIT is a *write-side* knob; `master_link_status:up` monitor near-vacuous → **best vacuity lower-bound demo** |
| **Oracle (Active) Data Guard** | Max Protection/Availability/Performance; real-time query on standby | **transport + apply lag** (`V$DATAGUARD_STATS`) | redo **SCN** + log seq | total | real-time-query reader on lagging standby reads stale; async mode can lose un-shipped redo on failover | **`STANDBY_MAX_DATA_DELAY` (=0 → ORA-3172) = closest existing per-consumer, witnessed, *enforced* bound**; still no reported rate |
| **MySQL semisync** | commit waits for ≥1 replica to **ACK receipt** (not apply) | `Seconds_Behind_Source` (coarse), semisync status | **GTID** / binlog pos | total | replica has event in relay log, not executed → stale read though semisync green; **silent downgrade to async** on timeout | no per-consumer read knob (weakest here); GTID a consumer *could* wait on |

**Reading of 4.1.** The witness is universal (a monotone log position in
every row); the consumer-relative knob is *partially* deployed (MongoDB
causal, Galera `wsrep_sync_wait`, Oracle `STANDBY_MAX_DATA_DELAY`, CRDB/
Spanner bounded staleness, etcd serializable, FDB `causal_read_risky`);
the measured false-clear rate is deployed *nowhere*. Spanner and
CockroachDB are the only members shipping an explicit staleness *bound* —
but a *claimed/target* bound, not a measured rate. That gap is the wedge.

### 4.2 Leaderless, eventual & conflict-resolution replication

Here the total order is mostly gone. A freshness certificate must
generalize from scalar `≤` to a **version-set dominance test** in the
causal partial order, and the cost of that test = the cost of the system's
native witness (vector clock / DVV / lattice state / dependency set).

| System | (1) claim | (2) blind monitor | (3) witness | (4) order | (5) false-clear | (6) status |
|---|---|---|---|---|---|---|
| **Dynamo** (DeCandia+ SOSP'07) | highly available, eventually consistent; R/W tunable | "R replicas responded"; R+W>N *presumed* to intersect | **vector clocks**; siblings on concurrency | partial (causal) | **sloppy quorum + hinted handoff**: under partition the W-set (first N *healthy*) and R-set can be **disjoint** → R+W>N does *not* force intersection → QUORUM-met read misses latest write | global R/W count, not per-footprint |
| **Cassandra** | tunable CL (ONE/QUORUM/ALL) | "consistency level met" = #acks | **wall-clock write ts only** (LWW); *no causal witness* | artificial total (LWW ts, not causal) | **LWW lost update**: concurrent writes, higher ts silently wins → dropped write **invisible to any ack-count monitor**; clock skew worsens | dominance test would need VCs added — **retrofit/expensive; structurally undetectable today** |
| **Riak** | eventually consistent; siblings surfaced | R/W count, sibling count | **dotted version vectors** (Almeida+ '14) | partial (causal, precise) | sloppy quorum + hinted handoff; LWW loss if `last_write_wins` | DVV makes dominance **cheap & exact** — best-witnessed of the trio |
| **Quorum theory** (Gifford '79; Herlihy '86; grid/tree) | quorum intersection ⇒ latest value | weighted vote count ≥ threshold | version number per register | total per register | vacuous only if quorum property *assumed* not *enforced* (sloppy quorum breaks Gifford's axiom) | theory is sound; the axiom is the object |
| **PBS** (Bailis+ VLDB'12) | ⟨k,t⟩-staleness with probability p | partial-quorum config → *predicted* staleness prob | write-dissemination timing (WARS) | partial, probabilistic | probability is **system-global**, not per-footprint; a hot key deviates from the aggregate | **calibrated but consumer-BLIND** — mirror image of the target |
| **CRDTs** (Shapiro+ '11) | strong eventual consistency | convergence assumed once delivered | **join-semilattice state** / causal op-history | partial (lattice) | no *conflict* false-clear by algebra; residual = "have I seen all updates for my keys yet?" (delivery unwitnessed per read) | lattice `⊑` **is** the dominance test — cheap; "converged for my footprint?" unmeasured |
| **Causal (COPS/Eiger, Bayou)** | causal(+) consistency; deps before value | dep-check on apply | **explicit dependency set** / commit set | partial (causal) | Bayou tentative-vs-committed reordering; COPS-GT needs read-txn | designed-in dominance; no measured rate |
| **Session guarantees** (Terry+ '94) | RYW, monotonic reads/writes, WFR | per-session read/write-set version checks | read-set & write-set **VCs** (per client) | partial, per-session | server lacking the client's write-set serves stale and looks clean; cross-session uncaught | **consumer-relative *by construction* — the program's exact template**; no measured rate |
| **PNUTS** (Cooper+ VLDB'08) | per-record timeline; read-any / read-critical(v) / read-latest | version ≥ requested; per-record master | **per-record version #** | total per record, partial across records | read-any returns arbitrarily old; multi-key footprint has no joint guarantee | read-critical(v) is per-record consumer-relative, uncalibrated |
| **Cosmos DB (5 levels)** | strong / bounded-staleness(k,t) / **session** / consistent-prefix / eventual | "level SLA met"; bounded within k/t | LSN / **session token** | strong=total; bounded; session=causal; eventual | bounded k is **region-global** — a consumer on a lagging replica exceeds k for *its* footprint while SLA shows green | **session level = consumer-relative by construction**, uncalibrated |
| **DynamoDB** | eventual vs strong read; global tables (multi-region) | read-type flag; strong read → leader | item version / **LWW region ts** | eventual=partial; strong=total; global=LWW | eventual read hits stale replica; **global-tables cross-region LWW** drops concurrent multi-region writes | read-type is global policy, not per-footprint |

**Reading of 4.2.** Witness cost tracks order structure exactly: cheap-and-
exact (Riak DVV, CRDT lattice), cheap-but-lossy (Dynamo VC truncation →
false concurrency), cheap-but-**blind** (Cassandra LWW — a total order that
*cannot represent concurrency*, so it cannot witness a lost update at all).
The program sits in a precise gap: **PBS is calibrated but consumer-blind;
session guarantees / PNUTS / Cosmos-session are consumer-relative but
uncalibrated.** Neither is simultaneously consumer-relative + witnessed +
calibrated.

### 4.3 BFT, probabilistic-finality & physical-time ordering

The regimes where "committed" is not a clean boolean. `PROB` = reversible
probabilistic total order; `BFT` = deterministic BFT-total order
(irreversible under ≤f faults); `PT` = physical-time-bounded.

| System | (1) finality claim | (2) blind monitor | (3) witness | (4) order | (5) false-clear | (6) prior-art status |
|---|---|---|---|---|---|---|
| **Nakamoto / Bitcoin** (2008 §11) | tx "confirmed" after *k* blocks bury it — a *reversal-probability bound*, never absolute | block depth ≥ *k* (conv. *k*=6) | cumulative PoW / most-work chain | **PROB** | reorg / double-spend reverts a "confirmed" tx | **strongest prior art**: *k* is a consumer-chosen safety bound; §11 gives the measured rate; required *k* scales with **tx value** ⇒ already consumer-relative |
| **PBFT / Tendermint / HotStuff** | committed = final, irreversible (deterministic) | quorum cert (2f+1 / 2/3+ votes) | signed **QCs**, view-change/lock evidence | **BFT** | >f (or >1/3) Byzantine → equivocation / two blocks final at one height; safety silently violated | boolean whose safety is a **hard assumption**; residual rate **assumed zero, never witnessed** — the gap |
| **Casper FFG** (Buterin/Griffith '17) | **justified** (tentative) vs **finalized** (irreversible barring slashing) | ≥2/3 supermajority link | supermajority-link graph; slashing evidence | PROB→BFT gadget | long-range / weak-subjectivity; ≥1/3 collusion finalizes conflicting checkpoints (punished, not prevented) | **justified-vs-finalized = explicit graded finality** — credit the grading; residual is economic, unmeasured |
| **GRANDPA** (Polkadot) | finalized chain *prefix* irreversible | ≥2/3 voting power (GHOST) | signed commit/justification over voted prefix | PROB→BFT | same 1/3 class; finality can lag production | decouples produced (prob) vs finalized (BFT); rate unmeasured |
| **Spanner TrueTime** | externally consistent (commit ts respects real time) | **commit-wait** ≈ 2ε | TrueTime interval `[earliest,latest]`, GPS+atomic | **PT** | ε **underestimate** → real-time-inverted timestamps | **second-strongest prior art**: ε is *measured & monitored*, commit-wait a calibrated margin; ε published (~1–7 ms) |
| **HLC** (Kulkarni+ '14) | timestamps track causality, bounded drift ε | HLC within ε of physical clock | NTP/physical clock | PT (bounded) | drift exceeds *assumed* ε → ordering/staleness violated silently | ε carried but typically *assumed*, not GPS-witnessed — weaker |
| **Chain replication** (van Renesse/Schneider '04) | read at **tail** = linearizable | read served only by tail | tail position = commit point | strong (crash-stop) | fail-stop violated (Byz/omission) → stale/forked read | freshness is binary/topological, not graded |
| **CRAQ** (Terrace/Freedman ATC'09) | every read linearizable, from any replica | per-object **clean → serve local; dirty → query tail** | tail's **version number** | strong | same fault-model breach as chain repl | **cleanest witness story**: a dirty (uncertain) object *forces* a per-object consult of the independent witness — the program's shape, rate 0-by-construction |

**Reading of 4.3.** Two members are *already calibrated, consumer-relative,
witnessed finality certificates in all but name* — **Nakamoto
confirmations** (depth-vs-value) and **Spanner commit-wait** (ε-vs-latency)
— and the program should credit them explicitly, not reinvent them.
Classical/BFT consensus (PBFT→HotStuff, Tendermint, GRANDPA) instead ships
an **un-witnessed boolean** whose false-clear rate is assumed-zero and
never graded per consumer: a whale's transfer and a coffee purchase get the
identical "finalized" bit. *Flags: exact Nakamoto reversal percentages vary
with attacker fraction q and are refined by Grunspan–Pérez-Marco; the ~0.1%
@z=6 figure is the historical convention, not exact. Deep-reorg empirics
were not pinned to a specific dataset.*

### 4.4 Edge, storage & hardware-level replication and coherence

The ends of the spectrum a database-only view misses — and, crucially, the
place where the **witnessed-invalidation certificate already exists in
hardware and in 1989-vintage systems.**

| System | (1) validity claim | (2) blind monitor | (3) witness | (4) order | (5) false-clear | (6) same idea? |
|---|---|---|---|---|---|---|
| **DNS (TTL)** | record valid to use | remaining **TTL** (origin-set clock) | authoritative **SOA serial** / current RRset | time-bounded (no callback) | authoritative value changes mid-TTL; resolver serves old until expiry | **partial** — a lease *without* a callback; sibling of the measured BGP-quiescence cell |
| **CDN / web cache** | cached representation fresh | `max-age`/`s-maxage`, Age vs TTL | origin **ETag/Last-Modified**; **purge/ban** event | time-bounded + invalidation | content changes before TTL and no purge → stale served as fresh | **yes** — purge/ban + ETag *is* a witnessed-invalidation certificate |
| **`stale-while-revalidate`** (RFC 5861) | served now, may be stale, refresh in flight | SWR window after `max-age` | origin revalidation (**not awaited**) | time-bounded | *designed* stale serving — a sanctioned/controlled false-clear | witness exists but decoupled; rate still unmeasured |
| **Leases** (Gray–Cheriton SOSP'89) | cached copy valid for lease term | lease timer at holder | **server callback** on write + wait-out | time-bounded **+ invalidation** | only lease-expiry races / clock skew | **canonical prior art** — "time-bounded validity + witness"; the program's certificate is its descendant |
| **HW cache coherence** (MESI/MOESI, directory) | line in M/E/S is valid for **this core** | per-core **coherence state** (already consumer-relative) | the **directory** / snoop bus; invalidations | invalidation-based (SWMR per location) | ~none within coherence; false-clear appears at the *consistency* layer above | **strongest structural match** — per-consumer cert + directory witness, in silicon; **enforces**, measures no rate |
| **Memory model** (SC vs TSO vs rel/acq) | read respects the model's ordering | (static contract; no runtime signal) | global memory/coherence order per location | total (SC) / relaxed (TSO) | **TSO store buffer**: a core reads a stale value before its store drains — controlled staleness *by contract* | formalizes consumer-observed staleness; fences, no rate |
| **Ceph RADOS (PG states)** | `active+clean` ⇒ acting set consistent, reads served | **PG state** (`active`/`degraded`/**`stale`**/`peering`/`inconsistent`) | **peering** across acting set + OSD map + per-object version | invalidation/consensus + per-object total | (a) literal **`stale`**: primary stopped reporting, mon's view aged out (the *monitor's own freshness* fails); (b) `active` served while a replica lags until deep-scrub finds `inconsistent` | peering = witnessed-agreement prior art; **`stale` names exactly the failure the program targets** — candidate cell |
| **HDFS / GFS** | block available & sufficiently replicated | **under-replicated count**, live-replica count | DataNode **block reports**; GFS **chunk version #** | invalidation/report + per-chunk total | reader hits a **stale replica** still counted "available" (GFS guards via chunk version) | GFS chunk-version = witness (prior art); HDFS count is blind → candidate cell |
| **DRBD (A/B/C)** | secondary is a valid replica | conn/disk state (`UpToDate`), protocol level | peer on-disk block + **out-of-sync bitmap** | commit-ordered (C sync, B semi, A async) | protocol A/B: primary acks, promoted secondary missing last writes → stale read on failover node | bitmap witnesses *resync*; steady-state status coarse → candidate cell |
| **RAID / erasure coding** | read correct despite failed device | array `degraded` / rebuild %, `mismatch_cnt` | parity / **k-of-n reconstruction**; scrub | reconstruction-based | **degraded read** reconstructs from stale/torn parity (RAID5 write-hole; EC fragments written at different times) → value never committed as current | scrub is a *delayed* witness → candidate cell |
| **NFS close-to-open** | after open, cached data valid | attribute-cache **timer** (`ac*`) | server **GETATTR** (change attr) at open | time-bounded + open-triggered | between opens, another client's write unseen → stale believed valid | open-time GETATTR is a periodic witness; degrades to a timer between opens |
| **AFS callbacks** | cached file valid until server recalls | valid **callback promise** held | server **callback (RPC break)** before write | invalidation-based (lease-like) | missed/lost callback (partition, server restart) → trust stale cache | **direct prior art** — a callback *is* a witnessed-invalidation certificate |
| **SMB2/3 oplocks/leases** | client may cache safely | held **oplock/lease level** (RWH) | server **break notification** before another opener | invalidation-based, lease-typed | lost/delayed/ignored break → stale cached read | **prior art** — SMB "lease" + break = witness channel |

**Reading of 4.4.** This cluster settles the novelty question honestly:
the **witnessed-invalidation certificate is not new** — it is Gray–Cheriton
leases (1989), AFS callbacks, SMB oplocks, and MESI+directory in silicon.
All of them **enforce or invalidate** (stall, recall, break, drain) rather
than **report a graded, measured confidence**, and none publishes a
false-clear rate. Ceph even *names* the target failure: a PG whose state
signal has itself gone `stale`.

## 5. Coverage map — measured, measurable, and hard

**Measured (1):** single-leader PostgreSQL streaming (sealed XPROTO-PG:
naive global-lag worst-case ~0.50 vs witnessed per-footprint ≤0.06).
Everything else below is *candidate*, ordered by expected divergence ×
deployability. No number transfers; each is a separate sealed measurement.

| candidate cell | order form | naive monitor | witness | why it diverges | substrate / deployability |
|---|---|---|---|---|---|
| **★ MongoDB `secondary`+`local` vs causal vs majority** | total | secondary optime lag | oplog `ts` / cluster time | **structural twin of the PG cell** in a system that *already ships* the per-consumer knob (`afterClusterTime`) | high — Docker replica set; top pick |
| **★ Sloppy quorum + hinted handoff under partition** (Dynamo/Riak/Cassandra) | partial | "QUORUM met" (R+W>N) | VC / DVV dominance | under partition R-set ∩ W-set can be **empty** → naive clear-rate can rise toward the ~0.5 two-sided ceiling | high — Cassandra/Riak + partition inject (Jepsen-style) |
| **★ Cassandra LWW concurrent-write lost update** | artificial total | ack count / timestamp | (must add VCs) | dropped write is **structurally undetectable** by the deployed monitor — best "why you need the certificate" exhibit | high — Cassandra + clock-skew inject |
| **Kafka ISR-shrink / HW** | total per-partition | ISR count, under-replicated=0 | offset + leader epoch | HW is a *global* watermark blind to which partitions a consumer reads | high — Kafka + unclean-failover inject |
| **Galera `wsrep_sync_wait` 0 vs 1** | total | apply-queue depth | writeset seqno | committed-but-unapplied cleanly isolable; knob is per-session | high — 3-node Galera |
| **Redis async + WAIT** | total (no consensus) | `master_link_status:up` | replication offset | monitor near-vacuous → likely rivals the ~0.5 PG worst case (vacuity lower-bound demo) | high — Redis + failover inject |
| **Ceph RADOS `stale` / lagging `active`** | invalidation + per-object | PG state string | peering + per-object version | **durability face, not read-staleness**: `HEALTH_OK` global while *this footprint*'s PGs are degraded; + the report-latency `active→stale` window (storage twin of the BMP witness-latency result) | **controlled dev Ceph on Atlas** (vstart/microceph, multi-OSD) — **NOT NRP's shared Ceph**: failure injection would harm other users and namespace users get PVC-level access only, not OSD control |
| **Spanner ε-underestimate / CRDB 4.2 s follower reads** | physical-time total | replica health / closed ts | TrueTime ε / HLC closed ts | the **calibrated-bound contrast** cell: a *claimed* bound vs a *measured* rate | medium — CRDB local; Spanner needs emulator |
| **Oracle `STANDBY_MAX_DATA_DELAY` residual** | total | apply lag | SCN | closest existing *enforced* per-consumer bound — measure the residual rate it never reports | medium — Oracle XE + standby |
| **DNS TTL / CDN SWR mid-TTL change** | time-bounded | remaining TTL | SOA serial / origin ETag | sanctioned stale-serving window; sibling of the measured BGP cell | high — authoritative zone / edge cache |
| **HDFS stale-replica / DRBD async failover / RAID degraded read** | report / commit / reconstruction | under-replicated count / `UpToDate` / array state | block report+chunk version / bitmap / scrub | per-read stale/reconstructed rate hidden behind a global tally | medium — local clusters |
| **EPaxos committed-but-unexecuted** | **partial (DAG)** | "command committed" | dependency set | purest consumer-relative object (per-conflict-footprint) in the consensus tier | low — needs research prototype |

**Substrate discipline note.** The compute-side cells (Mongo/Cassandra/
Kafka/Galera/Redis) are cleanly containerizable and, where geo-diversity
matters, fit the earlier NRP plan: **stock replicas on exempt-sized,
emptyDir, self-owned pods** where we inject our own failures — never on
shared services. Ceph specifically must run on a **controlled dev cluster
(Atlas)**, not NRP's production Ceph.

## 6. Prior art the program must credit

The survey's honest core. Three tiers, none of which the program should
claim to have invented:

**Tier A — already calibrated (publishes a staleness/finality rate):**
- **Nakamoto confirmations** — explicit reversal probability vs a
  consumer-chosen depth *k* that scales with transaction value. A
  calibrated, consumer-relative, work-witnessed finality certificate in
  all but name (deployed since 2009).
- **Spanner TrueTime commit-wait** — a measured, continuously monitored ε
  turned into a paid safety margin; masters self-evict when ε inflates.
- **PBS** (Bailis et al.) — the most literal academic instance of
  *measuring* a stale-read distribution — but **consumer-blind** (global).

**Tier B — consumer-relative by construction, but uncalibrated (the
program's template):** session guarantees (Terry), PNUTS read-critical,
Cosmos DB session level, MongoDB causal sessions, Galera `wsrep_sync_wait`,
Oracle `STANDBY_MAX_DATA_DELAY`, CRAQ dirty-object tail-query, hardware
cache-coherence line state. Each grades against a consumer's own footprint/
session — but none reports a *measured false-clear rate*.

**Tier C — witnessed-invalidation mechanism (enforces, doesn't measure):**
Gray–Cheriton leases, MESI/MOESI + directory, AFS callbacks, SMB oplocks/
leases, CDN purge/ban + ETag. The certificate *mechanism* is 1989-and-
silicon prior art.

**The delta, stated precisely.** No deployed scheme puts all four grammar
words together: a certificate that is simultaneously **consumer-relative**
(Tier B has this) **+ witnessed** (Tier C has this) **+ calibrated with a
measured false-clear rate** (only Tier A has this, and only
consumer-blind) — applied where enforcement is *absent* and only a
consumer-blind monitor exists. That intersection, and the registration-
first measurement of the rate, is the program's contribution. The
grammar is assembled from existing parts; the measurement is new.

## 7. Scope and honesty

No number in the one measured cell (PG) transfers to any scheme here; each
cluster's false-clear rate is a separate measurement under the same
registration-first discipline (sealed bars, kept FAILs, hash-chained
ledger). This survey enumerates *where the lens applies and what form the
certificate must take* — it does not claim to have measured any cell other
than PG. Its value is turning "reliability claims should be
consumer-relative and witnessed" from a slogan into a finite, ordered list
of concrete, measurable cells — and being explicit that the mechanism is
old, the grammar is assembled, and only the calibrated measurement is new.

Uncertainty flags carried from the research passes: Cosmos internal LSN
mechanics are vendor-doc-sourced; Riak's DVV-default version unverified;
Nakamoto reversal percentages are convention not exact; Calvin/Fast-Paxos
read behavior is design-level not ops-level; several 4.4 hardware details
(MESIF/MOESI state specifics, GFS chunk-version, RAID write-hole) are
well-established general knowledge not re-fetched to primary docs this
session. The four load-bearing 4.4 citations (Ceph `stale`, Gray–Cheriton,
RFC 5861, DRBD A/B/C) were verified against primary sources.
