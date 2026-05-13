from beanie import Document, init_beanie
from pydantic import BaseModel
from typing import Literal, Union
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Literal
# , 'процессор', 'ОЗУ', 'ПЗУ', 'видеокарта'

class moth_category(BaseModel):
    Type: Literal['материнская плата'] = 'материнская плата'
    Description: str
    format: str
    soket: str

class prots_category(BaseModel):
    Type: Literal['процессор'] = 'процессор'
    Description: str
    soket: str
    chast: str

class ozu_category(BaseModel):
    Type: Literal['ОЗУ'] = 'ОЗУ'
    Description: str
    chast: str
    volume: str

class pzu_category(BaseModel):
    Type: Literal['ПЗУ'] = 'ПЗУ'
    Description: str
    formfactor: str
    volume: str

class vidcart_category(BaseModel):
    Type: Literal['видеокарта'] = 'видеокарта'
    Description: str
    volume: str
    outputport: str

CategoryUnion = Union[
    moth_category, 
    prots_category, 
    ozu_category, 
    pzu_category, 
    vidcart_category
]

class PC_components (Document):
    Production: str
    Model: str
    Price: float
    Category: CategoryUnion = Field(discriminator='Type')

    class Settings:
        name = "PC_components"

def builddoc():
    docs = []

    moths = [
        ("ASUS", "ROG STRIX B550-F", 189.99, "ATX", "AM4"),
        ("MSI", "MAG B660 TOMAHAWK", 159.50, "ATX", "LGA1700"),
        ("Gigabyte", "AORUS X570 ELITE", 199.00, "ATX", "AM4"),
        ("ASRock", "B460M Pro4", 89.99, "mATX", "LGA1200"),
        ("Biostar", "B450MH", 74.99, "mATX", "AM4"),
        ("EVGA", "Z590 FTW", 249.99, "ATX", "LGA1200"),
    ]
    for prod, model, price, fmt, sok in moths:
        docs.append({
            "Production": prod,
            "Model": model,
            "Price": price,
            "Category": {
                "Type": "материнская плата",
                "Description": f"{prod} {model} материнская плата",
                "format": fmt,
                "soket": sok
            }
        })

    prots = [
        ("Intel", "Core i9-12900K", 589.99, "LGA1700", "3.2GHz"),
        ("AMD", "Ryzen 9 5900X", 399.99, "AM4", "3.7GHz"),
        ("Intel", "Core i5-12400F", 179.99, "LGA1700", "2.5GHz"),
        ("AMD", "Ryzen 5 5600X", 199.99, "AM4", "3.7GHz"),
        ("Intel", "Core i7-11700K", 349.99, "LGA1200", "3.6GHz"),
        ("AMD", "Ryzen 7 5800X", 329.99, "AM4", "3.8GHz"),
    ]
    for prod, model, price, sok, chast in prots:
        docs.append({
            "Production": prod,
            "Model": model,
            "Price": price,
            "Category": {
                "Type": "процессор",
                "Description": f"{prod} {model} процессор",
                "soket": sok,
                "chast": chast
            }
        })

    ozus = [
        ("Corsair", "Vengeance LPX 16GB", 79.99, "3200MHz", "16GB"),
        ("G.Skill", "Trident Z 32GB", 159.99, "3600MHz", "32GB"),
        ("Kingston", "HyperX 8GB", 39.99, "2666MHz", "8GB"),
        ("Patriot", "Viper Steel 16GB", 74.99, "3000MHz", "16GB"),
        ("Crucial", "Ballistix 16GB", 69.99, "3200MHz", "16GB"),
        ("TeamGroup", "T-Force 32GB", 149.99, "3600MHz", "32GB"),
    ]
    for prod, model, price, chast, vol in ozus:
        docs.append({
            "Production": prod,
            "Model": model,
            "Price": price,
            "Category": {
                "Type": "ОЗУ",
                "Description": f"{prod} {model} оперативная память",
                "chast": chast,
                "volume": vol
            }
        })

    pzus = [
        ("Samsung", "970 EVO Plus 1TB", 129.99, "M.2 NVMe", "1TB"),
        ("Western Digital", "Blue 500GB", 54.99, "2.5\"", "500GB"),
        ("Crucial", "MX500 1TB", 99.99, "2.5\"", "1TB"),
        ("Kingston", "A2000 500GB", 59.99, "M.2 NVMe", "500GB"),
        ("Seagate", "Barracuda 2TB", 49.99, "3.5\"", "2TB"),
        ("Intel", "660p 1TB", 119.99, "M.2 NVMe", "1TB"),
    ]
    for prod, model, price, ff, vol in pzus:
        docs.append({
            "Production": prod,
            "Model": model,
            "Price": price,
            "Category": {
                "Type": "ПЗУ",
                "Description": f"{prod} {model} накопитель",
                "formfactor": ff,
                "volume": vol
            }
        })

    vids = [
        ("NVIDIA", "RTX 3080", 699.99, "10GB", "HDMI;DisplayPort"),
        ("AMD", "Radeon RX 6800", 579.99, "16GB", "HDMI;DisplayPort"),
        ("NVIDIA", "RTX 3060 Ti", 399.99, "8GB", "HDMI;DisplayPort"),
        ("AMD", "RX 6600 XT", 379.99, "8GB", "HDMI;DisplayPort"),
        ("Gigabyte", "GTX 1660 Super", 229.99, "6GB", "HDMI;DVI;DisplayPort"),
        ("ASUS", "TUF RTX 3070", 499.99, "8GB", "HDMI;DisplayPort"),
    ]
    for prod, model, price, vol, ports in vids:
        docs.append({
            "Production": prod,
            "Model": model,
            "Price": price,
            "Category": {
                "Type": "видеокарта",
                "Description": f"{prod} {model} видеокарта",
                "volume": vol,
                "outputport": ports
            }
        })

    return docs

