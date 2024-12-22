import asyncio
import aiohttp
import click
import os
import aiofiles

async def download_image(session, destination, i):
    async with session.get("https://picsum.photos/200") as resp:
        if resp.status == 200:
            filename = f"{i + 1}_{resp.content_disposition.filename}"
            file_path = os.path.join(destination, filename)
            async with aiofiles.open(file_path, mode="wb") as f:
                await f.write(await resp.read())
            print(filename, "saved")
        else:
            print("Bad status:", resp.status)

async def _main(n, destination):
    if os.path.exists(destination) and not os.path.isdir(destination):
        raise NotADirectoryError()

    if not os.path.exists(destination):
        os.makedirs(destination)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(n):
            task = download_image(session, destination, i)
            tasks.append(task)
        
        await asyncio.gather(*tasks)

@click.command()
@click.option("-n", type=click.INT, default=1, help="number of files to be downloaded")
@click.argument("destination", type=click.Path())
def main(n, destination):
    asyncio.run(_main(n, destination))

if __name__ == '__main__':
    main()
