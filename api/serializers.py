def serialize_delegate_mandates(delegate, representees, settings):
    data = []
    for representee in representees:
        item = {
            'representee': {
                'identifier': representee['representee_identifier'],
                'legalName': representee['representee_legal_name'],
                'type': representee['representee_type']
            },
            'delegate': {
                'firstName': delegate['delegate_first_name'],
                'identifier': delegate['delegate_identifier'],
                'surname': delegate['delegate_surname'],
                'type': delegate['delegate_type']
            },
            'mandates': []
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
            'representee': serialize_item_by_type(representee, 'representee'),
            'delegate': serialize_item_by_type(delegate, 'delegate'),
            'mandates': [],
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

    mapped = {
        key_type + '_first_name': 'firstName',
        key_type + '_identifier': 'identifier',
        key_type + '_legal_name': 'legalName',
        key_type + '_surname': 'surname',
        key_type + '_type': 'type',
    }

    default = {
        mapped[k]: v
        for k, v in item.items()
        if v is not None and k in mapped
    }

    return switcher.get(item[key_type + '_type'], default)


def serialize_mandate(representee, delegate, mandate, settings):
    links = {}

    if mandate['link_delete']:
        links['delete'] = mandate['link_delete']

    if mandate['can_sub_delegate'] and mandate['link_add_sub_delegate']:
        links['addSubDelegate'] = mandate['link_add_sub_delegate']

    if mandate['link_origin']:
        links['origin'] = mandate['link_origin']

    validity_period = {}
    if mandate['validity_period_from']:
        validity_period['from'] = mandate['validity_period_from'].strftime('%Y-%m-%d') if mandate['validity_period_from'] is not None else None,
    if mandate['validity_period_through']:
        validity_period['through'] = mandate['validity_period_through'].strftime('%Y-%m-%d') if mandate['validity_period_through'] is not None else None

    mandate_data = {
        'links': links,
        'role': mandate['role'],
        **({'subDelegatorIdentifier': mandate['subdelegated_by_identifier']}
            if mandate['subdelegated_by_identifier'] else {}),
        **({'validityPeriod': validity_period}
            if validity_period else {}),
    }
    return mandate_data


def serialize_deleted_subdelegated_mandates(subdelegated_deleted_mandates, deleted_mandates, settings):
    data_rows = [deleted for deleted in deleted_mandates if deleted['id'] in [sub['id'] for sub in subdelegated_deleted_mandates]]
    deleted_sub_delegated_mandates = []
    for item in data_rows:
        validity_period = {
            'from': item['validity_period_from'].strftime('%Y-%m-%d') if item['validity_period_from'] is not None else None,
            'through': item['validity_period_through'].strftime('%Y-%m-%d') if item['validity_period_through'] is not None else None
        }
        validity_period = {k: v for k, v in validity_period.items() if v is not None}

        sub_delegate = {
            'type': item['delegate_type'],
            'firstName': item['delegate_first_name'],
            'surname': item['delegate_surname'],
            'legalName': item['delegate_legal_name'],
            'identifier': item['delegate_identifier']
        }
        sub_delegate = {k: v for k, v in sub_delegate.items() if v is not None}

        mandate = {'subDelegate': sub_delegate}
        if validity_period:
            mandate['validityPeriod'] = validity_period
        deleted_sub_delegated_mandates.append(mandate)

    response_data = {
        "deletedSubDelegatedMandates": deleted_sub_delegated_mandates
    }
    return response_data

