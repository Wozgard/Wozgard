#!/usr/bin/env python3
"""Download Pale Winter 1.20.1 Forge mods into a folder."""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GAME = "1.20.1"
LOADER = "forge"
UA_MR = "PaleWinter/1.0 (github.com/Wozgard/Wozgard)"
UA_CF = "Mozilla/5.0 (compatible; PaleWinter/1.0)"

# (name, modrinth_slug_or_None, curseforge_slug_or_None)
# Extra slugs tried in order if the first 404s.
MODS: list[tuple[str, str | None, str | None]] = [
    # Core
    ("Legendary Survival Overhaul", "legendary-survival-overhaul", "legendary-survival-overhaul"),
    ("Serene Seasons", "serene-seasons", "serene-seasons"),
    ("Farmer's Delight", "farmers-delight", "farmers-delight"),
    ("Comforts", "comforts", "comforts"),
    ("Spice of Life Classic Edition", "spice-of-life-classic-edition", "foodvariations"),
    ("Not Just Spoiled", "not-just-spoiled", "not-just-spoiled"),
    ("No Tree Punching", "no-tree-punching", "no-tree-punching"),
    ("In Control", "in-control", "in-control"),
    ("McJtyLib", "mcjtylib", "mcjtylib"),
    ("TaCZ", "timeless-and-classics-zero", "timeless-and-classics-zero"),
    ("Zombie Awareness", "zombie-awareness", "zombie-awareness"),
    ("Improved Mobs", "improved-mobs", "improved-mobs"),
    ("TenshiLib", "tenshilib", "tenshilib"),
    ("The Hordes", "the-hordes", "the-hordes"),
    ("Born in Chaos", "born-in-chaos", "born-in-chaos"),
    ("Terralith", "terralith", "terralith"),
    ("Tectonic", "tectonic", "tectonic"),
    ("ParCool", "parcool", "parcool"),
    ("Goety", "goety", "goety"),
    ("The Graveyard", "the-graveyard-forge", "the-graveyard-forge"),
    ("Mowzie's Mobs", "mowzies-mobs", "mowzies-mobs"),
    ("GeckoLib", "geckolib", "geckolib"),
    ("The Conjurer", "the-conjurer", "the-conjurer"),
    ("L_Ender's Cataclysm", "cataclysm", "lendercataclysm"),
    ("Goety Cataclysm", "goety-cataclysm", "goety-cataclysm"),
    ("Xaero's World Map", "xaeros-world-map", "xaeros-world-map"),
    # Variant B (conflicts with LSO)
    ("Cold Sweat", "cold-sweat", "cold-sweat"),
    ("Thirst Was Taken", "thirst-was-taken", "thirst-was-taken"),
    ("First Aid", "first-aid", "first-aid"),
    # Tools
    ("KubeJS", "kubejs", "kubejs"),
    ("Rhino", "rhino", "rhino"),
    ("Architectury API", "architectury-api", "architectury-api"),
    ("TaCZ JS", "tacz-js", "tacz-js"),
    ("Cloth Config", "cloth-config", "cloth-config"),
    ("Patchouli", "patchouli", "patchouli"),
    ("TaCZ Rebalance", None, "tac-z-rebalance"),
    # World / atmosphere
    ("William Wythers Overhauled Overworld", "wwoo", None),
    ("Immersive Weathering", "immersive-weathering", "immersive-weathering"),
    ("Moonlight Lib", "moonlight", "selene"),
    ("YUNG's API", "yungs-api", "yungs-api"),
    ("YUNG's Better Dungeons", "yungs-better-dungeons", "yungs-better-dungeons"),
    ("YUNG's Better Mineshafts", "yungs-better-mineshafts", "yungs-better-mineshafts"),
    ("YUNG's Better Strongholds", "yungs-better-strongholds", "yungs-better-strongholds"),
    ("Supplementaries", "supplementaries", "supplementaries"),
    ("Carry On", "carry-on", "carry-on"),
    ("Sound Physics Remastered", "sound-physics-remastered", "sound-physics-remastered"),
    ("Presence Footsteps", "presence-footsteps-forge", "presence-footsteps"),
    ("AmbientSounds", "ambientsounds", "ambientsounds"),
    ("CreativeCore", "creativecore", "creativecore"),
    # Atlas / Connector
    ("Antique Atlas 4", "antique-atlas-4", "antique-atlas-4"),
    ("Surveyor", "surveyor", "surveyor"),
    ("Sinytra Connector", "connector", "sinytra-connector"),
    ("Forgified Fabric API", "forgified-fabric-api", "forgified-fabric-api"),
    # Optional
    ("Diet", "diet", "diet"),
    ("Enigmatic Legacy", "enigmatic-legacy", "enigmatic-legacy"),
    ("Curios API", "curios", "curios"),
    ("Illage and Spillage", "illage-and-spillage-respillaged", "illage-and-spillage"),
    ("When Dungeons Arise", "when-dungeons-arise", "when-dungeons-arise"),
    ("Enhanced AI", "enhanced-ai", "enhanced-ai"),
    ("Distant Horizons", "distanthorizons", "distant-horizons"),
    # Known required libraries
    ("Structure Gel API", "structure-gel-api", "structure-gel-api"),
    ("InsaneLib", "insanelib", "insanelib"),
    ("Player Animator", "playeranimator", "playeranimator"),
    ("Kotlin for Forge", "kotlin-for-forge", "kotlin-for-forge"),
    ("Iceberg", "iceberg", "iceberg"),
    ("Puzzles Lib", "puzzles-lib", "puzzles-lib"),
    ("Citadel", "citadel", "citadel"),
    ("SmartBrainLib", "smartbrainlib", "smartbrainlib"),
]

