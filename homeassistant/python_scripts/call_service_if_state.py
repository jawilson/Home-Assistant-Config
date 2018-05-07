entity_ids = data.get('entity_id')
state = data.get('state')
service = data.get('service')

if isinstance(entity_ids, str):
    entity_ids = [entity_ids]

action_entities = []
for entity_id in entity_ids:
    if hass.states.is_state(entity_id, state):
        action_entities.append(entity_id)

domain, service = service.split('.')

if action_entities:
    hass.services.call(domain, service, {'entity_id': action_entities})