def short(doc):
    if not doc:
        return "—"
    return f"{doc.get('Production')} {doc.get('Model')} | {doc.get('Price')}"

async def get_sorted_by_price(db, type_name):
    cursor = db["PC_components"].find({"Category.Type": type_name, "Price": {"$exists": True}}).sort("Price", 1)
    return [d async for d in cursor]

async def build_assemblies_simple(db, socket_filter=None):
    moths = await get_sorted_by_price(db, "материнская плата")
    prots = await get_sorted_by_price(db, "процессор")
    rams = await get_sorted_by_price(db, "ОЗУ")
    storages = await get_sorted_by_price(db, "ПЗУ")
    gpus = await get_sorted_by_price(db, "видеокарта")

    prots_by_socket = {}
    for p in prots:
        s = p.get("Category", {}).get("soket")
        if s:
            prots_by_socket.setdefault(s, []).append(p)

    assemblies = []
    for m in moths:
        m_sock = m.get("Category", {}).get("soket")
        if not m_sock:
            continue
        if socket_filter and m_sock != socket_filter:
            continue
        for p in prots_by_socket.get(m_sock, []):
            for r in rams:
                for s in storages:
                    for g in gpus:
                        try:
                            total = float(m["Price"]) + float(p["Price"]) + float(r["Price"]) + float(s["Price"]) + float(g["Price"])
                        except Exception:
                            continue
                        assemblies.append({
                            "motherboard": m, "cpu": p, "ram": r, "storage": s, "gpu": g, "total": total
                        })
    assemblies.sort(key=lambda x: x["total"])
    return assemblies


async def main():
    from motor.motor_asyncio import AsyncIOMotorClient

    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["baseLZ"] 

    await init_beanie(database=db, document_models=[PC_components])
    print("=============================")
    print("  пункт 1  ")

    assemblies = await build_assemblies_simple(db)
    total_assemblies = len(assemblies)
    print("\nвсего возможных сборок:", total_assemblies)
    if total_assemblies == 0:
        print("нет совместимых сборок (проверьте поля Category.soket).")
    else:
        cheapest = assemblies[0]
        print("\n самая дешевая сборка ")
        print(" Total:", cheapest["total"])
        print(" MB:", short(cheapest["motherboard"]))
        print(" CPU:", short(cheapest["cpu"]))
        print(" RAM:", short(cheapest["ram"]))
        print(" Storage:", short(cheapest["storage"]))
        print(" GPU:", short(cheapest["gpu"]))

        most_expensive = assemblies[-1]
        print("\n самая дорогая сборка ")
        print(" Total:", most_expensive["total"])
        print(" MB:", short(most_expensive["motherboard"]))
        print(" CPU:", short(most_expensive["cpu"]))
        print(" RAM:", short(most_expensive["ram"]))
        print(" Storage:", short(most_expensive["storage"]))
        print(" GPU:", short(most_expensive["gpu"]))

    print("=============================")
    print("  пункт 2  ")

    types = ["материнская плата", "процессор", "ОЗУ", "ПЗУ", "видеокарта"]
    print("\n3-й и 5-й по цене в каждой категории ")
    for t in types:
        items = await get_sorted_by_price(db, t)
        print(f"{t}: найдено {len(items)} элементов")
        third = items[2] if len(items) >= 3 else None
        fifth = items[4] if len(items) >= 5 else None
        print("  3-й:", short(third))
        print("  5-й:", short(fifth))


    print("=============================")
    print("  пункт 3  ")

    assemblies_am4 = await build_assemblies_simple(db, socket_filter="AM4")
    print("\n сборки на сокете AM4 ")
    print("найдено сборок на AM4:", len(assemblies_am4))
    with open("am4.txt", "w", encoding="utf-8") as f:
        for i, a in enumerate(assemblies_am4, 1):
            f.write(f"{i}. {a['total']:.2f} | MB: {a['motherboard']['Model']} | CPU: {a['cpu']['Model']}\n")
    print("Сохранено в am4.txt")

if __name__ == "__main__":
    asyncio.run(main())