ALT_MR = {
    "the-graveyard-forge": ["the-graveyard", "graveyard"],
    "spice-of-life-classic-edition": [
        "spice-of-life-classic",
        "the-spice-of-life-classic-edition",
        "foodvariations",
    ],
    "yungs-better-dungeons": ["yungs-better-dungeons-forge"],
    "yungs-better-mineshafts": ["yungs-better-mineshafts-forge"],
    "yungs-better-strongholds": ["yungs-better-strongholds-forge"],
    "yungs-api": ["yungs-api-forge"],
    "ambientsounds": ["ambient-sounds"],
    "connector": ["sinytra-connector"],
    "cataclysm": ["lenders-cataclysm", "lendercataclysm"],
    "xaeros-world-map": ["world-map", "xaero-world-map"],
    "distanthorizons": ["distant-horizons"],
    "not-just-spoiled": ["notjustspoiled"],
}

ALT_CF = {
    "the-graveyard-forge": ["the-graveyard"],
    "foodvariations": ["spice-of-life-classic-edition", "the-spice-of-life"],
    "yungs-better-dungeons": ["yungs-better-dungeons-forge"],
    "yungs-better-mineshafts": ["yungs-better-mineshafts-forge"],
    "yungs-better-strongholds": ["yungs-better-strongholds-forge"],
    "yungs-api": ["yungs-api-forge"],
    "distant-horizons": ["distanthorizons"],
    "antique-atlas-4": ["antique-atlas"],
}


