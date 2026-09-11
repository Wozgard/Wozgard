# mods — Долгий Мороз

Minecraft **1.20.1**, лоадер **Forge**.  
Скачаны моды, о которых шла речь, плюс обязательные библиотеки (GeckoLib, Curios, Moonlight, CoroUtil и т.д.), без которых банки не встанут.

Скопируй `.jar` в `.minecraft/mods` (или в папку mods инстанса CurseForge / Prism / Modrinth App).

## Не класть в один инстанс одновременно

**Legendary Survival Overhaul** и связка **Cold Sweat + Thirst Was Taken + First Aid** — два варианта выживания. Вместе сломают HUD и температуру.

Оставь LSO (вариант A). Три других файла — запасной вариант B.

## Это не мод

`TaCZ-Rebalance-gunpack.zip` — ганпак, не банка. Распаковать в папку `tacz/` инстанса (рядом с `mods/`), не в `mods/`.

## Карта-атлас

Antique Atlas 4 + Surveyor + Connector + Forgified Fabric API тянут Fabric на Forge. Если инстанс без них стабильнее — вынь эти четыре банки и оставь Xaero's World Map.

## Не скачалось и не нужно

- **MixinExtras** — уже внутри Forge 1.20.1
- **Forge Config API Port** — это порт *на Fabric*. На Forge не нужен
- **Illage and Spillage** оригинал на 1.20.1 не живёт; лежит продолжение **Respillaged**

## Откуда качалось

Скрипт: `minecraft/pale-winter/scripts/download_mods.py`  
Список задумки: `minecraft/pale-winter/mods.md`
