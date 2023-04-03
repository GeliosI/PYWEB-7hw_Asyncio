import asyncio

from models import SwapiPeople, get_session_maker


Session = get_session_maker()


async def paste_to_db(people_list):
    async with Session() as session:
        orm_objects = [SwapiPeople(**item) for item in people_list if not item.get('detail') ]
        session.add_all(orm_objects)
        await session.commit()

async def download_links(links_list, client_session):
    coros = [client_session.get(link) for link in links_list]
    http_responses = await asyncio.gather(*coros)
    json_coros = [http_response.json() for http_response in http_responses]
    return await asyncio.gather(*json_coros)

async def get_people(people_id, client_session):
    async with client_session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        json_data = await response.json(content_type=None)
        items = ['films', 'vehicles', 'species', 'starships']
        links = [json_data.get(item, []) for item in items]
        download_coros = [download_links(link, client_session) for link in links]

        films, vehicles, species, starships = await asyncio.gather(*download_coros)
    
        json_data['films'] = ','.join([film['title'] for film in films])
        json_data['vehicles'] = ','.join([vehicle['name'] for vehicle in vehicles])
        json_data['species'] = ','.join([specie['name'] for specie in species])
        json_data['starships'] = ','.join([starship['name'] for starship in starships])

        json_data.pop('created', None)
        json_data.pop('edited', None)
        json_data.pop('url', None)

        return json_data