def request(url: str, ua: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def request_json(url: str, ua: str):
    return json.loads(request(url, ua).decode("utf-8"))


def is_forge_1201(game_versions: list[str], filename: str = "") -> bool:
    gv = [str(v) for v in game_versions]
    name = filename.lower()
    has_ver = GAME in gv or "1.20" in gv
    if not has_ver and GAME not in name and "1.20.1" not in name:
        return False
    fabric_only = (("Fabric" in gv or "Quilt" in gv) and "Forge" not in gv)
    neo_only = "NeoForge" in gv and "Forge" not in gv
    if fabric_only or neo_only:
        return False
    if "fabric" in name and "forge" not in name:
        return False
    if "neoforge" in name and "forge" not in name.replace("neoforge", ""):
        return False
    return "Forge" in gv or "forge" in name or (has_ver and "Fabric" not in gv)


def pick_mr_version(versions: list[dict]) -> dict | None:
    scored = []
    for v in versions:
        loaders = [x.lower() for x in v.get("loaders") or []]
        games = v.get("game_versions") or []
        if GAME not in games:
            continue
        if "forge" not in loaders and "datapack" not in loaders and "minecraft" not in loaders:
            continue
        files = v.get("files") or []
        if not files:
            continue
        forge_rank = 0 if "forge" in loaders else 1
        # 0 = release, 1 = beta, 2 = alpha
        t = {"release": 0, "beta": 1, "alpha": 2}.get(v.get("version_type"), 3)
        scored.append((forge_rank, t, v.get("date_published") or "", v))
    if not scored:
        return None
    scored.sort(key=lambda x: (x[0], x[1], x[2]), reverse=False)
    best = scored[0][0:2]
    typed = [x for x in scored if x[0:2] == best]
    typed.sort(key=lambda x: x[2], reverse=True)
    return typed[0][3]


def mr_file(version: dict) -> dict:
    files = version["files"]
    for f in files:
        if f.get("primary"):
            return f
    return files[0]


def download_to(url: str, dest: Path, ua: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=180) as resp, open(tmp, "wb") as out:
        while True:
            chunk = resp.read(1024 * 256)
            if not chunk:
                break
            out.write(chunk)
    tmp.replace(dest)


def try_modrinth(slug: str) -> tuple[dict, dict] | None:
    slugs = [slug] + ALT_MR.get(slug, [])
    for s in slugs:
        url = (
            "https://api.modrinth.com/v2/project/"
            + urllib.parse.quote(s)
            + "/version?"
            + urllib.parse.urlencode(
                {"game_versions": json.dumps([GAME]), "loaders": json.dumps([LOADER])}
            )
        )
        try:
            versions = request_json(url, UA_MR)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            raise
        if not isinstance(versions, list) or not versions:
            continue
        picked = pick_mr_version(versions)
        if not picked:
            continue
        f = mr_file(picked)
        return picked, f
    return None


def cf_project_id(slug: str) -> int | None:
    slugs = [slug] + ALT_CF.get(slug, [])
    for s in slugs:
        url = f"https://api.cfwidget.com/minecraft/mc-mods/{urllib.parse.quote(s)}"
        try:
            data = request_json(url, UA_MR)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # datapack?
                try:
                    data = request_json(
                        f"https://api.cfwidget.com/minecraft/mc-mods/{s}", UA_MR
                    )
                except Exception:
                    continue
            else:
                raise
        except Exception:
            continue
        pid = data.get("id")
        if pid:
            return int(pid)
    return None


def cf_pick_file(project_id: int) -> dict | None:
    scored = []
    for page in range(0, 12):
        url = (
            f"https://www.curseforge.com/api/v1/mods/{project_id}/files"
            f"?pageIndex={page}&pageSize=50&gameVersion={GAME}&sortBy=dateCreated"
        )
        try:
            payload = request_json(url, UA_CF)
        except urllib.error.HTTPError:
            break
        files = payload.get("data") or []
        if not files:
            break
        for f in files:
            gv = f.get("gameVersions") or []
            name = f.get("fileName") or ""
            if not is_forge_1201(gv, name):
                continue
            rt = f.get("releaseType") or 9
            date = f.get("dateCreated") or ""
            scored.append((rt, date, f))
        # if this page already older and we have hits, can stop later
        if len(files) < 50:
            break
        time.sleep(0.12)
    if not scored:
        return None
    scored.sort(key=lambda x: (x[0], x[1]), reverse=False)
    best_rt = scored[0][0]
    typed = [x for x in scored if x[0] == best_rt]
    typed.sort(key=lambda x: x[1], reverse=True)
    return typed[0][2]


def try_curseforge(slug: str) -> tuple[int, dict] | None:
    pid = cf_project_id(slug)
    if not pid:
        return None
    time.sleep(0.1)
    f = cf_pick_file(pid)
    if not f:
        return None
    return pid, f


def follow_mr_deps(version: dict, out_dir: Path, seen: set[str], log: list[str]) -> None:
    for dep in version.get("dependencies") or []:
        if dep.get("dependency_type") not in ("required", "embedded"):
            continue
        pid = dep.get("project_id")
        if not pid:
            continue
        try:
            proj = request_json(f"https://api.modrinth.com/v2/project/{pid}", UA_MR)
        except Exception as e:
            log.append(f"DEP skip {pid}: {e}")
            continue
        slug = proj.get("slug")
        title = proj.get("title") or slug
        if slug in seen:
            continue
        seen.add(slug)
        time.sleep(0.08)
        result = try_modrinth(slug)
        if not result:
            log.append(f"DEP FAIL {title} ({slug})")
            continue
        ver, f = result
        dest = out_dir / f["filename"]
        if dest.exists() and dest.stat().st_size > 0:
            log.append(f"DEP has {f['filename']}")
        else:
            download_to(f["url"], dest, UA_MR)
            log.append(f"DEP ok  {f['filename']}")
        follow_mr_deps(ver, out_dir, seen, log)


def main() -> int:
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "mods").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    log: list[str] = []
    seen: set[str] = set()
    failed: list[str] = []
    manifest: list[dict] = []

    print(f"Downloading into {out_dir}")
    for name, mr, cf in MODS:
        print(f"-> {name}", flush=True)
        saved = None
        source = None
        try:
            if mr:
                result = try_modrinth(mr)
                if result:
                    ver, f = result
                    dest = out_dir / f["filename"]
                    if not (dest.exists() and dest.stat().st_size > 0):
                        download_to(f["url"], dest, UA_MR)
                    saved = dest
                    source = f"modrinth:{mr} {ver.get('version_number')}"
                    seen.add(mr)
                    follow_mr_deps(ver, out_dir, seen, log)
            if saved is None and cf:
                time.sleep(0.1)
                cf_hit = try_curseforge(cf)
                if cf_hit:
                    pid, f = cf_hit
                    filename = f["fileName"]
                    dest = out_dir / filename
                    url = f"https://www.curseforge.com/api/v1/mods/{pid}/files/{f['id']}/download"
                    if not (dest.exists() and dest.stat().st_size > 0):
                        download_to(url, dest, UA_CF)
                    saved = dest
                    source = f"curseforge:{cf} file {f['id']}"
                    seen.add(cf)
            if saved is None:
                failed.append(name)
                log.append(f"FAIL {name}")
                print(f"   FAIL {name}", flush=True)
            else:
                log.append(f"OK   {name} -> {saved.name} ({source})")
                print(f"   {saved.name}", flush=True)
                manifest.append(
                    {
                        "name": name,
                        "file": saved.name,
                        "source": source,
                        "bytes": saved.stat().st_size,
                    }
                )
        except Exception as e:
            failed.append(f"{name}: {e}")
            log.append(f"ERROR {name}: {e}")
            print(f"   ERROR {e}", flush=True)
        time.sleep(0.08)

    (out_dir / "download.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    (out_dir / "manifest.json").write_text(
        json.dumps({"game": GAME, "loader": LOADER, "mods": manifest, "failed": failed}, indent=2),
        encoding="utf-8",
    )
    print("---")
    print(f"ok={len(manifest)} fail={len(failed)} files={len(list(out_dir.glob('*')))}")
    for f in failed:
        print("FAILED:", f)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
