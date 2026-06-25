from asyncua import Client
import asyncio


URL = "opc.tcp://localhost:4840"


TARGETS = [
    "Temperature",
    "Pressure",
    "TripActive",
    "Mode",
    "TestOverride",
    "CalibrationOffset",
    "ResetTrip",
    "EmergencyCooling"
]


async def main():

    async with Client(url=URL) as client:

        print("[+] Conected\n")

        found = {}


        async def browse(node):

            try:
                name = await node.read_browse_name()
                node_name = name.Name

                if node_name in TARGETS:

                    print(
                        f"[+] {node_name:20} -> {node.nodeid}"
                    )

                    found[node_name] = node.nodeid


            except Exception:
                pass


            try:
                children = await node.get_children()

                for child in children:
                    await browse(child)

            except Exception:
                pass


        await browse(client.nodes.root)


        print("\n===== Results =====")

        for k,v in found.items():
            print(f'{k} = "{v}"')


asyncio.run(main())