def serialize_delegate_mandates(delegate, representees, settings):
    data = []
    for representee in representees:
        item = {
            'delegate': {
                'firstName': delegate['delegate_first_name'],
                'identifier': delegate['delegate_identifier'],
                'surname': delegate['delegate_surname'],
                'type': delegate['delegate_type']
            },
            'mandates': [],
            'representee': {
                'identifier': representee['representee_identifier'],
                'legalName': representee['representee_legal_name'],
                'type': representee['representee_type']
            }
        }
        for mandate in representee['mandates']:
            mandate_data = serialize_mandate(representee, delegate, mandate, settings)
            item['mandates'].append(mandate_data)
        data.append(item)
    return data


def serialize_representee_mandates(representee, delegates, settings):
    response_data = []
    for delegate in delegates:
        item = {
            'delegate': serialize_item_by_type(delegate, 'delegate'),
            'mandates': [],
            'representee': serialize_item_by_type(representee, 'representee'),
        }
        for mandate in delegate['mandates']:
            mandate_data = serialize_mandate(representee, delegate, mandate, settings)
            item['mandates'].append(mandate_data)
        response_data.append(item)
    return response_data


def serialize_item_by_type(item, key_type):
    switcher = {
        'LEGAL_PERSON': {
            'identifier': item[key_type + '_identifier'],
            'type': item[key_type + '_type'],
            'legalName': item[key_type + '_legal_name']
        },
        'NATURAL_PERSON': {
            'identifier': item[key_type + '_identifier'],
            'type': item[key_type + '_type'],
            'firstName': item[key_type + '_first_name'],
            'surname': item[key_type + '_surname']
        },
    }

    default = {k: v for k, v in item.items() if v is not None and k != key_type + '_id'}
    return switcher.get(item[key_type + '_type'], default)


def serialize_mandate(representee, delegate, mandate, settings):
    links = {
        'delete': mandate['link_delete'],
        'origin': settings["origin_url"],
    }

    if mandate['can_sub_delegate'] and mandate['link_add_sub_delegate']:
        links['addSubDelegate'] = mandate['link_add_sub_delegate']

    validity_period = {}
    if mandate['validity_period_from']:
        validity_period['from'] = mandate['validity_period_from'].strftime('%Y-%m-%d')
    if mandate['validity_period_through']:
        validity_period['through'] = mandate['validity_period_through'].strftime('%Y-%m-%d')

    mandate_data = {
        'links': links,
        'role': mandate['role'],
        **({'subDelegatorIdentifier': mandate['created_by_represented_person']}
            if mandate['original_mandate_id'] and mandate['created_by_represented_person'] else {}),
        **({'validityPeriod': validity_period}
            if validity_period else {}),
    }
    return mandate_data


def set_subdelegate_link(mandate, representee, delegate):
    ns = mandate['role'].split(':')[0]
    representee_id = representee['representee_id']
    delegate_id = delegate['delegate_id']
    mandate_id = mandate['mandate_id']
    return f'/v1/nss/{ns}/representees/{representee_id}/delegates/{delegate_id}/mandates/{mandate_id}/subdelegates'


def set_delete_link(mandate, representee, delegate):
    ns = mandate['role'].split(':')[0] if mandate.get('role') else ''
    representee_id = representee['representee_id']
    delegate_id = delegate['delegate_id']
    mandate_id = mandate['mandate_id']
    return f'/v1/nss/{ns}/representees/{representee_id}/delegates/{delegate_id}/mandates/{mandate_id}'
